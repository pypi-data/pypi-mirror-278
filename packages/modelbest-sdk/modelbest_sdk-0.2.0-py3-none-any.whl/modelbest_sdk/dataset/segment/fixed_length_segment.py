from collections import deque
from typing import Generator
from modelbest_sdk.dataset.segment.segment import Segment
from modelbest_sdk.dataset.thrift_wrapper.base_doc import DetailedDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import LastSample


class FixedLengthSegment(Segment):
    def __init__(self, max_len: int, drop_last=False):
        self.max_len = max_len
        self.drop_last = drop_last
        
        self.buffer = deque()
        self.current_length = 0
        
    def put(self, data: DetailedDoc):
        self.buffer.append(data)
        self.current_length += len(data.base_doc.token_ids)
    
    def pop(self) -> DetailedDoc:
        remaining_seq_length = self.max_len + 1
        begin = 0
        concat_data = None
        last_sample = None
        while self.buffer and remaining_seq_length > 0:
            data: DetailedDoc = self.buffer.popleft()
            doc = data.base_doc
            self.current_length -= len(doc.token_ids)
            
            if remaining_seq_length >= len(doc.token_ids):
                end = begin + len(doc.token_ids)
                data_to_fill = data
            else:
                end = begin + remaining_seq_length
                data_to_fill, data_to_buffer = data.split(remaining_seq_length)
                self.buffer.appendleft(data_to_buffer)
                self.current_length += len(data_to_buffer.base_doc.token_ids)
                # useful when resume
                lask_chunk = next(iter(data_to_fill.position.keys()))
                last_index = data_to_fill.position[lask_chunk][0]
                last_offset = remaining_seq_length
                last_sample = LastSample(lask_chunk, last_index, last_offset)
            concat_data = data_to_fill if concat_data is None else concat_data.concat(data_to_fill, last_sample)
            remaining_seq_length -= len(data_to_fill.base_doc.token_ids)
            begin = end
        concat_data.last_sample = last_sample
        return concat_data
            
            
    def __call__(self, detailed_doc: DetailedDoc) -> Generator[DetailedDoc, None, None]:
        self.put(detailed_doc)
        while self.current_length > self.max_len:
            yield self.pop()

