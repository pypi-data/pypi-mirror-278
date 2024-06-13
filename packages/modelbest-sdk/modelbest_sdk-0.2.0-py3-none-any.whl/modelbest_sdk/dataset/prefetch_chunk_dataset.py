from collections import defaultdict
import itertools
import math
import multiprocessing
import random
import threading
import time
from typing import List
import torch
import torch.multiprocessing as mp
from modelbest_sdk.dataset.common.cache import AllCached, CacheFull, CacheNotFilled, PrefetchCache
from modelbest_sdk.dataset.common.range import Range
from modelbest_sdk.dataset.thrift_wrapper.base_doc import BaseDoc, DetailedDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import *
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext
from modelbest_sdk.file_format.mbtable import MbTable, MbTableIterator
from modelbest_sdk.file_format.mbtable_partition import MbTablePartition, MbTablePartitionIterator


class PrefetchChunkDataset(torch.utils.data.IterableDataset):
    def __init__(
        self, 
        context: DatasetContext, 
        path, 
        max_epoch,
        prefetch_chunk_cnt=2, 
        chunk_size=1024):
        
        self.context = context
        self.path = path
        self.max_epoch = max_epoch
        self.prefetch_chunk_cnt = prefetch_chunk_cnt
        
        self.num_workers = max(1, self.context.num_workers)
        
        self.cache = None
        self.exhausted = False
        self.used = Used()

        self._length = None
        self.chunk_size = chunk_size
        self.num_chunks = None
        
        self.shared_length = multiprocessing.Value('i', 0)
        self.shared_chunk_size = multiprocessing.Value('i', 0)
        self.shared_num_chunks = multiprocessing.Value('i', 0)
    
    def worker_init(self):
        """
        Worker initialization function used in the DataLoader's worker_init_fn.
        
        Obtaining the length of the dataset can be time-consuming, especially when dataset sources are remote. 
        
        The initialization is done asynchronously to allow each dataset to be initialized independently. 
        This way, when sampling from multiple datasets, one dataset does not need to wait for others to 
        finish initialization.

        Shared memory (shm) is used because the main process does not initialize these variables, but 
        they are needed during checkpointing. Synchronizing these values ensures they are available 
        when required.
        """
        self.mbtable_initialized = threading.Event()
        threading.Thread(target=self.lazy_init_mbtable).start()
    
    def lazy_init_mbtable(self):
        self.is_dir = os.path.isdir(self.path)
        if self.is_dir:
            self.mbtable_partition = MbTablePartition(self.path)
            self._length = self.mbtable_partition.get_total_count()
        else:
            self.mbtable = MbTable(self.path)
            self._length = self.mbtable.get_file_entry_count()
        self.chunk_size, self.num_chunks = self.safe_chunk_size(self.chunk_size)
        self.shared_length.value = self._length
        self.shared_chunk_size.value = self.chunk_size
        self.shared_num_chunks.value = self.num_chunks
        self.mbtable_initialized.set()
    
    def __len__(self):
        self._length = self.shared_length.value if self._length is None else self._length
        return self._length
    
    def get_chunk_data(self, chunk):
        assert isinstance(chunk, Chunk)
        start_index = chunk.start
        max_iter = chunk.stop - chunk.start
        ret = []
        # print(f"start_index: {start_index}, max_iter: {max_iter}")
        if self.is_dir:
            with MbTablePartitionIterator(self.mbtable_partition, start_index, max_iter) as iter:
                for record in iter:
                    ret.append(record)
        else:
            with MbTableIterator(self.path, start_index, max_iter) as iter:
                for record in iter:
                    ret.append(record)
        return ret
    
    def __iter__(self):
        self.mbtable_initialized.wait()
        self.init_epoch()
        prefetch_thread = threading.Thread(target=self.prefetch)
        prefetch_thread.start()
        while True:
            try:
                chunk_data = self.cache.get()
                for data in chunk_data:
                    yield data
            except CacheNotFilled:
                time.sleep(0.1)
            except StopIteration:
                self.exhausted = True
                return
    
    def init_epoch(self):
        if self.max_epoch is not None and self.used.epoch >= self.max_epoch:
            self.exhausted = True
        self.cache = PrefetchCache(size=self.prefetch_chunk_cnt)
        epoch_iterator = itertools.count(start=self.used.epoch) if self.max_epoch is None else range(self.used.epoch, self.max_epoch)
        chunks = itertools.chain.from_iterable(
            (self.random_chunks(epoch) for epoch in epoch_iterator)
        )
        chunks = itertools.filterfalse(
            lambda chunk: chunk in self.used.done.get(chunk.epoch, set()), chunks
        )
        self.cache.submit(chunks)

    def safe_chunk_size(self, chunk_size):
        assert chunk_size & (chunk_size - 1) == 0, f"chunk_size must be a power of 2, but got {chunk_size}"
        total_workers = self.num_workers * self.context.world_size
        if self._length < total_workers:
            raise ValueError(
                f"more concurrent loaders ({total_workers}) than " f"data entries ({self._length}) in '{self.path}'"
            )
        num_chunks = math.ceil(self._length / chunk_size)
        if num_chunks <= total_workers:
            chunk_size = self._length // total_workers
            chunk_size = 1 << (chunk_size.bit_length() - 1)
            num_chunks = math.ceil(self._length / chunk_size)
        return chunk_size, num_chunks

    def random_chunks(self, epoch):
        random.seed(self.context.seed)
        world_size = self.context.world_size
        rank = self.context.rank
        num_workers, worker_id = get_worker_info()
        # we only iteratre through start ids as they uniquely mark each slice
        r = Range(0, len(self), self.chunk_size)
        # split index among multi-gpu workers
        r = r.subrange(split=rank, nsplits=world_size)
        # split index among multi-process dataloader workers
        r = r.subrange(split=worker_id, nsplits=num_workers)
        # obtain random chunks
        chunks = (Chunk(epoch, st, min(st + self.chunk_size, len(self))) for st in r.random_iterate())
        return chunks

    def prefetch(self):
        while True:
            try:
                chunk = self.cache.pull_task()
                chunk_data = self.get_chunk_data(chunk)
                unused_chunk_data = [
                    DetailedDoc(position={chunk: [i]}, raw=data)
                    for i, data in zip(range(chunk.start, chunk.stop), chunk_data)
                    if (data is not None) and (i not in self.used.active.get(chunk, set()))
                ]
                self.cache.put_result(unused_chunk_data)
            except CacheFull:
                time.sleep(0.1)
            except AllCached:
                break

    def checkpoint(self):
        return DatasetCheckpoint(
            dataset_info=DatasetInfo(
                path=self.path, 
                max_epoch=self.max_epoch),
            used=self.used, 
            chunk_size=self.shared_chunk_size.value, 
            num_chunks=self.shared_num_chunks.value,
            )
    
    def load_checkpoint(self, checkpoint: DatasetCheckpoint):
        if len(checkpoint.used.active) == 0 and len(checkpoint.used.done) == 0:
            self.used.epoch = 0
        else:
            epochs_not_exhausted = set()
            for chunk in checkpoint.used.active.keys():
                epochs_not_exhausted.add(chunk.epoch)
            epoch = 0
            for epoch in sorted(list(checkpoint.used.done.keys())):
                if len(checkpoint.used.done[epoch]) == checkpoint.num_chunks:
                    del checkpoint.used.done[epoch]
                else:
                    epochs_not_exhausted.add(epoch)
                    break
            epochs_not_exhausted.add(epoch + 1)
            self.used.epoch = min(epochs_not_exhausted, default=0)

        assert checkpoint.chunk_size & (checkpoint.chunk_size - 1) == 0, f"chunk_size must be a power of 2, but got {checkpoint.chunk_size}"
        
        if self.chunk_size == checkpoint.chunk_size:
            self.used = checkpoint.used        
        
        elif self.chunk_size > checkpoint.chunk_size:
            assert self.chunk_size % checkpoint.chunk_size == 0
            for epoch in checkpoint.used.done.keys():
                merge_chunk_map = defaultdict(set)
                for chunk in checkpoint.used.done[epoch]:
                    merge_start = chunk.start - chunk.start % checkpoint.chunk_size
                    merge_stop = min(len(self), merge_start + checkpoint.chunk_size)
                    merge_chunk_map[Chunk(epoch, merge_start, merge_stop)].add(Chunk(epoch, chunk.start, chunk.stop))
                for merge_chunk, to_merge_chunks in merge_chunk_map.items():
                    if len(to_merge_chunks) == (merge_chunk.stop - merge_chunk.start) / checkpoint.chunk_size:
                        self.used.done.setdefault(epoch, set()).add(merge_chunk)
                    else:
                        for to_merge_chunk in to_merge_chunks:
                            self.used.active.setdefault(merge_chunk, set()).update(range(to_merge_chunk.start, to_merge_chunk.stop))
            for chunk, indexes in checkpoint.used.active.items():
                merge_start = chunk.start - chunk.start % self.chunk_size
                merge_stop = min(len(self), merge_start + self.chunk_size)
                self.used.active.setdefault(Chunk(chunk.epoch, merge_start, merge_stop), set()).update(indexes)
        elif self.chunk_size < checkpoint.chunk_size:
            
            assert checkpoint.chunk_size % self.chunk_size == 0
            for epoch in checkpoint.used.done.keys():
                for chunk in checkpoint.used.done[epoch]:
                    for split_start in range(chunk.start, chunk.stop, self.chunk_size):
                        self.used.done.setdefault(epoch, set()).add(Chunk(epoch, split_start, min(split_start + self.chunk_size, len(self))))
            for chunk, indexes in checkpoint.used.active.items():
                for split_start in range(chunk.start, chunk.stop, self.chunk_size):
                    split_stop = min(len(self), split_start + self.chunk_size)
                    split_indexes = set(filter(lambda x: x >= split_start and x < split_stop, indexes))
                    if len(split_indexes) == split_stop - split_start:
                        self.used.done.setdefault(chunk.epoch, set()).add(Chunk(chunk.epoch, split_start, split_stop))
                    else:
                        self.used.active.setdefault(Chunk(chunk.epoch, split_start, split_stop), set()).update(split_indexes)
                    
            
    def update(self, consumed_sample_indexes: Dict[Chunk, List[int]]):
        for chunk, indexes in sorted(consumed_sample_indexes.items(), key=lambda x: x[0].epoch): # chunk with lower epoch comes first
            assert chunk not in self.used.done, f"chunk {chunk} has been done in dataset {self.path} on rank {self.context.rank}, cannot update"
            self.used.active.setdefault(chunk, set()).update(set(indexes))
            
            if len(self.used.active[chunk]) == chunk.stop - chunk.start:
                self.used.done.setdefault(chunk.epoch, set()).add(chunk)
                del self.used.active[chunk]
                
            for epoch in range(chunk.epoch - 1, -1, -1):
                cur_chunk = Chunk(epoch, chunk.start, chunk.stop)
                if cur_chunk in self.used.active:
                    # Note that, if data contains None, it will be filtered out in prefetch, 
                    # active chunk with lower epoch may not len(chunk) == (chunk.stop - chunk.start), but it is still done
                    del self.used.active[cur_chunk]
                    self.used.done.setdefault(epoch, set()).add(cur_chunk)
                else:
                    break

def get_worker_info():
    worker_info = torch.utils.data.get_worker_info()
    if worker_info is None:
        num_workers, worker_id = 1, 0
    else:
        num_workers, worker_id = worker_info.num_workers, worker_info.id
    return num_workers, worker_id


if __name__ == '__main__':
    context = DatasetContext(world_size=1, rank=0, num_workers=1)
    dataset = PrefetchChunkDataset(
        context=context, 
        path="/home/emr-user/modelbest_sdk/test/base_doc_simple",
        max_epoch=3)
    i = 0
    for data in dataset:
        entries = {data['chunk']: [data['index']]}
        dataset.update(entries=entries)
        i += 1
        if i == 29:
            checkpoint = dataset.checkpoint()
            break
    
    print(checkpoint)
    dataset_next = PrefetchChunkDataset(
        context=context, 
        path="/home/emr-user/modelbest_sdk/test/base_doc_simple",
        max_epoch=3)
    dataset_next.load_checkpoint(checkpoint)
    for data in dataset_next:
        entries = {data['chunk']: [data['index']]}
        dataset_next.update(entries=entries)
        i += 1
        print(data)
        if i == 59:
            break
    checkpoint = dataset_next.checkpoint()
    print(checkpoint)