# =====================================================================
# T1. two_sum
# Tempo: O(n) | Espaço: O(n)
# =====================================================================
def two_sum(nums: list[int], target: int) -> list[int] | None:
    seen = {}
    for i, num in enumerate(nums):
        comp = target - num
        if comp in seen:
            return [seen[comp], i]
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
        if char in mapping.values():
            stack.append(char)
        elif char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            return False
    return len(stack) == 0


# =====================================================================
# T3. merge_intervals
# Tempo: O(n log n) | Espaço: O(n)
# =====================================================================
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    intervals_sorted = sorted(intervals, key=lambda x: x[0])
    merged = [intervals_sorted[0][:]]
    for start, end in intervals_sorted[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


# =====================================================================
# T4. longest_palindrome
# Tempo: O(n^2) | Espaço: O(1)
# =====================================================================
def longest_palindrome(s: str) -> str:
    if not s:
        return ""

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right

    start, end = 0, 0
    for i in range(len(s)):
        l1, r1 = expand(i, i)
        l2, r2 = expand(i, i + 1)
        if r1 - l1 > end - start:
            start, end = l1, r1
        if r2 - l2 > end - start:
            start, end = l2, r2

    return s[start:end]


# =====================================================================
# T5. edit_distance
# Tempo: O(m * n) | Espaço: O(min(m, n))
# =====================================================================
def edit_distance(a: str, b: str) -> int:
    m, n = len(a), len(b)
    if m < n:
        a, b = b, a
        m, n = n, m

    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if a[i - 1] == b[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp
    return dp[n]


# =====================================================================
# T6. class LRUCache
# Tempo: O(1) para get e put | Espaço: O(capacity)
# =====================================================================
from collections import OrderedDict


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
import heapq


def dijkstra(graph: dict, start) -> dict:
    nodes = set(graph.keys())
    for neighbors in graph.values():
        for v, _ in neighbors:
            nodes.add(v)
    nodes.add(start)

    dist = {node: float("inf") for node in nodes}
    dist[start] = 0

    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue

        for v, weight in graph.get(u, []):
            new_dist = d + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return dist


# =====================================================================
# T8. busca_binaria
# Tempo: O(log n) | Espaço: O(1)
#
# Bugs encontrados no código original:
# 1. Loop infinito: `lo = mid` não incrementa o índice inferior quando
#    hi - lo == 1 e arr[mid] < x, pois (lo + hi) // 2 resulta em lo.
#    Correção: `lo = mid + 1`.
# 2. Inconsistência de limites (off-by-one): Inicializou `hi = len(arr)`
#    (intervalo semiaberto [lo, hi)), mas no ramo else fez `hi = mid - 1`,
#    o que descarta incorretamente o elemento no índice mid - 1.
#    Correção: Adotar a convenção padrão de intervalo fechado [lo, hi],
#    com `hi = len(arr) - 1`, `while lo <= hi:`, `lo = mid + 1` e `hi = mid - 1`.
# =====================================================================
def busca_binaria(arr, x):
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