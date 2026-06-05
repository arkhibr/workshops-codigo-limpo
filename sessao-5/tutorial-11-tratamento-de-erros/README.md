# Tutorial 11 — Tratamento de Erros com IA

> Referência: *Clean Code*, Cap. 7 (Error Handling)

---

## 1. Contexto e Motivação

Este é o **exercício âncora da Sessão 5**. Dentre todos os vícios do código gerado por IA, engolir erros é o mais perigoso — e o mais difícil de detectar, porque o caminho feliz funciona. A função retorna um valor, o sistema continua rodando e o problema só aparece quando o dado corrompido chega à ponta: um estorno que nunca foi processado, uma assinatura cancelada que seguiu sendo cobrada, um saldo que não fecha.

A IA não engole erros por malícia — ela faz o que o prompt implicitamente pede: "faça funcionar". Se o prompt não menciona tratamento de erro, a IA tende a usar `except Exception: pass`, `catch {}` vazio ou retornar `None` em falha para que o fluxo principal não seja interrompido. O resultado é um código que parece robusto, mas na verdade **esconde os problemas em vez de tratá-los**.

---

## 2. Conceito Central

### Anti-padrões que a IA produz com frequência

**Python — erro silenciado:**

```python
def processar_estorno(estorno: dict):
    try:
        valor = estorno["valor"]
        # ... lógica ...
        return resultado
    except Exception:
        pass          # ← falha engolida; retorna None sem aviso
```

**TypeScript — catch vazio:**

```typescript
function procesarEstorno(estorno: Estorno): Resultado | null {
    try {
        // ... lógica ...
        return resultado;
    } catch (e) {
        return null;  // ← quem chamou não sabe o que falhou
    }
}
```

Esses padrões compartilham o mesmo vício: a **falha é invisível para quem chamou a função**. O sistema segue como se nada tivesse acontecido.

### Tratamento explícito

**Exceções específicas com mensagens úteis:**

```python
class EstornoInvalidoError(Exception):
    """Levantada quando os dados do estorno estão incompletos ou malformados."""

class ValorEstornoExcedidoError(Exception):
    """Levantada quando o valor do estorno excede o valor original da compra."""

def processar_estorno(estorno: dict) -> dict:
    if "valor" not in estorno:
        raise EstornoInvalidoError("Campo 'valor' ausente no estorno.")
    if estorno["valor"] > estorno["valor_original"]:
        raise ValorEstornoExcedidoError(
            f"Estorno de R$ {estorno['valor']:.2f} excede o valor original "
            f"de R$ {estorno['valor_original']:.2f}."
        )
    # ... lógica de processamento ...
    return {"status": "aprovado", "valor": estorno["valor"]}
```

**TypeScript — classes de erro tipadas:**

```typescript
class EstornoInvalidoError extends Error {
    constructor(mensagem: string) {
        super(mensagem);
        this.name = "EstornoInvalidoError";
    }
}
```

### Princípio: falha visível > falha silenciosa

Código que falha em voz alta é mais seguro do que código que falha em silêncio. Um `EstornoInvalidoError` com mensagem descritiva:

- Aparece no log imediatamente.
- Indica exatamente o que falhou e por quê.
- Permite que o sistema tomador de decisão (o chamador) decida o que fazer — tentar novamente, alertar, persistir o erro.

Retornar `None` ou engolir a exceção transfere o problema para mais tarde, quando o contexto do erro já se perdeu.

---

## 3. Exercício

O exercício está em `exercicios/` e tem duas partes:

**Parte estática** (`exercicio.py` / `exercicio.ts`): função de cancelamento de assinatura gerada por IA que mistura validação, cálculo e persistência em uma única função E silencia os erros. Sua tarefa:

1. Torne cada falha visível com uma exceção específica.
2. Separe as responsabilidades.
3. Liste os erros que estavam sendo silenciados.

```bash
# Veja o código atual (note como as falhas somem):
python3 sessao-5/tutorial-11-tratamento-de-erros/exercicios/exercicio.py

# Compare com a solução de referência:
python3 sessao-5/tutorial-11-tratamento-de-erros/exercicios/gabarito.py
```

**Parte hands-on** (`roteiro-ia.md`): peça à IA para tornar o tratamento de erro explícito, rode o arquivo provocando uma falha e confirme que agora ela aparece em vez de sumir.

> Arquivo: [`exercicios/exercicio.py`](exercicios/exercicio.py) · [`exercicios/exercicio.ts`](exercicios/exercicio.ts)
> Gabarito: [`exercicios/gabarito.py`](exercicios/gabarito.py) · [`exercicios/gabarito.ts`](exercicios/gabarito.ts)
> Revisão comentada: [`exercicios/gabarito_revisao.md`](exercicios/gabarito_revisao.md)
> Roteiro hands-on: [`exercicios/roteiro-ia.md`](exercicios/roteiro-ia.md)

---

## 4. Checklist de Revisão de Tratamento de Erros

Use estas perguntas ao revisar qualquer código gerado por IA:

1. **Há `except`/`catch` largo?** — `except Exception: pass` ou `catch (e) {}` vazio capturam tudo e descartam a informação do erro.
2. **Algum erro é silenciado?** — A função retorna `None`, `null`, `-1` ou `False` em falha sem indicar o motivo?
3. **As exceções são específicas?** — O chamador consegue distinguir "valor inválido" de "recurso não encontrado" apenas pela exceção?
4. **A mensagem ajuda a depurar?** — A mensagem de erro inclui os valores que causaram o problema (valor do estorno, ID da assinatura, etc.)?
5. **Falhas externas são propagadas?** — Erros de banco de dados, APIs ou arquivos são tratados ou engolidos?
6. **O chamador sabe o que fazer?** — Quando a função falha, quem chamou tem informação suficiente para decidir entre tentar novamente, alertar o usuário ou registrar o incidente?

---

## 5. Referências

- **Clean Code**, Robert C. Martin — Capítulo 7: *Error Handling* (p. 103–112)
- Arquivos de exemplo: [`exemplos/prompt.md`](exemplos/prompt.md) · [`exemplos/estorno_gerado.py`](exemplos/estorno_gerado.py) · [`exemplos/estorno_revisado.py`](exemplos/estorno_revisado.py)

---

> **Próximo tutorial:** [Tutorial 12 — Revisão Crítica de Código Gerado por IA](../tutorial-12-revisao-critica/README.md)
