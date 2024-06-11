import unittest
from src.sort.insertion_sort import insertion_sort

class TestInsertionSort(unittest.TestCase):
    def test_insertion_sort(self):
        self.assertEqual(insertion_sort([64, 34, 25, 12, 22, 11, 90]), [11, 12, 22, 25, 34, 64, 90])
        self.assertEqual(insertion_sort([5, 1, 4, 2, 8]), [1, 2, 4, 5, 8])
        self.assertEqual(insertion_sort([]), [])
        self.assertEqual(insertion_sort([1]), [1])
        self.assertEqual(insertion_sort([2, 1]), [1, 2])

if __name__ == '__main__':
    unittest.main()
