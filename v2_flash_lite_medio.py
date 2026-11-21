import collections
import heapq

# H1
# Tempo: O(log(min(n, m))) | Espaço: O(1)
def median_of_two_sorted_arrays(a: list[int], b: list[int]) -> float:
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    imin, imax, half_len = 0, m, (m + n + 1) // 2
    while imin <= imax:
        i = (imin + imax) // 2
        j = half_len - i
        if i < m and b[j - 1] > a[i]:
            imin = i + 1
        elif i > 0 and a[i - 1] > b[j]:
            imax = i - 1
        else:
            if i == 0: max_of_left = b[j - 1]
            elif j == 0: max_of_left = a[i - 1]
            else: max_of_left = max(a[i - 1], b[j - 1])
            
            if (m + n) % 2 == 1:
                return float(max_of_left)
            
            if i == m: min_of_right = b[j]
            elif j == n: min_of_right = a[i]
            else: min_of_right = min(a[i], b[j])
            
            return (max_of_left + min_of_right) / 2.0
    return 0.0


# H2
# Tempo: O(1) | Espaço: O(capacity)
class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val_freq = {}
        self.freq_to_keys = {}

    def get(self, key: int) -> int:
        if self.capacity <= 0 or key not in self.key_to_val_freq:
            return -1
        val, freq = self.key_to_val_freq[key]
        self._update_freq(key, val, freq)
        return val

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.key_to_val_freq:
            val, freq = self.key_to_val_freq[key]
            self.key_to_val_freq[key] = [value, freq]
            self._update_freq(key, value, freq)
            return
        if len(self.key_to_val_freq) >= self.capacity:
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val_freq[evict_key]
            if not self.freq_to_keys[self.min_freq]:
                del self.freq_to_keys[self.min_freq]
        
        self.key_to_val_freq[key] = [value, 1]
        if 1 not in self.freq_to_keys:
            self.freq_to_keys[1] = collections.OrderedDict()
        self.freq_to_keys[1][key] = None
        self.min_freq = 1

    def _update_freq(self, key, val, freq):
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        next_freq = freq + 1
        if next_freq not in self.freq_to_keys:
            self.freq_to_keys[next_freq] = collections.OrderedDict()
        self.freq_to_keys[next_freq][key] = None


# H3
# Tempo: O(n) | Espaço: O(n)
def evaluate(expr: str) -> float:
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        c = expr[i]
        if c.isspace():
            i += 1
        elif c in "+-*/^()":
            tokens.append(c)
            i += 1
        elif c.isdigit() or c == '.':
            start = i
            has_dot = False
            while i < n and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i] == '.':
                    if has_dot:
                        raise ValueError("Invalid decimal")
                    has_dot = True
                i += 1
            tokens.append(expr[start:i])
        else:
            raise ValueError(f"Invalid character {c}")
    
    pos = 0
    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def consume(expected=None):
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError("Unexpected end of expression")
        t = tokens[pos]
        if expected and t != expected:
            raise ValueError(f"Expected {expected}, got {t}")
        pos += 1
        return t

    def parse_expr():
        val = parse_term()
        while peek() in ('+', '-'):
            op = consume()
            right = parse_term()
            if op == '+': val += right
            else: val -= right
        return val

    def parse_term():
        val = parse_factor()
        while peek() in ('*', '/'):
            op = consume()
            right = parse_factor()
            if op == '*': val *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                val /= right
        return val

    def parse_factor():
        if peek() == '+':
            consume('+')
            return parse_power()
        elif peek() == '-':
            consume('-')
            return -parse_power()
        return parse_power()

    def parse_power():
        base = parse_base()
        if peek() == '^':
            consume('^')
            exp = parse_power()
            try:
                return base ** exp
            except OverflowError:
                return float('inf')
        return base

    def parse_base():
        t = peek()
        if t == '(':
            consume('(')
            val = parse_expr()
            consume(')')
            return val
        elif t is not None and (t[0].isdigit() or t[0] == '.'):
            consume()
            return float(t)
        else:
            raise ValueError("Invalid expression")

    if not tokens:
        raise ValueError("Empty expression")
    
    val = parse_expr()
    if pos < len(tokens):
        raise ValueError("Trailing tokens")
    return val


# H4
# Tempo: O(n) | Espaço: O(n)
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def serialize(root) -> str:
    if not root:
        return ""
    res = []
    queue = collections.deque([root])
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

def deserialize(data) -> TreeNode | None:
    if not data:
        return None
    nodes = data.split(",")
    root = TreeNode(int(nodes[0]))
    queue = collections.deque([root])
    i = 1
    while queue and i < len(nodes):
        node = queue.popleft()
        if i < len(nodes) and nodes[i] != "null":
            node.left = TreeNode(int(nodes[i]))
            queue.append(node.left)
        i += 1
        if i < len(nodes) and nodes[i] != "null":
            node.right = TreeNode(int(nodes[i]))
            queue.append(node.right)
        i += 1
    return root


# H5
# Tempo: O(n) | Espaço: O(n)
def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
    dict_t = collections.Counter(t)
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


# H6
# Tempo: O(n log n) | Espaço: O(n)
def count_inversions(arr: list[int]) -> int:
    def merge_sort(arr, temp, left, right):
        inv_count = 0
        if left < right:
            mid = (left + right) // 2
            inv_count += merge_sort(arr, temp, left, mid)
            inv_count += merge_sort(arr, temp, mid + 1, right)
            inv_count += merge(arr, temp, left, mid, right)
        return inv_count

    def merge(arr, temp, left, mid, right):
        i = left
        j = mid + 1
        k = left
        inv_count = 0
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp[k] = arr[i]
                i += 1
            else:
                temp[k] = arr[j]
                inv_count += (mid - i + 1)
                j += 1
            k += 1
        while i <= mid:
            temp[k] = arr[i]
            i += 1
            k += 1
        while j <= right:
            temp[k] = arr[j]
            j += 1
            k += 1
        for i in range(left, right + 1):
            arr[i] = temp[i]
        return inv_count

    temp = [0] * len(arr)
    return merge_sort(arr.copy(), temp, 0, len(arr) - 1)


# H7
# Tempo: O(V + E log V) | Espaço: O(V + E)
def topo_sort(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    adj = {i: [] for i in range(n)}
    in_degree = [0] * n
    
    seen_edges = set()
    for u, v in edges:
        if u == v or not (0 <= u < n and 0 <= v < n):
            return None
        if (u, v) in seen_edges:
            continue
        seen_edges.add((u, v))
        adj[u].append(v)
        in_degree[v] += 1
        
    heap = [i for i in range(n) if in_degree[i] == 0]
    heapq.heapify(heap)
    
    res = []
    while heap:
        curr = heapq.heappop(heap)
        res.append(curr)
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(heap, neighbor)
                
    if len(res) != n:
        return None
    return res


# H8
# Tempo: O(n) | Espaço: O(k)
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0:
        return []
    if k == 1:
        return nums
    
    deq = collections.deque()
    res = []
    for i in range(len(nums)):
        if deq and deq[0] < i - k + 1:
            deq.popleft()
        while deq and nums[deq[-1]] < nums[i]:
            deq.pop()
        deq.append(i)
        if i >= k - 1:
            res.append(nums[deq[0]])
    return res