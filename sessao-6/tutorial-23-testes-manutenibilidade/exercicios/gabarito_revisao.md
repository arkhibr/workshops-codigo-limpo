# Gabarito — Revisão de Testes de Caracterização

Este arquivo explica quais casos precisam ser caracterizados, por que mid-band
é insuficiente e qual regressão a suite completa detectaria no output de `frete_gerado.py`.

---

## Por que mid-band não é suficiente

Testar apenas valores no meio de cada faixa (5 kg, 8 kg, 15 kg) verifica se a
lógica principal existe — mas não verifica onde ela termina. Uma mudança que
desloca `<= 10` para `< 10` produz exatamente o mesmo resultado para 5 kg e 8 kg:
ambos ainda caem na faixa padrão. O erro fica escondido no único ponto que não
foi testado: a fronteira exata.

```
Faixa padrão correta:  2 kg < peso <= 10 kg
Faixa padrão gerada:   2 kg < peso < 10 kg   ← erro de fronteira

peso = 8 kg  → ambas retornam TARIFA_PADRAO (25.00 + distância) — OK para os dois
peso = 10 kg → correta: TARIFA_PADRAO; gerada: TARIFA_MEDIA    — FALHOU só no completo
```

O princípio se generaliza: **qualquer deslocamento de fronteira é invisível para
uma suite que não inclui o valor exato da fronteira**.

---

## Quais casos caracterizar — regra geral

Para uma função com `N` faixas separadas por `N-1` fronteiras:

| Tipo de caso         | Por quê incluir                                                   |
|----------------------|-------------------------------------------------------------------|
| Mid-band de cada faixa | Confirma que a lógica principal da faixa existe                 |
| Valor exato de cada fronteira | Detecta deslocamentos (< vs <=)                          |
| Valor imediatamente acima de cada fronteira | Confirma a faixa seguinte        |
| Zero e negativo      | Garante que a validação de entrada está presente                  |

Para `calcular_frete` com as 4 faixas (leve, padrão, intermediária, pesada):

```
Fronteiras: 2 kg, 10 kg, 20 kg

Casos mínimos para suite completa:
  faixa leve:          1.0, 2.0 (borda)
  transição leve→padrão: 2.1
  faixa padrão:        5.0, 8.0, 10.0 (borda crítica)
  transição padrão→intermediária: 10.1
  faixa intermediária: 15.0, 20.0 (borda)
  transição intermediária→pesada: 20.1
  faixa pesada:        25.0
  inválidos:           0.0, -1.0
```

---

## A regressão que a suite completa detectaria

`frete_gerado.py` usa `peso_kg < 10.0` na segunda condição (em vez de `<= 10.0`).
O efeito prático:

| Peso (kg) | Frete correto (frete_revisado) | Frete gerado (frete_gerado) | Diferença |
|-----------|--------------------------------|-----------------------------|-----------|
| 9.9       | R$ 33,00 (padrão + 100 km)    | R$ 33,00 (padrão)           | nenhuma   |
| **10.0**  | **R$ 33,00 (padrão)**         | **R$ 53,00 (intermediária)**| **R$ 20,00 a mais** |
| 10.1      | R$ 53,00 (intermediária)      | R$ 53,00 (intermediária)    | nenhuma   |

O cliente com uma encomenda de exatamente 10 kg paga R$ 20,00 a mais do que deveria.
Isso não aparece em logs de erro, não levanta exceção e não afeta nenhum caso da suite fraca.

A suite completa de `frete_revisado.py` inclui:

```python
(10.0, 100, False, 33.00, "10 kg, 100 km — borda SUPERIOR faixa padrão (fronteira crítica)"),
```

Rodando esse caso contra `frete_gerado.py`:
```
FALHOU: 10 kg, 100 km — borda SUPERIOR faixa padrão (fronteira crítica)
        (esperado 33.00, obtido 53.00)
```

A regressão aparece de forma explícita, com o valor esperado e o obtido.

---

## Passo a passo da detecção e correção

**Passo 1 — Escrever a suite antes da mudança:**
Rode `frete_revisado.py` (ou escreva a suite contra o código original).
Confirme que todos os casos passam — incluindo `10.0 kg`.

**Passo 2 — Pedir a mudança ao agente:**
"Adicione a faixa carga pesada: acima de 20 kg, tarifa_base = 80.00."

**Passo 3 — Rodar a suite contra o output:**
Se o modelo deslocou a fronteira, o caso `10.0 kg` vai falhar com:
`FALHOU: 10 kg, 100 km — esperado 33.00, obtido 53.00`

**Passo 4 — Identificar a causa no diff:**
```diff
-    elif peso_kg <= 10.0:
+    elif peso_kg < 10.0:
```
Uma linha. Um caractere. R$ 20,00 a mais por envio.

**Passo 5 — Corrigir e re-rodar:**
Restaurar `<= 10.0` e confirmar que todos os casos voltam a passar.

---

## Lição principal

A suite fraca de `frete_gerado.py` imprime todos os `OK` — porque ela não inclui
o valor de fronteira. Isso cria uma falsa sensação de que o output está correto.

A suite completa de `frete_revisado.py` inclui a fronteira exata — e seria suficiente
para detectar a regressão antes do commit. O tempo de escrita da suite completa
(adicionar 4 casos de borda) é menor do que o tempo de investigar um bug de cobrança
incorreta em produção.

A Regra do Escoteiro aplicada a agentes: **deixe o código com mais testes do que
encontrou — especialmente antes de pedir qualquer mudança**.
