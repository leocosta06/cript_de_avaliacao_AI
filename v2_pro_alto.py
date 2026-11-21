import collections
import heapq

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
    return 0.0

class _LFUNode:
    __slots__ = ('key', 'val', 'freq', 'prev', 'next')
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.freq = 1
        self.prev = self.next = None

class _LFUDLinkedList:
    def __init__(self):
        self.head = _LFUNode(None, None)
        self.tail = _LFUNode(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def append(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def pop(self, node=None):
        if self.size == 0:
            return None
        if not node:
            node = self.tail.prev
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        return node

# Tempo: O(1) para get e put | Espaço: O(capacity)
class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.size = 0
        self.min_freq = 0
        self.node_map = {}
        self.freq_map = collections.defaultdict(_LFUDLinkedList)

    def _update(self, node):
        freq = node.freq
        self.freq_map[freq].pop(node)
        if self.min_freq == freq and not self.freq_map[freq].size:
            self.min_freq += 1
        node.freq += 1
        self.freq_map[node.freq].append(node)

    def get(self, key: int) -> int:
        if key not in self.node_map:
            return -1
        node = self.node_map[key]
        self._update(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        if key in self.node_map:
            node = self.node_map[key]
            node.val = value
            self._update(node)
        else:
            if self.size == self.cap:
                node = self.freq_map[self.min_freq].pop()
                del self.node_map[node.key]
                self.size -= 1
            new_node = _LFUNode(key, value)
            self.node_map[key] = new_node
            self.freq_map[1].append(new_node)
            self.min_freq = 1
            self.size += 1

# Tempo: O(n) | Espaço: O(n)
def evaluate(expr: str) -> float:
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i].isspace():
            i += 1
        elif expr[i] in '+-*/^()':
            tokens.append(expr[i])
            i += 1
        elif expr[i].isdigit() or expr[i] == '.':
            start = i
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                i += 1
            tokens.append(expr[start:i])
        else:
            raise ValueError(f"Caractere inválido: {expr[i]}")

    parsed_tokens = []
    for i, t in enumerate(tokens):
        if t == '-':
            if i == 0 or tokens[i-1] in '+-*/^(':
                parsed_tokens.append('u-')
            else:
                parsed_tokens.append('-')
        else:
            parsed_tokens.append(t)

    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, 'u-': 3, '^': 4}
    associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R'}

    output = []
    ops = []

    for t in parsed_tokens:
        if t.replace('.', '', 1).isdigit():
            output.append(float(t))
        elif t in precedence:
            if t != 'u-':
                while ops and ops[-1] != '(' and \
                      ((associativity[t] == 'L' and precedence[t] <= precedence[ops[-1]]) or \
                       (associativity[t] == 'R' and precedence[t] < precedence[ops[-1]])):
                    output.append(ops.pop())
            ops.append(t)
        elif t == '(':
            ops.append(t)
        elif t == ')':
            while ops and ops[-1] != '(':
                output.append(ops.pop())
            if not ops:
                raise ValueError("Parênteses desbalanceados")
            ops.pop()
        else:
            raise ValueError(f"Token inválido: {t}")

    while ops:
        if ops[-1] == '(':
            raise ValueError("Parênteses desbalanceados")
        output.append(ops.pop())

    stack = []
    for t in output:
        if isinstance(t, float):
            stack.append(t)
        elif t == 'u-':
            if not stack: raise ValueError("Expressão inválida")
            stack.append(-stack.pop())
        else:
            if len(stack) < 2: raise ValueError("Expressão inválida")
            b = stack.pop()
            a = stack.pop()
            if t == '+': stack.append(a + b)
            elif t == '-': stack.append(a - b)
            elif t == '*': stack.append(a * b)
            elif t == '/':
                if b == 0: raise ZeroDivisionError("Divisão por zero")
                stack.append(a / b)
            elif t == '^':
                stack.append(a ** b)

    if len(stack) != 1:
        raise ValueError("Expressão inválida")
    return stack[0]

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Tempo: O(n) | Espaço: O(n)
def serialize(root) -> str:
    if not root:
        return ""
    q = collections.deque([root])
    res = []
    while q:
        node = q.popleft()
        if node:
            res.append(str(node.val))
            q.append(node.left)
            q.append(node.right)
        else:
            res.append("N")
    while res and res[-1] == "N":
        res.pop()
    return ",".join(res)

# Tempo: O(n) | Espaço: O(n)
def deserialize(data: str):
    if not data:
        return None
    vals = data.split(",")
    root = TreeNode(int(vals[0]))
    q = collections.deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if vals[i] != "N":
            node.left = TreeNode(int(vals[i]))
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] != "N":
            node.right = TreeNode(int(vals[i]))
            q.append(node.right)
        i += 1
    return root

# Tempo: O(n) | Espaço: O(1) (limitado pelo tamanho do alfabeto)
def min_window(s: str, t: str) -> str:
    if not s or not t:
        return ""
    
    dict_t = collections.Counter(t)
    required = len(dict_t)
    
    l = 0
    formed = 0
    window_counts = collections.defaultdict(int)
    
    ans = float("inf"), None, None
    
    for r in range(len(s)):
        char = s[r]
        window_counts[char] += 1
        
        if char in dict_t and window_counts[char] == dict_t[char]:
            formed += 1
            
        while l <= r and formed == required:
            char_l = s[l]
            if r - l + 1 < ans[0]:
                ans = (r - l + 1, l, r)
                
            window_counts[char_l] -= 1
            if char_l in dict_t and window_counts[char_l] < dict_t[char_l]:
                formed -= 1
                
            l += 1
            
    return "" if ans[0] == float("inf") else s[ans[1]: ans[2] + 1]

# Tempo: O(n log n) | Espaço: O(n)
def count_inversions(arr) -> int:
    def merge_sort_and_count(arr, temp_arr, left, right):
        inv_count = 0
        if left < right:
            mid = (left + right) // 2
            inv_count += merge_sort_and_count(arr, temp_arr, left, mid)
            inv_count += merge_sort_and_count(arr, temp_arr, mid + 1, right)
            inv_count += merge_and_count(arr, temp_arr, left, mid, right)
        return inv_count

    def merge_and_count(arr, temp_arr, left, mid, right):
        i = left
        j = mid + 1
        k = left
        inv_count = 0
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp_arr[k] = arr[i]
                i += 1
            else:
                temp_arr[k] = arr[j]
                inv_count += (mid - i + 1)
                j += 1
            k += 1
        while i <= mid:
            temp_arr[k] = arr[i]
            k += 1
            i += 1
        while j <= right:
            temp_arr[k] = arr[j]
            k += 1
            j += 1
        for loop_var in range(left, right + 1):
            arr[loop_var] = temp_arr[loop_var]
        return inv_count

    n = len(arr)
    temp_arr = [0] * n
    return merge_sort_and_count(arr, temp_arr, 0, n - 1)

# Tempo: O(V + E log V) | Espaço: O(V + E) onde V=n, E=len(edges)
def topo_sort(n: int, edges: list) -> list | None:
    adj = collections.defaultdict(list)
    indegree = [0] * n
    
    unique_edges = set(edges)
    for u, v in unique_edges:
        adj[u].append(v)
        indegree[v] += 1
        
    pq = []
    for i in range(n):
        if indegree[i] == 0:
            heapq.heappush(pq, i)
            
    res = []
    while pq:
        u = heapq.heappop(pq)
        res.append(u)
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                heapq.heappush(pq, v)
                
    if len(res) == n:
        return res
    return None

# Tempo: O(n) | Espaço: O(k)
def max_sliding_window(nums, k) -> list:
    if not nums:
        return []
    res = []
    dq = collections.deque()
    for i in range(len(nums)):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res