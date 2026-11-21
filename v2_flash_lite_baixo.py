from collections import OrderedDict, defaultdict, deque
import heapq

# H1. median_of_two_sorted_arrays
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


# H2. LFUCache
# Tempo: O(1) para get e put | Espaço: O(capacity)
class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val = {}
        self.key_to_freq = {}
        self.freq_to_keys = defaultdict(OrderedDict)

    def get(self, key: int) -> int:
        if key not in self.key_to_val:
            return -1
        self._update_freq(key)
        return self.key_to_val[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.key_to_val:
            self.key_to_val[key] = value
            self._update_freq(key)
            return
        if len(self.key_to_val) >= self.capacity:
            evict_freq_keys = self.freq_to_keys[self.min_freq]
            evict_key, _ = evict_freq_keys.popitem(last=False)
            del self.key_to_val[evict_key]
            del self.key_to_freq[evict_key]
        
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1

    def _update_freq(self, key: int):
        freq = self.key_to_freq[key]
        self.freq_to_keys[freq].pop(key)
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if freq == self.min_freq:
                self.min_freq += 1
        self.key_to_freq[key] = freq + 1
        self.freq_to_keys[freq + 1][key] = None


# H3. evaluate
# Tempo: O(n) | Espaço: O(n)
def evaluate(expr: str) -> float:
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        if c in "+-*/^()":
            tokens.append(c)
            i += 1
        elif c.isdigit() or c == '.':
            start = i
            has_dot = (c == '.')
            i += 1
            while i < n and (expr[i].isdigit() or (expr[i] == '.' and not has_dot)):
                if expr[i] == '.':
                    has_dot = True
                i += 1
            num_str = expr[start:i]
            if num_str == '.':
                raise ValueError("Invalid number")
            tokens.append(float(num_str) if '.' in num_str else int(num_str))
        else:
            raise ValueError(f"Invalid character: {c}")

    processed_tokens = []
    expect_operand = True
    for token in tokens:
        if token in "(+ -":
            if token in "+-":
                if expect_operand:
                    if token == '-':
                        processed_tokens.append('U-')
                    else:
                        processed_tokens.append('U+')
                    continue
            processed_tokens.append(token)
            expect_operand = True
        elif token in "*/^":
            if expect_operand:
                raise ValueError("Unexpected operator")
            processed_tokens.append(token)
            expect_operand = True
        elif token == ')':
            if expect_operand:
                raise ValueError("Unexpected closing parenthesis")
            processed_tokens.append(token)
            expect_operand = False
        else:
            if not expect_operand:
                raise ValueError("Expected operator")
            processed_tokens.append(token)
            expect_operand = False

    if expect_operand and processed_tokens and processed_tokens[-1] not in "()":
        raise ValueError("Trailing operator")

    prec = {'+': 1, '-': 1, '*': 2, '/': 2, 'U+': 3, 'U-': 3, '^': 4}
    right_assoc = {'^': True, 'U+': True, 'U-': True}

    output_queue = []
    op_stack = []

    for token in processed_tokens:
        if isinstance(token, (int, float)):
            output_queue.append(token)
        elif token in prec:
            while op_stack and op_stack[-1] in prec:
                top = op_stack[-1]
                if (not right_assoc.get(token, False) and prec[token] <= prec[top]) or \
                   (right_assoc.get(token, False) and prec[token] < prec[top]):
                    output_queue.append(op_stack.pop())
                else:
                    break
            op_stack.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack and op_stack[-1] != '(':
                output_queue.append(op_stack.pop())
            if not op_stack:
                raise ValueError("Mismatched parentheses")
            op_stack.pop()

    while op_stack:
        top = op_stack.pop()
        if top == '(' or top == ')':
            raise ValueError("Mismatched parentheses")
        output_queue.append(top)

    stack = []
    for token in output_queue:
        if isinstance(token, (int, float)):
            stack.append(float(token))
        elif token == 'U+':
            if not stack: raise ValueError("Invalid expression")
        elif token == 'U-':
            if not stack: raise ValueError("Invalid expression")
            stack.append(-stack.pop())
        else:
            if len(stack) < 2:
                raise ValueError("Invalid expression")
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                stack.append(a / b)
            elif token == '^':
                try:
                    res = a ** b
                except OverflowError:
                    res = float('inf')
                stack.append(res)

    if len(stack) != 1:
        raise ValueError("Invalid expression")
    return stack[0]


# H4. serialize and deserialize
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Tempo: O(n) | Espaço: O(n)
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

# Tempo: O(n) | Espaço: O(n)
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


# H5. min_window
# Tempo: O(n) | Espaço: O(sigma)
def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
    dict_t = defaultdict(int)
    for c in t:
        dict_t[c] += 1
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


# H6. count_inversions
# Tempo: O(n log n) | Espaço: O(n)
def count_inversions(arr: list[int]) -> int:
    def merge_sort(lst):
        if len(lst) <= 1:
            return lst, 0
        mid = len(lst) // 2
        left, inv_left = merge_sort(lst[:mid])
        right, inv_right = merge_sort(lst[mid:])
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


# H7. topo_sort
# Tempo: O(E + V log V) | Espaço: O(V + E)
def topo_sort(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    adj = {i: set() for i in range(n)}
    in_degree = [0] * n
    for u, v in edges:
        if u < 0 or u >= n or v < 0 or v >= n or u == v:
            return None
        if v not in adj[u]:
            adj[u].add(v)
            in_degree[v] += 1

    pq = [i for i in range(n) if in_degree[i] == 0]
    heapq.heapify(pq)
    
    order = []
    while pq:
        u = heapq.heappop(pq)
        order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(pq, v)
                
    if len(order) != n:
        return None
    return order


# H8. max_sliding_window
# Tempo: O(n) | Espaço: O(k)
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0:
        return []
    if k == 1:
        return nums
    
    res = []
    dq = deque()
    
    for i, val in enumerate(nums):
        if dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] <= val:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            res.append(nums[dq[0]])
            
    return res