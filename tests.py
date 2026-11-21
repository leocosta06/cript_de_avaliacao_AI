import time, math
import solucao_flash_lite_medio as s

resultados = []

def teste(nome, fn):
    try:
        t = time.time()
        fn()
        dt = time.time() - t
        resultados.append((nome, True, f"{dt:.3f}s"))
    except Exception as e:
        resultados.append((nome, False, f"{type(e).__name__}: {e}"))

def t1():
    assert sorted(s.two_sum([2,7,11,15], 9)) == [0,1]
    assert sorted(s.two_sum([3,2,4], 6)) == [1,2]
    assert sorted(s.two_sum([3,3], 6)) == [0,1]
    assert s.two_sum([1,2], 99) is None

def t1_perf():
    n = 200_000
    assert s.two_sum(list(range(n)), 2*n) is None  # sem solução, pior caso

def t2():
    for ok in ["()[]{}", "{[]}", ""]:
        assert s.valid_parentheses(ok) is True, ok
    for bad in ["(]", "([)]", "(", ")"]:
        assert s.valid_parentheses(bad) is False, bad

def t3():
    assert s.merge_intervals([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
    assert s.merge_intervals([[1,4],[4,5]]) == [[1,5]]
    assert s.merge_intervals([]) == []
    assert s.merge_intervals([[5,6],[1,2]]) == [[1,2],[5,6]]
    assert s.merge_intervals([[1,4],[2,3]]) == [[1,4]]

def t3_perf():
    s.merge_intervals([[i, i+1] for i in range(0, 200_000, 2)])

def t4():
    assert s.longest_palindrome("babad") in ("bab", "aba")
    assert s.longest_palindrome("cbbd") == "bb"
    assert s.longest_palindrome("a") == "a"
    assert s.longest_palindrome("") == ""

def t5():
    assert s.edit_distance("kitten", "sitting") == 3
    assert s.edit_distance("", "abc") == 3
    assert s.edit_distance("abc", "abc") == 0
    assert s.edit_distance("horse", "ros") == 3

def t5_perf():
    s.edit_distance("a"*1000, "b"*1000)

def t6():
    c = s.LRUCache(2)
    c.put(1, 1); c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)
    assert c.get(2) == -1
    c.put(4, 4)
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4

def t7():
    g = {'A':[('B',1),('C',4)], 'B':[('C',2),('D',5)], 'C':[('D',1)], 'D':[], 'E':[]}
    d = s.dijkstra(g, 'A')
    assert d['A']==0 and d['B']==1 and d['C']==3 and d['D']==4
    assert d['E'] == math.inf

for nome, fn in [("T1 two_sum", t1), ("T1 perf O(n)", t1_perf),
                 ("T2 parênteses", t2), ("T3 intervalos", t3),
                 ("T3 perf", t3_perf), ("T4 palíndromo", t4),
                 ("T5 edit distance", t5), ("T5 perf", t5_perf),
                 ("T6 LRU", t6), ("T7 dijkstra", t7)]:
    teste(nome, fn)

ok = sum(1 for _, p, _ in resultados if p)
for nome, p, info in resultados:
    print(("✅" if p else "❌"), nome, "-", info)
print(f"\nAcertos: {ok}/{len(resultados)} | Erros: {len(resultados)-ok}")