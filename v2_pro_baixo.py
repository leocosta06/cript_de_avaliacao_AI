import collections
import heapq
import math

# Tempo: O(log(min(n, m))) | Espaço: O(1)
def median_of_two_sorted_arrays(a, b) -> float:
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    low, high = 0, m
    while low <= high:
        partition_a = (low + high) // 2
        partition_b = (m + n + 1) // 2 - partition_a
        
        max_left_a = float('-inf') if partition_a == 0 else a[partition_a - 1]
        min_right_a = float('inf') if partition_a == m else a[partition_a]
        
        max_left_b = float('-inf') if partition_b == 0 else b[partition_b - 1]
        min_right_b = float('inf') if partition_b == n else b[partition_b]
        
        if max_left_a <= min_right_b and max_left_b <= min_right_a:
            if (m + n) % 2 == 0:
                return (max(max_left_a, max_left_b) + min(min_right_a, min_right_b)) / 2.0
            else:
                return float(max(max_left_a, max_left_b))
        elif max_left_a > min_right_b:
            high = partition_a - 1
        else:
            low = partition_a + 1
    raise ValueError

# Tempo: O(1) | Espaço: O(capacity)
class Node:
    def __init__(self, key, val):
        self.key, self.val, self.freq = key, val, 1
        self.prev = self.next = None

class DLinkedList:
    def __init__(self):
        self.head, self.tail = Node(0, 0), Node(0, 0)
        self.head.next, self.tail.prev = self.tail, self.head
        self.size = 0
    def insert(self, node):
        node.next, node.prev = self.head.next, self.head
        self.head.next.prev, self.head.next = node, node
        self.size += 1
    def pop(self, node=None):
        if self.size == 0: return None
        if not node: node = self.tail.prev
        node.prev.next, node.next.prev = node.next, node.prev
        self.size -= 1
        return node

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity, self.size, self.min_freq = capacity, 0, 0
        self.node_map = {}
        self.freq_map = collections.defaultdict(DLinkedList)
        
    def _update(self, node):
        freq = node.freq
        self.freq_map[freq].pop(node)
        if self.min_freq == freq and not self.freq_map[freq].size:
            self.min_freq += 1
        node.freq += 1
        self.freq_map[node.freq].insert(node)

    def get(self, key: int) -> int:
        if key not in self.node_map: return -1
        node = self.node_map[key]
        self._update(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0: return
        if key in self.node_map:
            node = self.node_map[key]
            node.val = value
            self._update(node)
        else:
            if self.size == self.capacity:
                node = self.freq_map[self.min_freq].pop()
                del self.node_map[node.key]
                self.size -= 1
            node = Node(key, value)
            self.node_map[key] = node
            self.freq_map[1].insert(node)
            self.min_freq, self.size = 1, self.size + 1

# Tempo: O(n) | Espaço: O(n)
def evaluate(expr: str) -> float:
    def parse(s):
        tokens = []
        i, n = 0, len(s)
        while i < n:
            if s[i].isspace():
                i += 1
            elif s[i] in "+-*/^()":
                tokens.append(s[i])
                i += 1
            else:
                j = i
                while j < n and (s[j].isdigit() or s[j] == '.'):
                    j += 1
                if i == j: raise ValueError
                tokens.append(float(s[i:j]))
                i = j
        return tokens

    tokens = parse(expr)
    if not tokens: raise ValueError
    
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 'u-': 4}
    right_assoc = {'^'}
    
    output = []
    ops = []
    
    prev_is_op = True
    for t in tokens:
        if isinstance(t, float):
            output.append(t)
            prev_is_op = False
        elif t == '-':
            if prev_is_op: ops.append('u-')
            else:
                while ops and ops[-1] != '(' and (precedence[ops[-1]] > precedence['-'] or (precedence[ops[-1]] == precedence['-'] and '-' not in right_assoc)):
                    output.append(ops.pop())
                ops.append('-')
                prev_is_op = True
        elif t in "+*/^":
            if prev_is_op: raise ValueError
            while ops and ops[-1] != '(' and (precedence[ops[-1]] > precedence[t] or (precedence[ops[-1]] == precedence[t] and t not in right_assoc)):
                output.append(ops.pop())
            ops.append(t)
            prev_is_op = True
        elif t == '(':
            ops.append(t)
            prev_is_op = True
        elif t == ')':
            if prev_is_op: raise ValueError
            while ops and ops[-1] != '(':
                output.append(ops.pop())
            if not ops: raise ValueError
            ops.pop()
            prev_is_op = False
            
    while ops:
        if ops[-1] == '(': raise ValueError
        output.append(ops.pop())
        
    stack = []
    for t in output:
        if isinstance(t, float): stack.append(t)
        elif t == 'u-':
            if not stack: raise ValueError
            stack.append(-stack.pop())
        else:
            if len(stack) < 2: raise ValueError
            b, a = stack.pop(), stack.pop()
            if t == '+': stack.append(a + b)
            elif t == '-': stack.append(a - b)
            elif t == '*': stack.append(a * b)
            elif t == '/': 
                if b == 0: raise ZeroDivisionError
                stack.append(a / b)
            elif t == '^': stack.append(a ** b)
            
    if len(stack) != 1: raise ValueError
    return stack[0]

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Tempo: O(n) | Espaço: O(n)
def serialize(root) -> str:
    if not root: return ""
    res, stack = [], [root]
    while stack:
        node = stack.pop()
        if node:
            res.append(str(node.val))
            stack.append(node.right)
            stack.append(node.left)
        else:
            res.append("#")
    return ",".join(res)

# Tempo: O(n) | Espaço: O(n)
def deserialize(data: str) -> TreeNode:
    if not data: return None
    vals = iter(data.split(","))
    val = next(vals)
    root = TreeNode(int(val))
    stack = [[root, 0]]
    for val in vals:
        if val == "#":
            node = None
        else:
            node = TreeNode(int(val))
        while stack[-1][1] == 2:
            stack.pop()
        parent = stack[-1][0]
        if stack[-1][1] == 0:
            parent.left = node
        else:
            parent.right = node
        stack[-1][1] += 1
        if node:
            stack.append([node, 0])
    return root

# Tempo: O(n) | Espaço: O(1)
def min_window(s, t) -> str:
    if not t or not s: return ""
    req = collections.Counter(t)
    required = len(req)
    l, r, formed = 0, 0, 0
    window = collections.defaultdict(int)
    ans = float("inf"), None, None
    while r < len(s):
        c = s[r]
        window[c] += 1
        if c in req and window[c] == req[c]:
            formed += 1
        while l <= r and formed == required:
            c = s[l]
            if r - l + 1 < ans[0]: ans = (r - l + 1, l, r)
            window[c] -= 1
            if c in req and window[c] < req[c]: formed -= 1
            l += 1
        r += 1
    return "" if ans[0] == float("inf") else s[ans[1]:ans[2]+1]

# Tempo: O(n log n) | Espaço: O(n)
def count_inversions(arr) -> int:
    def merge_sort(a, temp, left, right):
        inv = 0
        if left < right:
            mid = (left + right) // 2
            inv += merge_sort(a, temp, left, mid)
            inv += merge_sort(a, temp, mid + 1, right)
            inv += merge(a, temp, left, mid, right)
        return inv
    def merge(a, temp, left, mid, right):
        i, j, k = left, mid + 1, left
        inv = 0
        while i <= mid and j <= right:
            if a[i] <= a[j]:
                temp[k] = a[i]
                i += 1
            else:
                temp[k] = a[j]
                inv += (mid - i + 1)
                j += 1
            k += 1
        while i <= mid:
            temp[k] = a[i]
            i += 1
            k += 1
        while j <= right:
            temp[k] = a[j]
            j += 1
            k += 1
        for idx in range(left, right + 1):
            a[idx] = temp[idx]
        return inv
    return merge_sort(list(arr), [0]*len(arr), 0, len(arr)-1)

# Tempo: O(V + E log V) | Espaço: O(V + E)
def topo_sort(n, edges) -> list[int] | None:
    adj = collections.defaultdict(list)
    indegree = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indegree[v] += 1
    
    pq = [i for i in range(n) if indegree[i] == 0]
    heapq.heapify(pq)
    
    res = []
    while pq:
        u = heapq.heappop(pq)
        res.append(u)
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                heapq.heappush(pq, v)
                
    return res if len(res) == n else None

# Tempo: O(n) | Espaço: O(k)
def max_sliding_window(nums, k) -> list[int]:
    if not nums or k == 0: return []
    q = collections.deque()
    res = []
    for i in range(len(nums)):
        while q and q[0] < i - k + 1:
            q.popleft()
        while q and nums[q[-1]] < nums[i]:
            q.pop()
        q.append(i)
        if i >= k - 1:
            res.append(nums[q[0]])
    return res