from modelbest_sdk.dataset.segment.fixed_length_segment import FixedLengthSegment
from modelbest_sdk.dataset.segment.no_segment import NoSegment

NO_SEGMENT = 'no_segment'
FIXED_LENGTH_SEGMENT = 'fixed_length_segment'

class SegmentFactory:
    @staticmethod
    def create_segment(segment_type, max_len: int, drop_last=False):
        if segment_type == NO_SEGMENT:
            return NoSegment()
        elif segment_type == FIXED_LENGTH_SEGMENT:
            return FixedLengthSegment(max_len, drop_last)
        else:
            raise ValueError(f"Unsupported segment type: {segment_type}")