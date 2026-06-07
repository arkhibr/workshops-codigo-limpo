# Tutorial 22 — Idiom Patterns por Linguagem

> Referência: PEP 557 (dataclasses), TS Handbook, PHP 8.1 Changelog, Totvs TLPP docs

## 1. Contexto e Motivação

Idioms são padrões de uso estabelecidos em uma linguagem — não são padrões GoF, mas formas de escrever código que "soa certo" para quem conhece a linguagem. Ignorá-los cria código que funciona mas é difícil de ler para outros desenvolvedores da mesma plataforma.

## 2. Idioms Python

| Idiom | Sem idiom | Com idiom |
|-------|-----------|-----------|
| `@dataclass` | `__init__` manual, sem `__repr__`, sem `__eq__` | `@dataclass` gera tudo; `__post_init__` para validação |
| Context manager | `try/finally conn.fechar()` em todo lugar | `with Conexao() as conn:` — fechamento garantido |
| Generator | `lista = []; lista.append(...)` | `yield item` — processa sob demanda |
| Decorator | Código de logging/timing copiado | `@medir_tempo` — aplica em qualquer função |

## 3. Idioms PHP 8.1+

| Idiom | Benefício |
|-------|-----------|
| `readonly class` + constructor promotion | Remove boilerplate, immutability garantida |
| `enum` com métodos | Agrupa tipo + comportamento; substitui strings mágicas |
| Named arguments | Leitura clara, ordem independente |
| `match` expression | Expressão (retorna valor), exaustiva, sem fallthrough |

## 4. Idioms TypeScript

| Idiom | Benefício |
|-------|-----------|
| Discriminated Union | Narrowing seguro — `if (r.ok)` dá acesso ao tipo correto |
| `?.` Optional chaining | Elimina encadeamento de `&&` |
| `??` Nullish coalescing | Default apenas para `null`/`undefined` (não `0` ou `""`) |
| `async/await` + `Promise<T>` | I/O sem callback hell |

## 5. Idioms ADVPL/TLPP

| Necessidade | Idiom ADVPL |
|-------------|-------------|
| Struct com validação | Função `CriarX()` retornando array + validação inline |
| Cleanup garantido | `Begin Sequence / End Sequence` |
| Constantes nomeadas | `#define` no cabeçalho do arquivo |
| Funções de primeira classe | Codeblocks `{|param| expressao}` |
| Contexto multiempresa | `xFilial()`, `cEmpAnt` — padrão Protheus |

> **Nota:** ADVPL clássico não tem equivalente para `@dataclass`, `with`, `yield` ou `decorator`. TLPP 4.0+ traz classes e herança, mas sem açúcar sintático equivalente ao Python ou PHP 8.1.

## 6. Exercício

Domínio: folha de pagamento.

**`exercicios/exercicio.py`** — `Funcionario` sem `@dataclass`, `AbridorArquivo` sem context manager, lista em vez de generator, timing copiado.

**Objetivo:** Aplicar os 4 idioms Python (e equivalentes em sua linguagem principal).

## 7. Checklist

- [ ] `@dataclass` com `__post_init__` rejeita valores inválidos
- [ ] Context manager garante fechamento mesmo com exceção
- [ ] Generator não carrega todos os itens na memória
- [ ] Decorator aplicado em pelo menos 2 funções sem duplicar código
- [ ] (PHP) Usei `readonly class` + `enum` com método
- [ ] (TS) Usei Discriminated Union para resultado que pode falhar

## 8. Referências

- PEP 557 — Python dataclasses
- PEP 343 — Python context managers (The `with` Statement)
- TypeScript Handbook — Narrowing, Template Literal Types
- PHP 8.1 — Enums, readonly classes
- Totvs — TLPP 4.0 Class System
