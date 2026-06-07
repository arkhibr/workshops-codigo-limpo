# Prompt — Gerar sistema de reservas de sala com spec-first

Este arquivo demonstra **o mesmo objetivo de geração** expresso de dois modos:
sem spec firme (perde exigência implícita) e com spec estruturada (gera código correto).

**Objetivo:** gerar um módulo de reservas de sala com as operações criar e listar,
incluindo a exigência implícita crítica: *não permitir reservas sobrepostas na
mesma sala*.

---

## Sem spec firme (o problema)

```
Crie um sistema de reservas de sala em Python. Cada reserva tem sala, horário
de início, horário de fim e nome do responsável. Implemente as operações de
criar reserva e listar reservas. Use boas práticas.
```

**Saída típica:** código limpo, tipado, com `@dataclass` e `ValueError` para
campos inválidos — mas que **aceita silenciosamente reservas sobrepostas**:

```python
def criar_reserva(sala, inicio, fim, responsavel):
    reserva = Reserva(id=_proximo_id, sala=sala, inicio=inicio,
                      fim=fim, responsavel=responsavel)
    _repositorio.append(reserva)   # ← salva sem verificar sobreposição
    _proximo_id += 1
    return reserva
```

O código parece completo. Cria reservas, lista por sala, valida campos obrigatórios.
Apenas quando duas reservas ocupam o mesmo horário na mesma sala o problema aparece:
ambas são aceitas, e o conflito só é descoberto quando o participante chega à sala.
É o que está em `reserva_gerado.py`.

---

## Com spec estruturada (a solução)

A spec em `spec.md` fixa a exigência implícita antes da geração. Cada provedor
recebe o mesmo conteúdo da spec — a diferença está em como cada um é acionado.

### Claude (Opus 4.8 / Claude Code)

O `CLAUDE.md` já está no contexto permanente ao usar Claude Code. Peça o **plano
antes do código** — Claude é forte em decompor regras em estratégia antes de
implementar:

```
Leia a spec em sessao-5/tutorial-18-spec-first/exemplos/spec.md.

Antes de gerar qualquer código, descreva em 3–5 linhas:
  1. Como você vai detectar sobreposição de horário (a fórmula exata).
  2. Qual exceção vai levantar e com qual mensagem.
  3. Quais casos do contrato testam os limites da sobreposição.

Depois, gere o módulo reserva_revisado.py seguindo a spec completa:
  - @dataclass Reserva com os campos da spec
  - class ReservaSobrepostaError(Exception)
  - def criar_reserva(sala, inicio, fim, responsavel) -> Reserva
  - def listar_reservas(sala=None) -> list[Reserva]
  - Bloco __main__ exercitando todos os 6 casos do contrato

Restrições: sem dependências externas, repositório em memória,
módulo plano sem camadas adicionais.
```

**Por que funciona:** pedir o plano antes do código força o modelo a declarar
a fórmula de sobreposição antes de implementá-la. Se o modelo descrever a fórmula
errada no plano, você corrige no prompt — não no código. A spec também fornece
os exemplos de contrato (casos 2, 3, 4) que precisam de implementação explícita
da lógica de borda.

---

### OpenAI (Codex com AGENTS.md)

Configure `AGENTS.md` com as convenções do projeto. Use mensagem de sistema
(`developer`) para o contexto e a regra crítica no prompt:

```
[developer/system message — vai em AGENTS.md ou como system instruction]
You are a Python code generator for a Clean Code workshop (Brazilian Portuguese).
Follow the project conventions:
- All identifiers in Brazilian Portuguese (sala, inicio, fim, responsavel, reserva)
- @dataclass for entities — never raw dicts
- Raise ValueError for invalid input — never return error objects
- Custom exception class for domain errors (ReservaSobrepostaError)
- Flat module with free functions; no Repository/Service class layers
- if __name__ == "__main__": block with full print demo

[user message]
Before writing code, state in 3 sentences:
  1. The exact boolean formula you will use to detect overlapping reservations.
  2. The exception class name and message format.
  3. Which contract example (from the spec below) tests the adjacent-reservation edge case.

Then generate the booking module with:
  class ReservaSobrepostaError(Exception)
  @dataclass Reserva: id, sala, inicio (datetime), fim (datetime), responsavel
  def criar_reserva(sala, inicio, fim, responsavel) -> Reserva
  def listar_reservas(sala=None) -> list[Reserva]

CRITICAL business rule (from spec.md):
  Two reservations overlap when: inicio_nova < fim_existente AND fim_nova > inicio_existente
  Adjacent reservations (fim_nova == inicio_existente) do NOT overlap.
  Different rooms are independent.
  Raise ReservaSobrepostaError if overlap detected.

Contract examples the demo must reproduce:
  criar_reserva("Sala A", 10:00, 11:00, "Ana")   → created id=1
  criar_reserva("Sala A", 10:30, 11:30, "Bob")   → ReservaSobrepostaError
  criar_reserva("Sala A", 11:00, 12:00, "Dana")  → created id=2  (adjacent, OK)
  criar_reserva("Sala B", 10:00, 11:00, "Eva")   → created id=3  (different room, OK)
```

**Diferença relevante:** pedir ao modelo que declare a fórmula de sobreposição
antes do código expõe se ele entende a condição de adjacência. Se a resposta
incluir `<=` em vez de `<`, você corrige antes de receber o código.

---

### Gemini (Gemini CLI com GEMINI.md)

Configure `GEMINI.md` com as convenções do projeto. Use a janela de contexto
ampla para colar a `spec.md` completa como contexto antes do prompt:

```
# system_instruction (em GEMINI.md):
Você é um gerador de código para um workshop de Clean Code em português.
Siga estas convenções antes de gerar qualquer código:
- Identificadores em português (sala, inicio, fim, responsavel, reserva)
- @dataclass para entidades — nunca dicts crus
- ValueError para dados inválidos; exceção de domínio para violações de regra
- Funções planas no módulo — sem camadas Repository/Service
- Bloco __main__ com demo de print

# prompt (cole spec.md completa antes deste bloco):
Antes de gerar o código, responda em 3 frases:
  1. A fórmula exata para detectar sobreposição de horário.
  2. Como você vai tratar o caso de reservas adjacentes (fim == início).
  3. Qual caso do contrato valida que salas diferentes são independentes.

Depois, gere o módulo seguindo a spec acima:
  class ReservaSobrepostaError(Exception)
  @dataclass Reserva: id, sala, inicio, fim, responsavel
  def criar_reserva(sala, inicio, fim, responsavel) -> Reserva
  def listar_reservas(sala=None) -> list[Reserva]

O demo deve executar todos os 6 casos do contrato definidos na spec
e imprimir o resultado de cada um (OK ou erro capturado).
```

**Vantagem:** colar `spec.md` completa ancora todos os exemplos de contrato
sem reescrevê-los no prompt. O Gemini vê a fórmula de sobreposição, os casos
de borda e as assinaturas-alvo — tudo no mesmo contexto.

---

## O que muda na aderência

| Aspecto | Sem spec firme | Com spec estruturada |
|---|---|---|
| Sobreposição detectada? | Não — reservas sobrepostas aceitas | Sim — ReservaSobrepostaError |
| Caso adjacente (11:00–11:00) | Não testado | Testado — OK esperado |
| Sala diferente independente | Não testado | Testado — OK esperado |
| Detecção do defeito | Só em produção | No plano, antes do código |
| Iterações até acertar | 2–3 (descoberta + correção) | 1 (correto de primeira) |

**Conclusão:** nos três provedores, o segredo não é o modelo — é a spec.
A exigência implícita "não permitir sobreposição" estava na cabeça do
desenvolvedor mas não no prompt. Com a spec estruturada e o plano pedido
antes do código, o modelo declara a estratégia e você valida antes de
receber uma linha de implementação.
