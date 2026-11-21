from collections import Counter, OrderedDict, defaultdict, deque
import heapq


# ==============================================================================
# H1. median_of_two_sorted_arrays
# ==============================================================================
# Tempo: O(log(min(len(a), len(b)))) | Espaço: O(1)
def median_of_two_sorted_arrays(a: list[int | float], b: list[int | float]) -> float:
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    low, high = 0, m

    while low <= high:
        i = (low + high) // 2
        j = (m + n + 1) // 2 - i

        max_left_a = float("-inf") if i == 0 else a[i - 1]
        min_right_a = float("inf") if i == m else a[i]
        max_left_b = float("-inf") if j == 0 else b[j - 1]
        min_right_b = float("inf") if j == n else b[j]

        if max_left_a <= min_right_b and max_left_b <= min_right_a:
            if (m + n) % 2 == 1:
                return float(max(max_left_a, max_left_b))
            return (max(max_left_a, max_left_b) + min(min_right_a, min_right_b)) / 2.0
        elif max_left_a > min_right_b:
            high = i - 1
        else:
            low = i + 1

    return 0.0


# ==============================================================================
# H2. LFUCache
# ==============================================================================
# Tempo: O(1) para get e put | Espaço: O(capacity)
class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_to_val = {}
        self.key_to_freq = {}
        self.freq_to_keys = defaultdict(OrderedDict)
        self.min_freq = 0

    def _update_freq(self, key: int) -> None:
        freq = self.key_to_freq[key]
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        self.key_to_freq[key] = freq + 1
        self.freq_to_keys[freq + 1][key] = True

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
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[evict_key]
            del self.key_to_freq[evict_key]

        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = True
        self.min_freq = 1


# ==============================================================================
# H3. evaluate
# ==============================================================================
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
        elif c.isdigit() or c == ".":
            start = i
            has_dot = False
            while i < n and (expr[i].isdigit() or expr[i] == "."):
                if expr[i] == ".":
                    if has_dot:
                        raise ValueError("Invalid decimal format")
                    has_dot = True
                i += 1
            num_str = expr[start:i]
            if num_str == ".":
                raise ValueError("Isolated decimal point")
            tokens.append(float(num_str))
        else:
            raise ValueError(f"Invalid character: {c}")

    if not tokens:
        raise ValueError("Empty expression")

    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def consume(expected=None):
        nonlocal pos
        tok = peek()
        if tok is None:
            raise ValueError("Unexpected end of expression")
        if expected is not None and tok != expected:
            raise ValueError(f"Expected {expected}, got {tok}")
        pos += 1
        return tok

    def primary():
        tok = peek()
        if tok is None:
            raise ValueError("Unexpected end of expression")
        if tok == "(":
            consume("(")
            val = add_sub()
            consume(")")
            return val
        elif isinstance(tok, (int, float)):
            return float(consume())
        raise ValueError(f"Unexpected token: {tok}")

    def power():
        base = primary()
        if peek() == "^":
            consume("^")
            exp = unary()
            if base == 0 and exp < 0:
                raise ZeroDivisionError("Zero raised to a negative power")
            if base < 0 and not exp.is_integer():
                raise ValueError("Negative base with non-integer exponent")
            try:
                return float(base**exp)
            except OverflowError:
                raise ValueError("Calculation overflow")
        return base

    def unary():
        if peek() == "+":
            consume("+")
            return unary()
        elif peek() == "-":
            consume("-")
            return -unary()
        return power()

    def mul_div():
        val = unary()
        while peek() in ("*", "/"):
            op = consume()
            right = unary()
            if op == "*":
                val *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                val /= right
        return val

    def add_sub():
        val = mul_div()
        while peek() in ("+", "-"):
            op = consume()
            right = mul_div()
            if op == "+":
                val += right
            else:
                val -= right
        return val

    result = add_sub()
    if pos < len(tokens):
        raise ValueError("Unexpected trailing tokens")
    return float(result)


# ==============================================================================
# H4. serialize e deserialize
# ==============================================================================
# Tempo: O(1) | Espaço: O(1)
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Tempo: O(n) | Espaço: O(n)
def serialize(root: TreeNode | None) -> str:
    if not root:
        return ""
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node is not None:
            result.append(str(node.val))
            stack.append(node.right)
            stack.append(node.left)
        else:
            result.append("#")
    return ",".join(result)


# Tempo: O(n) | Espaço: O(n)
def deserialize(data: str) -> TreeNode | None:
    if not data:
        return None
    tokens = data.split(",")
    if not tokens or tokens[0] == "#":
        return None

    root = TreeNode(int(tokens[0]))
    stack = [[root, 0]]

    for token in tokens[1:]:
        child = TreeNode(int(token)) if token != "#" else None
        top = stack[-1]

        if top[1] == 0:
            top[0].left = child
            top[1] = 1
        else:
            top[0].right = child
            stack.pop()

        if child is not None:
            stack.append([child, 0])

    return root


# ==============================================================================
# H5. min_window
# ==============================================================================
# Tempo: O(len(s) + len(t)) | Espaço: O(len(s) + len(t))
def min_window(s: str, t: str) -> str:
    if not s or not t:
        return ""
    target_counts = Counter(t)
    required = len(target_counts)
    window_counts = {}
    formed = 0
    l, r = 0, 0
    min_len = float("inf")
    best_range = (0, 0)

    while r < len(s):
        char = s[r]
        window_counts[char] = window_counts.get(char, 0) + 1
        if char in target_counts and window_counts[char] == target_counts[char]:
            formed += 1

        while l <= r and formed == required:
            if (r - l + 1) < min_len:
                min_len = r - l + 1
                best_range = (l, r + 1)
            char = s[l]
            window_counts[char] -= 1
            if char in target_counts and window_counts[char] < target_counts[char]:
                formed -= 1
            l += 1
        r += 1

    return s[best_range[0] : best_range[1]] if min_len != float("inf") else ""


# ==============================================================================
# H6. count_inversions
# ==============================================================================
# Tempo: O(n log n) | Espaço: O(n)
def count_inversions(arr: list) -> int:
    def sort_and_count(a: list) -> tuple[list, int]:
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, inv_left = sort_and_count(a[:mid])
        right, inv_right = sort_and_count(a[mid:])
        merged = []
        i = j = 0
        inversions = inv_left + inv_right

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inversions += len(left) - i
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, inversions

    _, total_inversions = sort_and_count(arr)
    return total_inversions


# ==============================================================================
# H7. topo_sort
# ==============================================================================
# Tempo: O(n log n + len(edges)) | Espaço: O(n + len(edges))
def topo_sort(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    in_degree = [0] * n
    adj = [[] for _ in range(n)]
    seen_edges = set()

    for u, v in edges:
        if u == v:
            return None
        if (u, v) not in seen_edges:
            seen_edges.add((u, v))
            adj[u].append(v)
            in_degree[v] += 1

    heap = [i for i in range(n) if in_degree[i] == 0]
    heapq.heapify(heap)
    order = []

    while heap:
        u = heapq.heappop(heap)
        order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    return order if len(order) == n else None


# ==============================================================================
# H8. max_sliding_window
# ==============================================================================
# Tempo: O(n) | Espaço: O(k)
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0:
        return []
    if k == 1:
        return list(nums)

    dq = deque()
    result = []

    for i, num in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result