import unittest
from src.sort.quick_sort import quick_sort

class TestQuickSort(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(quick_sort([]), [])

    def test_single_element_list(self):
        self.assertEqual(quick_sort([5]), [5])

    def test_already_sorted_list(self):
        self.assertEqual(quick_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_unsorted_list(self):
        self.assertEqual(quick_sort([5, 2, 8, 3, 1]), [1, 2, 3, 5, 8])

if __name__ == '__main__':
    unittest.main()