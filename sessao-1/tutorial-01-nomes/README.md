# Tutorial 01 — Nomes Significativos

> Referência: *Clean Code*, Capítulo 2 — Meaningful Names

---

## 1. Contexto e Motivação

Lemos código muito mais do que o escrevemos. Robert Martin estima que a proporção é de **10:1** — para cada linha escrita, lemos dez. Isso muda o cálculo de onde investir esforço: o custo de escrever um bom nome é segundos; o benefício de lê-lo com clareza se acumula durante meses ou anos.

Nomes são a forma mais barata e poderosa de documentação que existe. Eles não precisam de manutenção separada, não ficam desatualizados quando o código muda (se você os mudar junto) e são lidos inline, no contexto certo.

O conceito-chave aqui é **cognitive load** — carga cognitiva. Cada nome ruim é um pequeno imposto pago pelo leitor toda vez que encontra aquele símbolo: ele precisa pausar, lembrar o que aquilo significa, traduzir mentalmente para algo com sentido, e só então continuar. Nomes ruins não tornam o código apenas menos bonito — eles tornam a leitura ativamente mais cara.

---

## 2. Conceito Central

Um bom nome responde a três perguntas sem precisar de comentário:

1. **Por que existe?** — qual é o propósito deste elemento?
2. **O que faz?** — qual é o seu comportamento ou valor?
3. **Como é usado?** — qual é o seu contexto de uso?

Se você precisa de um comentário para explicar o nome, o nome está errado.

### Os cinco pecados de nomenclatura

**1. Intenção oculta** — o nome não revela o propósito.

```python
d = 0          # O que é d? Dias? Distância? Dados?
x = get(l, s)  # Nenhum contexto. Força o leitor a ler a implementação.
```

**2. Desinformação** — o nome mente sobre o que o elemento é.

```python
lista_de_contas = {"joao": 1500.0, "maria": 3200.0}
# Não é uma lista. É um dicionário. O nome cria uma expectativa falsa.
```

**3. Distinção sem significado** — diferenças que não informam nada.

```python
def get_dados(id):   ...
def get_dados2(id):  ...  # O que diferencia get_dados de get_dados2?
def get_dados_info(id): ...  # "Info" acrescenta algo? Não.
```

**4. Impronunciabilidade** — nomes que não cabem numa conversa.

```python
DtRcrdMgr    # "Dê-tê-erre-cê-erre-dê-eme-jê-erre"?
gnrtn_ymdhms # Como você fala isso em uma code review?
```

Código é comunicação entre humanos. Se você não consegue pronunciar o nome, não consegue discuti-lo. Reuniões, pair programming e code reviews ficam travados em "aquela variável, sabe... a `g-n-r-t-n`...".

**5. Notação húngara** — prefixo de tipo no nome.

```python
str_nome     = "João"
int_idade    = 30
lst_pedidos  = []
```

Em linguagens tipadas — ou com type hints — o tipo já está declarado. O prefixo só polui. Em ADVPL/TLPP, os prefixos `c`, `n`, `a`, `l`, `d`, `o` são convenção obrigatória do ecossistema Totvs e **devem ser mantidos**; o princípio se aplica ao nome que vem *após* o prefixo.

---

### Dois eixos adicionais do Clean Code

**Nomes do domínio do problema vs. domínio da solução** (Clean Code p. 27)

Prefira nomes do domínio do negócio quando o conceito tem dono no mundo real:

```python
# Domínio da solução (técnico, genérico)
processar_item(dado)

# Domínio do problema (específico, comunicável com o negócio)
aprovar_solicitacao_de_reembolso(solicitacao)
```

Use nomes técnicos (`Queue`, `Stack`, `Visitor`) quando estiver implementando padrões ou estruturas que todo desenvolvedor reconhece. Use nomes do domínio quando estiver modelando regras de negócio.

**Uma palavra por conceito**

Escolha uma palavra para cada operação e mantenha-a em todo o codebase:

```python
# ❌ Mistura — leitor não sabe se há diferença semântica
def fetch_usuario(id): ...
def retrieve_produto(id): ...
def get_pedido(id): ...

# ✅ Consistência — uma palavra para "buscar"
def buscar_usuario(id): ...
def buscar_produto(id): ...
def buscar_pedido(id): ...
```

**Não faça trocadilhos** (Clean Code p. 26)

Um nome não deve ter dois propósitos diferentes. Se `add` significa "somar dois valores" em um contexto e "inserir na coleção" em outro, você criou um trocadilho. Use `inserir` ou `adicionar` para o segundo caso.

---

## 3. O Problema na Prática

```python
# O que este código faz? Quanto tempo você levou para entender?

d = 0                                               # (1)

def get(l, s):                                      # (2)
    r = []                                          # (3)
    for i in l:                                     # (4)
        if i[0] == s:                               # (5)
            r.append(i)
    return r

lista_de_contas = {"joao": 1500.0, "maria": 3200.0} # (6)
```

**Análise linha a linha:**

1. `d = 0` — variável de nome único. Dias? Desconto? Dado? Impossível saber sem contexto adicional.
2. `get(l, s)` — função sem intenção revelada. `l` é lista? `s` é string? Status? Símbolo?
3. `r = []` — resultado? registro? relatório? O nome de uma linha é `r`.
4. `for i in l` — `i` é o índice convencionado em loops numéricos; aqui parece ser um elemento composto (não um índice).
5. `if i[0] == s` — acessa posição 0 de algo e compara com `s`. Sem o nome, impossível saber se é `status`, `sigla`, `sku` ou outra coisa.
6. `lista_de_contas` que é um `dict` — desinformação ativa. Qualquer código que itere esperando uma lista vai se comportar de forma inesperada.

> Arquivo completo: [`exemplos/nomes_ruins.py`](exemplos/nomes_ruins.py)

---

## 4. A Solução

```python
dias_desde_criacao = 0                              # (1)

def filtrar_pedidos_por_status(pedidos, status):    # (2)
    pedidos_filtrados = []                          # (3)
    for pedido in pedidos:                          # (4)
        if pedido[0] == status:                     # (5)
            pedidos_filtrados.append(pedido)
    return pedidos_filtrados

saldo_por_titular = {"joao": 1500.0, "maria": 3200.0}  # (6)
```

**Decisões de renomeação:**

1. `dias_desde_criacao` — agora sabemos o que representa, a unidade (dias) e o ponto de referência (desde a criação).
2. `filtrar_pedidos_por_status(pedidos, status)` — lê-se como uma frase em português. O verbo ("filtrar") deixa claro que é uma seleção, não uma mutação.
3. `pedidos_filtrados` — o sufixo `_filtrados` conecta o resultado ao critério da função.
4. `for pedido in pedidos` — agora `pedido` é singular de `pedidos`; a relação todo-parte fica visível.
5. `pedido[0] == status` — ainda acessa por índice (melhoraria com dataclass), mas ao menos `status` revela o que está sendo comparado.
6. `saldo_por_titular` — descreve a estrutura corretamente: um mapeamento de titular para saldo.

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

> **Nota ADVPL/TLPP:** Os prefixos de tipo (`n`, `c`, `a`, `l`, `d`, `o`) são **convenção obrigatória** do ecossistema Totvs e devem ser mantidos. O princípio de Clean Code se aplica ao nome que vem *após* o prefixo: `cS` é inaceitável; `cStatus` é correto.

> Arquivos completos: [`exemplos/equivalente.php`](exemplos/equivalente.php) · [`exemplos/equivalente.ts`](exemplos/equivalente.ts) · [`exemplos/equivalente.tlpp`](exemplos/equivalente.tlpp)

---

## 6. Aprofundamento: Nomes em Contexto de Time

O impacto de nomes ruins se multiplica em times. Quando cada desenvolvedor usa seu próprio vocabulário para os mesmos conceitos, o codebase vira uma Torre de Babel.

### Glossário de domínio

A solução mais eficaz é criar um **glossário de domínio** compartilhado — uma lista curta (não precisa ser exaustiva) que define os termos canônicos usados no código:

| Conceito de negócio | Termo canônico no código |
|---|---|
| Pessoa que fez a compra | `comprador` (não `cliente`, não `user`, não `pessoa`) |
| Ação de buscar do banco | `buscar_` (não `get_`, não `fetch_`, não `retrieve_`) |
| Pedido ainda não pago | `pedido_pendente` (não `pedido_aberto`, não `order_open`) |

Esse documento não precisa ter mais de uma página. O valor está na decisão, não no tamanho.

### Como definir convenções em equipe

1. **Comece pelo domínio**, não pela tecnologia. Quais são os 10 conceitos que mais aparecem no código?
2. **Decida por consenso, documente por autoridade.** Uma pessoa escreve, o time aprova, todos seguem.
3. **Trate violações em code review**, não depois. Nomes são mais fáceis de corrigir antes do merge.
4. **Evolua o glossário quando o negócio evoluir.** Um glossário congelado envelhece e perde credibilidade.

### Consistência é mais importante que perfeição

`buscar_usuario` é um nome razoável. `fetch_usuario` também é. Mas usar os dois no mesmo codebase é pior do que qualquer um deles sozinho — porque força o leitor a questionar se há uma diferença intencional.

---

> **👉 ATIVIDADE:** Liste 5 nomes do código real da equipe que poderiam ser melhorados. Para cada um, escreva: (a) o nome atual, (b) o problema específico, (c) o nome proposto.

---

## 7. Regras de Ouro

- **Nomes revelam intenção** — se precisar de comentário para explicar o nome, troque o nome
- **Classes são substantivos** (`GerenciadorDeRegistros`, `CarrinhoDeCompras`)
- **Funções são verbos** (`calcular_total`, `filtrar_por_status`, `validar_usuario`)
- **Evite abreviações** — editores modernos completam nomes longos; leitores humanos não completam nomes curtos
- **Consistência é lei** — se você usa `buscar_usuario` em um lugar, não use `get_user` em outro
- **Uma palavra por conceito** — escolha `buscar`, `calcular` ou `validar` e use sempre a mesma palavra para a mesma operação
- **Não faça trocadilhos** — o mesmo nome não deve ter dois propósitos distintos no mesmo codebase

---

## 8. Exercício

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

## 9. Para se Aprofundar

- **Clean Code**, Robert C. Martin — Capítulo 2: *Meaningful Names* (p. 17–30)
- **The Pragmatic Programmer**, Hunt & Thomas — Tópico 22: *Naming Things*
- **Domain-Driven Design**, Eric Evans — Capítulo 2: *Ubiquitous Language* (a linguagem compartilhada entre código e negócio)
- Ferramenta: [`pylint`](https://pylint.org/) detecta automaticamente nomes de variável com menos de 3 caracteres

---

> **Próximo tutorial:** [Tutorial 02 — Funções](../tutorial-02-funcoes/README.md)
