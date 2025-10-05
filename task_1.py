from typing import List, Tuple

def find_min_max(arr: List[float]) -> Tuple[float, float]:
    """Return (min, max) using divide-and-conquer in O(n)."""
    if not arr:
        raise ValueError("Array must not be empty")

    def rec(lo: int, hi: int) -> Tuple[float, float]:
        length = hi - lo + 1
        if length == 1:
            x = arr[lo]
            return x, x
        if length == 2:
            a, b = arr[lo], arr[hi]
            return (a, b) if a < b else (b, a)
        mid = (lo + hi) // 2
        left_min, left_max = rec(lo, mid)
        right_min, right_max = rec(mid + 1, hi)
        return min(left_min, right_min), max(left_max, right_max)

    return rec(0, len(arr) - 1)

if __name__ == "__main__":
    tests = [
        [5, -2, 9, 1, 9, 3, -7, 4],
        [1],
        [2, 1],
        [10, 3, 8, 6, 7]
    ]
    for t in tests:
        mn, mx = find_min_max(t)
        print(f"Input: {t} -> min={mn}, max={mx}")
