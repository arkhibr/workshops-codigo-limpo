# Roteiro Hands-on — Tratamento de Erros Explícito com IA

> Duração estimada: 20–30 minutos
> Pré-requisito: acesso a um assistente de IA (ChatGPT, Claude, Gemini, Copilot ou similar)

---

## Objetivo

Usar a IA como parceira para tornar o tratamento de erro explícito em uma função que silencia falhas — e verificar, rodando o arquivo, que as falhas agora aparecem em vez de sumir.

---

## Passo a Passo

### 1. Observe o comportamento atual

Rode o exercício e anote o que aparece para cada caso:

```bash
python3 sessao-5/tutorial-11-tratamento-de-erros/exercicios/exercicio.py
```

Você deve ver algo como:

```
ASS-001 (ativa, 18 dias restantes): {'id': 'ASS-001', ...}
ASS-002 (já cancelada): None
ASS-999 (não existe): None
ASS-001 (motivo None): None
```

Os três últimos retornam `None` — as falhas somem sem deixar rastro. Anote quais casos falharam silenciosamente.

---

### 2. Identifique os erros silenciados

Leia o código do `exercicio.py` e responda:

- Onde está o `except Exception: pass`?
- Em quais condições a função retorna `None` em vez de levantar uma exceção?
- O que o chamador perdeu de informação em cada caso?

---

### 3. Peça à IA para tornar as falhas visíveis

Envie para o assistente de IA:

```
Tenho a função abaixo que cancela uma assinatura. Ela tem dois problemas:
1. Usa except Exception: pass, que engole qualquer erro sem rastro.
2. Retorna None em três situações de falha distintas, sem indicar o motivo.

Sua tarefa:
- Defina três classes de exceção específicas que herdam de Exception:
  AssinaturaNaoEncontradaError, AssinaturaJaCanceladaError e MotivoAusenteError.
- Substitua cada retorno None de falha pela exceção correspondente com uma
  mensagem descritiva que inclua o ID ou o campo problemático.
- Remova o except Exception: pass — deixe os erros inesperados se propagarem.
- Não altere a lógica de cálculo de reembolso nem a estrutura de dados.
- Todos os identificadores devem permanecer em português brasileiro.

[cole o código do exercicio.py aqui]
```

---

### 4. Substitua o código e rode

Copie o código gerado pela IA para `exercicio.py` (ou crie um arquivo separado para não perder o original) e rode:

```bash
python3 sessao-5/tutorial-11-tratamento-de-erros/exercicios/exercicio.py
```

**Verifique:** as três falhas que antes retornavam `None` agora devem levantar exceções com mensagens descritivas. Se alguma ainda retornar `None` silenciosamente, o passo 3 não foi completamente atendido — revise o código gerado e peça à IA para corrigir o ponto específico.

---

### 5. Separe as responsabilidades (opcional)

Se quiser ir além, peça à IA:

```
Agora separe a função cancelar em funções menores, cada uma com uma
única responsabilidade:
- buscar_assinatura(id): localiza a assinatura ou levanta AssinaturaNaoEncontradaError
- validar_cancelamento(id, dados, motivo): verifica estado e motivo
- calcular_reembolso(dados): calcula o valor proporcional
- registrar_cancelamento(id, motivo, reembolso): persiste no banco
- cancelar_assinatura(id, motivo): orquestra as quatro funções acima

Não altere o comportamento. Mantenha os identificadores em português.

[cole o código do passo anterior aqui]
```

Rode após a mudança e confirme que a saída é idêntica.

---

### 6. Compare com o gabarito

```bash
python3 sessao-5/tutorial-11-tratamento-de-erros/exercicios/gabarito.py
```

As saídas devem ser equivalentes: um cancelamento aprovado e três falhas com tipos e mensagens específicos.

---

### 7. Reflexão

Responda para cada critério abaixo:

| # | Critério                                                                        | Atendido? |
|---|---------------------------------------------------------------------------------|-----------|
| 1 | Pedi exceções nomeadas no prompt, não apenas "melhore o tratamento de erro"?    |           |
| 2 | Rodei o arquivo após a mudança e confirmei que as falhas aparecem?              |           |
| 3 | Cada exceção tem uma mensagem com o contexto que causou o problema?             |           |
| 4 | O `except Exception: pass` foi completamente removido?                          |           |
| 5 | Erros inesperados ainda se propagam (não foram capturados em outro catch-all)?  |           |
| 6 | As responsabilidades estão separadas (validação, cálculo, persistência)?        |           |

---

## Aviso — Fallback sem IA

Se você não tiver acesso a um assistente de IA no momento, refatore diretamente o `exercicio.py` / `exercicio.ts` seguindo os passos acima manualmente. Consulte o `gabarito_revisao.md` para a lista completa de erros silenciados e as exceções sugeridas.

O objetivo é a **prática de tornar falhas visíveis** — a IA é uma ferramenta, não o foco. Um `except Exception: pass` que você remove manualmente vale tanto quanto um que a IA removeu.

---

## Reflexão final

> Um erro silenciado não desaparece — ele se acumula. Em produção, o sintoma aparece longe da causa: um saldo que não fecha, um cliente que nunca recebeu o reembolso, um cancelamento que consta no sistema mas nunca foi processado. Tornar as falhas visíveis no momento em que acontecem é a forma mais barata de depurar.

Discuta com o grupo: qual é o custo de um `except Exception: pass` que chega ao código de produção? Em que situação o retorno de `None` em falha seria aceitável?
