import heapq
from collections import OrderedDict

# =====================================================================
# T1. two_sum
# Tempo: O(n) | Espaço: O(n)
# =====================================================================
def two_sum(nums: list[int], target: int) -> list[int] | None:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None


# =====================================================================
# T2. valid_parentheses
# Tempo: O(n) | Espaço: O(n)
# =====================================================================
def valid_parentheses(s: str) -> bool:
    mapping = {")": "(", "]": "[", "}": "{"}
    stack = []
    for char in s:
        if char in mapping:
            top_element = stack.pop() if stack else "#"
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
    return not stack


# =====================================================================
# T3. merge_intervals
# Tempo: O(n log n) | Espaço: O(n)
# =====================================================================
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)
    return merged


# =====================================================================
# T4. longest_palindrome
# Tempo: O(n^2) | Espaço: O(1)
# =====================================================================
def longest_palindrome(s: str) -> str:
    if not s:
        return ""

    start, max_len = 0, 1

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - left - 1

    for i in range(len(s)):
        l1, len1 = expand(i, i)
        l2, len2 = expand(i, i + 1)
        if len1 > max_len:
            start, max_len = l1, len1
        if len2 > max_len:
            start, max_len = l2, len2

    return s[start : start + max_len]


# =====================================================================
# T5. edit_distance
# Tempo: O(m * n) | Espaço: O(min(m, n))
# =====================================================================
def edit_distance(a: str, b: str) -> int:
    if len(a) < len(b):
        a, b = b, a
    m, n = len(a), len(b)
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev = curr
    return prev[n]


# =====================================================================
# T6. class LRUCache
# Tempo: get: O(1), put: O(1) | Espaço: O(capacity)
# =====================================================================
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# =====================================================================
# T7. dijkstra
# Tempo: O((V + E) log V) | Espaço: O(V + E)
# =====================================================================
def dijkstra(graph: dict, start) -> dict:
    distances = {node: float("inf") for node in graph}
    if start not in distances:
        distances[start] = float("inf")
    distances[start] = 0.0

    pq = [(0.0, start)]
    while pq:
        curr_dist, u = heapq.heappop(pq)
        if curr_dist > distances[u]:
            continue
        for v, weight in graph.get(u, []):
            if v not in distances:
                distances[v] = float("inf")
            if curr_dist + weight < distances[v]:
                distances[v] = curr_dist + weight
                heapq.heappush(pq, (distances[v], v))

    return distances


# =====================================================================
# T8. busca_binaria
# Bugs encontrados no código original:
# 1. 'lo = mid' causa loop infinito se len(arr) == 2 e x está à direita,
#    pois (lo + hi) // 2 resulta em lo, tornando a atribuição redundante.
# 2. Inconsistência de limites: ao inicializar com hi = len(arr) (intervalo
#    semiaberto [lo, hi)), a redução deveria ser 'hi = mid', e não 'mid - 1',
#    que pode excluir o elemento correto da busca.
#
# Tempo: O(log n) | Espaço: O(1)
# =====================================================================
def busca_binaria(arr: list, x) -> int:
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1