import unittest
from sort.quick_sort import Quick

class TestQuickSort(unittest.TestCase):

    def test_quick(self):
        arr = [0, 50, 7, 34, 66, 85]
        print('this is the unsorted list:')
        print(arr)
        result = Quick.quick_sort(arr)
        print('this is the (quick) sorted list:')
        print(result)

if __name__ == "__main__":
    unittest.main()