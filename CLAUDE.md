# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Propósito

Workshop de qualidade e testes de software para equipes de desenvolvimento, cobrindo 33 tutoriais em 9 sessões, organizadas em 5 temas (18h no total):

- **Tema 1 (Sessões 1–2):** Fundamentos de Clean Code
- **Tema 2 (Sessões 3–4):** Design Patterns e Idiom Patterns
- **Tema 3 (Sessões 5–6):** Clean Code e uso consciente de IA
- **Tema 4 (Sessão 7):** Testes de Unidade
- **Tema 5 (Sessões 8–9):** Testes de Integração, E2E e Performance

Baseado em "Clean Code" (Martin), "Working Effectively with Legacy Code" (Feathers), na pirâmide de testes (Fowler) e nas ferramentas de mercado (pytest, FastAPI, Maestro, k6). Código de exemplo em Python (principal), PHP, TypeScript e ADVPL/TLPP; a Sessão 9 usa YAML (Maestro) e JavaScript (K6), as linguagens nativas de cada ferramenta.

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

**Sessões 7–9 (ferramentas reais):** estas sessões usam frameworks e ferramentas de verdade, e exigem instalação prévia para rodar. A verificação é feita executando a ferramenta, não por `print`/stdout.

```bash
# Sessões 7, 8 — testes de unidade e integração (Python é a referência executável)
pip install -r <sessao>/requirements.txt
cd <tutorial>/exemplos && python3 -m pytest integracao_bons.py -v   # nomear o arquivo: o padrão test_*.py não casa

# Sessão 9 — Maestro (E2E, YAML) e K6 (performance, JavaScript)
# E2E roda contra apps de demonstração EXTERNOS: saucedemo.com (T31, web) e
# Sauce Labs My Demo App (T32, mobile) — exigem internet / emulador com o app.
maestro test <tutorial>/exemplos/fluxo_bons.yaml   # requer Maestro + navegador/emulador + app-alvo
k6 run <tutorial>/exemplos/teste_bons.js           # requer o binário k6 + o alvo local em exemplos/alvo/ no ar
```

Integração (Sessão 8) roda em memória — FastAPI `TestClient` e SQLite `:memory:` —, sem Docker nem serviço externo.

## Estrutura e arquitetura

```
sessao-1/   # Fundamentos: nomes, funções, comentários, formatação
sessao-2/   # Escala: code review, dívida técnica, código legado
sessao-3/   # Design Patterns: SOLID, criação, estrutura, anti-patterns
sessao-4/   # Design Patterns: comportamento, idioms, code review
sessao-5/   # IA: dirigir e revisar geração de código (Python + TS)
sessao-6/   # IA: revisar e sustentar código gerado (Python + TS)
sessao-7/   # Testes de unidade: fundamentos, dublês, massa de dados, legado
sessao-8/   # Testes de integração: API, banco, ponta a ponta (pytest + FastAPI + sqlite)
sessao-9/   # E2E e performance: Maestro (YAML), K6 (JavaScript)
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

**Autocontido:** nenhum arquivo importa de outros arquivos do repositório. Nas Sessões 1–6, toda verificação é via print/stdout, sem frameworks de teste. As Sessões 7–9 são a exceção documentada: usam ferramentas reais (pytest, PHPUnit, Vitest, PROBAT, FastAPI, Maestro, k6) e são verificadas executando essas ferramentas. Mesmo lá, cada tutorial continua autocontido — o `app.py`/`repositorio.py` (Sessão 8) e o subflow `login.yaml` do Maestro (Sessão 9) são replicados dentro de `exercicios/` em vez de importados.

**Linguagem por ferramenta:** os fluxos do Maestro (Sessão 9) só existem em YAML; os testes do K6, só em JavaScript. Esses dois tutoriais não têm equivalentes multilíngue.

**Escrita dos READMEs:** seguir os SOPs de escrita do PKA (`anti-cacoetes-llm.md`, `padrao-escrita.md`) — conceito antes da ferramenta, sem sigla em inglês (ex.: "SUT"), sem cacoetes de IA, com fragmentos de código e links relativos aos arquivos.

**Convenções de commit:** `<type>: <mensagem>` — tipos usados: `feat`, `docs`, `refactor`, `fix`.
