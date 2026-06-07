# Gabarito de Revisão — Exercício: Frete no Carrinho

## A inconsistência cross-file

**Tarefa solicitada ao agente:** "Adicionar cálculo de frete ao pedido. Atualizar
a precificação e todos os chamadores."

O agente atualizou `exercicio_precificacao.py/.ts` corretamente: a função
`calcular_total_pedido` / `calcularTotalPedido` passou a exigir `regiao` como
segundo argumento obrigatório.

O agente adicionou o campo `regiao` ao `Pedido` e criou `definir_regiao` /
`definirRegiao` em `exercicio_carrinho.py/.ts` — tudo isso correto.

**O que o agente esqueceu:** atualizar `fechar_pedido` / `fecharPedido`.

### Onde está a inconsistência

```
exercicio_precificacao.py:
  def calcular_total_pedido(itens, regiao)     ← exige 2 argumentos

exercicio_carrinho.py:
  def fechar_pedido(pedido):
      total = _calcular_total_local(pedido.itens)   ← usa versão antiga (1 arg)
```

```
exercicio_precificacao.ts:
  function calcularTotalPedido(itens, regiao)  ← exige 2 argumentos

exercicio_carrinho.ts:
  function fecharPedido(pedido):
      total = _calcularTotalLocal(pedido.itens)  ← usa versão antiga (1 arg)
```

### Por que passa despercebida arquivo por arquivo

- **Em `exercicio_precificacao.py`:** a função está correta; o arquivo roda sem erro.
- **Em `exercicio_carrinho.py`:** `fechar_pedido` usa `_calcular_total_local` (uma
  cópia local sem frete), então o arquivo também roda sem erro.
- O campo `regiao` aparece no dict de retorno de `fechar_pedido`, sugerindo
  que a região está sendo considerada — mas o `total` ao lado foi calculado sem frete.

### Consequência

Em produção, `fechar_pedido` retornaria o total **sem frete**, mesmo para pedidos
com região definida. O cupom / a região estão no objeto `Pedido` mas o desconto
nunca chega ao cálculo. A discrepância financeira afeta todos os pedidos.

---

## A correção (uma linha)

### Python

```python
# exercicio_carrinho.py → fechar_pedido:

# ANTES (incorreto):
total = _calcular_total_local(pedido.itens)

# DEPOIS (correto):
resultado = calcular_total_pedido(pedido.itens, pedido.regiao)
total = resultado.total
frete = resultado.frete
```

E atualizar o dict de retorno para incluir `subtotal`, `frete` e `total`:

```python
return {
    "pedido_id": pedido.id,
    "qtd_itens": sum(i.quantidade for i in pedido.itens),
    "regiao":    resultado.regiao,
    "subtotal":  resultado.subtotal,
    "frete":     resultado.frete,
    "total":     resultado.total,
}
```

### TypeScript

```typescript
// exercicio_carrinho.ts → fecharPedido:

// ANTES (incorreto):
const total = _calcularTotalLocal(pedido.itens);

// DEPOIS (correto):
const resultado = calcularTotalPedido(pedido.itens, pedido.regiao);
// resultado já contém subtotal, frete, total, regiao
```

---

## Perguntas do checklist que detectariam a inconsistência

- **"A assinatura mudou e todos os chamadores acompanharam?"**
  — `calcular_total_pedido` ganhou `regiao`; `fechar_pedido` não foi atualizado.

- **"Campo novo → lógica nova?"**
  — `Pedido.regiao` foi adicionado; `fechar_pedido` usa o campo no dict de retorno
    mas não o passa para a função de cálculo.

- **"Rodei os dois arquivos JUNTOS após a mudança?"**
  — Cada arquivo roda isoladamente; o bug só aparece no fluxo integrado.

- **"A mudança ficou coesa entre arquivos?"**
  — Não: `precificacao` foi atualizado; `carrinho` não propagou a mudança até o cálculo.

---

## Comparação exercício vs. gabarito

```bash
python3 sessao-5/tutorial-19-multiarquivo-agentes/exercicios/exercicio_carrinho.py
python3 sessao-5/tutorial-19-multiarquivo-agentes/exercicios/gabarito_carrinho.py
```

No exercício: `Total: R$ 189.70` (sem frete nordeste de R$ 29.90).
No gabarito:  `Total: R$ 219.60` (com frete nordeste de R$ 29.90).

A diferença de R$ 29,90 é o frete que estava definido no pedido mas nunca foi calculado.
