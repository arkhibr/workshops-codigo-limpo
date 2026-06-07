# Tutorial 23 — Code Review Orientado a Padrões (Âncora)

> Este é o tutorial de encerramento do Tema 2. Integra os conceitos de T16–T22.

## Objetivo

Praticar identificação de padrões e anti-patterns em código real sem dicas visuais.
O código em `codigo_para_revisar.py` (e equivalentes) é funcional e bem formatado —
mas contém oportunidades de melhoria que você aprendeu ao longo deste workshop.

## Como usar

1. **Leia** `codigo_para_revisar.py` com atenção (15 minutos)
2. **Liste** as oportunidades de melhoria que você encontrar — use o Checklist abaixo
3. **Compare** com `gabarito_review.md` (6 violações esperadas)
4. **Consulte** `gabarito_patterns.md` para referência permanente em revisões futuras

## Checklist de revisão (sem spoilers)

Antes de ver o gabarito, responda:
- [ ] Há alguma classe que faz coisas demais?
- [ ] Existem strings ou números sem significado explícito?
- [ ] Algum método parece se importar mais com os dados de outro objeto do que com os seus?
- [ ] Há algum `if/elif` que cresce toda vez que um novo tipo é adicionado?
- [ ] O código ficaria mais difícil de testar por causa de dependências criadas internamente?
- [ ] Algum trecho de código aparece em mais de um lugar?

## Pontuação sugerida

| Encontradas | Avaliação |
|-------------|-----------|
| 6/6 | Excelente — pronto para aplicar em produção |
| 4–5/6 | Bom — revisite os tutoriais das violações que faltaram |
| 2–3/6 | Regular — rever T19 (Anti-patterns) e T16–T21 |
| 0–1/6 | Reiniciar — rever o workshop do início |

## `gabarito_patterns.md` — seu guia permanente

Após o workshop, use `gabarito_patterns.md` como referência em code reviews da sua equipe.
Ele contém uma tabela de todos os padrões vistos, com: quando usar, quando NÃO usar,
e equivalentes ADVPL/TLPP.

## Referências

- *Clean Code* — Robert C. Martin (Cap. 17)
- *Design Patterns* — GoF (Caps. 3, 4, 5)
- *Refactoring* — Martin Fowler (Cap. 3: Bad Smells)
