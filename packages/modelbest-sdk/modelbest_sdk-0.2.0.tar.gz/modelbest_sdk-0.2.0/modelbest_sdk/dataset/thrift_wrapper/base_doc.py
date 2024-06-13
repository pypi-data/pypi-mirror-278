import logging
from typing import Dict, List, Tuple, Union
import thriftpy2
from thriftpy2.utils import deserialize, serialize
import os

from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import Chunk, LastSample
from modelbest_sdk.dataset.thrift_wrapper.utils import Utils

proto_dir = os.path.join(os.path.dirname(__file__), "../..", "proto")

doc_thrift = thriftpy2.load(os.path.join(proto_dir, "traindoc.thrift"), module_name="doc_thrift")
logger = logging.getLogger(__name__)


class BaseDoc:
    def __init__(self, token_ids=None, mask=None, docid=None, tag=None, token=None, tokenizer_version=None, reserved_col=None):
        self.token_ids = token_ids
        self.mask = mask
        self.docid = docid
        self.tag = tag
        self.token = token
        self.tokenizer_version = tokenizer_version
        self.reserved_col = reserved_col
    
    def split(self, offset) -> Tuple["BaseDoc", "BaseDoc"]:
        if not (1 <= offset <= len(self.token_ids)):
            raise ValueError("Offset must be between 1 and the length of the token_ids minus one.")
        # Split token_ids and mask with an overlap of one token at offset
        token_ids_1, token_ids_2 = self.token_ids[:offset], self.token_ids[offset-1:]
        mask_1, mask_2 = self.mask[:offset], self.mask[offset-1:]
        
        doc1 = BaseDoc(token_ids=token_ids_1, mask=mask_1, docid=self.docid, tag=self.tag, token=self.token, tokenizer_version=self.tokenizer_version, reserved_col=self.reserved_col)
        doc2 = BaseDoc(token_ids=token_ids_2, mask=mask_2, docid=self.docid, tag=self.tag, token=self.token, tokenizer_version=self.tokenizer_version, reserved_col=self.reserved_col)
        return doc1, doc2
    
    def concat(self, other: "BaseDoc") -> "BaseDoc":
        if self.tag is None or other.tag is None:
            tag = None
        else:
            tag = list(set(self.tag + other.tag))
        return BaseDoc(
            token_ids=self.token_ids + other.token_ids,
            mask=self.mask + other.mask,
            docid=self.docid,
            tag=tag, # TODO：now there should be only one tag since concat happens in the same dataset, and same dataset should have only one tag
            token=self.token,
            tokenizer_version=self.tokenizer_version,
            reserved_col=self.reserved_col
        )

    @staticmethod
    def deserialize(bin):
        return BaseDoc.from_thrift(deserialize(doc_thrift.BaseDoc(), bin))
    
    def serialize(self):
        return serialize(self.to_thrift())
    
    def to_thrift(self):#反射
        return doc_thrift.BaseDoc(
            token_ids=self.token_ids,
            mask=self.mask,
            docid=self.docid,
            tag=self.tag,
            token=self.token,
            tokenizer_version=self.tokenizer_version,
            reserved_col=self.reserved_col
        )
    
    @staticmethod
    def from_thrift(thrift_base_doc):
        return BaseDoc(
            token_ids=thrift_base_doc.token_ids,
            mask=thrift_base_doc.mask,
            docid=thrift_base_doc.docid,
            tag=thrift_base_doc.tag,
            token=thrift_base_doc.token,
            tokenizer_version=thrift_base_doc.tokenizer_version,
            reserved_col=thrift_base_doc.reserved_col
        )
        
    def __repr__(self) -> str:
        return f"BaseDoc(token_ids={self.token_ids}, mask={self.mask}, tag={self.tag}, token={self.token}, tokenizer_version={self.tokenizer_version}, reserved_col={self.reserved_col})"
    
class DetailedDoc:
    def __init__(self, base_doc: BaseDoc=None, position: Dict[Chunk, List[int]]=None, dataset_idx: int=None, raw: str=None, last_sample: LastSample=None):
        self.base_doc = base_doc
        self.position = position
        self.dataset_idx = dataset_idx
        self.raw = raw
        self.last_sample = last_sample
    
    def split(self, offset) -> Tuple["DetailedDoc", "DetailedDoc"]:
        doc1, doc2 = self.base_doc.split(offset)
        return DetailedDoc(base_doc=doc1, position=self.position, dataset_idx=self.dataset_idx, raw=self.raw), \
               DetailedDoc(base_doc=doc2, position=self.position, dataset_idx=self.dataset_idx, raw=self.raw)
    
    def chunk_and_idx(self):
        assert len(self.position) == 1
        assert len(list(self.position.values())[0]) == 1
        chunk, idx_list = list(self.position.items())[0]
        return chunk, idx_list[0]
    
    @staticmethod
    def merge_position(pos1, pos2):
        pos = {}
        for chunk, idx_list in pos1.items():
            if chunk in pos2:
                pos[chunk] = idx_list + pos2[chunk]
            else:
                pos[chunk] = idx_list
        for chunk, idx_list in pos2.items():
            if chunk not in pos1:
                pos[chunk] = idx_list
        return pos
    
    def concat(self, other: "DetailedDoc", is_last_sample: bool=False) -> "DetailedDoc":
        # only used for merging data in the same dataset
        return DetailedDoc(
            base_doc=self.base_doc.concat(other.base_doc),
            position=self.position if is_last_sample else DetailedDoc.merge_position(self.position, other.position),
            dataset_idx=self.dataset_idx,
        )
    
    def __repr__(self) -> str:
        return f"DetailedDoc(base_doc={self.base_doc}, position={self.position}, dataset_idx={self.dataset_idx})"