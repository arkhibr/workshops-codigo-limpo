# Tutorial 12 — Strategy e Template Method

> Referência: Gang of Four, *Design Patterns*, Cap. 5 — Behavioral Patterns

## 1. Contexto e Motivação

Dois padrões para eliminar duplicação e tornar o código extensível sem alterar o que já funciona.

## 2. Strategy

**Problema:** `if/elif` que cresce a cada novo algoritmo. Adicionar "MEI" exige alterar `calcular_imposto()`.

**Solução:** Encapsule cada variante em uma classe com a mesma interface. O "calculador" recebe a estratégia — não sabe qual é.

**Quando usar:**
- Vários algoritmos intercambiáveis para o mesmo problema (impostos, frete, descontos, ordenação)
- Precisa trocar o algoritmo em runtime
- Quer adicionar variantes sem alterar o código existente (OCP)

**Quando NÃO usar:**
- Apenas 2 variantes que nunca mudarão — if/else é suficiente
- A variante é determinada por dados simples que não têm comportamento associado

## 3. Template Method

**Problema:** Duas classes com o mesmo esqueleto de 4 etapas, diferindo apenas em 1 etapa. Qualquer fix em "filtrar" precisa ser replicado.

**Solução:** Extraia o esqueleto para uma classe base abstrata. As subclasses sobrescrevem APENAS as etapas variáveis.

**Quando usar:**
- Processo com etapas fixas e pelo menos uma etapa variável por subtipo
- Quer garantir que o esqueleto não seja acidentalmente alterado (declare `gerar()` como `final` em PHP)

**Quando NÃO usar:**
- Apenas uma subclasse — use a classe concreta diretamente
- Variação é melhor capturada por composição (prefira Strategy nesse caso)

## 4. Strategy vs Template Method

| Dimensão | Strategy | Template Method |
|----------|----------|-----------------|
| Mecanismo | Composição (objeto injetado) | Herança (subclasse) |
| Variação | Algoritmo inteiro | Etapas específicas |
| Runtime | Troca em runtime possível | Fixo em compile-time |
| ADVPL | Codeblock | Codeblock de etapa |

## 5. Exercício

Domínio: logística de entregas.

**`exercicios/exercicio.py`** — `calcular_frete()` com if/elif de transportadoras + `RelatorioEntregas`/`RelatorioColetas` com esqueleto de 4 etapas duplicado.

**Objetivo:** Refatorar para Strategy (frete) + Template Method (relatórios).

## 6. Checklist

- [ ] Identifiquei o if/elif que pode virar Strategy
- [ ] Criei o protocolo/interface e pelo menos 3 estratégias concretas
- [ ] Adicionei uma nova estratégia sem alterar o calculador
- [ ] Extraí o esqueleto do relatório para uma classe base
- [ ] Subclasses sobrescrevem apenas a etapa de formatação

## 7. Referências

- GoF, *Design Patterns*, Cap. 5 — Strategy (p. 315) e Template Method (p. 325)
- Fowler, *Refactoring*, Cap. 12 — *Replace Conditional with Polymorphism*
