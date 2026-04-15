# Workshop Código Limpo — Plano de Implementação

> **Para agentes:** use superpowers:executing-plans para implementar este plano.

**Goal:** Criar o repositório completo do workshop de 4h sobre Clean Code, com 6 tutoriais, exemplos executáveis, exercícios e gabaritos.

**Architecture:** Um repo único com duas pastas de sessão. Cada tutorial tem README.md (material formal), exemplos Python + equivalentes (PHP, TS, TLPP), exercício e gabarito.

**Tech Stack:** Python 3, PHP 8, TypeScript, ADVPL/TLPP. Sem dependências externas — todos os exemplos Python rodam com `python <arquivo>.py`.

---

## Tarefas

- [ ] **Task 1:** Scaffold — criar estrutura de diretórios + README raiz
- [ ] **Task 2:** Tutorial 01 — Nomes Significativos (Cap. 2 Clean Code)
- [ ] **Task 3:** Tutorial 02 — Funções (Cap. 3 Clean Code)
- [ ] **Task 4:** Tutorial 03 — Comentários (Cap. 4 Clean Code)
- [ ] **Task 5:** Tutorial 04 — Formatação (Cap. 5 Clean Code)
- [ ] **Task 6:** Tutorial 05 — Code Review Simulado (exercício âncora)
- [ ] **Task 7:** Tutorial 06 — Dívida Técnica (Cap. 17 Clean Code)
- [ ] **Task 8:** Commit final

## Arquivos por tutorial

Cada `tutorial-0N-<tema>/` contém:
```
README.md                  # teoria + fragmentos de código
exemplos/
  <tema>_ruins.py          # código problemático (Python principal)
  <tema>_bons.py           # versão corrigida
  equivalente.php
  equivalente.ts
  equivalente.tlpp
exercicios/
  exercicio.py             # código para o participante corrigir/implementar
  gabarito.py
```

Exceção: `tutorial-05-code-review/` tem `codigo_para_revisar.py` + `gabarito_review.md` (sem pasta exemplos/).

## Anatomia do README.md de cada tutorial

1. Contexto e Motivação
2. Conceito Central (teoria)
3. O Problema na Prática (fragmento código ruim)
4. A Solução (fragmento código bom)
5. Equivalentes em Outras Linguagens
6. Regras de Ouro (3–5 bullets)
7. Exercício (enunciado + como rodar)
8. Para se Aprofundar (ref. ao capítulo do Clean Code)
