import glob, importlib.util, math, os, time

# ---------- testes (recebem o módulo 's') ----------
def t1(s):
    assert sorted(s.two_sum([2,7,11,15], 9)) == [0,1]
    assert sorted(s.two_sum([3,2,4], 6)) == [1,2]
    assert sorted(s.two_sum([3,3], 6)) == [0,1]
    assert s.two_sum([1,2], 99) is None

def t1_perf(s):
    n = 200_000
    assert s.two_sum(list(range(n)), 2*n) is None

def t2(s):
    for ok in ["()[]{}", "{[]}", ""]:
        assert s.valid_parentheses(ok) is True, ok
    for bad in ["(]", "([)]", "(", ")"]:
        assert s.valid_parentheses(bad) is False, bad

def t3(s):
    assert s.merge_intervals([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
    assert s.merge_intervals([[1,4],[4,5]]) == [[1,5]]
    assert s.merge_intervals([]) == []
    assert s.merge_intervals([[5,6],[1,2]]) == [[1,2],[5,6]]
    assert s.merge_intervals([[1,4],[2,3]]) == [[1,4]]

def t3_perf(s):
    s.merge_intervals([[i, i+1] for i in range(0, 200_000, 2)])

def t4(s):
    assert s.longest_palindrome("babad") in ("bab", "aba")
    assert s.longest_palindrome("cbbd") == "bb"
    assert s.longest_palindrome("a") == "a"
    assert s.longest_palindrome("") == ""

def t5(s):
    assert s.edit_distance("kitten", "sitting") == 3
    assert s.edit_distance("", "abc") == 3
    assert s.edit_distance("abc", "abc") == 0
    assert s.edit_distance("horse", "ros") == 3

def t5_perf(s):
    s.edit_distance("a"*1000, "b"*1000)

def t6(s):
    c = s.LRUCache(2)
    c.put(1, 1); c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)
    assert c.get(2) == -1
    c.put(4, 4)
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4

def t7(s):
    g = {'A':[('B',1),('C',4)], 'B':[('C',2),('D',5)], 'C':[('D',1)], 'D':[], 'E':[]}
    d = s.dijkstra(g, 'A')
    assert d['A']==0 and d['B']==1 and d['C']==3 and d['D']==4
    assert d['E'] == math.inf

TESTES = [("T1 two_sum", t1), ("T1 perf", t1_perf), ("T2 parênteses", t2),
          ("T3 intervalos", t3), ("T3 perf", t3_perf), ("T4 palíndromo", t4),
          ("T5 edit distance", t5), ("T5 perf", t5_perf), ("T6 LRU", t6),
          ("T7 dijkstra", t7)]

# ---------- execução ----------
def carregar(caminho):
    spec = importlib.util.spec_from_file_location("mod", caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

pasta = os.path.dirname(os.path.abspath(__file__))
arquivos = sorted(glob.glob(os.path.join(pasta, "solucao_*.py")))
placar = []

for caminho in arquivos:
    nome = os.path.basename(caminho)[:-3].replace("solucao_", "")
    falhas, tempo_total = [], 0.0
    try:
        mod = carregar(caminho)
    except Exception as e:
        placar.append((nome, 0, len(TESTES), 0.0, [f"IMPORT: {type(e).__name__}: {e}"]))
        continue
    for tn, fn in TESTES:
        t = time.time()
        try:
            fn(mod)
        except BaseException as e:
            falhas.append(f"{tn} -> {type(e).__name__}")
        tempo_total += time.time() - t
    placar.append((nome, len(TESTES) - len(falhas), len(TESTES), tempo_total, falhas))

# ---------- placar ----------
placar.sort(key=lambda x: (-x[1], x[3]))
print(f"\n{'MODELO':<22}{'ACERTOS':<10}{'ERROS':<8}{'TEMPO':<9}")
print("-" * 50)
for nome, ok, total, tempo, falhas in placar:
    print(f"{nome:<22}{ok}/{total:<8}{total-ok:<8}{tempo:.2f}s")
print("\nDETALHE DOS ERROS")
for nome, ok, total, tempo, falhas in placar:
    if falhas:
        print(f"\n{nome}:")
        for f in falhas:
            print("   ❌", f)