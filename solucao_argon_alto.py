from collections import OrderedDict
import heapq


# ==========================================
# T1
# Tempo: O(n) | Espaço: O(n)
# ==========================================
def two_sum(nums, target) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None


# ==========================================
# T2
# Tempo: O(n) | Espaço: O(n)
# ==========================================
def valid_parentheses(s) -> bool:
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in ('(', '[', '{'):
            stack.append(char)
        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
        else:
            return False
    return len(stack) == 0


# ==========================================
# T3
# Tempo: O(n log n) | Espaço: O(n)
# ==========================================
def merge_intervals(intervals) -> list[list[int]]:
    if not intervals:
        return []
    sorted_intervals = sorted(intervals, key=lambda x: (x[0], x[1]))
    merged = [[sorted_intervals[0][0], sorted_intervals[0][1]]]
    for start, end in sorted_intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


# ==========================================
# T4
# Tempo: O(n^2) | Espaço: O(1) auxiliar (O(n) para a substring de saída)
# ==========================================
def longest_palindrome(s) -> str:
    if not s:
        return ""
    n = len(s)
    start, max_len = 0, 1

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - left - 1

    for i in range(n):
        l1, len1 = expand(i, i)
        if len1 > max_len:
            start, max_len = l1, len1

        l2, len2 = expand(i, i + 1)
        if len2 > max_len:
            start, max_len = l2, len2

    return s[start:start + max_len]


# ==========================================
# T5
# Tempo: O(n * m) | Espaço: O(min(n, m))
# ==========================================
def edit_distance(a, b) -> int:
    if len(a) < len(b):
        a, b = b, a
    m = len(b)
    prev = list(range(m + 1))
    for char_a in a:
        curr = [prev[0] + 1]
        for j, char_b in enumerate(b, 1):
            if char_a == char_b:
                curr.append(prev[j - 1])
            else:
                curr.append(1 + min(
                    curr[-1],    # Inserir
                    prev[j],     # Remover
                    prev[j - 1]  # Substituir
                ))
        prev = curr
    return prev[m]


# ==========================================
# T6
# Tempo: O(1) para get e put | Espaço: O(capacity)
# ==========================================
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


# ==========================================
# T7
# Tempo: O((V + E) log V) | Espaço: O(V)
# ==========================================
def dijkstra(graph, start) -> dict:
    distances = {node: float('inf') for node in graph}
    for edges in graph.values():
        for neighbor, _ in edges:
            if neighbor not in distances:
                distances[neighbor] = float('inf')

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


# ==========================================
# T8
# Tempo: O(log n) | Espaço: O(1)
# ==========================================
# BUGS ENCONTRADOS NO CÓDIGO ORIGINAL:
# 1. Inconsistência de intervalo fechado vs. semiaberto em `hi = len(arr)` e `while lo < hi`:
#    - O código mistura convenção de intervalo semiaberto `[lo, hi)` (ao iniciar `hi = len(arr)`
#      e usar `lo < hi`) com atualização de intervalo fechado `[lo, hi]` (`hi = mid - 1`).
#    - Com `while lo < hi` e `hi = mid - 1`, o índice `mid - 1` é descartado sem ser testado
#      quando `lo == mid - 1` (ex.: `arr = [1, 3], x = 1` -> `mid = 1`, `hi` vira `0`, o loop
#      termina pois `0 < 0` é falso e retorna `-1` incorretamente).
#    - Adicionalmente, se adotado o intervalo fechado `while lo <= hi`, iniciar `hi = len(arr)`
#      causaria `IndexError` caso `x` seja maior que todos os elementos.
# 2. Loop infinito em `lo = mid` (no ramo `elif arr[mid] < x`):
#    - Como `mid = (lo + hi) // 2` arredonda para baixo, quando `hi == lo + 1`, temos `mid == lo`.
#      Se `arr[mid] < x`, fazer `lo = mid` não avança `lo`, gerando loop infinito.
#    - Além disso, `arr[mid]` já foi testado e é menor que `x`, portanto o novo limite inferior
#      deve ser `lo = mid + 1`.
#
# CORREÇÃO (adotando intervalo fechado padrão [lo, hi]):
# - Inicializar `hi = len(arr) - 1`
# - Alterar condição do loop para `while lo <= hi:`
# - Atualizar `lo = mid + 1` quando `arr[mid] < x`
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