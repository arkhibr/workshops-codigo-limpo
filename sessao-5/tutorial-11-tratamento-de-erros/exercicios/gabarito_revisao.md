# Gabarito de Revisão — Cancelamento de Assinatura

> Este documento lista os erros silenciados no `exercicio.py` / `exercicio.ts`, explica como cada um foi tornado visível e apresenta as exceções específicas sugeridas.

---

## Erros silenciados identificados

### 1. Assinatura não encontrada — retorno `None`/`null`

**Onde aparece:**

```python
dados = banco_assinaturas.get(id)
if not dados:
    return None  # ← falha silenciosa
```

**O problema:** o chamador recebe `None` sem saber se a assinatura não existe, se o ID está errado ou se houve outro problema. Não há como distinguir "cancelamento bem-sucedido que não retorna nada" de "falha que foi engolida".

**Como tornar visível:**

```python
def buscar_assinatura(id_assinatura: str) -> dict:
    dados = banco_assinaturas.get(id_assinatura)
    if dados is None:
        raise AssinaturaNaoEncontradaError(
            f"Assinatura '{id_assinatura}' não encontrada."
        )
    return dados
```

---

### 2. Assinatura já cancelada — retorno `None`/`null`

**Onde aparece:**

```python
if not dados["ativa"]:
    return None  # ← falha silenciosa
```

**O problema:** um estado inválido de negócio (cancelar algo que já está cancelado) é tratado como se fosse uma situação normal. Não há registro de que a tentativa aconteceu.

**Como tornar visível:**

```python
if not dados["ativa"]:
    raise AssinaturaJaCanceladaError(
        f"Assinatura '{id_assinatura}' já foi cancelada anteriormente."
    )
```

---

### 3. Motivo ausente — aceito silenciosamente

**Onde aparece:**

A função original aceita qualquer valor de `motivo`, incluindo `None` e string vazia, sem validar. O campo é persistido no cancelamento sem verificação.

**O problema:** o registro de cancelamento fica com `motivo: None` no banco, o que pode quebrar relatórios e auditorias em produção — sem nunca ter levantado um erro.

**Como tornar visível:**

```python
if not motivo or not motivo.strip():
    raise MotivoAusenteError(
        "O motivo do cancelamento é obrigatório e não pode ser vazio."
    )
```

---

### 4. `except Exception: pass` — catch-all que engole tudo

**Onde aparece:**

```python
except Exception:
    pass  # ← qualquer erro desaparece sem rastro
```

**O problema:** qualquer erro inesperado — `KeyError`, `TypeError`, `AttributeError` — é silenciado. O chamador nunca sabe que algo deu errado. Esse padrão é especialmente perigoso porque mascara bugs que deveriam ser corrigidos.

**Como tornar visível:**

Remova o `except Exception: pass`. Cada caso de erro esperado deve ser tratado explicitamente com uma exceção nomeada (como os três acima). Erros inesperados devem se propagar naturalmente para que o sistema possa registrá-los e tratá-los na camada correta.

---

## Problema de coesão: função que faz quatro coisas

Além do tratamento de erro, a função `cancelar` / `cancelar()` mistura quatro responsabilidades:

| Responsabilidade       | Onde aparece                                     |
|------------------------|--------------------------------------------------|
| Busca no banco         | `banco_assinaturas.get(id)`                      |
| Validação de estado    | `if not dados["ativa"]`                          |
| Cálculo de reembolso   | `reembolso = round(valor * (dias / 30), 2)`      |
| Persistência           | `dados["ativa"] = False` + `append(...)`         |

O gabarito separa cada uma em uma função própria:

- `buscar_assinatura` — localiza e retorna ou levanta `AssinaturaNaoEncontradaError`
- `validar_cancelamento` — verifica estado e motivo ou levanta exceção
- `calcular_reembolso` — calcula o valor proporcional sem efeitos colaterais
- `registrar_cancelamento` — persiste o cancelamento no banco

---

## Exceções específicas sugeridas

| Exceção                       | Quando levantar                                        |
|-------------------------------|--------------------------------------------------------|
| `AssinaturaNaoEncontradaError` | ID não existe no banco de dados                       |
| `AssinaturaJaCanceladaError`  | Assinatura com `ativa = False` sendo cancelada de novo |
| `MotivoAusenteError`          | Motivo `None`, vazio ou apenas espaços                 |

Cada exceção herda de `Exception` (Python) / `Error` (TypeScript) e carrega uma mensagem com o contexto que causou o problema — ID, valor ou campo — para facilitar a depuração.

---

## Resumo

| Falha no exercício              | Comportamento original    | Comportamento no gabarito            |
|---------------------------------|---------------------------|--------------------------------------|
| ID inexistente                  | Retorna `None` silencioso | `AssinaturaNaoEncontradaError`       |
| Assinatura já cancelada         | Retorna `None` silencioso | `AssinaturaJaCanceladaError`         |
| Motivo ausente                  | Aceito silenciosamente    | `MotivoAusenteError`                 |
| Qualquer outro erro inesperado  | Engolido pelo catch-all   | Propaga naturalmente para o chamador |
