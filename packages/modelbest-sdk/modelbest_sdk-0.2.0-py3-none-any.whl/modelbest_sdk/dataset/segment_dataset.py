from typing import Dict, List
import torch

from modelbest_sdk.dataset.prefetch_chunk_dataset import PrefetchChunkDataset
from modelbest_sdk.dataset.segment.segment_factory import FIXED_LENGTH_SEGMENT, NO_SEGMENT, SegmentFactory
from modelbest_sdk.dataset.thrift_wrapper.base_doc import BaseDoc, DetailedDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import Chunk, DatasetCheckpoint, LastSample
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext


class SegmentDataset(torch.utils.data.IterableDataset):
    def __init__(self, context, path, max_epoch, segment_type=NO_SEGMENT, max_len=1024, prefetch_chunk_cnt=2, chunk_size=1024):
        self.context = context
        self.path = path
        self.prefetch_chunk_dataset = PrefetchChunkDataset(
            context=context,
            path=path,
            max_epoch=max_epoch,
            prefetch_chunk_cnt=prefetch_chunk_cnt,
            chunk_size=chunk_size
        )
        
        self.segment = SegmentFactory.create_segment(segment_type, max_len, drop_last=False)
        self.load_last_sample = None
        self.last_sample = None
    
    @property
    def exhausted(self):
        return self.prefetch_chunk_dataset.exhausted
        
    def worker_init(self):
        self.prefetch_chunk_dataset.worker_init()
    
    def __iter__(self):
        for detailed_doc in self.prefetch_chunk_dataset:
            detailed_doc: DetailedDoc
            detailed_doc.base_doc = BaseDoc.deserialize(detailed_doc.raw)
            chunk, idx = detailed_doc.chunk_and_idx()
            if self.load_last_sample is not None and chunk == self.load_last_sample.chunk and idx == self.load_last_sample.index:
                _, detailed_doc = detailed_doc.split(self.load_last_sample.offset)
            for data in self.segment(detailed_doc):
                if data is not None:
                    yield data 
    
    def checkpoint(self):
        ckpt = self.prefetch_chunk_dataset.checkpoint()
        ckpt.last_sample = self.last_sample
        return ckpt
    
    def load_checkpoint(self, checkpoint: DatasetCheckpoint):
        self.prefetch_chunk_dataset.load_checkpoint(checkpoint)
        self.load_last_sample = checkpoint.last_sample
            
    def update(self, consumed_sample_indexes: Dict[Chunk, List[int]], last_sample: LastSample):
        self.prefetch_chunk_dataset.update(consumed_sample_indexes)
        self.last_sample = last_sample
    
    def __len__(self):
        return len(self.prefetch_chunk_dataset)
    
    
                
if __name__ == '__main__':

    dataset = SegmentDataset(
        context=DatasetContext(),
        path='human.BaseDoc.sstable',
        max_epoch=1,
        segment_type=FIXED_LENGTH_SEGMENT,
        max_len=16
    )
    i = 0
    for data in dataset:
        print(data)
        i += 1
        if i == 100:
            break