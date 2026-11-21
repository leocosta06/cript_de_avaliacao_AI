from collections import Counter, OrderedDict, defaultdict, deque
import heapq


# ==========================================
# H1
# Tempo: O(log(min(n, m))) | Espaço: O(1)
# ==========================================
def median_of_two_sorted_arrays(a, b) -> float:
    if len(a) > len(b):
        a, b = b, a

    n, m = len(a), len(b)
    half = (n + m + 1) // 2
    lo, hi = 0, n

    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i

        a_left = a[i - 1] if i > 0 else float('-inf')
        a_right = a[i] if i < n else float('inf')
        b_left = b[j - 1] if j > 0 else float('-inf')
        b_right = b[j] if j < m else float('inf')

        if a_left <= b_right and b_left <= a_right:
            if (n + m) % 2 == 1:
                return float(max(a_left, b_left))
            return (max(a_left, b_left) + min(a_right, b_right)) / 2.0
        elif a_left > b_right:
            hi = i - 1
        else:
            lo = i + 1

    raise ValueError("Entradas inválidas.")


# ==========================================
# H2
# Tempo: O(1) para get e put | Espaço: O(capacity)
# ==========================================
class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_val = {}
        self.key_freq = {}
        self.freq_keys = defaultdict(OrderedDict)

    def _touch(self, key: int) -> None:
        freq = self.key_freq[key]
        del self.freq_keys[freq][key]
        if not self.freq_keys[freq]:
            del self.freq_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1

        new_freq = freq + 1
        self.key_freq[key] = new_freq
        self.freq_keys[new_freq][key] = None

    def get(self, key: int) -> int:
        if key not in self.key_val:
            return -1
        self._touch(key)
        return self.key_val[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return

        if key in self.key_val:
            self.key_val[key] = value
            self._touch(key)
            return

        if len(self.key_val) >= self.capacity:
            evict_key, _ = self.freq_keys[self.min_freq].popitem(last=False)
            if not self.freq_keys[self.min_freq]:
                del self.freq_keys[self.min_freq]
            del self.key_val[evict_key]
            del self.key_freq[evict_key]

        self.key_val[key] = value
        self.key_freq[key] = 1
        self.freq_keys[1][key] = None
        self.min_freq = 1


# ==========================================
# H3
# Tempo: O(n) | Espaço: O(n)
# ==========================================
def evaluate(expr: str) -> float:
    if not isinstance(expr, str):
        raise ValueError("A expressão deve ser uma string.")

    tokens = []
    i, n = 0, len(expr)
    while i < n:
        ch = expr[i]
        if ch.isspace():
            i += 1
        elif ch in '+-*/^()':
            tokens.append(ch)
            i += 1
        elif ch.isdigit() or ch == '.':
            start = i
            dot_count = 0
            digit_count = 0
            while i < n and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i] == '.':
                    dot_count += 1
                    if dot_count > 1:
                        raise ValueError("Número decimal inválido.")
                else:
                    digit_count += 1
                i += 1
            if digit_count == 0:
                raise ValueError("Número decimal inválido.")
            tokens.append(float(expr[start:i]))
        else:
            raise ValueError(f"Caractere inválido: {ch}")

    if not tokens:
        raise ValueError("Expressão vazia.")

    pos = 0

    def parse_expr() -> float:
        nonlocal pos
        val = parse_term()
        while pos < len(tokens) and tokens[pos] in ('+', '-'):
            op = tokens[pos]
            pos += 1
            right = parse_term()
            if op == '+':
                val += right
            else:
                val -= right
        return val

    def parse_term() -> float:
        nonlocal pos
        val = parse_factor()
        while pos < len(tokens) and tokens[pos] in ('*', '/'):
            op = tokens[pos]
            pos += 1
            right = parse_factor()
            if op == '*':
                val *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("Divisão por zero.")
                val /= right
        return val

    def parse_factor() -> float:
        nonlocal pos
        if pos < len(tokens) and tokens[pos] in ('+', '-'):
            op = tokens[pos]
            pos += 1
            val = parse_factor()
            return -val if op == '-' else val
        return parse_power()

    def parse_power() -> float:
        nonlocal pos
        base = parse_atom()
        if pos < len(tokens) and tokens[pos] == '^':
            pos += 1
            exp = parse_factor()
            if base == 0.0 and exp < 0:
                raise ZeroDivisionError("Zero elevado a expoente negativo.")
            res = base ** exp
            if isinstance(res, complex):
                raise ValueError("Resultado complexo não suportado.")
            return float(res)
        return base

    def parse_atom() -> float:
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError("Fim inesperado da expressão.")
        tok = tokens[pos]
        if isinstance(tok, float):
            pos += 1
            return tok
        if tok == '(':
            pos += 1
            val = parse_expr()
            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError("Parênteses desbalanceados.")
            pos += 1
            return val
        raise ValueError(f"Token inesperado: {tok}")

    result = parse_expr()
    if pos != len(tokens):
        raise ValueError("Tokens extras ao final da expressão.")
    return float(result)


# ==========================================
# H4
# Tempo: O(n) | Espaço: O(n)
# ==========================================
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Tempo: O(n) | Espaço: O(n)
def serialize(root) -> str:
    if root is None:
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
def deserialize(data):
    if not data:
        return None
    tokens = data.split(",")
    if tokens[0] == "#":
        return None

    root = TreeNode(int(tokens[0]))
    queue = deque([root])
    idx = 1
    n = len(tokens)

    while queue and idx < n:
        parent = queue.popleft()
        if tokens[idx] != "#":
            parent.left = TreeNode(int(tokens[idx]))
            queue.append(parent.left)
        idx += 1

        if idx < n and tokens[idx] != "#":
            parent.right = TreeNode(int(tokens[idx]))
            queue.append(parent.right)
        idx += 1

    return root


# ==========================================
# H5
# Tempo: O(|s| + |t|) | Espaço: O(|s| + |t|)
# ==========================================
def min_window(s, t) -> str:
    if not s or not t or len(s) < len(t):
        return ""

    need = Counter(t)
    required = len(need)
    window = defaultdict(int)
    formed = 0

    best_len = float('inf')
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

    return "" if best_len == float('inf') else s[best_l:best_l + best_len]


# ==========================================
# H6
# Tempo: O(n log n) | Espaço: O(n)
# ==========================================
def count_inversions(arr) -> int:
    n = len(arr)
    if n < 2:
        return 0

    work = list(arr)
    temp = [0] * n
    inversions = 0
    width = 1

    while width < n:
        for left in range(0, n, 2 * width):
            mid = min(left + width, n)
            right = min(left + 2 * width, n)
            i, j, k = left, mid, left

            while i < mid and j < right:
                if work[i] <= work[j]:
                    temp[k] = work[i]
                    i += 1
                else:
                    temp[k] = work[j]
                    inversions += mid - i
                    j += 1
                k += 1

            while i < mid:
                temp[k] = work[i]
                i += 1
                k += 1

            while j < right:
                temp[k] = work[j]
                j += 1
                k += 1

            work[left:right] = temp[left:right]

        width *= 2

    return inversions


# ==========================================
# H7
# Tempo: O((V + E) log V) | Espaço: O(V + E)
# ==========================================
def topo_sort(n, edges) -> list[int] | None:
    if n <= 0:
        return []

    adj = [[] for _ in range(n)]
    in_degree = [0] * n

    for u, v in set(edges):
        if u == v:
            return None
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


# ==========================================
# H8
# Tempo: O(n) | Espaço: O(k) auxiliar (O(n) com a lista de saída)
# ==========================================
def max_sliding_window(nums, k) -> list[int]:
    if not nums or k <= 0 or k > len(nums):
        return []

    dq = deque()
    result = []

    for i, val in enumerate(nums):
        if dq and dq[0] <= i - k:
            dq.popleft()

        while dq and nums[dq[-1]] <= val:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result