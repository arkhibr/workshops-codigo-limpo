# Gabarito — Revisão de Segurança do Exercício

Este arquivo aplica o checklist do Tutorial 14 ao código de `exercicio.py` / `exercicio.ts`,
identifica cada vulnerabilidade e explica a correção adotada em `gabarito.py` / `gabarito.ts`.

---

## Vulnerabilidades encontradas

### 1. LIKE por concatenação de string (brecha principal)

**Onde está:**

```python
# exercicio.py — linha da query
f"WHERE categoria = ? AND descricao LIKE '%{filtros.termo_busca}%' "
```

```typescript
// exercicio.ts — filtro em memória (equivalente)
p.descricao.toLowerCase().includes(filtros.termoBusca.toLowerCase())
// sem validação de entrada antes do includes()
```

**Por que é sutil:** a cláusula `WHERE categoria = ?` usa parâmetro posicional — parece
seguro à primeira vista. O `ORDER BY` usa allow-list — também correto. O olhar do revisor
vê os dois controles e relaxa. A concatenação do `termo_busca` no LIKE fica na mesma linha
da query, sem destaque visual, e escapa da revisão.

**Impacto:** em SQL, `LIKE '%{termo}%'` com `termo = '%'` resulta em `LIKE '%%%'`, que o
SQLite trata como `LIKE '%'` — retornando todos os registros da categoria.
Com `termo = '_'`, cada `_` casa com qualquer caractere individual. Com `termo = "'; DROP TABLE--"`,
a query fica sintaticamente inválida dependendo do driver (pode causar erro ou — em drivers
menos rigorosos — executar o restante).

**Correção em gabarito.py:**

```python
# Termo vai como parâmetro — nunca concatenado na query
termo_like = f"%{filtros.termo_busca}%" if filtros.termo_busca else "%"
query = (
    "...WHERE categoria = ? AND descricao LIKE ? "
    f"ORDER BY {coluna}"
)
cursor = _conn.execute(query, (filtros.categoria, termo_like))
```

O `%` delimitador é embutido no **valor do parâmetro**, não na string da query.
O driver trata o valor como texto literal — incluindo os `%` e `_` que o usuário
possa passar dentro do texto (com escape automático via parametrização).

---

### 2. Ausência de validação de entrada para o termo de busca

**Onde está:** `exercicio.py` valida `categoria` via allow-list mas não valida `termo_busca`
antes de usá-lo. Qualquer string chega à query sem verificação.

**Por que é sutil:** o `FiltroProduto.__post_init__` tem validação de `categoria` — parece
que a validação de entrada está feita. A ausência de validação do `termo_busca` fica implícita.

**Correção em gabarito.py:**

```python
_PADRAO_TERMO_SEGURO = re.compile(r"^[a-zA-ZáàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇ0-9 ]{1,50}$")

def __post_init__(self) -> None:
    if self.categoria not in CATEGORIAS_VALIDAS:
        raise ValueError(...)
    if self.termo_busca and not _PADRAO_TERMO_SEGURO.match(self.termo_busca):
        raise ValueError(...)
```

O padrão bloqueia `%`, `_`, `;`, aspas, parênteses e outros caracteres perigosos
antes que o termo chegue à query. A validação é **defesa em profundidade** — a
barreira principal é a parametrização do LIKE; a regex é uma segunda linha de defesa.

---

## O que estava correto no exercício

O exercício não era completamente vulnerável — dois controles já estavam corretos:

| Controle | Status no exercício | Status no gabarito |
|---|---|---|
| Filtro de `categoria` | Parametrizado com `?` | Parametrizado com `?` |
| `ORDER BY` | Allow-list (`COLUNAS_ORDENACAO_PERMITIDAS`) | Allow-list (mantido) |
| Termo no `LIKE` | Concatenação direta | Parâmetro posicional |
| Validação do termo | Ausente | Regex restrita |

O ORDER BY já estava protegido — isso é o que tornava o exercício "sutil": dois
controles corretos, um ausente, e o ausente estava na parte mais visível da query.

---

## Checklist aplicado

1. **Toda parte da query é parametrizada?**
   - `exercicio.py`: **Não** — `LIKE '%{termo}%'` concatena o termo.
   - `gabarito.py`: **Sim** — `LIKE ?` com valor `f"%{termo}%"` como parâmetro.

2. **A ordenação usa allow-list?**
   - `exercicio.py`: **Sim** — `COLUNAS_ORDENACAO_PERMITIDAS` já presente.
   - `gabarito.py`: **Sim** — mantido.

3. **A validação tem bypass?**
   - `exercicio.py`: **Sim** — sem validação de `termo_busca`, qualquer string passa.
   - `gabarito.py`: **Não** — regex bloqueia `%`, `_`, caracteres especiais.

4. **Algum segredo está inline?**
   - Ambos: **Não** — banco em memória, sem credenciais.

5. **LIKE monta o `%` com parâmetro ou concatenação?**
   - `exercicio.py`: **Concatenação** — `f"LIKE '%{termo}%'"` — vulnerável.
   - `gabarito.py`: **Parâmetro** — `execute(..., (f"%{termo}%",))` — seguro.

6. **A dependência nova foi justificada?**
   - Ambos: **Não aplicável** — módulo `sqlite3` é da biblioteca padrão.

---

## Lição principal

O código do exercício protege o que o desenvolvedor "lembrou" de proteger:
o filtro de categoria (porque category injection é um exemplo clássico) e
o ORDER BY (porque o tutorial mencionou esse padrão). O LIKE ficou fora
da atenção — não porque o desenvolvedor fosse negligente, mas porque
o código *parecia* completo depois dos dois controles presentes.

Esta é a dinâmica central do Tutorial 14: código gerado por IA (ou escrito
com pressa) protege as brechas conhecidas e deixa as adjacentes. A revisão
de segurança precisa ir além do "tem parâmetros?" e perguntar "**qual parte
da query não tem parâmetros?**".
