from collections import defaultdict, OrderedDict, Counter, deque
import heapq


# H1
# Tempo: O(log(min(n, m))) | Espaço: O(1)
def median_of_two_sorted_arrays(a: list[float], b: list[float]) -> float:
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    lo, hi = 0, m
    half_len = (m + n + 1) // 2

    while lo <= hi:
        i = (lo + hi) // 2
        j = half_len - i

        max_left_a = float("-inf") if i == 0 else a[i - 1]
        min_right_a = float("inf") if i == m else a[i]

        max_left_b = float("-inf") if j == 0 else b[j - 1]
        min_right_b = float("inf") if j == n else b[j]

        if max_left_a <= min_right_b and max_left_b <= min_right_a:
            if (m + n) % 2 == 1:
                return float(max(max_left_a, max_left_b))
            return (max(max_left_a, max_left_b) + min(min_right_a, min_right_b)) / 2.0
        elif max_left_a > min_right_b:
            hi = i - 1
        else:
            lo = i + 1

    raise ValueError("Arrays de entrada inválidos.")


# H2
# Tempo: O(1) para get e put | Espaço: O(capacity)
class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val_freq: dict[int, list[int]] = {}
        self.freq_to_keys: defaultdict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)

    def _update_freq(self, key: int) -> None:
        val, freq = self.key_to_val_freq[key]
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        new_freq = freq + 1
        self.key_to_val_freq[key][1] = new_freq
        self.freq_to_keys[new_freq][key] = None

    def get(self, key: int) -> int:
        if key not in self.key_to_val_freq:
            return -1
        self._update_freq(key)
        return self.key_to_val_freq[key][0]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.key_to_val_freq:
            self.key_to_val_freq[key][0] = value
            self._update_freq(key)
            return
        if len(self.key_to_val_freq) >= self.capacity:
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            if not self.freq_to_keys[self.min_freq]:
                del self.freq_to_keys[self.min_freq]
            del self.key_to_val_freq[evict_key]
        self.key_to_val_freq[key] = [value, 1]
        self.freq_to_keys[1][key] = None
        self.min_freq = 1


# H3
# Tempo: O(n) | Espaço: O(n)
def evaluate(expr: str) -> float:
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        if ch.isspace():
            i += 1
        elif ch in "+-*/^()":
            tokens.append(ch)
            i += 1
        elif ch.isdigit() or ch == ".":
            start = i
            dot_count = 0
            while i < n and (expr[i].isdigit() or expr[i] == "."):
                if expr[i] == ".":
                    dot_count += 1
                i += 1
            num_str = expr[start:i]
            if dot_count > 1 or num_str == ".":
                raise ValueError("Número decimal inválido.")
            tokens.append(float(num_str))
        else:
            raise ValueError(f"Caractere inválido: {ch}")

    if not tokens:
        raise ValueError("Expressão vazia.")

    pos = 0

    def parse_expr() -> float:
        nonlocal pos
        res = parse_term()
        while pos < len(tokens) and tokens[pos] in ("+", "-"):
            op = tokens[pos]
            pos += 1
            right = parse_term()
            res = res + right if op == "+" else res - right
        return res

    def parse_term() -> float:
        nonlocal pos
        res = parse_unary()
        while pos < len(tokens) and tokens[pos] in ("*", "/"):
            op = tokens[pos]
            pos += 1
            right = parse_unary()
            if op == "*":
                res *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("Divisão por zero.")
                res /= right
        return res

    def parse_unary() -> float:
        nonlocal pos
        if pos < len(tokens) and tokens[pos] in ("+", "-"):
            op = tokens[pos]
            pos += 1
            val = parse_unary()
            return -val if op == "-" else val
        return parse_power()

    def parse_power() -> float:
        nonlocal pos
        base = parse_primary()
        if pos < len(tokens) and tokens[pos] == "^":
            pos += 1
            exp = parse_unary()
            if base == 0.0 and exp < 0:
                raise ZeroDivisionError("Zero elevado a expoente negativo.")
            res = base ** exp
            if isinstance(res, complex):
                raise ValueError("Resultado complexo não suportado.")
            return float(res)
        return base

    def parse_primary() -> float:
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError("Fim inesperado da expressão.")
        tok = tokens[pos]
        if tok == "(":
            pos += 1
            val = parse_expr()
            if pos >= len(tokens) or tokens[pos] != ")":
                raise ValueError("Parênteses desbalanceados.")
            pos += 1
            return val
        elif isinstance(tok, float):
            pos += 1
            return tok
        else:
            raise ValueError(f"Token inesperado: {tok}")

    result = parse_expr()
    if pos < len(tokens):
        raise ValueError("Tokens extras ao final da expressão.")
    return float(result)


# H4
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Tempo: O(n) | Espaço: O(n)
def serialize(root: TreeNode | None) -> str:
    if not root:
        return ""
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append("#")
        else:
            out.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
    return ",".join(out)


# Tempo: O(n) | Espaço: O(n)
def deserialize(data: str) -> TreeNode | None:
    if not data:
        return None
    tokens = data.split(",")
    if not tokens or tokens[0] == "#":
        return None
    root = TreeNode(int(tokens[0]))
    queue = deque([root])
    idx = 1
    n = len(tokens)
    while queue and idx < n:
        node = queue.popleft()
        if tokens[idx] != "#":
            node.left = TreeNode(int(tokens[idx]))
            queue.append(node.left)
        idx += 1
        if idx < n and tokens[idx] != "#":
            node.right = TreeNode(int(tokens[idx]))
            queue.append(node.right)
        idx += 1
    return root


# H5
# Tempo: O(|s| + |t|) | Espaço: O(|s| + |t|)
def min_window(s: str, t: str) -> str:
    if not s or not t or len(t) > len(s):
        return ""
    need = Counter(t)
    window: defaultdict[str, int] = defaultdict(int)
    required = len(need)
    formed = 0

    best_len = float("inf")
    best_l = 0
    l = 0

    for r, ch in enumerate(s):
        window[ch] += 1
        if ch in need and window[ch] == need[ch]:
            formed += 1

        while formed == required:
            if r - l + 1 < best_len:
                best_len = r - l + 1
                best_l = l
            left_ch = s[l]
            window[left_ch] -= 1
            if left_ch in need and window[left_ch] < need[left_ch]:
                formed -= 1
            l += 1

    return "" if best_len == float("inf") else s[best_l : best_l + best_len]


# H6
# Tempo: O(n log n) | Espaço: O(n)
def count_inversions(arr: list[int]) -> int:
    n = len(arr)
    if n < 2:
        return 0
    src = list(arr)
    aux = [0] * n
    inversions = 0
    width = 1

    while width < n:
        for i in range(0, n, 2 * width):
            left = i
            mid = min(i + width, n)
            right = min(i + 2 * width, n)
            p1, p2, k = left, mid, left

            while p1 < mid and p2 < right:
                if src[p1] <= src[p2]:
                    aux[k] = src[p1]
                    p1 += 1
                else:
                    aux[k] = src[p2]
                    inversions += mid - p1
                    p2 += 1
                k += 1

            while p1 < mid:
                aux[k] = src[p1]
                p1 += 1
                k += 1

            while p2 < right:
                aux[k] = src[p2]
                p2 += 1
                k += 1

        src, aux = aux, src
        width *= 2

    return inversions


# H7
# Tempo: O((V + E) log V) | Espaço: O(V + E)
def topo_sort(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    if n <= 0:
        return []
    adj: list[set[int]] = [set() for _ in range(n)]
    in_degree = [0] * n

    for u, v in edges:
        if u == v:
            return None
        if v not in adj[u]:
            adj[u].add(v)
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


# H8
# Tempo: O(n) | Espaço: O(k)
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0:
        return []
    dq: deque[int] = deque()
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
