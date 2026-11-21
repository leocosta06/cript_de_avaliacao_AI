from collections import OrderedDict
import heapq

# T1. two_sum(nums, target) -> list[int]
# Tempo: O(n) | Espaço: O(n)
def two_sum(nums: list[int], target: int) -> list[int] | None:
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return None


# T2. valid_parentheses(s) -> bool
# Tempo: O(n) | Espaço: O(n)
def valid_parentheses(s: str) -> bool:
    stack = []
    mapping = {")": "(", "]": "[", "}": "{"}
    for char in s:
        if char in mapping:
            top_element = stack.pop() if stack else "#"
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
    return not stack


# T3. merge_intervals(intervals) -> list[list[int]]
# Tempo: O(n log n) | Espaço: O(n)
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for current in intervals[1:]:
        prev = merged[-1]
        if current[0] <= prev[1]:
            prev[1] = max(prev[1], current[1])
        else:
            merged.append(current)
    return merged


# T4. longest_palindrome(s) -> str
# Tempo: O(n^2) | Espaço: O(1)
def longest_palindrome(s: str) -> str:
    if not s:
        return ""
    start, end = 0, 0
    
    def expand_around_center(left: int, right: int) -> int:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1

    for i in range(len(s)):
        len1 = expand_around_center(i, i)
        len2 = expand_around_center(i, i + 1)
        length = max(len1, len2)
        if length > end - start:
            start = i - (length - 1) // 2
            end = i + length // 2
    return s[start:end + 1]


# T5. edit_distance(a, b) -> int
# Tempo: O(m * n) | Espaço: O(m * n)
def edit_distance(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]


# T6. class LRUCache
# Tempo: O(1) para get/put | Espaço: O(capacity)
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


# T7. dijkstra(graph, start) -> dict
# Tempo: O((V + E) log V) | Espaço: O(V + E)
def dijkstra(graph: dict, start) -> dict:
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight in graph.get(current_node, []):
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    return distances


# T8. Correção de bugs e complexidade da busca binária
# Tempo: O(log n) | Espaço: O(1)
# Bugs encontrados na versão original:
# 1. `lo = mid` gera loop infinito quando `arr[mid] < x` (deveria ser `lo = mid + 1`).
# 2. Inicialização com `hi = len(arr)` combinada com `lo < hi` e atualizações incorretas pode causar falhas em limites de array.
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