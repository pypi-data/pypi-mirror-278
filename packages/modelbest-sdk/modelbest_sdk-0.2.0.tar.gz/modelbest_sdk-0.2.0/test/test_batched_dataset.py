import torch
from modelbest_sdk.dataset.modelbest_dataloader import CpmFlashAttnDataloader
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext
from test.test_base import TestBase


class TestBatchedDataset(TestBase):
    def test_pack_batch(self):
        context = DatasetContext.load_from_file(self.simple_dataset_context_path)
        dataloader = CpmFlashAttnDataloader(context, self.simple_dataset_info_list, batch_size=1, max_len=16, cuda_prefetch=False)
        for batch in dataloader:
            '''
            doc.token_ids = [-1, 2, 3, 4, 5, 6, 0]
            doc.mask = [False, False, False, False, False, False, True]
            '''
            assert (batch['input_ids'] == torch.tensor([[-1, 2, 3, 4, 5, 6, 0, -1, 2, 3, 4, 5, 6, 0, 0, 0]])).all()
            assert batch['input_ids'].shape == torch.Size([1, 16])
            assert (batch['target_ids'] == torch.tensor([[2, 3, 4, 5, 6, -100, -100, 2, 3, 4, 5, 6, -100, -100, -100, -100]])).all()
            assert batch['target_ids'].shape == torch.Size([1, 16])
            assert (batch['cu_seqlens'] == torch.tensor([ 0,  7, 14, 16])).all()
            assert (batch['position_ids'] == torch.tensor([[0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 0]])).all()