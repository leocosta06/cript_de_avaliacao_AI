# T1
# Tempo: O(n) | Espaço: O(n)
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return None

# T2
# Tempo: O(n) | Espaço: O(n)
def valid_parentheses(s):
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    return not stack

# T3
# Tempo: O(n log n) | Espaço: O(n)
def merge_intervals(intervals):
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
    
    longest = ""
    for i in range(len(s)):
        pal1 = expand_around_center(i, i)
        if len(pal1) > len(longest):
            longest = pal1
            
        pal2 = expand_around_center(i, i + 1)
        if len(pal2) > len(longest):
            longest = pal2
            
    return longest

# T5
# Tempo: O(m * n) | Espaço: O(m * n)
def edit_distance(a, b):
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
                dp[i][j] = 1 + min(dp[i - 1][j],      # remoção
                                   dp[i][j - 1],      # inserção
                                   dp[i - 1][j - 1])  # substituição
    return dp[m][n]

# T6
# Tempo: O(1) | Espaço: O(capacity)
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# T7
# Tempo: O((V + E) log V) | Espaço: O(V)
import heapq

def dijkstra(graph, start):
    nodes = set(graph.keys())
    for edges in graph.values():
        for neighbor, _ in edges:
            nodes.add(neighbor)
            
    distances = {node: float('inf') for node in nodes}
    if start in distances:
        distances[start] = 0
    else:
        distances[start] = 0
        
    pq = [(0, start)]
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_dist > distances.get(current_node, float('inf')):
            continue
            
        for neighbor, weight in graph.get(current_node, []):
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    return distances

# T8
# Bugs encontrados no código original:
# 1. Limite superior: 'hi = len(arr)' deveria ser 'len(arr) - 1' para funcionar com índices inclusivos.
# 2. Condição do while: 'lo < hi' falha quando o alvo é o último elemento; deve ser 'lo <= hi'.
# 3. Atualização do limite inferior: 'lo = mid' causa loop infinito se arr[mid] < x e lo, hi são adjacentes; deve ser 'lo = mid + 1'.
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