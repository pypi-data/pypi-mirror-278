# Fastest algorithm to calculate h-index in efficient way
# Time complexity: O(nlogn)

from typing import List


def h_index(citations: List[int]) -> int:
    """
    Calculate the h-index for a given list of citations.

    Args:
        citations (List[int]): A list of integers representing the citations of a entity.

    Returns:
        int: The h-index value for the given list of citations.
    """
    citations.sort()
    n = len(citations)
    for i in range(n):
        if citations[i] >= n - i:
            return n - i
    return 0


# Path: scientometrics/indices/h_index.py
