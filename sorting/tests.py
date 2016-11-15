import copy
import random
import unittest

import time

from sorting import bubble_sort, shaker_sort, insertion_sort, merge_sort


class SortingTestCase(unittest.TestCase):

    def setUp(self):
        self.data = [random.randrange(1000) for _ in range(10000)]
        self.data_for_sorting = copy.deepcopy(self.data)
        # sort with python sort
        self.data.sort()
        self.start_time = time.time()

    def tearDown(self):
        print("Execution took {}".format(time.time() - self.start_time))

    def test_bubble_sort(self):
        print("Bubble-Sort")
        self.assertEqual(bubble_sort(self.data_for_sorting), self.data)

    def test_shaker_sort(self):
        print("Shaker-Sort")
        self.assertEqual(shaker_sort(self.data_for_sorting), self.data)

    def test_insertion_sort(self):
        print("Insertion-Sort")
        self.assertEqual(insertion_sort(self.data_for_sorting), self.data)

    def test_merge_sort(self):
        print("Merge-Sort")
        self.assertEqual(merge_sort(self.data_for_sorting), self.data)
