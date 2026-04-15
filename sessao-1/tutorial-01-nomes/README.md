# Tutorial 01 — Nomes Significativos

> **Sessão 1 · Bloco 1 · 20 min de teoria + 10 min de exercício**
> Referência: *Clean Code*, Capítulo 2 — Meaningful Names

---

## 1. Contexto e Motivação

Lemos código muito mais do que o escrevemos. Robert Martin estima que a proporção é de **10:1** — para cada linha escrita, lemos dez. Por isso, um nome ruim não é apenas esteticamente desagradável: ele é um imposto cognitivo pago toda vez que alguém (inclusive você) lê aquele trecho.

Nomes são a forma mais barata e poderosa de documentação que existe. Eles não precisam de manutenção separada, não ficam desatualizados quando o código muda (se você os mudar junto) e são lidos inline, no contexto certo.

---

## 2. Conceito Central

Um bom nome responde a três perguntas sem precisar de comentário:

1. **Por que existe?** — qual é o propósito deste elemento?
2. **O que faz?** — qual é o seu comportamento ou valor?
3. **Como é usado?** — qual é o seu contexto de uso?

Se você precisa de um comentário para explicar o nome, o nome está errado.

### Os cinco pecados de nomenclatura

| Pecado | Descrição |
|---|---|
| **Intenção oculta** | `d`, `x`, `tmp` — nenhum contexto |
| **Desinformação** | `lista_de_contas` que é um dict |
| **Distinção sem significado** | `get_dados` vs `get_dados2` |
| **Impronunciabilidade** | `DtRcrdMgr`, `gnrtn_ymdhms` |
| **Notação húngara** | `str_nome`, `int_idade`, `lst_pedidos` |

---

## 3. O Problema na Prática

```python
# O que este código faz? Quanto tempo você levou para entender?

d = 0

def get(l, s):
    r = []
    for i in l:
        if i[0] == s:
            r.append(i)
    return r

lista_de_contas = {"joao": 1500.0, "maria": 3200.0}  # não é uma lista!
```

**Problemas identificados:**
- `d` não revela o que representa (dias? distância? dados?)
- `get`, `l`, `s`, `r`, `i` — nenhum nome carrega contexto
- `lista_de_contas` mente sobre o tipo da estrutura de dados

> Arquivo completo: [`exemplos/nomes_ruins.py`](exemplos/nomes_ruins.py)

---

## 4. A Solução

```python
dias_desde_criacao = 0

def filtrar_pedidos_por_status(pedidos, status):
    pedidos_filtrados = []
    for pedido in pedidos:
        if pedido[0] == status:
            pedidos_filtrados.append(pedido)
    return pedidos_filtrados

saldo_por_titular = {"joao": 1500.0, "maria": 3200.0}
```

**O que mudou:**
- `dias_desde_criacao` responde imediatamente "o que é `d`?"
- `filtrar_pedidos_por_status(pedidos, status)` — lê-se como uma frase em português
- `saldo_por_titular` descreve a estrutura corretamente (mapeamento nome → saldo)

> Arquivo completo: [`exemplos/nomes_bons.py`](exemplos/nomes_bons.py)

---

## 5. Equivalentes em Outras Linguagens

### PHP

```php
// ❌ Ruim
function get($l, $s) { return array_filter($l, fn($i) => $i[0] === $s); }

// ✅ Bom
function filtrarPedidosPorStatus(array $pedidos, string $status): array {
    return array_filter($pedidos, fn($pedido) => $pedido['status'] === $status);
}
```

### TypeScript

```typescript
// ❌ Ruim
const get = (l: any[], s: string) => l.filter(i => i[0] === s);

// ✅ Bom
const filtrarPedidosPorStatus = (pedidos: Pedido[], status: string): Pedido[] =>
  pedidos.filter(pedido => pedido.status === status);
```

### ADVPL/TLPP

```advpl
// ❌ Ruim — abreviações além do prefixo de tipo
Function Proc( aL, cS )

// ✅ Bom — prefixos de tipo MANTIDOS (convenção Totvs), nome descritivo
Function FiltrarPedidosPorStatus( aPedidos, cStatus )
```

> **Nota ADVPL/TLPP:** Os prefixos de tipo (`n`, `c`, `a`, `l`, `d`, `o`) são **convenção obrigatória** do ecossistema Totvs e devem ser mantidos. O princípio de Clean Code se aplica ao nome que vem *após* o prefixo.

> Arquivos completos: [`exemplos/equivalente.php`](exemplos/equivalente.php) · [`exemplos/equivalente.ts`](exemplos/equivalente.ts) · [`exemplos/equivalente.tlpp`](exemplos/equivalente.tlpp)

---

## 6. Regras de Ouro

- **Nomes revelam intenção** — se precisar de comentário para explicar o nome, troque o nome
- **Classes são substantivos** (`GerenciadorDeRegistros`, `CarrinhoDeCompras`)
- **Funções são verbos** (`calcular_total`, `filtrar_por_status`, `validar_usuario`)
- **Evite abreviações** — editores modernos completam nomes longos; leitores humanos não completam nomes curtos
- **Consistência é lei** — se você usa `get_usuario` em um lugar, não use `buscar_user` em outro

---

## 7. Exercício

**Tarefa:** Renomeie todas as variáveis, parâmetros, funções e classes do arquivo de exercício para que os nomes revelem claramente a intenção. Não altere a lógica.

```bash
# Rode o exercício para ver o output esperado:
python exercicios/exercicio.py

# Quando terminar, compare com o gabarito:
python exercicios/gabarito.py
```

> Arquivo: [`exercicios/exercicio.py`](exercicios/exercicio.py)
> Gabarito: [`exercicios/gabarito.py`](exercicios/gabarito.py)

---

## 8. Para se Aprofundar

- **Clean Code**, Robert C. Martin — Capítulo 2: *Meaningful Names* (p. 17–30)
- **The Pragmatic Programmer**, Hunt & Thomas — Tópico 22: *Naming Things*
- Ferramenta: [`pylint`](https://pylint.org/) detecta automaticamente nomes de variável com menos de 3 caracteres

---

> **Próximo tutorial:** [Tutorial 02 — Funções](../tutorial-02-funcoes/README.md)
