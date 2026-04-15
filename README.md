# Workshop: Fundamentos de Qualidade e Padronização de Código

Workshop de 4 horas dividido em duas sessões, baseado nos princípios do livro **Clean Code** de Robert C. Martin (Uncle Bob).

## Como usar este material

Cada tutorial é autossuficiente. Navegue até a pasta do tutorial e execute os exemplos diretamente:

```bash
python sessao-1/tutorial-01-nomes/exemplos/nomes_ruins.py
python sessao-1/tutorial-01-nomes/exemplos/nomes_bons.py
python sessao-1/tutorial-01-nomes/exercicios/exercicio.py
```

Requisito: **Python 3.8+**. Nenhuma dependência externa.

---

## Sessão 1 — 2 horas

| Tutorial | Tema | Capítulo (Clean Code) |
|---|---|---|
| [01](sessao-1/tutorial-01-nomes/) | Nomes Significativos | Cap. 2 |
| [02](sessao-1/tutorial-02-funcoes/) | Funções | Cap. 3 |
| [03](sessao-1/tutorial-03-comentarios/) | Comentários | Cap. 4 |

## Sessão 2 — 2 horas

| Tutorial | Tema | Capítulo (Clean Code) |
|---|---|---|
| [04](sessao-2/tutorial-04-formatacao/) | Formatação | Cap. 5 |
| [05](sessao-2/tutorial-05-code-review/) | Code Review Simulado ⭐ | — |
| [06](sessao-2/tutorial-06-divida-tecnica/) | Dívida Técnica | Cap. 17 |

---

## Estrutura de cada tutorial

```
tutorial-0N-<tema>/
├── README.md          # Material teórico + fragmentos de código (leia primeiro)
├── exemplos/
│   ├── <tema>_ruins.py    # Código problemático — Python
│   ├── <tema>_bons.py     # Versão corrigida — Python
│   ├── equivalente.php
│   ├── equivalente.ts
│   └── equivalente.tlpp
└── exercicios/
    ├── exercicio.py   # Seu desafio
    └── gabarito.py    # Solução (abra só depois de tentar!)
```

---

> **Referência:** MARTIN, Robert C. *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall, 2008.
