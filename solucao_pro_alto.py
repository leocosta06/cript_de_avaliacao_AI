# T1
# Tempo: O(n) | Espaço: O(n)
def two_sum(nums, target):
    vistos = {}
    for i, num in enumerate(nums):
        complemento = target - num
        if complemento in vistos:
            return [vistos[complemento], i]
        vistos[num] = i
    return None

# T2
# Tempo: O(n) | Espaço: O(n)
def valid_parentheses(s):
    pilha = []
    pares = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in pares.values():
            pilha.append(char)
        elif char in pares:
            if not pilha or pilha.pop() != pares[char]:
                return False
    return not pilha

# T3
# Tempo: O(n log n) | Espaço: O(n)
def merge_intervals(intervals):
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

# T4
# Tempo: O(n^2) | Espaço: O(1)
def longest_palindrome(s):
    if not s:
        return ""
    
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    maior = ""
    for i in range(len(s)):
        impar = expand_around_center(i, i)
        par = expand_around_center(i, i + 1)
        if len(impar) > len(maior):
            maior = impar
        if len(par) > len(maior):
            maior = par
    return maior

# T5
# Tempo: O(m * n) | Espaço: O(min(m, n))
def edit_distance(a, b):
    if len(a) < len(b):
        a, b = b, a
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    
    for i in range(1, m + 1):
        prev_diag = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if a[i - 1] == b[j - 1]:
                dp[j] = prev_diag
            else:
                dp[j] = 1 + min(dp[j - 1], dp[j], prev_diag)
            prev_diag = temp
    return dp[n]

# T6
# Tempo: O(1) | Espaço: O(capacity)
from collections import OrderedDict

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

# T7
# Tempo: O((V + E) log V) | Espaço: O(V + E)
import heapq

def dijkstra(graph, start):
    todos_nos = set(graph.keys())
    for vizinhos in graph.values():
        for vizinho, _ in vizinhos:
            todos_nos.add(vizinho)
            
    distancias = {no: float('inf') for no in todos_nos}
    if start in distancias:
        distancias[start] = 0
        
    pq = [(0, start)]
    
    while pq:
        dist_atual, no_atual = heapq.heappop(pq)
        
        if dist_atual > distancias.get(no_atual, float('inf')):
            continue
            
        for vizinho, peso in graph.get(no_atual, []):
            distancia = dist_atual + peso
            if distancia < distancias[vizinho]:
                distancias[vizinho] = distancia
                heapq.heappush(pq, (distancia, vizinho))
                
    return distancias

# T8
# Bugs encontrados:
# 1. hi = len(arr) (podia causar out of bounds ou errar o limite lógico, corrigido para len(arr) - 1).
# 2. while lo < hi (falhava se o elemento estivesse em lo == hi, corrigido para lo <= hi).
# 3. lo = mid (causava loop infinito, corrigido para lo = mid + 1).
# Tempo: O(log n) | Espaço: O(1)
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