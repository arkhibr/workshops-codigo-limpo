# Design Spec — Workshop: Fundamentos de Qualidade e Padronização de Código

**Data:** 2026-04-14  
**Autor:** Marco Mendes  
**Status:** Aprovado

---

## 1. Visão Geral

Workshop de 4 horas dividido em duas sessões de 2 horas, baseado nos princípios do livro *Clean Code* de Robert C. Martin (Uncle Bob). O objetivo é criar uma base comum de qualidade, legibilidade e padronização de código para a equipe.

---

## 2. Público-Alvo

- Turma mista: desenvolvedores júnior e pleno
- Dois seniores presentes como referência técnica
- Turma pequena (aproximadamente 2 participantes por grupo)

---

## 3. Linguagens

| Papel | Linguagem |
|---|---|
| Principal | Python |
| Equivalentes | PHP, TypeScript, ADVPL/TLPP |

Os exemplos principais são escritos em Python. Para cada conceito central, há uma seção de equivalentes mostrando o mesmo padrão nas demais linguagens sem repetir toda a explicação.

---

## 4. Abordagem Pedagógica

**Abordagem B — Ciclos Teoria + Prática**

Cada tutorial segue o ciclo:
1. Teoria e demo ao vivo (fragmentos de código no Markdown)
2. Exercício prático (arquivo executável isolado)
3. Discussão coletiva com gabarito

Os Markdowns servem como **material formal de treinamento e de consulta** — são autossuficientes para uso sem o facilitador.

**Tipo de exercícios:**
- Refatoração (corrigir código ruim)
- Implementação do zero
- Code review simulado (exercício âncora da Sessão 2)

**Código de exemplo:** híbrido — fictício mas realista nos tutoriais, com placeholders explícitos para substituição por código real da equipe durante a facilitação.

---

## 5. Estrutura de Temporização

### Sessão 1 — 120 min

| Bloco | Atividade | Tempo |
|---|---|---|
| Abertura | Contexto, objetivos | 5min |
| Tutorial 1 | Nomes Significativos — teoria + demo | 20min |
| Exercício 1 | Refatoração: renomear variáveis/funções ruins | 10min |
| Discussão 1 | Correção coletiva com gabarito | 5min |
| Tutorial 2 | Funções — teoria + demo | 25min |
| Exercício 2 | Refatoração: quebrar função longa | 15min |
| Discussão 2 | Correção coletiva com gabarito | 5min |
| Tutorial 3 | Comentários — teoria + demo | 15min |
| Exercício 3 | Híbrido: identificar comentários ruins + reescrever | 10min |
| Discussão 3 | Correção coletiva com gabarito | 5min |
| Buffer | Dúvidas, respiro | 5min |

### Sessão 2 — 120 min

| Bloco | Atividade | Tempo |
|---|---|---|
| Abertura | Recapitulação da sessão 1 | 5min |
| Tutorial 4 | Formatação — teoria + demo | 15min |
| Exercício 4 | Refatoração: formatar código desorganizado | 10min |
| Discussão 4 | Correção coletiva com gabarito | 5min |
| Tutorial 5 | Code Review Simulado — instruções do exercício âncora | 10min |
| Exercício 5 ⭐ | Code review de sistema fictício com múltiplos problemas | 25min |
| Discussão 5 | Revisão coletiva dos comentários de review esperados | 10min |
| Tutorial 6 | Dívida Técnica — teoria + smells + como medir | 15min |
| Exercício 6 | Implementação: escrever versão limpa de módulo com dívidas | 15min |
| Discussão 6 | Gabarito + checklist de qualidade | 5min |
| Fechamento | Próximos passos, perguntas finais | 5min |

---

## 6. Estrutura do Repositório

```
workshops-codigo-limpo/
├── README.md
├── sessao-1/
│   ├── tutorial-01-nomes/
│   │   ├── README.md
│   │   ├── exemplos/
│   │   │   ├── nomes_ruins.py
│   │   │   ├── nomes_bons.py
│   │   │   ├── equivalente.php
│   │   │   ├── equivalente.ts
│   │   │   └── equivalente.tlpp
│   │   └── exercicios/
│   │       ├── exercicio.py
│   │       └── gabarito.py
│   ├── tutorial-02-funcoes/
│   │   ├── README.md
│   │   ├── exemplos/
│   │   │   ├── funcoes_ruins.py
│   │   │   ├── funcoes_boas.py
│   │   │   ├── equivalente.php
│   │   │   ├── equivalente.ts
│   │   │   └── equivalente.tlpp
│   │   └── exercicios/
│   │       ├── exercicio.py
│   │       └── gabarito.py
│   └── tutorial-03-comentarios/
│       ├── README.md
│       ├── exemplos/
│       │   ├── comentarios_ruins.py
│       │   ├── comentarios_bons.py
│       │   ├── equivalente.php
│       │   ├── equivalente.ts
│       │   └── equivalente.tlpp
│       └── exercicios/
│           ├── exercicio.py
│           └── gabarito.py
└── sessao-2/
    ├── tutorial-04-formatacao/
    │   ├── README.md
    │   ├── exemplos/
    │   │   ├── formatacao_ruim.py
    │   │   ├── formatacao_boa.py
    │   │   ├── equivalente.php
    │   │   ├── equivalente.ts
    │   │   └── equivalente.tlpp
    │   └── exercicios/
    │       ├── exercicio.py
    │       └── gabarito.py
    ├── tutorial-05-code-review/
    │   ├── README.md
    │   ├── codigo_para_revisar.py
    │   └── gabarito_review.md
    └── tutorial-06-divida-tecnica/
        ├── README.md
        ├── exemplos/
        │   ├── divida_antes.py
        │   ├── divida_depois.py
        │   ├── equivalente.php
        │   ├── equivalente.ts
        │   └── equivalente.tlpp
        └── exercicios/
            ├── exercicio.py
            └── gabarito.py
```

---

## 7. Anatomia dos Arquivos Markdown

Cada `README.md` de tutorial segue esta estrutura:

1. **Contexto e Motivação** — por que o tema importa, referência ao capítulo do Clean Code
2. **Conceito Central** — explicação teórica sem código, definição e raciocínio
3. **O Problema na Prática** — fragmento de código ruim (Python) com explicação linha a linha
4. **A Solução** — mesmo código refatorado com explicação das decisões
5. **Equivalentes em Outras Linguagens** — PHP, TypeScript, ADVPL/TLPP
6. **Regras de Ouro** — 3–5 princípios resumidos para consulta rápida
7. **Exercício** — enunciado, instruções de execução, localização do gabarito
8. **Para se Aprofundar** — capítulo exato do Clean Code + referências complementares

---

## 8. Conteúdo por Tutorial

### Tutorial 1 — Nomes Significativos (Cap. 2 - Clean Code)
- Nomes que revelam intenção
- Evitar desinformação e distinções sem sentido
- Nomes pronunciáveis e pesquisáveis
- Evitar prefixos e notação húngara
- Convenção: classes = substantivos, funções = verbos
- Placeholder para código real da equipe

### Tutorial 2 — Funções (Cap. 3 - Clean Code)
- Funções pequenas, uma responsabilidade (SRP no nível de função)
- Um nível de abstração por função
- Máximo de 2 argumentos idealmente; evitar flags booleanas
- Sem side effects ocultos
- Preferir exceções a retornar códigos de erro

### Tutorial 3 — Comentários (Cap. 4 - Clean Code)
- Comentários bons: licença, intenção, amplificação, TODOs rastreáveis
- Comentários ruins: redundantes, enganosos, código comentado
- O melhor comentário é o código que não precisa de um
- Código autodocumentado com nomes expressivos

### Tutorial 4 — Formatação (Cap. 5 - Clean Code)
- Formatação vertical: funções relacionadas próximas, declarações perto do uso
- Formatação horizontal: indentação, espaçamento, limite de linha
- Padrões de formatação de time com ferramentas: `black`/`flake8` (Python), `prettier` (TS), `phpcs` (PHP)

### Tutorial 5 — Code Review Simulado ⭐
- Exercício âncora que integra os 4 tutoriais anteriores
- `codigo_para_revisar.py`: módulo fictício `sistema_pedidos.py` (~80 linhas) com problemas intencionais de nomes, funções, comentários e formatação
- Participante escreve comentários de review como se fosse um PR real
- `gabarito_review.md`: comentários de review esperados categorizados por tipo
- Placeholder: facilitador pode substituir o arquivo por código real da equipe

### Tutorial 6 — Dívida Técnica (Cap. 17 - Clean Code + Quadrante Cunningham)
- Metáfora da dívida técnica (Ward Cunningham)
- Quadrante da dívida: deliberada vs inadvertida × imprudente vs prudente
- Code smells mais comuns: funções longas, classes grandes, código duplicado, nomes obscuros
- Como identificar e priorizar dívidas
- Checklist de qualidade para o time
- Placeholder para análise de código real da equipe

---

## 9. Critérios de Sucesso

- [ ] Cada exemplo Python roda de forma isolada com `python <arquivo>.py`
- [ ] Cada tutorial é autossuficiente — funciona sem o facilitador
- [ ] Cada exercício tem gabarito completo e executável
- [ ] Os Markdowns têm bagagem teórica formal suficiente para servir como material de consulta
- [ ] Os placeholders para código real da equipe estão claramente sinalizados
- [ ] O exercício âncora de code review integra todos os tópicos anteriores
- [ ] O checklist de qualidade do Tutorial 6 é aplicável no dia a dia da equipe
