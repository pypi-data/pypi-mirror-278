import json
import os
import unittest
from modelbest_sdk.file_format.mbtable import MbTable, MbTableListIterator
from modelbest_sdk.file_format.mbtable_builder import MbTableBuilder


class TestListTable(unittest.TestCase):
    def setUp(self):
        self.path = "test/data/list_table.mbt"
        builder = MbTableBuilder(self.path)
        for i in range(10):
            values=[]
            for j in range(9):
                values.append(json.dumps({"col": f"value_{i}_{j}"}))
            values.append("")
            builder.write_list(values)
        builder.add_metadata("table_type", "list_table")
        builder.flush()
        self.mbtable = MbTable(self.path)
    
    def tearDown(self):
        os.remove(self.path)
    
    def test_get_record(self):
        with self.assertRaises(TypeError):
            self.mbtable.read(0)

    def test_get_list(self):
        for i in range(10): 
            values=[]
            for j in range(9):
                values.append(json.dumps({"col": f"value_{i}_{j}"}).encode())
            values.append(b"")
            self.assertEqual(values, self.mbtable.read_list(i)) 


class TestMbTableListIterator(TestListTable):
    def test_iterator(self):
        cnt = 0
        with MbTableListIterator(self.path) as iterator:
            expected = []
            for i in range(10):
                values = []
                for j in range(9):
                    values.append(json.dumps({"col": f"value_{i}_{j}"}).encode())
                values.append(b"")
                expected.append(values)
            for record in iterator:
                self.assertEqual(expected[cnt], record)
                cnt += 1
        assert cnt == 10
    
    def test_iterator_raw(self):
        iterator = MbTableListIterator(self.path)
        iterator.__enter__()
        record = iterator.__next__()
        iterator.__exit__(None, None, None)
        expected =[]
        for j in range(9):
            expected.append(json.dumps({"col": f"value_0_{j}"}).encode())
        expected.append(b"")
        self.assertEqual(expected, record)
        pass
        

    def test_iterator_with_args(self):
        key, cnt = 5, 0
        with MbTableListIterator(self.path, start_index=key, max_iterations=2) as iterator:  
            for _ in iterator:
                cnt += 1
        assert cnt == 2
        
        key, cnt = 9, 0
        with MbTableListIterator(self.path, start_index=key, max_iterations=1000) as iterator:  
            for _ in iterator:
                cnt += 1
        assert cnt == 1
    
        key, cnt = 1000, 0
        # !!! note that key in mbtable is string and is sorted in lexicographic order
        # so key 1000 is greater than 10 but less than 11, this would start from 11
        with MbTableListIterator(self.path, start_index=key, max_iterations=1000) as iterator:  
            for _ in iterator:
                cnt += 1
        assert cnt == 0


if __name__ == '__main__':
    unittest.main()
