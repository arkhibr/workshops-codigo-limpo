# Tutorial 03 — Comentários

> **Sessão 1 · Bloco 3 · 20 min de teoria + 10 min de exercício**
> Referência: *Clean Code*, Capítulo 4 — Comments

---

## 1. Contexto e Motivação

O capítulo 4 do Clean Code começa com uma provocação: "A necessidade de comentários é, com frequência, uma falha de expressividade do código." Robert Martin não é contra comentários — ele é contra comentários que existem para compensar um código que deveria se explicar sozinho.

O problema real é a **defasagem**. Comentários envelhecem. O código muda, o comentário não. Em pouco tempo, o comentário deixa de descrever o presente e começa a descrever um passado que já não existe — ou pior, descreve algo errado. Quando isso acontece, o comentário não é apenas inútil: ele é ativamente prejudicial.

---

## 2. Conceito Central

Existem dois tipos de comentários:

| Tipo | Descrição | Veredicto |
|---|---|---|
| **Redundante** | Repete o que o código já diz | Remova |
| **Enganoso** | Descreve algo diferente do que o código faz | Remova + corrija o código |
| **Código comentado** | Código morto sem explicação | Remova (use git) |
| **Diário de bordo** | Log de mudanças inline | Remova (use git log) |
| **TODO sem rastreabilidade** | "TODO: melhorar isso" | Reescreva com ticket |
| **Intenção** | Explica o *porquê*, não o *o quê* | Mantenha |
| **Amplificação** | Destaca algo não óbvio que passaria batido | Mantenha |
| **TODO rastreável** | Com ticket, responsável e prazo | Mantenha |
| **Licença/Cabeçalho** | Informação legal obrigatória | Mantenha |

A regra de ouro: **se você pode substituir o comentário por um nome melhor, faça isso**.

---

## 3. O Problema na Prática

```python
# ❌ Comentário redundante
def calcular_total(preco, quantidade):
    # multiplica preço pela quantidade
    total = preco * quantidade
    # retorna o total
    return total

# ❌ Comentário enganoso
def esta_disponivel(produto):
    # retorna True se o produto NÃO estiver disponível
    return produto["estoque"] > 0  # na verdade retorna True quando ESTÁ disponível

# ❌ Código comentado sem contexto
def processar_pagamento(valor, metodo):
    # if metodo == "pix":
    #     taxa = 0.0
    # enviar_para_gateway_antigo(valor)
    ...

# ❌ TODO sem rastreabilidade
def buscar_usuario(usuario_id):
    # TODO: adicionar cache
    # TODO: melhorar isso depois
    ...

# ❌ Diário de bordo
def calcular_imposto(valor_bruto):
    # 12/03/2023 - João alterou a alíquota de 12% para 15%
    # 05/07/2023 - Maria reverteu para 12%
    aliquota = 0.13
    ...
```

> Arquivo completo: [`exemplos/comentarios_ruins.py`](exemplos/comentarios_ruins.py)

---

## 4. A Solução

```python
# ✅ Sem comentário: o nome já diz tudo
def calcular_total(preco: float, quantidade: int) -> float:
    return preco * quantidade

# ✅ Comentário de intenção: explica a REGRA DE NEGÓCIO
PERCENTUAL_RETENCAO_ISS = 2.0

def calcular_valor_liquido(valor_bruto: float) -> float:
    # ISS retido na fonte conforme contrato-padrão (cláusula 7.3, rev. 2025).
    return valor_bruto * (1 - PERCENTUAL_RETENCAO_ISS / 100)

# ✅ TODO rastreável
def buscar_usuario(usuario_id: str) -> dict:
    # TODO [PLAT-1847]: substituir mock por chamada real ao serviço de usuários.
    # Responsável: @ana.souza  |  Prazo: Sprint 42 (2026-05-05)
    return {"id": usuario_id, "nome": "Usuário Mockado"}

# ✅ Amplificação: destaca algo que passaria despercebido
def pode_cancelar_pedido(pedido: dict) -> bool:
    # IMPORTANTE: usamos timezone UTC em ambos os lados intencionalmente.
    # O campo "criado_em" é sempre gravado em UTC no banco para evitar
    # ambiguidade no horário de verão.
    ...
```

> Arquivo completo: [`exemplos/comentarios_bons.py`](exemplos/comentarios_bons.py)

---

## 5. Equivalentes em Outras Linguagens

### PHP

```php
// ❌ PHPDoc redundante
/**
 * Calcula o total.
 * @param float $preco O preço.
 * @param int $quantidade A quantidade.
 * @return float O total.
 */
function calcularTotal(float $preco, int $quantidade): float {
    return $preco * $quantidade;
}

// ✅ PHPDoc que agrega: documenta exceção e restrição de uso
/**
 * Calcula o valor líquido retendo ISS na fonte.
 * Alíquota fixada em 2% conforme contrato-padrão (cláusula 7.3, rev. 2025).
 * Não use para contratos com ISS variável.
 *
 * @throws \InvalidArgumentException se $valorBruto for negativo.
 */
function calcularValorLiquido(float $valorBruto): float { ... }
```

### TypeScript

```typescript
// ❌ JSDoc desnecessário: TypeScript já documenta os tipos
/**
 * @param preco - O preço do produto.
 * @param quantidade - A quantidade.
 * @returns O total calculado.
 */
function calcularTotal(preco: number, quantidade: number): number {
  return preco * quantidade;
}

// ✅ JSDoc útil: explica o comportamento do arredondamento bancário
/**
 * Aplica arredondamento bancário (half-even) ao valor.
 * 2.5 → 2, 3.5 → 4. Neutraliza viés acumulado em grandes volumes.
 */
function aplicarArredondamentoBancario(valor: number): number { ... }
```

### ADVPL/TLPP

```advpl
// ✅ Cabeçalho Protheus.doc (padrão do ecossistema TDS)
/*/{Protheus.doc} CalcularValorLiquido
    Calcula o valor líquido retendo ISS na fonte conforme contrato-padrão.
    A alíquota de 2% está fixada na cláusula 7.3 do contrato modelo (rev. 2025).

    @author  ana.souza
    @since   14/04/2026
    @param   nValorBruto  Numeric  Valor bruto antes da retenção
    @return  Numeric  Valor após dedução do ISS
/*/
Function CalcularValorLiquido( nValorBruto )
    Local nAliquotaISS := 0.02
Return nValorBruto * ( 1 - nAliquotaISS )
```

> **Nota ADVPL/TLPP:** O cabeçalho `{Protheus.doc}` é gerado pelo TDS e deve ser mantido em funções públicas de negócio. Para funções auxiliares, um comentário de intenção simples é suficiente.

> Arquivos completos: [`exemplos/equivalente.php`](exemplos/equivalente.php) · [`exemplos/equivalente.ts`](exemplos/equivalente.ts) · [`exemplos/equivalente.tlpp`](exemplos/equivalente.tlpp)

---

## 6. Regras de Ouro

- **Comentário bom explica o "porquê"** — não o "o quê" nem o "como"; esses devem estar no próprio código
- **Código comentado vai para o lixo** — o histórico está no git; use `git log` ou `git blame`
- **TODO sem ticket é promessa vazia** — inclua sempre o número do ticket, responsável e prazo
- **Comentário enganoso é pior que nenhum** — quando o comentário mente, o leitor perde a confiança em todos os outros
- **Nomes melhores eliminam comentários** — antes de escrever um comentário, pergunte: "posso refatorar o código para dispensá-lo?"

---

## 7. Exercício

**Problema 1 (remover/reescrever):** O arquivo de exercício contém funções com comentários redundantes, enganosos e código comentado. Remova o ruído, reescreva os TODOs com rastreabilidade e, quando necessário, renomeie funções e variáveis para tornar o código autodocumentado.

**Problema 2 (adicionar):** O mesmo arquivo contém uma função de cálculo de parcela de financiamento sem nenhum comentário. A fórmula usada tem nome e contexto específicos que o código não consegue expressar. Adicione o comentário correto.

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

- **Clean Code**, Robert C. Martin — Capítulo 4: *Comments* (p. 53–74)
- **The Art of Readable Code**, Boswell & Foucher — Capítulo 5: *Knowing What to Comment*
- Ferramenta: [`flake8`](https://flake8.pycqa.org/) com plugin `flake8-bugbear` detecta comentários `# noqa` excessivos e blocos de código comentado
- Conceito: `git blame` e `git log -p -- <arquivo>` substituem completamente os diários de bordo inline

---

> **Próximo tutorial:** [Tutorial 04 — Formatação](../../sessao-2/tutorial-04-formatacao/README.md)
