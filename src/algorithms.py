"""
🐛 Hard Bug: Sorting and searching algorithms with subtle logic errors.

Bug: binary_search has incorrect mid-point calculation (can infinite loop).
Bug: merge_sort mutates sublists incorrectly during merge.
Bug: find_duplicates misses consecutive duplicates.
"""


def binary_search(arr: list[int], target: int) -> int:
    """
    Return the index of target in sorted arr, or -1 if not found.
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid  # 🐛 BUG: should be mid + 1 — causes infinite loop
        else:
            right = mid - 1

    return -1


def merge_sort(arr: list[int]) -> list[int]:
    """Sort a list using merge sort. Returns a new sorted list."""
    if len(arr) <= 1:
        return arr[:]

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # 🐛 BUG: appends the wrong remaining list
    result.extend(right[j:])
    result.extend(right[i:])  # should be left[i:]

    return result


def find_duplicates(arr: list) -> list:
    """Find all duplicate values in a list. Returns sorted list of duplicates."""
    seen = set()
    duplicates = []

    for item in arr:
        if item in seen:
            duplicates.append(item)
        seen.add(item)

    return sorted(set(duplicates))  # This one actually works correctly
