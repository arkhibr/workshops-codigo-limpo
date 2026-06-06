# Revisão do Gabarito — Tutorial 14

## Quais casos caracterizar

Para uma função com N faixas baseadas em um valor numérico, a suite mínima cobre:

| Tipo de caso | Exemplo no exercício | Por que incluir |
|---|---|---|
| Caso típico de cada faixa | 100 pts, 750 pts, 1.500 pts, 2.500 pts | Garante que o comportamento central de cada faixa está correto |
| Limite inferior de cada faixa | 500 pts, 1.000 pts, 2.000 pts (exatos) | Off-by-one em `<` vs `<=` é a causa mais comum de regressão em faixas |
| Valor imediatamente abaixo do limite | 499 pts, 999 pts, 1.999 pts | Confirma que o valor ainda pertence à faixa anterior |
| Borda do domínio | 0 pts, valorCompra = 0 | Garante comportamento previsível em entradas extremas |

A regra prática: **um caso típico por faixa + os dois lados de cada limite.**

---

## Por que o caminho feliz não basta

A função `calcular_desconto_fidelidade` original tinha três faixas. Um desenvolvedor apressado escreveria três testes — um para cada faixa com um valor "no meio". Isso passa facilmente.

O problema: quando a IA adiciona a faixa de 2.000+ pontos, ela precisa introduzir um novo `elif pontos < 2000` antes do `else`. Se errar o valor — escrevendo `elif pontos < 1000` em vez de `elif pontos < 2000` — a faixa prata desaparece silenciosamente para clientes com 1.000–1.999 pontos. Um teste que usa apenas `pontos=1500` para a faixa prata detectaria isso imediatamente. Um teste que usa apenas `pontos=750` (bronze) passaria sem perceber.

**Resumo:** testes no meio da faixa protegem o centro; testes nos limites protegem as bordas — que são exatamente onde regressões acontecem.

---

## A regressão que os testes pegam

No exercício, a mudança assistida pode introduzir o seguinte erro típico:

```python
# Antes (correto):
elif pontos < 1000:
    percentual = DESCONTO_BRONZE

# Depois (com regressão — limite da prata errado):
elif pontos < 1000:
    percentual = DESCONTO_BRONZE
elif pontos < 1000:   # duplicado ou valor errado
    percentual = DESCONTO_PRATA
else:
    percentual = DESCONTO_OURO
```

Ou, mais sutilmente:

```python
# Faixa prata com limite errado (1.500 em vez de 2.000):
elif pontos < 1500:
    percentual = DESCONTO_PRATA
else:
    percentual = DESCONTO_OURO   # clientes com 1.500–1.999 pts recebem 25% indevidamente
```

As verificações `verificar_limite_superior_prata` (1.999 pts → 10%) e `verificar_limite_inferior_ouro_exato` (2.000 pts → 25%) detectam essa regressão imediatamente.

---

## Lição central

A IA não conhece o seu contrato. Ela implementa o que o prompt descreve e pode alterar silenciosamente o comportamento de faixas não mencionadas. Os testes de caracterização são o contrato escrito em código — e a IA deve respeitar esse contrato tanto quanto qualquer desenvolvedor humano.

Fluxo recomendado:

```
1. Escreva os verificar_* → rode → confirme que todos imprimem OK
2. Peça a mudança à IA
3. Rode novamente → qualquer FALHOU é uma regressão a corrigir
4. Só aceite o código quando todos voltarem a OK
```
