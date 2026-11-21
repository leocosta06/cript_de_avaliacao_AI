# Tempo: O(log(min(n, m))) | Espaço: O(1)
def median_of_two_sorted_arrays(a, b) -> float:
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    if m == 0 and n == 0:
        return 0.0
    
    low, high = 0, m
    while low <= high:
        partitionX = (low + high) // 2
        partitionY = (m + n + 1) // 2 - partitionX
        
        maxLeftX = float('-inf') if partitionX == 0 else a[partitionX - 1]
        minRightX = float('inf') if partitionX == m else a[partitionX]
        
        maxLeftY = float('-inf') if partitionY == 0 else b[partitionY - 1]
        minRightY = float('inf') if partitionY == n else b[partitionY]
        
        if maxLeftX <= minRightY and maxLeftY <= minRightX:
            if (m + n) % 2 == 0:
                return (max(maxLeftX, maxLeftY) + min(minRightX, minRightY)) / 2.0
            else:
                return float(max(maxLeftX, maxLeftY))
        elif maxLeftX > minRightY:
            high = partitionX - 1
        else:
            low = partitionX + 1
    return 0.0

# Tempo: get: O(1), put: O(1) | Espaço: O(capacity)
class DLinkedNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.freq = 1
        self.prev = None
        self.next = None

class DLinkedList:
    def __init__(self):
        self.head = DLinkedNode()
        self.tail = DLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_node(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def pop_tail(self):
        if self.size > 0:
            tail = self.tail.prev
            self.remove_node(tail)
            return tail
        return None

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.size = 0
        self.min_freq = 0
        self.cache = {}
        self.freq_map = collections.defaultdict(DLinkedList)

    def _update_node(self, node):
        freq = node.freq
        self.freq_map[freq].remove_node(node)
        if self.min_freq == freq and self.freq_map[freq].size == 0:
            self.min_freq += 1
        node.freq += 1
        self.freq_map[node.freq].add_node(node)

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._update_node(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._update_node(node)
        else:
            if self.size == self.capacity:
                tail = self.freq_map[self.min_freq].pop_tail()
                del self.cache[tail.key]
                self.size -= 1
            new_node = DLinkedNode(key, value)
            self.cache[key] = new_node
            self.freq_map[1].add_node(new_node)
            self.min_freq = 1
            self.size += 1


# Tempo: O(N) | Espaço: O(N)
def evaluate(expr: str) -> float:
    import re
    tokens = re.findall(r'\d+\.\d+|\d+|[+\-*/^()]', expr.replace(' ', ''))
    
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '_': 3, '^': 4}
    right_associative = {'^', '_'}
    
    output = []
    ops = []
    
    prev_token = None
    for token in tokens:
        if re.match(r'^\d+(\.\d+)?$', token):
            output.append(float(token))
        elif token in '+-*/^':
            if token == '-' and (prev_token is None or prev_token in '+-*/^('):
                op = '_'
            elif token == '+' and (prev_token is None or prev_token in '+-*/^('):
                continue
            else:
                op = token
                
            while ops and ops[-1] != '(':
                top = ops[-1]
                if (op not in right_associative and precedence[op] <= precedence[top]) or \
                   (op in right_associative and precedence[op] < precedence[top]):
                    output.append(ops.pop())
                else:
                    break
            ops.append(op)
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while ops and ops[-1] != '(':
                output.append(ops.pop())
            if not ops:
                raise ValueError("Mismatched parentheses")
            ops.pop()
        else:
            raise ValueError(f"Invalid token: {token}")
        prev_token = token
        
    while ops:
        op = ops.pop()
        if op in '()':
            raise ValueError("Mismatched parentheses")
        output.append(op)
        
    stack = []
    for token in output:
        if isinstance(token, float):
            stack.append(token)
        elif token == '_':
            if not stack: raise ValueError("Invalid expression")
            stack.append(-stack.pop())
        else:
            if len(stack) < 2: raise ValueError("Invalid expression")
            b = stack.pop()
            a = stack.pop()
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            elif token == '/':
                if b == 0: raise ZeroDivisionError("Division by zero")
                stack.append(a / b)
            elif token == '^': stack.append(a ** b)
            
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    return stack[0]


# Tempo: O(N) | Espaço: O(N)
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def serialize(root: TreeNode) -> str:
    if not root:
        return "[]"
    
    queue = collections.deque([root])
    res = []
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
        
    return "[" + ",".join(res) + "]"

def deserialize(data: str) -> TreeNode:
    if data == "[]" or not data:
        return None
    
    vals = data[1:-1].split(",")
    root = TreeNode(int(vals[0]))
    queue = collections.deque([root])
    i = 1
    
    while queue and i < len(vals):
        node = queue.popleft()
        
        if vals[i] != "null":
            node.left = TreeNode(int(vals[i]))
            queue.append(node.left)
        i += 1
        
        if i < len(vals) and vals[i] != "null":
            node.right = TreeNode(int(vals[i]))
            queue.append(node.right)
        i += 1
        
    return root


# Tempo: O(N) | Espaço: O(1)
def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
    
    dict_t = collections.Counter(t)
    required = len(dict_t)
    
    l, r = 0, 0
    formed = 0
    window_counts = collections.defaultdict(int)
    
    ans = float("inf"), None, None
    
    while r < len(s):
        char = s[r]
        window_counts[char] += 1
        
        if char in dict_t and window_counts[char] == dict_t[char]:
            formed += 1
            
        while l <= r and formed == required:
            char = s[l]
            
            if r - l + 1 < ans[0]:
                ans = (r - l + 1, l, r)
                
            window_counts[char] -= 1
            if char in dict_t and window_counts[char] < dict_t[char]:
                formed -= 1
                
            l += 1
            
        r += 1
        
    return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]


# Tempo: O(n log n) | Espaço: O(n)
def count_inversions(arr: list[int]) -> int:
    def merge_sort(arr, temp_arr, left, right):
        inv_count = 0
        if left < right:
            mid = (left + right) // 2
            inv_count += merge_sort(arr, temp_arr, left, mid)
            inv_count += merge_sort(arr, temp_arr, mid + 1, right)
            inv_count += merge(arr, temp_arr, left, mid, right)
        return inv_count

    def merge(arr, temp_arr, left, mid, right):
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
            i += 1
            k += 1
            
        while j <= right:
            temp_arr[k] = arr[j]
            j += 1
            k += 1
            
        for loop_var in range(left, right + 1):
            arr[loop_var] = temp_arr[loop_var]
            
        return inv_count

    temp_arr = [0] * len(arr)
    return merge_sort(arr.copy(), temp_arr, 0, len(arr) - 1)


# Tempo: O(V + E log V) | Espaço: O(V + E)
def topo_sort(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    import heapq
    
    graph = collections.defaultdict(list)
    indegree = [0] * n
    
    unique_edges = set(edges)
    
    for u, v in unique_edges:
        if u == v:
            return None
        graph[u].append(v)
        indegree[v] += 1
        
    min_heap = []
    for i in range(n):
        if indegree[i] == 0:
            heapq.heappush(min_heap, i)
            
    topo_order = []
    
    while min_heap:
        u = heapq.heappop(min_heap)
        topo_order.append(u)
        
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                heapq.heappush(min_heap, v)
                
    if len(topo_order) == n:
        return topo_order
    return None


# Tempo: O(N) | Espaço: O(K)
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    if not nums:
        return []
    if k == 1:
        return nums
        
    deq = collections.deque()
    res = []
    
    for i in range(len(nums)):
        while deq and deq[0] < i - k + 1:
            deq.popleft()
            
        while deq and nums[deq[-1]] < nums[i]:
            deq.pop()
            
        deq.append(i)
        
        if i >= k - 1:
            res.append(nums[deq[0]])
            
    return res