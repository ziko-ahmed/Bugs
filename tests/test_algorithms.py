"""Tests for Hard Bug: Algorithms"""

import threading
from src.algorithms import binary_search, merge_sort, find_duplicates


class TestBinarySearch:
    def test_find_existing(self):
        arr = [1, 3, 5, 7, 9, 11, 13]
        assert binary_search(arr, 7) == 3

    def test_find_first(self):
        arr = [1, 3, 5, 7, 9]
        assert binary_search(arr, 1) == 0

    def test_find_last(self):
        """This test exposes the infinite loop bug when target > arr[mid]."""
        arr = [1, 3, 5, 7, 9]
        result = [None]
        error = [None]

        def run_search():
            try:
                result[0] = binary_search(arr, 9)
            except Exception as e:
                error[0] = e

        t = threading.Thread(target=run_search, daemon=True)
        t.start()
        t.join(timeout=2)  # 2-second timeout

        if t.is_alive():
            assert False, "binary_search entered an infinite loop (hung for >2s)"
        assert result[0] == 4

    def test_not_found(self):
        arr = [1, 3, 5, 7, 9]
        assert binary_search(arr, 6) == -1

    def test_empty_array(self):
        assert binary_search([], 5) == -1


class TestMergeSort:
    def test_basic_sort(self):
        assert merge_sort([3, 1, 4, 1, 5, 9]) == [1, 1, 3, 4, 5, 9]

    def test_already_sorted(self):
        assert merge_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        assert merge_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]  # Will fail: wrong merge

    def test_single_element(self):
        assert merge_sort([42]) == [42]

    def test_empty(self):
        assert merge_sort([]) == []

    def test_duplicates(self):
        assert merge_sort([3, 3, 1, 1, 2, 2]) == [1, 1, 2, 2, 3, 3]  # Will fail


class TestFindDuplicates:
    def test_with_duplicates(self):
        assert find_duplicates([1, 2, 3, 2, 4, 3, 5]) == [2, 3]

    def test_no_duplicates(self):
        assert find_duplicates([1, 2, 3, 4, 5]) == []

    def test_all_same(self):
        assert find_duplicates([7, 7, 7, 7]) == [7]
