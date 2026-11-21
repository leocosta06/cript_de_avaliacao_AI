# Teste de Modelos Gemini — Benchmark de Código em Python

Um benchmark simples e reproduzível para comparar a **qualidade do código gerado** por diferentes modelos (e níveis de raciocínio) do Gemini.

Cada modelo recebe o **mesmo prompt**, o código que ele devolve é salvo em um arquivo, e um script roda uma bateria de testes automáticos contra todos os arquivos de uma vez, gerando um placar com **acertos, erros, tempo e complexidade declarada**.

## O que é medido

- **Correção:** o código passa em casos normais e em casos de borda (entradas vazias, negativos, duplicados, ciclos...)?
- **Performance real:** testes com entradas grandes pegam solução O(n²) disfarçada de O(n).
- **Robustez:** por exemplo, árvore com 20.000 níveis de profundidade derruba quem usa recursão.
- **Complexidade declarada:** cada modelo precisa comentar `# Tempo: O(...)`; o script compara com o gabarito.
- **Timeout por teste:** loop infinito não trava o benchmark (cada teste roda em um subprocesso).

## Estrutura

```
teste_IA/
├── rodar_todos.py          # Rodada 1 (7 problemas clássicos)
├── rodar_v2.py             # Rodada 2 (8 problemas difíceis, com timeout)
├── solucao_<modelo>_<nivel>.py   # Código gerado na rodada 1
└── v2_<modelo>_<nivel>.py        # Código gerado na rodada 2
```

Exemplos de nomes: `solucao_pro_alto.py`, `v2_flash_lite_medio.py`.

## Como usar

Requisito: **Python 3.9+** (só biblioteca padrão, nada para instalar).

1. Copie o prompt da rodada desejada (veja abaixo) e envie **igual** para cada modelo.
2. Salve a resposta de cada modelo como arquivo `.py` seguindo o padrão de nomes:
   - Rodada 1: `solucao_<modelo>_<nivel>.py`
   - Rodada 2: `v2_<modelo>_<nivel>.py`
3. Rode:

```bash
python rodar_todos.py   # rodada 1
python rodar_v2.py      # rodada 2
```

O script descobre todos os arquivos automaticamente, roda os testes em cada um e imprime o placar ordenado por acertos e depois por tempo.

## Rodada 1 — problemas clássicos

`two_sum`, `valid_parentheses`, `merge_intervals`, `longest_palindrome`, `edit_distance`, `LRUCache`, `dijkstra` (mais um exercício de debug de busca binária, avaliado à mão).

**Resultado:** os 12 modelos testados tiraram **10/10**. O teste ficou fácil demais, o que motivou a rodada 2.

<details>
<summary>Ver prompt da rodada 1</summary>

```
Responda APENAS com código Python, sem explicações fora do código.
Use exatamente os nomes de função/classe pedidos. Para cada tarefa, coloque
em comentário no topo: "# Tempo: O(...) | Espaço: O(...)".

T1. two_sum(nums, target) -> list[int]
Retorna os índices [i, j] (i != j) cuja soma é target. Se não existir, None.
Deve rodar em O(n).

T2. valid_parentheses(s) -> bool
Valida (), [] e {} balanceados e na ordem correta. String vazia é válida.

T3. merge_intervals(intervals) -> list[list[int]]
Mescla intervalos sobrepostos ou que se tocam. A entrada pode estar
desordenada e pode ser vazia.

T4. longest_palindrome(s) -> str
Maior substring palíndroma. String vazia retorna "".

T5. edit_distance(a, b) -> int
Distância de Levenshtein (inserir, remover, substituir).

T6. class LRUCache
Métodos: __init__(capacity), get(key) -> int (retorna -1 se não existir),
put(key, value). get e put devem ser O(1). Remove o menos recentemente
usado ao estourar a capacidade.

T7. dijkstra(graph, start) -> dict
graph é {nó: [(vizinho, peso), ...]}. Retorna {nó: menor distância}.
Nós inalcançáveis = float('inf').
```

</details>

## Rodada 2 — problemas difíceis

| # | Problema | Pegadinha / o que testa |
|---|---|---|
| H1 | `median_of_two_sorted_arrays` | Exige O(log(min(n, m))); teste de performance com 2 milhões de elementos |
| H2 | `LFUCache` | Desempate por LRU, capacidade 0, atualização conta como uso, O(1) |
| H3 | `evaluate` (parser de expressões) | Sem `eval`; `^` associativo à direita; `-2^2 = -4`; erros específicos |
| H4 | `serialize` / `deserialize` de árvore | Árvore com 20.000 níveis (quebra recursão) |
| H5 | `min_window` | Menor janela com todos os caracteres, O(n) |
| H6 | `count_inversions` | Entrada de 200.000 elementos; exige O(n log n) |
| H7 | `topo_sort` | Ordem lexicograficamente menor, ciclos, laços e arestas repetidas |
| H8 | `max_sliding_window` | O(n) com deque; O(n·k) estoura o timeout |

Cada problema tem um teste de correção e um de performance (**16 testes no total**). Timeout: 5s (normal) e 10s (performance).

### Resultado (execução única)

| Modelo | Acertos |
|---|---|
| argon_baixo | 16/16 |
| argon_medio | 16/16 |
| flash_medio | 16/16 |
| argon_alto | 16/16 |
| flash_baixo | 15/16 |
| pro_baixo | 15/16 |
| flash_lite_alto | 15/16 |
| flash_lite_baixo | 14/16 |
| flash_lite_medio | 13/16 |
| pro_medio | 5/16 |

O teste **H3 (parser)** foi o que mais separou os modelos: vários ignoraram a regra de que `-2^2` deve dar `-4`.

> **Leia com cuidado.** Cada modelo foi testado **uma única vez**. A diferença entre 15/16 e 16/16 pode ser sorte, e o `pro_medio` perdeu 10 dos 11 testes por um único `import collections` esquecido. Para conclusões mais sólidas, rode cada modelo várias vezes e compare a média.

<details>
<summary>Ver prompt da rodada 2</summary>

```
Responda APENAS com código Python, sem explicações fora do código.
Use exatamente os nomes pedidos. Antes de cada função/classe, coloque
um comentário: "# Tempo: O(...) | Espaço: O(...)".
Não use bibliotecas externas (só a biblioteca padrão).

H1. median_of_two_sorted_arrays(a, b) -> float
Mediana de dois arrays ordenados (podem ser vazios, nunca os dois).
Deve rodar em O(log(min(n, m))).

H2. class LFUCache
__init__(capacity), get(key) -> int (-1 se não existir), put(key, value).
Remove o menos frequentemente usado; em empate, o menos recentemente
usado. put em chave existente atualiza o valor e conta como uso.
capacity 0 não guarda nada. get e put devem ser O(1).

H3. evaluate(expr: str) -> float
Calculadora com + - * / ^ e parênteses, números decimais e espaços.
^ é associativo à direita (2^3^2 = 512) e tem precedência maior que o
menos unário (-2^2 = -4). O expoente pode ter sinal (2^-1 = 0.5).
Expressão inválida -> ValueError. Divisão por zero -> ZeroDivisionError.
Não pode usar eval, exec nem ast.

H4. serialize(root) -> str e deserialize(data) -> root
Árvore binária com esta classe (inclua no seu código):
class TreeNode:
    def __init__(self, val=0, left=None, right=None): ...
Valores inteiros (negativos e com vários dígitos). Árvore vazia (None)
deve funcionar. Precisa aguentar árvores com 20.000 níveis de profundidade.

H5. min_window(s, t) -> str
Menor substring de s que contém todos os caracteres de t (com
repetições). Se não existir ou t for vazio, retorna "". O(n).

H6. count_inversions(arr) -> int
Número de pares (i < j) com arr[i] > arr[j] (estritamente maior).
Deve rodar em O(n log n).

H7. topo_sort(n, edges) -> list[int] | None
Nós 0..n-1, edges é lista de (u, v) significando u antes de v.
Retorna a ordem topológica lexicograficamente menor, ou None se
houver ciclo (inclusive laço u == v). Pode haver arestas repetidas.

H8. max_sliding_window(nums, k) -> list[int]
Máximo de cada janela de tamanho k. Lista vazia -> []. O(n).
```

</details>

## Limitações conhecidas

- **Complexidade declarada:** a comparação associa os comentários `# Tempo:` às tarefas pela **ordem** em que aparecem no arquivo. Se o modelo omitir um comentário ou comentar uma função auxiliar, os resultados deslocam. Use essa coluna como pista, não como veredito.
- **Tempo de execução:** mede o código gerado, não a velocidade do modelo, e varia com a carga da máquina.
- **Execução única:** modelos são não determinísticos; os resultados podem mudar entre execuções.
- **Escopo:** só avalia geração de código algorítmico em Python, não representa a qualidade geral do modelo.

## Próximos passos

- [ ] Associar a complexidade declarada a cada função pelo nome, em vez da ordem
- [ ] Rodar cada modelo N vezes e reportar a média
- [ ] Rodada 3 com problemas ainda mais difíceis
- [ ] Gerar a tabela final em Markdown/CSV automaticamente

Defina a licença do seu repositório (por exemplo, MIT).
