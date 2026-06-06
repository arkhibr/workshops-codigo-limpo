# Exemplos de Prompt — Testes de Caracterização vs Mudança Direta

---

## Prompt fraco: mudança sem proteção

```
Adiciona uma nova faixa de peso para frete entre 10 kg e 20 kg,
com valor de R$ 0,90 por kg mais R$ 5,00 fixo.
```

**O que acontece:**
A IA implementa a nova faixa. Ela pode funcionar perfeitamente para o caso novo. Mas uma faixa existente pode ter sido silenciosamente alterada — por um off-by-one nos limites, por uma reordenação de condicionais, ou simplesmente por um erro de transcrição. Sem testes, essa regressão só aparece quando um cliente recebe o valor errado.

---

## Prompt forte: caracterização antes da mudança

```
Antes de qualquer alteração, escreva testes de caracterização da
função calcular_frete(peso, distancia) usando a convenção verificar_*:
funções que imprimem "OK: <caso>" ou "FALHOU: <caso> (esperado X, obtido Y)".

Cubra cada faixa de peso existente com pelo menos um caso típico e
um valor no limite da faixa.

Só depois que eu confirmar que todos os testes passam com o código
atual, implemente a nova faixa (10–20 kg: R$ 0,90/kg + R$ 5,00 fixo).
```

**O que muda:**
1. A IA produz as verificações primeiro — você as revisa antes de aceitar.
2. Você roda o arquivo com o código atual: todos os `verificar_*` devem imprimir OK.
3. Você aceita a mudança.
4. Você roda novamente: se algum `verificar_*` imprimir FALHOU, a regressão foi capturada antes de entrar na base.

---

## Por que o prompt fraco é arriscado

O prompt fraco não é errado — ele descreve o que você quer. O problema é que ele pede **resultado** sem pedir **proteção**. A IA não sabe o que você considera correto para os casos já existentes. Ela otimiza para o caso descrito no prompt e pode introduzir efeitos colaterais que só aparecem em produção.

A regra prática: **nunca peça à IA uma mudança em código sem testes antes de ter uma suite de caracterização passando.**

---

## Prompt para TDD assistido (código novo)

```
Vou implementar calcular_frete(peso, distancia) com estas faixas:
  - até 5 kg: R$ 2,00/kg
  - 5,01–10 kg: R$ 1,80/kg + R$ 3,00
  - acima de 10 kg: R$ 1,50/kg + R$ 5,00
Multiplica pela distância (em km) dividida por 100.

Passo 1: escreva apenas os testes verificar_* para todas as faixas e
bordas (peso=0, exatamente 5 kg, exatamente 10 kg, peso muito alto).
Passo 2 (só depois da minha confirmação): implemente a função.
```

**Resultado esperado:** a função nasce já protegida, e a revisão das verificações acontece antes de qualquer implementação.
