import copy
from typing import Iterable
import torch

from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext


class CudaPrefetcher(Iterable):
    """
    Wrap around a batch iterator for asynchornously copying data to gpu to shield memcpy latency.
    """

    def __init__(self, context: DatasetContext, loader):
        self.context = context
        self.loader = iter(loader)
        self.stream = torch.cuda.Stream()
        self.preload()

    def preload(self):
        try:
            self.data = next(self.loader)
        except StopIteration:
            self.data = None
            return
        with torch.cuda.stream(self.stream):
            for key in self.data.keys():
                if isinstance(self.data[key], torch.Tensor):
                    self.data[key] = self.data[key].cuda(non_blocking=True)

    def __next__(self):
        torch.cuda.current_stream().wait_stream(self.stream)
        data = copy.deepcopy(self.data)
        self.preload()
        return data

    def __iter__(self):
        return self
