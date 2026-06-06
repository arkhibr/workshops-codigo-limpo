# Tutorial 14 — Segurança em Código Gerado por IA

> Referência: segurança em código gerado por IA; complementa o tutorial 12.

---

## 1. Contexto e Motivação

O Tutorial 12 apresentou os seis modos de falha de código gerado por IA de
fronteira. O Modo 3 — "segurança sutil" — merece um tutorial inteiro. Não porque
seja o mais comum, mas porque é o mais silencioso: o defeito passa no caminho
feliz, passa na leitura rápida e muitas vezes passa na revisão de pull request.

Em 2026, Claude Opus 4.8, GPT-4o e Gemini 2.5 não geram `sk-prod-` em texto
plano nem deixam `except: pass` em código de produção. O perigo é diferente.
O modelo parametriza o `WHERE` da query — porque sabe que SQL injection é o
problema a evitar — e interpola o `ORDER BY` por concatenação de string, porque
`ORDER BY` não pode ser parametrizado pela maioria dos drivers e o modelo não
tem contexto de que aquele campo vem do usuário.

O resultado é código que *parece* seguro. A parametrização do `WHERE` está lá,
visível. O `ORDER BY` fica numa linha diferente, num bloco de montagem de
query, longe do contexto de validação. Em revisão rápida, a linha escapa.

> *"The last security review found what the author couldn't see — not because
> the author was incompetent, but because the author knew the intended behavior."*
>
> — Michael Feathers, *Working Effectively with Legacy Code*

O princípio vale para o modelo: ele gera o que é estatisticamente provável
para aquele padrão de query. O que é provável para `ORDER BY` no conjunto de
treinamento é a interpolação de string — porque é o que a maioria dos exemplos
na internet faz.

---

## 2. Conceito Central

### A brecha mais comum: ORDER BY por interpolação

Considere um endpoint de busca com filtro e ordenação. O desenvolvedor (ou o
modelo) sabe que `WHERE` precisa ser parametrizado:

```python
# WHERE parametrizado — CORRETO
cursor.execute(
    "SELECT * FROM pedidos WHERE status = ? AND cliente_id = ?",
    (filtros["status"], filtros["cliente_id"]),
)
```

Agora o `ORDER BY`. A maioria dos drivers não aceita parâmetro posicional em
cláusulas de ordenação — `ORDER BY ?` levanta erro. Então o modelo interpola:

```python
# ORDER BY interpolado — VULNERÁVEL
query = f"SELECT * FROM pedidos WHERE ... ORDER BY {ordenacao}"
```

A query parece correta: o `WHERE` usa `?`, a parametrização está lá. Mas
`ordenacao` vem do usuário. Um valor como `(SELECT secret FROM tokens LIMIT 1)`
ou `1; DROP TABLE pedidos--` abusa da interpolação.

**Por que é sutil:** o `WHERE` parametrizado cria uma falsa sensação de
segurança. O olhar do revisor vê os `?`, relaxa, e não checa a cláusula de
ordenação na linha seguinte.

### A correção: allow-list de colunas

`ORDER BY` não pode ser parametrizado — mas pode ser validado antes de interpolado:

```python
COLUNAS_ORDENACAO_PERMITIDAS = {"data_criacao", "valor_total", "numero_pedido"}

def _coluna_ordenacao_segura(ordenacao: str) -> str:
    coluna = ordenacao.strip().lower()
    if coluna not in COLUNAS_ORDENACAO_PERMITIDAS:
        raise ValueError(f"Coluna de ordenação inválida: '{ordenacao}'")
    return coluna
```

O allow-list garante que apenas identificadores conhecidos cheguem à query.
Qualquer outro valor — incluindo payloads de injeção — é rejeitado antes de
tocar no banco.

### Antes e depois da brecha

**Vulnerável:**
```python
# ordenacao vem do usuário; nenhuma validação antes da interpolação
query = (
    "SELECT id, numero_pedido, valor_total, data_criacao "
    "FROM pedidos "
    f"WHERE status = ? AND cliente_id = ? "
    f"ORDER BY {ordenacao}"
)
```

**Seguro:**
```python
coluna = _coluna_ordenacao_segura(ordenacao)   # rejeita tudo fora do allow-list
query = (
    "SELECT id, numero_pedido, valor_total, data_criacao "
    "FROM pedidos "
    "WHERE status = ? AND cliente_id = ? "
    f"ORDER BY {coluna}"                        # só chega coluna validada
)
```

### Outras brechas sutis em código de IA

Além do `ORDER BY`, código gerado por IA frequentemente apresenta:

- **LIKE por concatenação:** `f"WHERE descricao LIKE '%{termo}%'"` — o `%`
  delimitador é inserido pelo código, mas o `termo` não é escapado. Um termo
  com `%` ou `_` abusa do padrão LIKE. (`LIKE ?` com o `%` no valor passado
  como parâmetro é o padrão seguro.)

- **Segredo inline junto com env:** o modelo usa `os.getenv("DB_PASSWORD")` para
  a senha — mas deixa um token de API hardcoded na linha seguinte porque "é só
  para autenticação interna".

- **Regex com bypass:** `re.match(r"^\w+$", campo)` parece validar apenas
  palavras — mas `\w` inclui letras Unicode em locales não-ASCII, e o padrão
  sem delimitador final aceita strings com sufixo inesperado em algumas versões.

---

## 3. Exercício

### O que fazer

1. **Leia** `exercicios/exercicio.py` (ou `.ts`) como um Pull Request real.
   O código parece correto — toda a query está montada de forma aparentemente
   segura. Encontre a brecha sutil.

2. **Rode** o código para confirmar que o caminho feliz funciona e que a
   demonstração em memória exibe o comportamento:
   ```bash
   python3 exercicios/exercicio.py
   npx ts-node exercicios/exercicio.ts
   ```

3. **Responda** às três perguntas do cabeçalho:
   - Onde está a brecha sutil?
   - Como endurecer?
   - O que faltava no código original?

4. **Implemente** a correção no próprio arquivo ou em uma cópia.

5. **Compare** com `gabarito.py` (ou `.ts`) e leia `gabarito_revisao.md`
   para conferir o checklist aplicado.

---

## 4. Checklist de Segurança para Código Gerado por IA

Use este checklist em qualquer revisão de endpoint que acesse banco de dados.

1. **Toda parte da query é parametrizada?** — Não apenas o `WHERE`. Verifique
   `ORDER BY`, `LIKE`, `GROUP BY`, nomes de tabela e nomes de coluna.

2. **A ordenação usa allow-list?** — Qualquer campo de ordenação que vem do
   usuário precisa ser validado contra um conjunto fixo de colunas permitidas
   antes de ser interpolado.

3. **A validação tem bypass?** — Regexes com `\w`, `\d` ou âncoras ausentes
   podem aceitar inputs que parecem bloqueados. Teste com `%`, `_`, espaço,
   Unicode e sufixos inesperados.

4. **Algum segredo está inline?** — Usar `os.getenv` para a senha do banco não
   garante que o token de API na linha seguinte também venha do ambiente.
   Verifique todos os campos de autenticação no mesmo módulo.

5. **LIKE monta o `%` com parâmetro ou concatenação?** — `cursor.execute(
   "WHERE x LIKE ?", (f"%{termo}%",))` é seguro. `f"WHERE x LIKE '%{termo}%'"` não é.

6. **A dependência nova foi justificada?** — Uma biblioteca adicionada pelo
   modelo para "facilitar a parametrização" pode ter CVEs conhecidos ou
   comportamento diferente do que o modelo descreveu.

---

## 5. Referências

- *Clean Code* — Robert C. Martin (Cap. 3: funções pequenas e responsabilidade única)
- *Working Effectively with Legacy Code* — Michael Feathers (Cap. 8: efeitos colaterais)
- Tutorial 12 — Revisão Crítica de Código Gerado por IA: o Modo 3 (segurança sutil)
- Tutorial 09 — Engenharia de Contexto e Prompt: como pedir com requisitos de segurança
- OWASP SQL Injection Prevention Cheat Sheet — parametrização e allow-lists

---

> **Próximo tutorial:** [Tutorial 15 — Testes guard-rails e manutenibilidade](../tutorial-15-testes-guard-rails/README.md)
