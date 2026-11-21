import heapq
from collections import OrderedDict

# T1. two_sum(nums, target) -> list[int]
# Tempo: O(n) | Espaço: O(n)
def two_sum(nums, target) -> list[int]:
    vistos = {}
    for i, num in enumerate(nums):
        complemento = target - num
        if complemento in vistos:
            return [vistos[complemento], i]
        vistos[num] = i
    return None

# T2. valid_parentheses(s) -> bool
# Tempo: O(n) | Espaço: O(n)
def valid_parentheses(s) -> bool:
    mapa = {')': '(', ']': '[', '}': '{'}
    pilha = []
    for char in s:
        if char in mapa.values():
            pilha.append(char)
        elif char in mapa.keys():
            if not pilha or pilha.pop() != mapa[char]:
                return False
    return not pilha

# T3. merge_intervals(intervals) -> list[list[int]]
# Tempo: O(n log n) | Espaço: O(n)
def merge_intervals(intervals) -> list[list[int]]:
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for atual in intervals[1:]:
        ultimo = merged[-1]
        if atual[0] <= ultimo[1]:
            ultimo[1] = max(ultimo[1], atual[1])
        else:
            merged.append(atual)
    return merged

# T4. longest_palindrome(s) -> str
# Tempo: O(n^2) | Espaço: O(1)
def longest_palindrome(s) -> str:
    if not s:
        return ""
    
    def expandir(esq, dir):
        while esq >= 0 and dir < len(s) and s[esq] == s[dir]:
            esq -= 1
            dir += 1
        return s[esq + 1:dir]
    
    maior = ""
    for i in range(len(s)):
        impar = expandir(i, i)
        par = expandir(i, i + 1)
        if len(impar) > len(maior):
            maior = impar
        if len(par) > len(maior):
            maior = par
    return maior

# T5. edit_distance(a, b) -> int
# Tempo: O(m * n) | Espaço: O(m * n)
def edit_distance(a, b) -> int:
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
# Tempo: O(1) para get e put | Espaço: O(capacity)
class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

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
# Tempo: O((V + E) log V) | Espaço: O(V)
def dijkstra(graph, start) -> dict:
    distancias = {no: float('inf') for no in graph}
    distancias[start] = 0
    pq = [(0, start)]
    
    while pq:
        dist_atual, no_atual = heapq.heappop(pq)
        
        if dist_atual > distancias[no_atual]:
            continue
            
        for vizinho, peso in graph.get(no_atual, []):
            dist = dist_atual + peso
            if dist < distancias[vizinho]:
                distancias[vizinho] = dist
                heapq.heappush(pq, (dist, vizinho))
                
    return distancias

# T8. busca_binaria(arr, x)
# Tempo: O(log n) | Espaço: O(1)
# Bugs encontrados e corrigidos:
# 1. 'hi' era len(arr), corrigido para len(arr) - 1.
# 2. 'while lo < hi' corrigido para '<=' para cobrir o último elemento.
# 3. 'lo = mid' corrigido para 'lo = mid + 1' para evitar loop infinito.
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