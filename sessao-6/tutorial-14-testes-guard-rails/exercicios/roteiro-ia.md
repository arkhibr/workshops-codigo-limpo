# Roteiro Hands-on — Testes de Caracterização com IA

**Arquivo de trabalho:** `exercicios/exercicio.py` (ou `.ts`)
**Objetivo:** escrever testes de caracterização ANTES de pedir uma mudança à IA,
e confirmar que nenhum teste quebra após a mudança.

---

## Etapa 1 — Peça os testes de caracterização à IA

Cole o conteúdo de `exercicio.py` no assistente e use este prompt:

```
Dado o código abaixo, escreva testes de caracterização usando a
convenção verificar_*: funções Python que comparam o resultado com
um valor esperado e imprimem "OK: <caso>" ou
"FALHOU: <caso> (esperado X, obtido Y)".

Cubra:
  - um caso típico para cada faixa de desconto
  - o valor exato de cada limite de faixa (499, 500, 999, 1.000)
  - valor de compra zero

Não altere a implementação — apenas escreva as verificações.
[cole o código aqui]
```

---

## Etapa 2 — Rode os testes com o código original

Adicione as funções `verificar_*` geradas ao arquivo e chame-as no `if __name__ == "__main__"`. Rode:

```bash
python3 sessao-6/tutorial-14-testes-guard-rails/exercicios/exercicio.py
```

**Critério de aceite:** todas as linhas imprimem `OK`. Se alguma imprimir `FALHOU`, revise o esperado — pode ser que a IA tenha usado um valor incorreto, ou que você tenha que ajustar o expected para o comportamento real atual (é isso que "caracterização" significa).

---

## Etapa 3 — Peça a mudança à IA

Agora que a suite está verde, peça a mudança com as verificações já no contexto:

```
O código abaixo já tem testes de caracterização que passam.
Adicione uma nova faixa: clientes com 2.000 ou mais pontos recebem
25% de desconto.

Não quebre nenhuma verificação existente. Após a mudança, todas
ainda devem imprimir OK.
[cole o código com as verificações]
```

---

## Etapa 4 — Rode os testes depois da mudança

Substitua a implementação pelo código gerado pela IA (mantenha suas verificações). Rode novamente:

```bash
python3 sessao-6/tutorial-14-testes-guard-rails/exercicios/exercicio.py
```

**Se todos imprimirem OK:** a mudança foi integrada sem regressão.

**Se algum imprimir FALHOU:** a IA introduziu uma regressão. Leia a mensagem de falha — ela indica qual caso e qual valor está errado. Corrija o código antes de aceitar.

---

## Etapa 5 (opcional) — Compare com o gabarito

```bash
python3 sessao-6/tutorial-14-testes-guard-rails/exercicios/gabarito.py
```

O gabarito inclui verificações adicionais nos limites superiores de cada faixa e na nova faixa ouro. Compare com o que a IA gerou — quais bordas ela cobriu? Quais ela ignorou?

---

## Fallback sem IA

Se preferir trabalhar diretamente no código:

1. Leia o comportamento atual em `exercicio.py` (coluna "Comportamento atual").
2. Escreva as verificações manualmente — use os valores da tabela de casos do arquivo.
3. Adicione a nova faixa ouro (2.000+ pts → 25%) à implementação.
4. Rode e confirme que todas as verificações imprimem OK.
5. Confira com `gabarito.py`.

---

## Nota sobre TDD assistido

Se o projeto ainda não tiver implementação, inverta a ordem:

1. Descreva o comportamento esperado no prompt.
2. Peça à IA **apenas os testes** primeiro.
3. Revise as verificações — elas descrevem o que você quer?
4. Só então peça a implementação.

O risco de pular essa ordem: a IA escreve testes que confirmam a implementação incorreta, e todos passam — inclusive os bugs.
