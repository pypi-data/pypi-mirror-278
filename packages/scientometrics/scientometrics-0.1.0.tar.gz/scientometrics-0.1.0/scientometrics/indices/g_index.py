# Calculate g-index in efficient way
# Time complexity: O(nlogn)

from typing import List


def g_index(citations: List[int]) -> int:
    """
    Calculate the g-index for a given list of citations.

    Args:
        citations (List[int]): A list of integers representing the citations of a entity.

    Returns:
        int: The g-index value for the given list of citations.
    """
    citations.sort()
    n = len(citations)
    g = 0
    for i in range(n):
        if citations[i] >= i + 1:
            g = i + 1
    return g


# Path: scientometrics/indices/g_index.py
