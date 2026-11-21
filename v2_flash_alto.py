from collections import Counter, OrderedDict, defaultdict, deque
import heapq


# =====================================================================
# H1. median_of_two_sorted_arrays
# Tempo: O(log(min(len(a), len(b)))) | Espaço: O(1)
# =====================================================================
def median_of_two_sorted_arrays(
    a: list[int | float], b: list[int | float]
) -> float:
    if len(a) > len(b):
        a, b = b, a

    m, n = len(a), len(b)
    low, high = 0, m
    half_len = (m + n + 1) // 2

    while low <= high:
        i = (low + high) // 2
        j = half_len - i

        max_left_a = float("-inf") if i == 0 else a[i - 1]
        min_right_a = float("inf") if i == m else a[i]

        max_left_b = float("-inf") if j == 0 else b[j - 1]
        min_right_b = float("inf") if j == n else b[j]

        if max_left_a <= min_right_b and max_left_b <= min_right_a:
            if (m + n) % 2 == 1:
                return float(max(max_left_a, max_left_b))
            return (
                max(max_left_a, max_left_b) + min(min_right_a, min_right_b)
            ) / 2.0
        elif max_left_a > min_right_b:
            high = i - 1
        else:
            low = i + 1

    raise ValueError("Input arrays are not sorted")


# =====================================================================
# H2. class LFUCache
# Tempo: O(1) por operação | Espaço: O(capacity)
# =====================================================================
class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val = {}
        self.key_to_freq = {}
        self.freq_to_keys = defaultdict(OrderedDict)

    def _update_freq(self, key: int) -> None:
        freq = self.key_to_freq[key]
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq] and self.min_freq == freq:
            self.min_freq += 1
        new_freq = freq + 1
        self.key_to_freq[key] = new_freq
        self.freq_to_keys[new_freq][key] = None

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
        self.freq_to_keys[1][key] = None
        self.min_freq = 1


# =====================================================================
# H3. evaluate
# Tempo: O(n) | Espaço: O(n)
# =====================================================================
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
                        raise ValueError(f"Invalid decimal format at index {i}")
                    has_dot = True
                i += 1
            token_str = expr[start:i]
            if token_str == ".":
                raise ValueError("Standalone decimal point is invalid")
            tokens.append(float(token_str))
        else:
            raise ValueError(f"Invalid character encountered: {c}")

    if not tokens:
        raise ValueError("Empty expression")

    pos = 0

    def parse_expr() -> float:
        return parse_additive()

    def parse_additive() -> float:
        nonlocal pos
        val = parse_multiplicative()
        while pos < len(tokens) and tokens[pos] in ("+", "-"):
            op = tokens[pos]
            pos += 1
            rhs = parse_multiplicative()
            if op == "+":
                val += rhs
            else:
                val -= rhs
        return val

    def parse_multiplicative() -> float:
        nonlocal pos
        val = parse_unary()
        while pos < len(tokens) and tokens[pos] in ("*", "/"):
            op = tokens[pos]
            pos += 1
            rhs = parse_unary()
            if op == "*":
                val *= rhs
            else:
                if rhs == 0:
                    raise ZeroDivisionError("Division by zero")
                val /= rhs
        return val

    def parse_unary() -> float:
        nonlocal pos
        if pos < len(tokens):
            if tokens[pos] == "+":
                pos += 1
                return parse_power()
            if tokens[pos] == "-":
                pos += 1
                return -parse_power()
        return parse_power()

    def parse_power() -> float:
        nonlocal pos
        base = parse_primary()
        if pos < len(tokens) and tokens[pos] == "^":
            pos += 1
            exp = parse_unary()
            if base == 0 and exp < 0:
                raise ZeroDivisionError(
                    "Zero cannot be raised to a negative power"
                )
            try:
                res = base**exp
            except ZeroDivisionError:
                raise ZeroDivisionError("Zero cannot be raised to a negative power")
            if isinstance(res, complex) or (
                hasattr(res, "imag") and res.imag != 0
            ):
                raise ValueError("Complex result is not supported")
            return float(res)
        return base

    def parse_primary() -> float:
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError("Unexpected end of expression")
        tok = tokens[pos]
        if isinstance(tok, float):
            pos += 1
            return tok
        elif tok == "(":
            pos += 1
            val = parse_expr()
            if pos >= len(tokens) or tokens[pos] != ")":
                raise ValueError("Mismatched parentheses")
            pos += 1
            return val
        else:
            raise ValueError(f"Unexpected token: {tok}")

    result = parse_expr()
    if pos < len(tokens):
        raise ValueError(f"Unexpected trailing tokens: {tokens[pos:]}")
    return float(result)


# =====================================================================
# H4. TreeNode, serialize e deserialize
# =====================================================================
# Tempo: O(1) | Espaço: O(1)
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Tempo: O(n) | Espaço: O(n)
def serialize(root: TreeNode | None) -> str:
    if root is None:
        return "#"
    parts = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            parts.append("#")
        else:
            parts.append(str(node.val))
            stack.append(node.right)
            stack.append(node.left)
    return ",".join(parts)


# Tempo: O(n) | Espaço: O(n)
def deserialize(data: str) -> TreeNode | None:
    if not data or data == "#":
        return None
    tokens = data.split(",")
    root = TreeNode(int(tokens[0]))
    stack = [[root, 0]]

    for tok in tokens[1:]:
        child = None if tok == "#" else TreeNode(int(tok))
        parent, state = stack[-1]
        if state == 0:
            parent.left = child
            stack[-1][1] = 1
        else:
            parent.right = child
            stack.pop()

        if child is not None:
            stack.append([child, 0])

    return root


# =====================================================================
# H5. min_window
# Tempo: O(len(s) + len(t)) | Espaço: O(len(s) + len(t))
# =====================================================================
def min_window(s: str, t: str) -> str:
    if not s or not t:
        return ""

    target_counts = Counter(t)
    required = len(target_counts)
    window_counts = {}
    formed = 0

    best_len = float("inf")
    best_left = 0
    best_right = 0

    l = 0
    for r, char in enumerate(s):
        window_counts[char] = window_counts.get(char, 0) + 1
        if char in target_counts and window_counts[char] == target_counts[char]:
            formed += 1

        while l <= r and formed == required:
            curr_len = r - l + 1
            if curr_len < best_len:
                best_len = curr_len
                best_left = l
                best_right = r

            char_l = s[l]
            window_counts[char_l] -= 1
            if (
                char_l in target_counts
                and window_counts[char_l] < target_counts[char_l]
            ):
                formed -= 1
            l += 1

    return "" if best_len == float("inf") else s[best_left : best_right + 1]


# =====================================================================
# H6. count_inversions
# Tempo: O(n log n) | Espaço: O(n)
# =====================================================================
def count_inversions(arr: list[int]) -> int:
    def merge_and_count(a: list[int]) -> tuple[list[int], int]:
        n = len(a)
        if n <= 1:
            return a, 0
        mid = n // 2
        left, inv_left = merge_and_count(a[:mid])
        right, inv_right = merge_and_count(a[mid:])

        merged = []
        i = j = 0
        inv_split = 0
        len_left, len_right = len(left), len(right)

        while i < len_left and j < len_right:
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inv_split += len_left - i
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, inv_left + inv_right + inv_split

    _, total = merge_and_count(arr)
    return total


# =====================================================================
# H7. topo_sort
# Tempo: O((V + E) log V) | Espaço: O(V + E)
# =====================================================================
def topo_sort(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    adj = [set() for _ in range(n)]
    for u, v in edges:
        if u == v:
            return None
        adj[u].add(v)

    in_degree = [0] * n
    for u in range(n):
        for v in adj[u]:
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

    if len(order) == n:
        return order
    return None


# =====================================================================
# H8. max_sliding_window
# Tempo: O(n) | Espaço: O(k)
# =====================================================================
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0:
        return []
    dq = deque()
    res = []
    for i, num in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res