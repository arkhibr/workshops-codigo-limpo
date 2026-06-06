# Tutorial 13 — Refatoração assistida avançada

> Referência: Feathers (preservar comportamento) + refatoração assistida por modelos de fronteira

---

## 1. Contexto e Motivação

Em 2026, modelos de fronteira executam refatorações estruturais com qualidade
alta: extraem métodos, migram if/elif para tabelas, renomeiam identificadores,
reorganizam módulos. O resultado é idiomático, bem tipado e legível.

O problema não está na qualidade técnica da refatoração — está na verificação
do comportamento depois de feita. Uma refatoração estrutural *parece* preservar
o comportamento. Muitas vezes preserva. E às vezes não preserva — especialmente
nos **limites exatos** de faixas e condições.

> *"The fundamental question is: how do we know that our changes don't break
> anything? The key is feedback. We need to know what the software is supposed to
> do, and we need to detect when we change that."*
> — Michael Feathers, *Working Effectively with Legacy Code*, Cap. 2

O fragmento abaixo ilustra o ponto crítico. Original:

```python
def calcular_comissao_original(venda: Venda) -> float:
    if venda.valor >= 10_000:
        return venda.valor * 0.06
    elif venda.valor >= 5_000:
        return venda.valor * 0.04
    ...
```

Refatoração gerada pela IA — idiomática, limpa, mas com um operador diferente:

```python
def calcular_comissao_refatorada(venda: Venda) -> float:
    for faixa in TABELA_COMISSAO:
        if venda.valor > faixa.limite_inferior:   # ← '>' em vez de '>='
            return venda.valor * faixa.percentual
    ...
```

Para `valor = 15.000`: ambas retornam 6% — sem diferença.
Para `valor = 10.000`: original retorna 6% (`>= 10.000`); refatorada retorna 4%
(`10.000 > 10.000` é falso, cai para a faixa abaixo). A regressão é silenciosa.

---

## 2. Conceito Central

### Refatoração assistida em passos verificáveis

Uma refatoração maior executada com IA deve seguir três etapas — e a verificação
acontece na terceira, não depois da integração:

```
1. Declara a estratégia    → o modelo descreve o que vai mudar e como
2. Gera o diff             → apenas a transformação estrutural
3. Verifica equivalência   → compara original vs. refatorado em todos os casos
```

A etapa 1 é onde a regressão pode ser detectada mais barato: se o modelo
declarar `>` em vez de `>=`, você corrige antes de ver qualquer código.

---

### Por que as bordas são o ponto crítico

Para qualquer refatoração de if/elif para tabela:

- Casos no **interior** das faixas: `>` e `>=` produzem o mesmo resultado.
- Casos nos **limites exatos**: `>` faz o valor cair para a faixa abaixo.

A verificação fraca (só interior) passa em ambas as versões — certa e errada.
A verificação completa (inclui bordas) detecta a divergência imediatamente.

```python
# Verificação fraca — passa em ambas as versões (esconde a regressão)
casos = [Venda("V1", 1_000), Venda("V2", 7_500), Venda("V3", 15_000)]

# Verificação completa — detecta a regressão
casos += [
    Venda("limite", 5_000),   # >= 5000 → 4%  vs.  > 5000 → 2%  ← FALHOU
    Venda("limite", 10_000),  # >= 10000 → 6%  vs.  > 10000 → 4%  ← FALHOU
]
```

---

### A função `verificar_equivalencia` como contrato

A forma mais prática de fechar o contrato de uma refatoração é uma função
que compara o original e o refatorado ponto a ponto, incluindo as bordas:

```python
def verificar_equivalencia() -> None:
    casos = [
        # interior das faixas
        Venda("interior", 7_500),
        # limites exatos — críticos
        Venda("limite",   5_000),
        Venda("limite",  10_000),
        # logo abaixo dos limites
        Venda("abaixo",   4_999),
        Venda("abaixo",   9_999),
    ]
    for venda in casos:
        esperado = calcular_comissao_original(venda)
        obtido   = calcular_comissao_refatorada(venda)
        if abs(obtido - esperado) < 0.001:
            print(f"OK: {venda.vendedor_id}  valor={venda.valor}  comissão={obtido:.2f}")
        else:
            print(f"FALHOU: {venda.vendedor_id}  esperado={esperado:.2f}  obtido={obtido:.2f}")
```

Esta função é o que `comissao_revisado.py` tem e `comissao_gerado.py` não tem.
A diferença não é a função em si — é a inclusão dos **limites exatos** como casos.

---

## 3. Exercício

**Contexto:** o arquivo `exercicios/exercicio.py` (e `.ts`) contém um módulo
de cálculo de bônus por meta de vendas, com uma refatoração gerada por IA —
idiomática e com uma verificação que passa. Mas a verificação é fraca: não
inclui os limites exatos de atingimento (80%, 100%, 120%).

**Tarefas:**

1. Execute o exercício e observe o resultado:
   ```bash
   python3 sessao-6/tutorial-13-refatoracao-avancada/exercicios/exercicio.py
   ```

2. Complete a função `verificar_equivalencia` incluindo os limites exatos
   de atingimento: `[0.80, 1.00, 1.20]` e os valores logo abaixo:
   `[0.799, 0.999, 1.199]`.

3. Rode a verificação e identifique qual caso de borda regrediu.

4. Corrija a refatoração (`calcular_bonus_refatorado`) para preservar o
   comportamento original, e rode de novo até todas as linhas serem `OK:`.

**Referência:** `exercicios/gabarito.py` contém a verificação completa e a
correção. `exercicios/gabarito_revisao.md` detalha o caso de borda quebrado
e a sequência de passos.

---

## 4. Checklist — Refatoração assistida com preservação de comportamento

Use estas perguntas antes de integrar qualquer refatoração gerada por IA:

- [ ] Defini o **comportamento a preservar** — especialmente nos limites de faixas?
- [ ] Pedi ao modelo que declarasse a **estratégia e o operador** de comparação antes do código?
- [ ] A **verificação de equivalência** inclui os **limites exatos** de cada faixa?
- [ ] Rodei a verificação contra a versão original **e** contra a refatorada?
- [ ] Qualquer `FALHOU:` foi investigado e corrigido antes de integrar?
- [ ] O diff entre original e refatorado está **restrito à transformação estrutural** — sem mudança de lógica?

---

## 5. Referências

- Feathers, Michael. *Working Effectively with Legacy Code*. Cap. 2 — Working with Feedback.
- Martin, Robert C. *Clean Code: A Handbook of Agile Software Craftsmanship*. Cap. 5.
- Documentação Claude Code: [Claude Code e CLAUDE.md](https://docs.anthropic.com/claude-code)
- OpenAI Codex: [AGENTS.md e system instructions](https://platform.openai.com/docs/agents)
- Gemini CLI: [GEMINI.md e system instructions](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- Exemplos do repositório:
  - `sessao-6/tutorial-13-refatoracao-avancada/exemplos/prompt.md`
  - `sessao-6/tutorial-13-refatoracao-avancada/exemplos/comissao_revisado.py`
  - `sessao-6/tutorial-13-refatoracao-avancada/exercicios/gabarito_revisao.md`
