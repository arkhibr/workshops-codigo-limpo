# Tutorial 14 — Testes como Guard-Rails para Mudanças Assistidas

> Referência: Feathers (testes de caracterização) + *Clean Code*, Cap. 9 (Testes)

---

## 1. Contexto e Motivação

A IA acelera mudanças. Em segundos, uma função de cálculo de frete pode ganhar uma nova faixa de peso, um desconto por distância ou uma regra sazonal. O risco não está na velocidade — está em fazer a mudança **sem rede de segurança**.

Sem testes, a IA pode introduzir uma regressão silenciosa: o caso novo funciona, mas um caso antigo que antes retornava 25,00 agora retorna 22,50 e ninguém percebe até o cliente reclamar. Com testes, a regressão é detectada no segundo em que o código muda — antes de chegar à produção.

Este tutorial cobre dois cenários:

1. **Código sem testes:** use *testes de caracterização* para documentar e proteger o comportamento atual antes de deixar a IA mexer.
2. **Código novo:** pratique *TDD assistido* — peça à IA o teste primeiro, depois a implementação.

---

## 2. Conceito Central

### Testes de caracterização

Michael Feathers (em *Working Effectively with Legacy Code*) chama de **testes de caracterização** os testes que descrevem o comportamento atual do código — certo ou errado. O objetivo não é validar que o comportamento é correto; é criar um registro do que o código faz hoje, para que qualquer mudança que altere esse comportamento seja detectada.

O fluxo é simples:

```
1. Rode o código atual → observe as saídas.
2. Escreva verificações que fixam essas saídas.
3. Confirme que todas passam com o código intocado.
4. Só então peça à IA a mudança.
5. Se alguma verificação falhar → a mudança introduziu uma regressão.
```

Neste workshop, a convenção de testes é: funções `verificar_*()` que comparam resultado com valor esperado e imprimem `OK` ou `FALHOU`.

```python
def verificar_frete_ate_5kg() -> None:
    resultado = calcular_frete(peso=3.0, distancia=100)
    esperado = 15.00
    if abs(resultado - esperado) < 0.01:
        print("OK: frete até 5 kg")
    else:
        print(f"FALHOU: frete até 5 kg (esperado {esperado}, obtido {resultado})")
```

A função não usa nenhum framework — apenas `print`. Isso é suficiente para a lição.

### TDD assistido

Em vez de pedir "implemente X", você pede:

> "Primeiro escreva testes que descrevem o comportamento esperado. Depois implemente."

A IA gera as verificações, você as revisa, e só então a implementação nasce sob proteção. O risco do TDD assistido é a IA escrever testes que confirmam o bug — por isso a revisão humana das verificações é obrigatória antes de rodar a implementação.

### O risco do caminho feliz

Suites de teste que cobrem apenas o caso principal dão **falsa sensação de segurança**. Uma função com quatro faixas de peso precisa de verificações para cada faixa — incluindo os limites. Cobrir só a faixa mais comum não detecta regressão nas faixas menos usadas.

O arquivo `frete_gerado.py` ilustra esse risco: a suite fraca passa, mas a regressão na faixa intermediária já está lá.

---

## 3. Exercício

O exercício está em `exercicios/` e tem duas partes:

**Parte estática** (`exercicio.py` / `exercicio.ts`): função `calcular_desconto_fidelidade` com faixas de pontos e **sem nenhum teste**. Sua tarefa:

1. Escreva testes de caracterização do comportamento atual (use a convenção `verificar_*`).
2. Só então peça à IA uma mudança (ex.: nova faixa para clientes acima de 2 000 pontos).
3. Rode os testes antes e depois da mudança — confirme que nenhum foi quebrado.

```bash
# Veja o comportamento atual:
python3 sessao-6/tutorial-14-testes-guard-rails/exercicios/exercicio.py

# Compare com a solução de referência:
python3 sessao-6/tutorial-14-testes-guard-rails/exercicios/gabarito.py
```

**Parte hands-on** (`roteiro-ia.md`): roteiro passo a passo com prompts prontos para cada etapa.

> Arquivo: [`exercicios/exercicio.py`](exercicios/exercicio.py) · [`exercicios/exercicio.ts`](exercicios/exercicio.ts)
> Gabarito: [`exercicios/gabarito.py`](exercicios/gabarito.py) · [`exercicios/gabarito.ts`](exercicios/gabarito.ts)
> Revisão comentada: [`exercicios/gabarito_revisao.md`](exercicios/gabarito_revisao.md)
> Roteiro hands-on: [`exercicios/roteiro-ia.md`](exercicios/roteiro-ia.md)

---

## 4. Checklist — Guard-Rails para Mudanças Assistidas

Use estas perguntas antes de aceitar qualquer mudança gerada por IA:

1. **Havia testes antes da mudança?** — Se não, você caracterizou o comportamento atual antes de deixar a IA mexer?
2. **Você cobriu todas as faixas?** — A suite inclui cada ramo de decisão e os valores-limite de cada faixa?
3. **Os testes pegam regressão?** — Rode a suite com uma mudança deliberadamente errada: ela falha?
4. **A IA testou o comportamento certo?** — Revise as verificações geradas: elas descrevem o que você quer, não apenas o que o código já faz (incluindo bugs)?
5. **Você rodou antes e depois?** — Uma suite que passa com o código original E depois da mudança dá confiança real.
6. **O caminho infeliz está coberto?** — Casos de borda (peso zero, limite exato de faixa, valor negativo) estão entre as verificações?

---

## 5. Referências

- **Working Effectively with Legacy Code**, Michael C. Feathers — Capítulo 13: *I Need to Make a Change but I Don't Know What Tests to Write* (testes de caracterização)
- **Clean Code**, Robert C. Martin — Capítulo 9: *Unit Tests* (p. 121–133)
- Arquivos de exemplo: [`exemplos/prompt.md`](exemplos/prompt.md) · [`exemplos/frete_gerado.py`](exemplos/frete_gerado.py) · [`exemplos/frete_revisado.py`](exemplos/frete_revisado.py)

---

> **Próximo tutorial:** [Tutorial 15 — Manutenibilidade e Agentes de IA](../tutorial-15-manutenibilidade-agentes/README.md)
