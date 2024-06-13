import unittest
from sort.insertion_sort import Insertion

class TestInsertionSort(unittest.TestCase):
    def test_insertion(self):
        arr = [0, 50, 7, 34, 66, 85]
        print('this is the unsorted list:')
        print(arr)
        result = Insertion.insertion_sort(arr)
        print('this is the (insertion) sorted list:')
        print(result)

if __name__ == "__main__":
    unittest.main()