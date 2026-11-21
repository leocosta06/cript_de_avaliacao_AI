"""
Rodada 2 - testes mais dificeis, timeout por teste (subprocesso) e
comparacao da complexidade declarada com o gabarito.

Uso:  python rodar_v2.py
Le todos os arquivos  v2_*.py  da mesma pasta (ex.: v2_pro_alto.py).
"""
import glob, importlib.util, math, os, random, re, subprocess, sys, time

TIMEOUT_NORMAL = 5
TIMEOUT_PERF = 10


# ======================= TESTES (recebem o modulo s) =======================
def h1(s):
    f = s.median_of_two_sorted_arrays
    assert f([1, 3], [2]) == 2
    assert f([1, 2], [3, 4]) == 2.5
    assert f([], [1]) == 1
    assert f([], [2, 3]) == 2.5
    assert f([0, 0], [0, 0]) == 0
    assert f([-5, -3], [-4]) == -4
    assert f([1, 2, 3, 4, 5], [6]) == 3.5
    assert f([100], [1, 2, 3, 4]) == 3


def h1_perf(s):
    a = list(range(0, 2_000_000, 2))
    b = list(range(1, 2_000_000, 2))
    for _ in range(300):
        assert s.median_of_two_sorted_arrays(a, b) == 999999.5


def h2(s):
    c = s.LFUCache(2)
    c.put(1, 1); c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)                      # remove a chave 2
    assert c.get(2) == -1
    assert c.get(3) == 3
    c.put(4, 4)                      # empate de freq. entre 1 e 3 -> remove o LRU (1)
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4
    z = s.LFUCache(0)
    z.put(0, 0)
    assert z.get(0) == -1
    u = s.LFUCache(2)
    u.put(1, 1); u.put(2, 2)
    u.put(1, 10)                     # atualizar conta como uso
    u.put(3, 3)                      # deve remover a chave 2
    assert u.get(1) == 10 and u.get(2) == -1 and u.get(3) == 3


def h2_perf(s):
    rnd = random.Random(1)
    c = s.LFUCache(5000)
    for i in range(200_000):
        k = rnd.randint(0, 20000)
        if i % 2:
            c.put(k, i)
        else:
            c.get(k)


def h3(s):
    ev = s.evaluate
    ok = [("1+2*3", 7), ("(1+2)*3", 9), ("2^3^2", 512), ("2*-3", -6),
          ("--3", 3), (" 7 / 2 ", 3.5), ("10-4-3", 3), ("8/4/2", 1),
          ("((2))", 2), ("-2^2", -4), ("2^-1", 0.5), ("3.5*2", 7),
          ("-(1+2)", -3), ("2*(3+4)*5", 70)]
    for expr, want in ok:
        got = ev(expr)
        assert abs(got - want) < 1e-9, f"{expr!r}: {got} != {want}"
    for bad in ["1+", "(1", "1 2", "", ")(", "1+*2", "()", "abc"]:
        try:
            ev(bad)
        except ValueError:
            continue
        except Exception as e:
            raise AssertionError(f"{bad!r} levantou {type(e).__name__}, esperado ValueError")
        raise AssertionError(f"{bad!r} nao levantou erro")
    try:
        ev("1/0")
    except ZeroDivisionError:
        pass
    else:
        raise AssertionError("1/0 deveria levantar ZeroDivisionError")


def h3_perf(s):
    assert s.evaluate("1+" * 100_000 + "1") == 100_001


def _build_chain(s, n):
    root = s.TreeNode(0)
    cur = root
    for i in range(1, n):
        cur.right = s.TreeNode(i)
        cur = cur.right
    return root


def _same(a, b):
    stack = [(a, b)]
    while stack:
        x, y = stack.pop()
        if x is None and y is None:
            continue
        if x is None or y is None or x.val != y.val:
            return False
        stack.append((x.left, y.left))
        stack.append((x.right, y.right))
    return True


def h4(s):
    T = s.TreeNode
    assert s.deserialize(s.serialize(None)) is None
    one = T(5)
    assert _same(s.deserialize(s.serialize(one)), one)
    r = T(-10, T(123456, None, T(-7)), T(0, T(9), None))
    out = s.serialize(r)
    assert isinstance(out, str)
    assert _same(s.deserialize(out), r)
    r2 = T(1, T(2, T(3, T(4))), None)
    assert _same(s.deserialize(s.serialize(r2)), r2)


def h4_perf(s):
    root = _build_chain(s, 20_000)      # arvore muito profunda (testa recursao)
    back = s.deserialize(s.serialize(root))
    assert _same(back, root)


def h5(s):
    f = s.min_window
    assert f("ADOBECODEBANC", "ABC") == "BANC"
    assert f("a", "a") == "a"
    assert f("a", "aa") == ""
    assert f("aa", "aa") == "aa"
    assert f("ab", "b") == "b"
    assert f("abc", "") == ""
    assert f("", "a") == ""
    assert f("aabdec", "abc") == "abdec"


def h5_perf(s):
    big = "a" * 100_000 + "b" + "c" * 100_000
    assert s.min_window(big, "abc") == "abc"


def h6(s):
    f = s.count_inversions
    assert f([2, 4, 1, 3, 5]) == 3
    assert f([]) == 0
    assert f([1]) == 0
    assert f([5, 4, 3, 2, 1]) == 10
    assert f([1, 1, 1]) == 0
    assert f([2, 1, 1]) == 2
    assert f([-1, -2, -3]) == 3


def h6_perf(s):
    n = 200_000
    assert s.count_inversions(list(range(n, 0, -1))) == n * (n - 1) // 2


def h7(s):
    f = s.topo_sort
    assert f(4, [(3, 1), (2, 1), (0, 3)]) == [0, 2, 3, 1]
    assert f(3, [(0, 1), (1, 2), (2, 0)]) is None
    assert f(0, []) == []
    assert f(3, []) == [0, 1, 2]
    assert f(3, [(1, 1)]) is None
    assert f(2, [(0, 1), (0, 1)]) == [0, 1]
    assert f(5, [(4, 0), (3, 0), (2, 1)]) == [2, 1, 3, 4, 0]


def h7_perf(s):
    n = 200_000
    edges = [(i + 1, i) for i in range(n - 1)]
    assert s.topo_sort(n, edges) == list(range(n - 1, -1, -1))


def h8(s):
    f = s.max_sliding_window
    assert f([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert f([1], 1) == [1]
    assert f([9, 11], 2) == [11]
    assert f([4, -2], 1) == [4, -2]
    assert f([], 3) == []
    assert f([1, 1, 1, 1], 2) == [1, 1, 1]
    assert f([5, 4, 3, 2, 1], 2) == [5, 4, 3, 2]


def h8_perf(s):
    n, k = 200_000, 50_000
    arr = list(range(n))
    res = s.max_sliding_window(arr, k)
    assert len(res) == n - k + 1 and res[0] == k - 1 and res[-1] == n - 1


TESTES = [
    ("H1 mediana", h1, False), ("H1 perf", h1_perf, True),
    ("H2 LFU", h2, False), ("H2 perf", h2_perf, True),
    ("H3 parser", h3, False), ("H3 perf", h3_perf, True),
    ("H4 arvore", h4, False), ("H4 perf/recursao", h4_perf, True),
    ("H5 janela min", h5, False), ("H5 perf", h5_perf, True),
    ("H6 inversoes", h6, False), ("H6 perf", h6_perf, True),
    ("H7 topo", h7, False), ("H7 perf", h7_perf, True),
    ("H8 janela deslizante", h8, False), ("H8 perf", h8_perf, True),
]
NOMES = {n: f for n, f, _ in TESTES}

# ===================== GABARITO DE COMPLEXIDADE (tempo) =====================
def norm(x):
    x = x.lower().replace("·", "").replace("×", "").replace("*", "")
    x = x.replace("log2", "log").replace(" ", "").replace("^", "")
    return x

GABARITO = [
    ("H1", "O(log(min(n,m)))", {"o(log(min(n,m)))", "o(log(min(m,n)))"}),
    ("H2", "O(1)", {"o(1)"}),
    ("H3", "O(n)", {"o(n)"}),
    ("H4", "O(n)", {"o(n)"}),
    ("H5", "O(n+m)", {"o(n+m)", "o(m+n)", "o(n)"}),
    ("H6", "O(n log n)", {"o(nlogn)", "o(nlog(n))"}),
    ("H7", "O((V+E) log V)", {"o((v+e)logv)", "o((e+v)logv)", "o((v+e)log(v))",
                              "o(elogv)", "o(elog(v))", "o((n+e)logn)",
                              "o((n+m)logn)"}),
    ("H8", "O(n)", {"o(n)"}),
]


# ============================== MODO FILHO ==============================
def carregar(caminho):
    spec = importlib.util.spec_from_file_location("mod", caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def filho(caminho, nome):
    mod = carregar(caminho)
    t = time.time()
    try:
        NOMES[nome](mod)
    except BaseException as e:
        msg = str(e).splitlines()[0][:80] if str(e) else ""
        print(f"{type(e).__name__}: {msg}", file=sys.stderr)
        sys.exit(1)
    print(f"{time.time() - t:.4f}")


# ============================== MODO PAI ==============================
def rodar_um(caminho, nome, perf):
    limite = TIMEOUT_PERF if perf else TIMEOUT_NORMAL
    try:
        p = subprocess.run([sys.executable, os.path.abspath(__file__), "--child", caminho, nome],
                           capture_output=True, text=True, timeout=limite)
    except subprocess.TimeoutExpired:
        return False, limite, f"TIMEOUT (>{limite}s)"
    if p.returncode == 0:
        return True, float(p.stdout.strip() or 0), ""
    err = (p.stderr.strip().splitlines() or ["erro desconhecido"])[-1]
    return False, 0.0, err[:90]


def complexidade_declarada(caminho):
    with open(caminho, encoding="utf-8", errors="ignore") as f:
        linhas = [l for l in f if "tempo:" in l.lower()]
    saida = []
    for l in linhas:
        m = re.search(r"tempo:\s*(.*?)\s*(\||$)", l, re.I)
        saida.append(m.group(1).strip() if m else "?")
    return saida


def principal():
    pasta = os.path.dirname(os.path.abspath(__file__))
    arquivos = sorted(glob.glob(os.path.join(pasta, "v2_*.py")))
    if not arquivos:
        print("Nenhum arquivo v2_*.py encontrado.")
        return
    placar, detalhes, compl = [], {}, {}
    for caminho in arquivos:
        nome = os.path.basename(caminho)[3:-3]
        print(f"rodando {nome} ...", flush=True)
        falhas, total_t, ok = [], 0.0, 0
        for tn, _, perf in TESTES:
            passou, dt, info = rodar_um(caminho, tn, perf)
            total_t += dt
            if passou:
                ok += 1
            else:
                falhas.append(f"{tn} -> {info}")
        placar.append((nome, ok, len(TESTES), total_t))
        detalhes[nome] = falhas
        compl[nome] = complexidade_declarada(caminho)

    placar.sort(key=lambda x: (-x[1], x[3]))
    print(f"\n{'MODELO':<22}{'ACERTOS':<10}{'ERROS':<8}{'TEMPO':<9}")
    print("-" * 50)
    for nome, ok, total, t in placar:
        print(f"{nome:<22}{ok}/{total:<8}{total - ok:<8}{t:.2f}s")

    print("\nDETALHE DOS ERROS")
    for nome, *_ in placar:
        if detalhes[nome]:
            print(f"\n{nome}:")
            for f in detalhes[nome]:
                print("   X", f)

    print("\nCOMPLEXIDADE DECLARADA (tempo) vs GABARITO")
    print("(OK = bate com o gabarito; REVISAR = diferente ou ausente, confira a mao)")
    for nome, *_ in placar:
        dec = compl[nome]
        certas = 0
        linhas = []
        for i, (tid, esperado, aceitos) in enumerate(GABARITO):
            d = dec[i] if i < len(dec) else "(ausente)"
            bateu = norm(d) in aceitos
            certas += bateu
            if not bateu:
                linhas.append(f"   REVISAR {tid}: declarou {d} | esperado {esperado}")
        print(f"\n{nome}: {certas}/{len(GABARITO)} complexidades OK")
        for l in linhas:
            print(l)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--child":
        filho(sys.argv[2], sys.argv[3])
    else:
        principal()