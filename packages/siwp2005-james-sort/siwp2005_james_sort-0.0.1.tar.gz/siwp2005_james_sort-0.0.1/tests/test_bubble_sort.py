import unittest
from src.sort.bubble_sort import bubble_sort

class TestBubbleSort(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(bubble_sort([]), [])

    def test_single_element_list(self):
        self.assertEqual(bubble_sort([1]), [1])

    def test_already_sorted_list(self):
        self.assertEqual(bubble_sort([1, 2, 3]), [1, 2, 3])

    def test_unsorted_list(self):
        self.assertEqual(bubble_sort([3, 2, 1]), [1, 2, 3])

if __name__ == '__main__':
    unittest.main()