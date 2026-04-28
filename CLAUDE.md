# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Propósito

Workshop de Clean Code para equipes de desenvolvimento, cobrindo 7 tutoriais em 2 sessões (4h total). Baseado em "Clean Code" (Martin) e "Working Effectively with Legacy Code" (Feathers). Código de exemplo em Python, PHP, TypeScript e ADVPL/TLPP.

## Executar exemplos e exercícios

**Python** (linguagem principal, sem dependências externas):
```bash
python3 <caminho/para/arquivo.py>
```

**PHP** (requer PHP 8.1+):
```bash
php <caminho/para/arquivo.php>
php -l <arquivo.php>   # validar sintaxe
```

**TypeScript** (requer Node.js 18+ e ts-node):
```bash
npx ts-node <caminho/para/arquivo.ts>
```

**ADVPL/TLPP**: compilar no Totvs IDE (SmartClient/TDS). O ponto de entrada está no cabeçalho de cada arquivo.

## Estrutura e arquitetura

```
sessao-1/   # Fundamentos (2h): nomes, funções, comentários, formatação
sessao-2/   # Escala (2h): code review, dívida técnica, código legado
```

Cada tutorial segue o padrão:
- `README.md` — teoria completa (fonte primária do conteúdo)
- `exemplos/<tema>_ruins.py` + `<tema>_bons.py` — par antes/depois
- `exemplos/equivalente.{php,ts,tlpp}` — mesmos problemas em outras linguagens
- `exercicios/exercicio.*` — desafio para o participante
- `exercicios/gabarito.*` — solução

Tutorial 05 (code review) usa `codigo_para_revisar.*` + `gabarito_review_*.md`.

## Convenções críticas

**Linguagem de domínio:** todo o código usa português nos identificadores e domínios de negócio (padrão intencional para ensino de consistência).

**Paridade entre linguagens:** alterações em Python normalmente precisam de equivalentes em PHP, TypeScript e ADVPL/TLPP.

**Arquivos "_ruins" são intencionalmente incorretos** — demonstram anti-padrões. Não "corrigir" violações de Clean Code em arquivos `*_ruins.*` ou `codigo_para_revisar.*`.

**Autocontido:** nenhum arquivo importa de outros arquivos do repositório. Toda verificação é via print/stdout — sem frameworks de teste.

**Convenções de commit:** `<type>: <mensagem>` — tipos usados: `feat`, `docs`, `refactor`, `fix`.
