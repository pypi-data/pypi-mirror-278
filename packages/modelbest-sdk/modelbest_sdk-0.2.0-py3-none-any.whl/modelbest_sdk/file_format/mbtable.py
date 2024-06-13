import ctypes
import os

class ByteArray(ctypes.Structure):
    _fields_ = [("data", ctypes.POINTER(ctypes.c_char)),
                ("length", ctypes.c_size_t)]

class ByteArrayList(ctypes.Structure):
    _fields_ = [("data_list", ctypes.POINTER(ByteArray)),
                ("size", ctypes.c_size_t)]

class MetaDataEntry(ctypes.Structure):
    _fields_ = [("key", ctypes.c_char_p),
                ("value", ctypes.c_char_p)]

class MetaDataList(ctypes.Structure):
    _fields_ = [("entries", ctypes.POINTER(MetaDataEntry)),
                ("count", ctypes.c_int)]
    
    def to_dict(self):
        # 将entries转换为Python字典
        return {self.entries[i].key.decode("utf-8"): self.entries[i].value.decode("utf-8") for i in range(self.count)}


lib_path = os.path.join(os.path.dirname(__file__), 'lib', 'libmbtable_sdk_shared.so')
lib = ctypes.CDLL(lib_path)


lib.MbTableOpen.argtypes = [ctypes.c_char_p]
lib.MbTableOpen.restype = ctypes.c_void_p

lib.MbTableClose.argtypes = [ctypes.c_void_p]
lib.MbTableClose.restype = None

lib.MbTableRead.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
lib.MbTableRead.restype = ctypes.POINTER(ByteArray)

lib.MbTableReadList.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
lib.MbTableReadList.restype = ctypes.POINTER(ByteArrayList)

lib.MbTableGetMetaData.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
lib.MbTableGetMetaData.restype = ctypes.POINTER(ByteArray)

lib.MbTableGetAllMetaData.argtypes = [ctypes.c_void_p, ctypes.POINTER(MetaDataList)]
lib.MbTableGetAllMetaData.restype = None

lib.MbTableGetEntryCount.argtypes = [ctypes.c_void_p]
lib.MbTableGetEntryCount.restype = ctypes.c_int32

# Get metadata by giving file path.
lib.GetFileMetaData.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.GetFileMetaData.restype = ctypes.POINTER(ByteArray)

# Get entry count by giving file path.
lib.GetFileEntryCount.argtypes = [ctypes.c_char_p]
lib.GetFileEntryCount.restype = ctypes.c_int32

# Single record iterator methods
lib.MbTableCreateIterator.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
lib.MbTableCreateIterator.restype = ctypes.c_void_p

lib.IteratorGetRecord.argtypes = [ctypes.c_void_p]
lib.IteratorGetRecord.restype = ctypes.POINTER(ByteArray)

lib.IteratorHasNext.argtypes = [ctypes.c_void_p]
lib.IteratorHasNext.restype = ctypes.c_bool

lib.IteratorNext.argtypes = [ctypes.c_void_p]
lib.IteratorNext.restype = None

lib.IteratorDelete.argtypes = [ctypes.c_void_p]
lib.IteratorDelete.restype = None

# List record iterator methods
lib.MbTableCreateListIterator.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
lib.MbTableCreateIterator.restype = ctypes.c_void_p

lib.IteratorGetList.argtypes = [ctypes.c_void_p]
lib.IteratorGetList.restype = ctypes.POINTER(ByteArrayList)

lib.ListIteratorHasNext.argtypes = [ctypes.c_void_p]
lib.ListIteratorHasNext.restype = ctypes.c_bool

lib.ListIteratorNext.argtypes = [ctypes.c_void_p]
lib.ListIteratorNext.restype = None

lib.ListIteratorDelete.argtypes = [ctypes.c_void_p]
lib.ListIteratorDelete.restype = None

lib.FreeByteArray.argtypes = [ctypes.POINTER(ByteArray)]
lib.FreeByteArray.restype = None

lib.FreeByteArrayList.argtypes = [ctypes.POINTER(ByteArrayList)]
lib.FreeByteArrayList.restype = None

class MbTable:
    def __init__(self, path: str, max_retry=5):
        if not os.path.exists(path):
            raise Exception(f'MbTable file {path} not found')
        self.path = path
        self.max_retry = max_retry
        
    def get_handle(self):
        self.handle = lib.MbTableOpen(self.path.encode('utf-8'))
        retry = 0
        while not self.handle and retry < self.max_retry:
            retry += 1
            print('Failed to open mbtable, retrying in 5 second')
            import time
            import random
            time.sleep(random.randint(1, 5))
            self.handle = lib.MbTableOpen(self.path.encode('utf-8'))
        if not self.handle:
            raise Exception(f'Failed to open mbtable after {self.max_retry} retries')

        return self.handle

    def read(self, index):
        '''
        only use this method if you seek few non-sequential records, otherwise use iterator
        '''
        table_type = self.get_metadata('table_type')
        if table_type == b"list_table":
            raise TypeError('read() function does not support list_table')

        self.get_handle()
        value_bytes = lib.MbTableRead(self.handle, index).contents
        value = ctypes.string_at(value_bytes.data, value_bytes.length)
        lib.FreeByteArray(value_bytes)
        self.close()
        return value

    def read_list(self, index):
        '''
        only use this method if you seek a record of list data, otherwise use
        iterator.
        '''
        table_type = self.get_metadata("table_type")
        if table_type != b"list_table":
            raise TypeError('readlist() function only supports list_table')

        self.get_handle()
        ret = lib.MbTableReadList(self.handle, index).contents
        values = []
        for i in range(0, ret.size):
            values.append(ctypes.string_at(ret.data_list[i].data,
                                           ret.data_list[i].length))
        lib.FreeByteArrayList(ret)
        self.close()
        return values

    def get_metadata(self, metadata_key):
        self.get_handle()
        key_bytes = metadata_key.encode('utf-8')
        value_bytes = lib.MbTableGetMetaData(self.handle, key_bytes).contents
        value = ctypes.string_at(value_bytes.data, value_bytes.length)
        lib.FreeByteArray(value_bytes)
        self.close()
        return value
    
    def get_file_metadata(self, metadata_key):
        path_bytes = self.path.encode('utf-8')
        key_bytes = metadata_key.encode('utf-8')
        value_bytes = lib.GetFileMetaData(path_bytes, key_bytes).contents
        value = ctypes.string_at(value_bytes.data, value_bytes.length)
        lib.FreeByteArray(value_bytes)
        return value
        
    def get_all_metadata(self):
        self.get_handle()
        meta_list = MetaDataList()
        lib.MbTableGetAllMetaData(self.handle, ctypes.byref(meta_list))
        return meta_list.to_dict()

    def get_entry_count(self):
        self.get_handle()
        count = lib.MbTableGetEntryCount(self.handle)
        self.close()
        return count

    def get_file_entry_count(self):
        path_bytes = self.path.encode('utf-8')
        count = lib.GetFileEntryCount(path_bytes)
        return count

    def close(self):
        if self.handle:
            lib.MbTableClose(self.handle)
            self.handle = None

class MbTableIterator:
    def __init__(self, path, start_index=0, max_iterations=None):
        self.path = path
        self.start_index = start_index
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.iterator = None
        self.mbtable = None

    def __enter__(self):
        self.mbtable = MbTable(self.path)
        self.iterator = lib.MbTableCreateIterator(self.mbtable.get_handle(), self.start_index)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.iterator:
            lib.IteratorDelete(self.iterator)
        if self.mbtable:
            self.mbtable.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.max_iterations is not None and self.current_iteration >= self.max_iterations:
            raise StopIteration
        if lib.IteratorHasNext(self.iterator):
            self.current_iteration += 1
            value = self.get_record()
            lib.IteratorNext(self.iterator)
            return value
        else:
            raise StopIteration

    def next(self):
        # Python 2的兼容性方法
        return self.__next__()
    
    def get_record(self):
        ret = lib.IteratorGetRecord(self.iterator).contents
        record = ctypes.string_at(ret.data, ret.length)
        lib.FreeByteArray(ret)
        return record


class MbTableListIterator:
    def __init__(self, path, start_index=0, max_iterations=None):
        self.path = path
        self.start_index = start_index
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.iterator = None
        self.mbtable = None

    def __enter__(self):
        self.mbtable = MbTable(self.path)
        self.iterator = lib.MbTableCreateListIterator(
                self.mbtable.get_handle(), self.start_index)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.iterator:
            lib.ListIteratorDelete(self.iterator)
        if self.mbtable:
            self.mbtable.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.max_iterations is not None and self.current_iteration >= self.max_iterations:
            raise StopIteration
        if lib.ListIteratorHasNext(self.iterator):
            self.current_iteration += 1
            values = self.get_records()
            lib.ListIteratorNext(self.iterator)
            return values
        else:
            raise StopIteration

    def next(self):
        # Python 2的兼容性方法
        return self.__next__()
    
    def get_record(self):
        raise TypeError('get_record() is not supported, use get_records() instead.')

    def get_records(self):
        ret = lib.IteratorGetList(self.iterator).contents
        values = []
        for i in range(0, ret.size):
            values.append(ctypes.string_at(ret.data_list[i].data,
                                           ret.data_list[i].length))
        lib.FreeByteArrayList(ret)
        return values


if __name__ == '__main__':
    mbt_path = '/mnt/jfs-ee/jeeves-agi/projects/8691-qwen-megatron-sft-sst/checkpoints/sstable/whoru'
    mbtable = MbTable(mbt_path)
    print(mbtable.get_entry_count())
    # print(mbtable.read(1))
    print(mbtable.get_metadata('meta_key'))
    print(mbtable.get_all_metadata())
    from modelbest_sdk.dataset.thrift_wrapper.base_doc import BaseDoc
    with MbTableIterator(mbt_path) as it:
        for record in it:
            print(record)
            doc = BaseDoc.deserialize(record)
            print(doc)
            break
