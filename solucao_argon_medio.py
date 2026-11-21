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
    mapping = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        elif char in '([{':
            stack.append(char)
    return not stack


# T3
# Tempo: O(n log n) | Espaço: O(n)
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [[sorted_intervals[0][0], sorted_intervals[0][1]]]
    for current in sorted_intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            merged.append([current[0], current[1]])
    return merged


# T4
# Tempo: O(n^2) | Espaço: O(1)
def longest_palindrome(s: str) -> str:
    if not s:
        return ""
    start, max_len = 0, 1

    for i in range(len(s)):
        # Palíndromos de tamanho ímpar
        l, r = i, i
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if (r - l + 1) > max_len:
                start = l
                max_len = r - l + 1
            l -= 1
            r += 1

        # Palíndromos de tamanho par
        l, r = i, i + 1
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if (r - l + 1) > max_len:
                start = l
                max_len = r - l + 1
            l -= 1
            r += 1

    return s[start:start + max_len]


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
        for v, _ in neighbors:
            nodes.add(v)

    dist = {node: float('inf') for node in nodes}
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, weight in graph.get(u, []):
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))

    return dist


# T8
# Tempo: O(log n) | Espaço: O(1)
# Bugs encontrados no código original:
# 1. Inicialização de `hi = len(arr)` com atualização `hi = mid - 1` mistura intervalos
#    semi-abertos [lo, hi) com intervalos fechados [lo, hi]. Se `hi = mid - 1` é usado,
#    `hi` deve iniciar em `len(arr) - 1`.
# 2. Condição `while lo < hi:` combinada com `hi = mid - 1` falha em verificar o último
#    elemento restante quando `lo == hi` (ex: array de 1 elemento ou elemento na borda).
#    O correto para intervalo fechado é `while lo <= hi:`.
# 3. `lo = mid` no ramo `elif arr[mid] < x:` causa loop infinito quando `lo + 1 == hi`
#    (pois `mid` será igual a `lo`, não avançando os limites da busca). Deve ser `lo = mid + 1`.
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