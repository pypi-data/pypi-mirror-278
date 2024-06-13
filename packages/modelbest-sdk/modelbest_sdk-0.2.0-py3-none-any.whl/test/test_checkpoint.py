import os
import unittest
import torch.distributed as dist
import torch.multiprocessing as mp

from modelbest_sdk.dataset.modelbest_dataloader import CpmFlashAttnDataloader
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import Chunk
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext
from test.test_base import TestBase

class TestCheckpoint(TestBase):
    def test_simple_dataset_checkpoint(self):
        # dataset has 20 records, each records length is 7, max_epoch is 1
        # context suggest to use 16 as batch size * max len, so every 2 records will be grouped into one batch
        context = DatasetContext.load_from_file(self.simple_dataset_context_path)
        dataloader = CpmFlashAttnDataloader(context, self.simple_dataset_info_list, batch_size=1, max_len=16, cuda_prefetch=False)
        for i, batch in enumerate(dataloader, start=1):
            dataloader.update(batch['indexes'])
            if i == 5:
                break
        dataloader.save()
        assert dataloader.checkpoint().checkpoint_list[0].chunk_size == 16
        assert dataloader.checkpoint().checkpoint_list[0].num_chunks == 2
        
        context = DatasetContext.load_from_file(self.simple_dataset_context_path)
        dataloader = CpmFlashAttnDataloader(context, self.simple_dataset_info_list, batch_size=1, max_len=16, cuda_prefetch=False)
        dataloader.resume()

        for i, batch in enumerate(dataloader, start=1):
            dataloader.update(batch['indexes'])
            
        assert dataloader.checkpoint().checkpoint_list[0].used.active == {}
        assert dataloader.checkpoint().checkpoint_list[0].used.done == {0: {Chunk(epoch=0, start=0, stop=16), Chunk(epoch=0, start=16, stop=20)}}
    
    def test_dist_dataset_checkpoint(self):
        context = DatasetContext.load_from_file(self.dist_dataset_context_path)
        dataloader = CpmFlashAttnDataloader(context, self.dist_dataset_info_list, batch_size=1, max_len=16, cuda_prefetch=False)
        for i, batch in enumerate(dataloader, start=1):
            dataloader.update(batch['indexes'])
            # print(batch)
            if i == 30:
                break
        dataloader.save()
        assert dataloader.checkpoint().checkpoint_list[0].num_chunks == 3
        assert dataloader.checkpoint().checkpoint_list[0].chunk_size == 8
        
        dataloader = CpmFlashAttnDataloader(context, self.dist_dataset_info_list, batch_size=1, max_len=16, cuda_prefetch=False)
        dataloader.resume()
        for i, batch in enumerate(dataloader, start=1):
            dataloader.update(batch['indexes'])
            if i == 1001:
                break
        cnt_0 = cnt_1 = 0
        for chunk, set in dataloader.checkpoint().checkpoint_list[0].used.active.items():
            cnt_0 += len(set)
        for epoch, chunk_set in dataloader.checkpoint().checkpoint_list[0].used.done.items():
            for chunk in chunk_set:
                cnt_0 += chunk.stop - chunk.start
        for chunk, set in dataloader.checkpoint().checkpoint_list[1].used.active.items():
            cnt_1 += len(set)
        for epoch, chunk_set in dataloader.checkpoint().checkpoint_list[1].used.done.items():
            for chunk in chunk_set:
                cnt_1 += chunk.stop - chunk.start
        assert round(cnt_1 / cnt_0, 0) == 2 # weight_1 : weight_0 = 2 : 1
        
    
    def test_world_size_change(self):
        world_size = 2
        mp.spawn(process_run, args=(world_size, self.dist_dataset_context_path, self.dist_dataset_info_list, ), nprocs=world_size, join=True)
        world_size = 3
        mp.spawn(process_run, args=(world_size, self.dist_dataset_context_path, self.dist_dataset_info_list, ), nprocs=world_size, join=True)
        


def process_run(rank, world_size, context_path, dataset_info_list):
    print(f"rank {rank} start")
    print(f"world_size {world_size}")
    # 设置环境变量
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'
    
    # 初始化进程组
    dist.init_process_group("gloo", rank=rank, world_size=world_size)


    context = DatasetContext.load_from_file(context_path)
    context.rank = rank
    context.world_size = world_size
    dataloader = CpmFlashAttnDataloader(context, dataset_info_list, batch_size=1, max_len=16, cuda_prefetch=False)
    dataloader.resume()
    print(dataloader.checkpoint().checkpoint_list[0].used)
    for i, batch in enumerate(dataloader, start=1):
        dataloader.update(batch['indexes'])
        if i == 20:
            break
    dataloader.save()
    print(dataloader.checkpoint().checkpoint_list[0].used)
    
    dist.destroy_process_group()

if __name__ == '__main__':
    unittest.main()