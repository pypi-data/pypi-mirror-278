from typing import Tuple
import numpy as np
import concurrent.futures
import torch
from modelbest_sdk.dataset.sampler.sampler_factory import WEIGHTED_SAMPLER, WEIGHTED_MEGATRON_SAMPLER,SamplerFactory
from modelbest_sdk.dataset.segment.segment_factory import FIXED_LENGTH_SEGMENT, NO_SEGMENT
from modelbest_sdk.dataset.segment_dataset import SegmentDataset
from modelbest_sdk.dataset.thrift_wrapper.base_doc import DetailedDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import *
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext

logger = logging.getLogger(__name__)

class WeightedDataset(torch.utils.data.IterableDataset):
    def __init__(
        self, 
        context: DatasetContext, 
        dataset_info_list: DatasetInfoList,
        segment_type=NO_SEGMENT,
        sampler_type=WEIGHTED_SAMPLER,
        max_len=1024,
        prefetch_chunk_cnt=2,
        chunk_size=1024,
        ):
        
        self.context = context
        self.dataset_info_list = dataset_info_list.dataset_info_list

        self.dataset_weights = []
        self.datasets: List[SegmentDataset] = []
        self.datasets_iter = []
        weights = []
        for dataset_info in self.dataset_info_list:
            path = dataset_info.path
            weight = dataset_info.weight
            if weight == 0:
                print(f"Dataset {path} has weight 0, skip it")
                continue
            max_epoch = dataset_info.max_epoch
            dataset = SegmentDataset(
                context=context,
                path=path,
                max_epoch=max_epoch,
                segment_type=segment_type,
                max_len=max_len,
                prefetch_chunk_cnt=prefetch_chunk_cnt,
                chunk_size=chunk_size
            )
            self.datasets.append(dataset)
            weights.append(weight)
        weights = np.array(weights)
        self.dataset_weights = weights / weights.sum()
        self.sampler_type = sampler_type

        
        self.current_samples = np.zeros(len(self.dataset_weights), dtype=np.int64)
        self.sample_idx = 0
            
    def worker_init(self, worker_id):
        for dataset in self.datasets:
            dataset.worker_init()
    
    def __iter__(self):
        self.sampler = SamplerFactory.create_sampler(self.sampler_type, weights=self.dataset_weights, rank=self.context.rank, world_size=self.context.world_size, seed=self.context.seed)
        if self.sampler_type == WEIGHTED_MEGATRON_SAMPLER:
            self.sampler.resume(self.sample_idx, self.current_samples)
        for dataset in self.datasets:
            self.datasets_iter.append(iter(dataset))
        while True:
            if all(d.exhausted for d in self.datasets):
                logger.warning(f"All dataset exhaust on rank {self.context.rank}")
                break
            idx = self.sampler()
            if self.datasets[idx].exhausted:
                logger.warning(f"Dataset {idx} exhaust on rank {self.context.rank}")
                self.sampler.remove_index(idx)
                continue
            chosen_iter = self.datasets_iter[idx]
            try:
                data: DetailedDoc = next(chosen_iter)
                if data is None:
                    continue
                data.dataset_idx = idx
                yield data
            except StopIteration:
                continue

    def checkpoint(self):
        checkpoint_list = [dataset.checkpoint() for dataset in self.datasets]
        return DatasetCheckpointList(
            checkpoint_list=checkpoint_list,
            world_size=self.context.world_size,
            tp_size=self.context.tp_size,
            sample_idx=self.sample_idx,
            current_samples=self.current_samples.tolist()
        )
    
    def load_checkpoint(self, dataset_checkpoint_list: DatasetCheckpointList):
        for i, checkpoint in enumerate(dataset_checkpoint_list.checkpoint_list):
            self.datasets[i].load_checkpoint(checkpoint)
        self.sample_idx = dataset_checkpoint_list.sample_idx
        self.current_samples = np.array(dataset_checkpoint_list.current_samples)

    def update(self, consumed_sample_indexes: List[Tuple[int, Dict[Chunk, List[int]]]], last_samples: Dict[int, LastSample]={}):
        '''
        Update dataset checkpoint with consumed samples and last samples in this batch.

        Args:
            consumed_samples: [(dataset_idx, samples), ...]
                - A list where each element represents a sampling action that contributes to a batch.
                - Each element is a tuple:
                    - dataset_idx: The index of the dataset from which samples are taken.
                    - samples: A dictionary where:
                        - key: The Chunk(epoch, start, stop) within the dataset.
                        - value: A list of indexes within the chunk.
                        - EXAMPLE: {Chunk(0, 0, 16): [0, 1, 2], Chunk(0, 16, 32): [16, 17, 18]}

            last_samples: {dataset_idx: LastSample, ...}
                - A dictionary mapping each dataset index to its last partially read sample.
                - LastSample represents the last sample that was not fully consumed in the batch.

                # NOTE: last_samples are used only in scenarios where the raw data is segmented 
                # into multiple lines. This ensures that during resumption, each batch can be 
                # exactly reproduced.
        '''
        for dataset_idx, indexes in consumed_sample_indexes:
            self.datasets[dataset_idx].update(indexes, last_samples.get(dataset_idx, None))
            self.sample_idx += 1
            self.current_samples[dataset_idx] += 1
            
    def __len__(self):
        return sum(len(dataset) for dataset in self.datasets)
    
    def get_path_len_map(self):
        return {dataset.path: len(dataset) for dataset in self.datasets}

if __name__ == '__main__':
    context = DatasetContext(world_size=1, rank=0, num_workers=1)

    dataset_info_list = [
        DatasetInfo(
            path="human.BaseDoc.sstable",
            weight=1,
            max_epoch=1
        ),
        DatasetInfo(
            path="hot_chars.BaseDoc.sstable",
            weight=2,
            max_epoch=2
        )
    ]
    
    dataset_info_list = DatasetInfoList(dataset_info_list=dataset_info_list)
    
    dataset = WeightedDataset(
        context=context,
        dataset_info_list=dataset_info_list,
        segment_type=FIXED_LENGTH_SEGMENT,
    )

    for data in dataset:
        print(data)