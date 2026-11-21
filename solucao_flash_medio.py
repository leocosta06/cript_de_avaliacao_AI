from collections import OrderedDict
import heapq

# ==============================================================================
# T1. two_sum
# ==============================================================================
# Tempo: O(n) | Espaço: O(n)
def two_sum(nums: list[int], target: int) -> list[int] | None:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None


# ==============================================================================
# T2. valid_parentheses
# ==============================================================================
# Tempo: O(n) | Espaço: O(n)
def valid_parentheses(s: str) -> bool:
    matching = {")": "(", "]": "[", "}": "{"}
    stack = []
    for char in s:
        if char in matching.values():
            stack.append(char)
        elif char in matching:
            if not stack or stack[-1] != matching[char]:
                return False
            stack.pop()
    return len(stack) == 0


# ==============================================================================
# T3. merge_intervals
# ==============================================================================
# Tempo: O(n log n) | Espaço: O(n)
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0][:]]
    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            merged.append(current[:])
    return merged


# ==============================================================================
# T4. longest_palindrome
# ==============================================================================
# Tempo: O(n^2) | Espaço: O(1)
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


# ==============================================================================
# T5. edit_distance
# ==============================================================================
# Tempo: O(m * n) | Espaço: O(min(m, n))
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


# ==============================================================================
# T6. LRUCache
# ==============================================================================
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
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# ==============================================================================
# T7. dijkstra
# ==============================================================================
# Tempo: O((V + E) log V) | Espaço: O(V)
def dijkstra(graph: dict, start) -> dict:
    nodes = set(graph.keys())
    for edges in graph.values():
        for neighbor, _ in edges:
            nodes.add(neighbor)

    distances = {node: float("inf") for node in nodes}
    if start in distances:
        distances[start] = 0
    else:
        distances[start] = float("inf")
        return distances

    pq = [(0, start)]
    while pq:
        current_dist, u = heapq.heappop(pq)
        if current_dist > distances[u]:
            continue
        for neighbor, weight in graph.get(u, []):
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances


# ==============================================================================
# T8. busca_binaria
# ==============================================================================
# BUGS IDENTIFICADOS:
# 1. `lo = mid`: gera loop infinito quando arr[mid] < x e (hi - lo) == 1,
#    pois a divisão inteira (lo + hi) // 2 resulta em mid == lo. Correção: `lo = mid + 1`.
# 2. Inconsistência nos limites: inicializar com `hi = len(arr)` define um intervalo
#    semiaberto [lo, hi). Nesse padrão, o ajuste superior deveria ser `hi = mid`,
#    enquanto `hi = mid - 1` pula elementos válidos e desalinha os limites.
#    Em contrapartida, no padrão de intervalo fechado [lo, hi], deve-se usar
#    `hi = len(arr) - 1`, `while lo <= hi:` e `hi = mid - 1`.

# Tempo: O(log n) | Espaço: O(1)
def busca_binaria(arr: list[int], x: int) -> int:
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