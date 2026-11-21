import collections
import heapq
import sys


# H1. median_of_two_sorted_arrays
# Tempo: O(log(min(n, m))) | Espaço: O(1)
def median_of_two_sorted_arrays(a: list[int | float], b: list[int | float]) -> float:
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
            return (max(max_left_a, max_left_b) + min(min_right_a, min_right_b)) / 2.0
        elif max_left_a > min_right_b:
            high = i - 1
        else:
            low = i + 1

    raise ValueError("Entrada inválida.")


# H2. class LFUCache
# Tempo: O(1) | Espaço: O(capacity)
class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_to_val = {}
        self.key_to_freq = {}
        self.freq_to_keys = collections.defaultdict(collections.OrderedDict)
        self.min_freq = 0

    def _update_freq(self, key: int) -> None:
        freq = self.key_to_freq[key]
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        self.key_to_freq[key] = freq + 1
        self.freq_to_keys[freq + 1][key] = None

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
            if not self.freq_to_keys[self.min_freq]:
                del self.freq_to_keys[self.min_freq]

        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1


# H3. evaluate
# Tempo: O(n) | Espaço: O(n)
def evaluate(expr: str) -> float:
    tokens = []
    i = 0
    n = len(expr)
    expect_binary_op = False

    while i < n:
        c = expr[i]
        if c.isspace():
            i += 1
            continue

        if c.isdigit() or c == ".":
            start = i
            has_dot = False
            while i < n and (expr[i].isdigit() or expr[i] == "."):
                if expr[i] == ".":
                    if has_dot:
                        raise ValueError("Formato de número inválido")
                    has_dot = True
                i += 1
            num_str = expr[start:i]
            if num_str == ".":
                raise ValueError("Ponto decimal isolado")
            tokens.append(("NUM", float(num_str)))
            expect_binary_op = True
        elif c in "+-*/^()":
            if c in "+-":
                if not expect_binary_op:
                    tokens.append(("U" + c, None))
                else:
                    tokens.append((c, None))
                    expect_binary_op = False
            elif c in "*/^":
                if not expect_binary_op:
                    raise ValueError(f"Operador inesperado '{c}'")
                tokens.append((c, None))
                expect_binary_op = False
            elif c == "(":
                if expect_binary_op:
                    raise ValueError("Parêntese de abertura inesperado")
                tokens.append((c, None))
                expect_binary_op = False
            elif c == ")":
                if not expect_binary_op:
                    raise ValueError("Parêntese de fechamento inesperado")
                tokens.append((c, None))
                expect_binary_op = True
            i += 1
        else:
            raise ValueError(f"Caractere inválido: {c}")

    if not expect_binary_op and tokens:
        raise ValueError("Expressão incompleta")
    if not tokens:
        raise ValueError("Expressão vazia")

    precedence = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "U+": 3,
        "U-": 3,
        "^": 4,
    }
    right_assoc = {"^", "U+", "U-"}

    output = []
    op_stack = []

    for t_type, t_val in tokens:
        if t_type == "NUM":
            output.append(("NUM", t_val))
        elif t_type in precedence:
            p = precedence[t_type]
            is_ra = t_type in right_assoc
            while op_stack and op_stack[-1] != "(":
                top_p = precedence[op_stack[-1]]
                if (not is_ra and p <= top_p) or (is_ra and p < top_p):
                    output.append((op_stack.pop(), None))
                else:
                    break
            op_stack.append(t_type)
        elif t_type == "(":
            op_stack.append("(")
        elif t_type == ")":
            while op_stack and op_stack[-1] != "(":
                output.append((op_stack.pop(), None))
            if not op_stack:
                raise ValueError("Parênteses desbalanceados")
            op_stack.pop()

    while op_stack:
        op = op_stack.pop()
        if op == "(":
            raise ValueError("Parênteses desbalanceados")
        output.append((op, None))

    val_stack = []
    for op, val in output:
        if op == "NUM":
            val_stack.append(val)
        elif op == "U+":
            if not val_stack:
                raise ValueError("Operando ausente para + unário")
        elif op == "U-":
            if not val_stack:
                raise ValueError("Operando ausente para - unário")
            val_stack.append(-val_stack.pop())
        else:
            if len(val_stack) < 2:
                raise ValueError("Operandos insuficientes")
            right = val_stack.pop()
            left = val_stack.pop()
            if op == "+":
                val_stack.append(left + right)
            elif op == "-":
                val_stack.append(left - right)
            elif op == "*":
                val_stack.append(left * right)
            elif op == "/":
                if right == 0:
                    raise ZeroDivisionError("Divisão por zero")
                val_stack.append(left / right)
            elif op == "^":
                if left == 0 and right < 0:
                    raise ZeroDivisionError("Zero elevado a expoente negativo")
                val_stack.append(left ** right)

    if len(val_stack) != 1:
        raise ValueError("Expressão malformada")

    res = val_stack[0]
    if isinstance(res, complex):
        raise ValueError("Resultado complexo não suportado")
    return float(res)


# H4. serialize e deserialize
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
    stack = [(root, False)]
    while stack:
        node, visited = stack.pop()
        if node is None:
            result.append("#")
            continue
        if visited:
            continue
        result.append(str(node.val))
        stack.append((node.right, False))
        stack.append((node.left, False))
    return ",".join(result)


# Tempo: O(n) | Espaço: O(n)
def deserialize(data: str) -> TreeNode | None:
    if not data:
        return None
    tokens = data.split(",")
    if not tokens or tokens[0] == "#":
        return None

    root = TreeNode(int(tokens[0]))
    stack = [root]
    state = [0]  # 0: próximo é left, 1: próximo é right

    for val_str in tokens[1:]:
        is_null = val_str == "#"
        child_node = TreeNode(int(val_str)) if not is_null else None

        while state and state[-1] == 2:
            stack.pop()
            state.pop()

        parent = stack[-1]
        if state[-1] == 0:
            parent.left = child_node
            state[-1] = 1
        else:
            parent.right = child_node
            state[-1] = 2

        if child_node is not None:
            stack.append(child_node)
            state.append(0)

    return root


# H5. min_window
# Tempo: O(len(s) + len(t)) | Espaço: O(len(s) + len(t))
def min_window(s: str, t: str) -> str:
    if not s or not t:
        return ""

    target_counts = collections.Counter(t)
    required = len(target_counts)
    window_counts = collections.defaultdict(int)

    formed = 0
    left = 0
    min_len = float("inf")
    best_range = (0, 0)

    for right, char in enumerate(s):
        window_counts[char] += 1
        if char in target_counts and window_counts[char] == target_counts[char]:
            formed += 1

        while left <= right and formed == required:
            curr_len = right - left + 1
            if curr_len < min_len:
                min_len = curr_len
                best_range = (left, right + 1)

            left_char = s[left]
            window_counts[left_char] -= 1
            if left_char in target_counts and window_counts[left_char] < target_counts[left_char]:
                formed -= 1
            left += 1

    return s[best_range[0] : best_range[1]] if min_len != float("inf") else ""


# H6. count_inversions
# Tempo: O(n log n) | Espaço: O(n)
def count_inversions(arr: list[int | float]) -> int:
    def sort_and_count(a: list[int | float]) -> tuple[list[int | float], int]:
        n = len(a)
        if n <= 1:
            return a, 0

        mid = n // 2
        left, left_inv = sort_and_count(a[:mid])
        right, right_inv = sort_and_count(a[mid:])

        merged = []
        inversions = left_inv + right_inv
        i = j = 0
        len_left = len(left)
        len_right = len(right)

        while i < len_left and j < len_right:
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inversions += len_left - i
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, inversions

    _, total_inversions = sort_and_count(arr)
    return total_inversions


# H7. topo_sort
# Tempo: O(V log V + E) | Espaço: O(V + E)
def topo_sort(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    adj = collections.defaultdict(list)
    in_degree = [0] * n

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

    if len(order) != n:
        return None
    return order


# H8. max_sliding_window
# Tempo: O(n) | Espaço: O(k)
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0:
        return []

    deq = collections.deque()
    result = []

    for i in range(len(nums)):
        while deq and deq[0] <= i - k:
            deq.popleft()

        while deq and nums[deq[-1]] <= nums[i]:
            deq.pop()

        deq.append(i)

        if i >= k - 1:
            result.append(nums[deq[0]])

    return result