from collections import OrderedDict
import heapq


# T1
# Tempo: O(n) | Espaço: O(n)
def two_sum(nums: list[int], target: int) -> list[int] | None:
    seen = {}
    for i, num in enumerate(nums):
        comp = target - num
        if comp in seen:
            return [seen[comp], i]
        seen[num] = i
    return None


# T2
# Tempo: O(n) | Espaço: O(n)
def valid_parentheses(s: str) -> bool:
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for char in s:
        if char in pairs.values():
            stack.append(char)
        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
        else:
            return False
    return len(stack) == 0


# T3
# Tempo: O(n log n) | Espaço: O(n)
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [[sorted_intervals[0][0], sorted_intervals[0][1]]]
    for start, end in sorted_intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


# T4
# Tempo: O(n^2) | Espaço: O(1)
def longest_palindrome(s: str) -> str:
    if not s:
        return ""
    start, max_len = 0, 1
    n = len(s)

    def expand(left: int, right: int) -> None:
        nonlocal start, max_len
        while left >= 0 and right < n and s[left] == s[right]:
            curr_len = right - left + 1
            if curr_len > max_len:
                start = left
                max_len = curr_len
            left -= 1
            right += 1

    for i in range(n):
        expand(i, i)
        expand(i, i + 1)

    return s[start : start + max_len]


# T5
# Tempo: O(m * n) | Espaço: O(min(m, n))
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


# T6
# Tempo: O(1) para get e put | Espaço: O(capacity)
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
        if self.capacity <= 0:
            return
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# T7
# Tempo: O((V + E) log V) | Espaço: O(V)
def dijkstra(graph: dict, start) -> dict:
    nodes = set(graph.keys())
    for neighbors in graph.values():
        for neighbor, _ in neighbors:
            nodes.add(neighbor)

    distances = {node: float("inf") for node in nodes}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        curr_dist, u = heapq.heappop(pq)
        if curr_dist > distances[u]:
            continue
        for v, weight in graph.get(u, []):
            new_dist = curr_dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return distances


# T8
# Tempo: O(log n) | Espaço: O(1)
# Bugs encontrados no código original:
# 1. Inicialização/Condição inconsistentes: `hi = len(arr)` define um intervalo semiaberto [lo, hi),
#    mas no `else` foi usado `hi = mid - 1` (típico de intervalo fechado [lo, hi]), fazendo o algoritmo
#    pular e perder o elemento na posição `mid - 1`.
# 2. Loop infinito: Em `elif arr[mid] < x:`, fazer `lo = mid` não avança o ponteiro quando `lo + 1 == hi`
#    (pois `mid` será igual a `lo`), causando loop infinito se `x` for maior que `arr[lo]`.
# Correção: Usar intervalo fechado `hi = len(arr) - 1`, condição `while lo <= hi:` e `lo = mid + 1`.
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