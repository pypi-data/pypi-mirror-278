from collections import defaultdict
import hashlib
import torch


class BatchPacker:
    def __init__(self):
        self.hash_to_tag = defaultdict()
    
    def encode_tags(self, token_ids, tag):
        tag_hash = self._get_tag_hash(tag)
        self.hash_to_tag[tag_hash] = tag
        return torch.full((len(token_ids),), tag_hash, dtype=torch.int64)
    
    def _get_tag_hash(self, tag: str) -> int:
        hash_obj = hashlib.sha256(tag.encode('utf-8'))
        return int(hash_obj.hexdigest(), 16) & ((1 << 63) - 1)        
            