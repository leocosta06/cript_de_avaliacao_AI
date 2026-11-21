from collections import defaultdict, OrderedDict, deque
import heapq
import re

# Tempo: O(log(min(n, m))) | Espaço: O(1)
def median_of_two_sorted_arrays(a: list[int], b: list[int]) -> float:
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    total_left = (m + n + 1) // 2
    low, high = 0, m
    while low <= high:
        i = (low + high) // 2
        j = total_left - i
        a_left = a[i - 1] if i > 0 else float('-inf')
        a_right = a[i] if i < m else float('inf')
        b_left = b[j - 1] if j > 0 else float('-inf')
        b_right = b[j] if j < n else float('inf')
        
        if a_left <= b_right and b_left <= a_right:
            if (m + n) % 2 == 1:
                return float(max(a_left, b_left))
            else:
                return float(max(a_left, b_left) + min(a_right, b_right)) / 2.0
        elif a_left > b_right:
            high = i - 1
        else:
            low = i + 1
    return 0.0


# Tempo: O(1) | Espaço: O(capacity)
class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.vals = {}
        self.counts = {}
        self.lists = defaultdict(OrderedDict)

    def get(self, key: int) -> int:
        if self.capacity <= 0 or key not in self.vals:
            return -1
        freq = self.counts[key]
        del self.lists[freq][key]
        if not self.lists[freq] and self.min_freq == freq:
            self.min_freq += 1
        
        self.counts[key] = freq + 1
        self.lists[freq + 1][key] = None
        return self.vals[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self.get(key)
            return
        
        if len(self.vals) >= self.capacity:
            evict_key, _ = self.lists[self.min_freq].popitem(last=False)
            del self.vals[evict_key]
            del self.counts[evict_key]
        
        self.vals[key] = value
        self.counts[key] = 1
        self.min_freq = 1
        self.lists[1][key] = None


# Tempo: O(n) | Espaço: O(n)
def evaluate(expr: str) -> float:
    token_pattern = re.compile(r'\s*([0-9]+(?:\.[0-9]+)?|\+|\-|\*|/|\^|\(|\))')
    tokens = []
    pos = 0
    while pos < len(expr):
        match = token_pattern.match(expr, pos)
        if not match:
            if expr[pos].isspace():
                pos += 1
                continue
            raise ValueError(f"Invalid character: {expr[pos]}")
        tokens.append(match.group(1))
        pos = match.end(0)
    
    if not tokens:
        raise ValueError("Empty expression")

    idx = 0

    def peek():
        return tokens[idx] if idx < len(tokens) else None

    def consume():
        nonlocal idx
        tok = tokens[idx]
        idx += 1
        return tok

    def parse_expression():
        return parse_additive()

    def parse_additive():
        val = parse_multiplicative()
        while peek() in ('+', '-'):
            op = consume()
            right = parse_multiplicative()
            if op == '+':
                val += right
            else:
                val -= right
        return val

    def parse_multiplicative():
        val = parse_exponent()
        while peek() in ('*', '/'):
            op = consume()
            right = parse_exponent()
            if op == '*':
                val *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                val /= right
        return val

    def parse_exponent():
        val = parse_unary()
        if peek() == '^':
            consume()
            right = parse_exponent()
            try:
                val = val ** right
            except ZeroDivisionError:
                raise ZeroDivisionError("Division by zero in exponent")
        return val

    def parse_unary():
        if peek() == '+':
            consume()
            return parse_unary()
        elif peek() == '-':
            consume()
            return -parse_unary()
        return parse_primary()

    def parse_primary():
        tok = peek()
        if tok is None:
            raise ValueError("Unexpected end of expression")
        if tok == '(':
            consume()
            val = parse_expression()
            if peek() == ')':
                consume()
            else:
                raise ValueError("Missing closing parenthesis")
            return val
        else:
            consume()
            try:
                return float(tok)
            except ValueError:
                raise ValueError(f"Invalid number: {tok}")

    result = parse_expression()
    if idx < len(tokens):
        raise ValueError("Extra tokens at the end")
    return result


# Tempo: O(n) | Espaço: O(n)
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def serialize(root: TreeNode) -> str:
    if not root:
        return ""
    res = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node:
            res.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        else:
            res.append("null")
    while res and res[-1] == "null":
        res.pop()
    return ",".join(res)

def deserialize(data: str) -> TreeNode:
    if not data:
        return None
    vals = data.split(",")
    root = TreeNode(int(vals[0]))
    queue = deque([root])
    i = 1
    while queue and i < len(vals):
        node = queue.popleft()
        if i < len(vals) and vals[i] != "null":
            node.left = TreeNode(int(vals[i]))
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] != "null":
            node.right = TreeNode(int(vals[i]))
            queue.append(node.right)
        i += 1
    return root


# Tempo: O(n) | Espaço: O(n)
from collections import Counter
def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
    dict_t = Counter(t)
    required = len(dict_t)
    l, r = 0, 0
    formed = 0
    window_counts = {}
    ans = float("inf"), None, None
    
    while r < len(s):
        character = s[r]
        window_counts[character] = window_counts.get(character, 0) + 1
        
        if character in dict_t and window_counts[character] == dict_t[character]:
            formed += 1
            
        while l <= r and formed == required:
            character = s[l]
            if r - l + 1 < ans[0]:
                ans = (r - l + 1, l, r)
            
            window_counts[character] -= 1
            if character in dict_t and window_counts[character] < dict_t[character]:
                formed -= 1
            l += 1
        r += 1
        
    return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]


# Tempo: O(n log n) | Espaço: O(n)
def count_inversions(arr: list[int]) -> int:
    def merge_sort(sub_arr):
        if len(sub_arr) <= 1:
            return sub_arr, 0
        mid = len(sub_arr) // 2
        left, inv_left = merge_sort(sub_arr[:mid])
        right, inv_right = merge_sort(sub_arr[mid:])
        merged, inv_merge = merge(left, right)
        return merged, inv_left + inv_right + inv_merge

    def merge(left, right):
        res = []
        i = j = inv = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                res.append(left[i])
                i += 1
            else:
                res.append(right[j])
                inv += len(left) - i
                j += 1
        res.extend(left[i:])
        res.extend(right[j:])
        return res, inv

    _, total_inv = merge_sort(arr)
    return total_inv


# Tempo: O(V + E log V) | Espaço: O(V + E)
def topo_sort(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    adj = defaultdict(list)
    in_degree = [0] * n
    
    unique_edges = set(edges)
    for u, v in unique_edges:
        if 0 <= u < n and 0 <= v < n:
            if u == v:
                return None
            adj[u].append(v)
            in_degree[v] += 1
        else:
            return None
            
    heap = [i for i in range(n) if in_degree[i] == 0]
    heapq.heapify(heap)
    
    res = []
    while heap:
        u = heapq.heappop(heap)
        res.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)
                
    if len(res) != n:
        return None
    return res


# Tempo: O(n) | Espaço: O(k)
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0:
        return []
    res = []
    dq = deque()
    for i in range(len(nums)):
        if dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res