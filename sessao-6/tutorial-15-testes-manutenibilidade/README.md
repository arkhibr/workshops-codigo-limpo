# Tutorial 15 — Testes como guard-rails e manutenibilidade

> Referência: Feathers (testes de caracterização) + *Clean Code*, Cap. 9; Regra do Escoteiro.

---

## 1. Contexto e Motivação

O Tutorial 13 mostrou como um agente de IA pode refatorar código legado em várias etapas
coordenadas. O Tutorial 15 endereça o risco adjacente: o que acontece quando você pede a
uma mudança localizada — adicionar uma faixa de peso, um novo desconto, uma nova categoria —
e confia que o modelo não vai tocar o comportamento existente?

Em 2026, Claude Opus 4.8, Codex e Gemini CLI produzem código polido, tipado e bem nomeado.
Não deixam `except: pass` nem variáveis de letra única. O perigo é diferente: ao estender
uma função com uma nova faixa, o modelo pode reposicionar silenciosamente a fronteira entre
duas faixas existentes — um `<= 10` que vira `< 10`, por exemplo — e nenhuma das verificações
do mid-band (5 kg, 8 kg, 15 kg) vai capturar isso.

O resultado é um sistema que parece correto porque a suite fraca imprime todos os `OK`.
A regressão fica invisível até o cliente da faixa de exatamente 10 kg reclamar do desconto
errado ou do frete mais barato do que deveria ser.

> *"Before you change legacy code, write tests that characterize what the code actually does —
> not what you think it does."*
>
> — Michael Feathers, *Working Effectively with Legacy Code*

O princípio se aplica diretamente ao fluxo de trabalho com IA: antes de pedir a mudança,
escreva os testes de caracterização. Depois de receber o output, rode-os novamente.
Se algum falhar, o agente introduziu uma regressão — mesmo que o código pareça correto.

---

## 2. Conceito Central

### Testes de caracterização

Um teste de caracterização não verifica o que o código *deveria* fazer — verifica o que
ele *faz hoje*. O objetivo inicial é documentar o comportamento existente antes de qualquer
mudança. Depois da mudança, o mesmo teste serve para detectar regressões.

A convenção usada neste workshop é a função `verificar_*()` com `print("OK: <caso>")` ou
`print("FALHOU: <caso> (esperado X, obtido Y)")`. Sem frameworks. Sem decoradores.
O feedback é imediato no terminal.

```python
def verificar_frete_faixa_media() -> None:
    """Casos mid-band: confirma o comportamento atual para pesos dentro de cada faixa."""
    casos = [
        (5.0,  100, 25.00, "5 kg, 100 km"),
        (8.0,  100, 25.00, "8 kg, 100 km"),
        (15.0, 100, 45.00, "15 kg, 100 km"),
    ]
    for peso, distancia, esperado, descricao in casos:
        obtido = calcular_frete(peso, distancia)
        if abs(obtido - esperado) < 0.001:
            print(f"OK: {descricao}")
        else:
            print(f"FALHOU: {descricao} (esperado {esperado:.2f}, obtido {obtido:.2f})")
```

Esta suite cobre o mid-band. **Não cobre as bordas.** Uma mudança que desloca `<= 10` para
`< 10` passa nela sem falhar — porque 8 kg e 15 kg não tocam a fronteira entre as faixas.

### O risco da suite que o agente escreve para você

Pedir ao agente que "escreva os testes antes de fazer a mudança" é um passo na direção
certa — mas tem uma armadilha: o modelo pode escrever testes que caracterizam o *código
novo* (já com a regressão) em vez do *código original*. O resultado é uma suite que
confirma a regressão como se fosse o comportamento correto.

A sequência segura é:

1. **Você** escreve os testes de caracterização (ou revisa os que o agente escreve)
   contra o código original.
2. Você roda a suite e confirma que todos passam.
3. Você pede a mudança ao agente.
4. Você roda a suite novamente contra o output do agente.
5. Se algo falhar, a mudança introduziu regressão — rejeite ou corrija.

### Revisar o diff, não só o output

Mesmo com uma suite de caracterização, revise o diff linha a linha após receber a mudança.
Um deslocamento de fronteira de `<= 10` para `< 10` ocupa uma única posição num `if` —
é invisível numa leitura rápida do output completo, mas é imediatamente visível num `git diff`.

### Regra do Escoteiro com agentes

A Regra do Escoteiro diz: deixe o código melhor do que encontrou. Com agentes, o risco
é o inverso: o agente pode deixar o comportamento *diferente* do que encontrou sem avisar.
Testes de caracterização antes da mudança são o mecanismo de verificação que garante que
"melhorar" não silenciosamente significa "alterar".

---

## 3. Exercício

O arquivo `exercicios/exercicio.py` (e o equivalente `.ts`) contém uma função
`calcular_desconto_fidelidade(meses_cliente, valor_compra)` com faixas de desconto
e **nenhum teste de caracterização**.

**Tarefa:**

1. Escreva os testes de caracterização incluindo **exatamente os valores de borda** entre
   as faixas — não apenas os valores mid-band. Confirme que todos passam com o código atual.
2. Use `exemplos/prompt.md` para pedir ao seu modelo preferido que adicione uma nova faixa
   de fidelidade (clientes com mais de 36 meses).
3. Rode sua suite de caracterização contra o output recebido. Se algum caso falhar, a mudança
   introduziu regressão — use o relatório para corrigir o agente.

O gabarito em `exercicios/gabarito.py` mostra a suite completa com bordas e a nova faixa
adicionada corretamente, com todos os casos passando.

---

## 4. Checklist

Antes de aceitar qualquer output de IA que muda código com faixas ou condicionais:

- [ ] Você escreveu (ou revisou) os testes de caracterização **antes** de pedir a mudança?
- [ ] A suite cobre os valores de **borda exatos** entre faixas, não apenas os mid-band?
- [ ] O agente escreveu testes que validam o comportamento **original** (não o novo)?
- [ ] Você rodou a suite contra o output e todos os casos passaram?
- [ ] Você revisou o **diff** linha a linha para detectar deslocamentos de fronteira?
- [ ] O agente adicionou alguma **dependência nova** desnecessária?

---

## 5. Referências

- Michael Feathers — *Working Effectively with Legacy Code*, Cap. 13 (Characterization Tests)
- Robert C. Martin — *Clean Code*, Cap. 9 (Unit Tests)
- `exemplos/frete_gerado.py` — suite fraca que não detecta a regressão de fronteira
- `exemplos/frete_revisado.py` — suite completa com bordas que detecta e confirma a correção
- `exercicios/gabarito_revisao.md` — análise dos casos que precisam de caracterização e por quê
