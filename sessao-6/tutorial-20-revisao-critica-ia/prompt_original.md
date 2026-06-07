# Prompt Original — Módulo de Gateway de Pagamento

Este arquivo demonstra **o mesmo objetivo de geração** expresso para os três
modelos de fronteira — sem restrições de segurança ou edge cases explícitos.
O objetivo é mostrar que um prompt razoável ainda produz código a revisar.

**Objetivo:** gerar um módulo Python/TypeScript de integração com gateway de
pagamento que exponha três operações: `cobrar`, `estornar`, `consultar_status`.

---

## Prompt base (enviado aos três modelos)

```
Crie um módulo Python de integração com um gateway de pagamento.
O módulo deve expor três funções: cobrar, estornar, consultar_status.

Use as seguintes convenções:
- Identificadores em português (cobranca, parcela, transacao_id)
- Dataclasses para os modelos de dados
- Tipagem estática completa
- Docstrings nas funções públicas
- Bloco if __name__ == "__main__": com uma demo de cobrança parcelada

O gateway pode ser simulado em memória — não precisa de rede real.
Inclua lógica de parcelamento com juros compostos de 1,99% ao mês.
```

---

## Claude (Opus 4.8 / Claude Code)

O `CLAUDE.md` já está no contexto permanente ao usar Claude Code. O prompt
acima é suficiente para gerar código polido e tipado. Complemente assim:

```
[contexto permanente: CLAUDE.md com convenções do projeto]

Crie um módulo Python de integração com um gateway de pagamento.
O módulo deve expor três funções: cobrar, estornar, consultar_status.

Use as seguintes convenções:
- Identificadores em português (cobranca, parcela, transacao_id)
- Dataclasses para os modelos de dados
- Tipagem estática completa
- Docstrings nas funções públicas
- Bloco if __name__ == "__main__": com uma demo de cobrança parcelada

O gateway pode ser simulado em memória — não precisa de rede real.
Inclua lógica de parcelamento com juros compostos de 1,99% ao mês.
```

**Saída típica:** código bem estruturado, com `@dataclass`, constantes nomeadas
e demo funcional. O modelo não inventa edge cases que não foram pedidos — CPF e
idempotência aparecem na docstring mas não no corpo da função. O parcelamento
fica com off-by-one sutil. A comparação de assinatura de webhook usa `==`.

---

## OpenAI (Codex com AGENTS.md)

O Codex usa `AGENTS.md` como arquivo de instrução permanente. Configure as
convenções no `developer` message e envie o prompt como `user`:

```
[developer/system message — em AGENTS.md ou como system instruction]
You are a Python code generator for a Clean Code workshop (Brazilian Portuguese).
Follow these conventions:
- All public identifiers in Brazilian Portuguese
- @dataclass for data models — never raw dicts
- Full static typing with type hints
- Docstrings on all public functions
- Flat module structure — no Repository/Service class layers unless requested
- if __name__ == "__main__": block with full stdout demo

[user message]
Crie um módulo de integração com gateway de pagamento com três funções:
cobrar, estornar, consultar_status.

Gateway simulado em memória (sem rede real).
Parcelamento com juros compostos de 1,99% ao mês.
Bloco __main__ com demo de cobrança parcelada em 3x.
```

**Saída típica:** estrutura correta, mas a factory/strategy para tipos de
pagamento (cartão, PIX, boleto) costuma aparecer mesmo sem ser pedida — o
modelo infere que um gateway real teria múltiplos instrumentos. O parcelamento
terá range com off-by-one com alta probabilidade.

---

## Gemini (Gemini CLI com GEMINI.md)

Configure `GEMINI.md` com as convenções do projeto. Use a janela de contexto
ampla para colar exemplos reais do repositório como few-shot:

```
# system_instruction (em GEMINI.md):
Você é um gerador de código para um workshop de Clean Code em português.
Siga estas convenções antes de gerar qualquer código:
- Identificadores em português brasileiro
- @dataclass para entidades — nunca dicts crus
- Tipagem estática completa
- Docstrings nas funções públicas
- Funções planas no módulo — sem camadas Repository/Service a menos que pedido
- Bloco __main__ com demo de print

# prompt (cole um exemplo do repositório como few-shot antes deste bloco):
Crie um módulo de integração com gateway de pagamento com as funções:
cobrar(cobranca: Cobranca) -> ResultadoCobranca
estornar(transacao_id: str, valor: float) -> ResultadoEstorno
consultar_status(transacao_id: str) -> StatusTransacao

Gateway simulado em memória.
Parcelamento com juros compostos de 1,99% ao mês.
Demo no __main__ com cobrança de R$ 450,00 em 3x.
```

**Saída típica:** o Gemini tende a ser literal com os nomes de função fornecidos,
o que reduz a chance de over-engineering. O off-by-one no parcelamento e a
comparação de assinatura sem constant-time permanecem — são padrões que o modelo
reproduz por consistência com exemplos na internet.

---

## O que muda (e o que não muda)

| Aspecto | Claude | Codex | Gemini |
|---|---|---|---|
| Over-engineering de factory | Provável | Muito provável | Menos provável |
| Off-by-one no parcelamento | Alta chance | Alta chance | Alta chance |
| Comparação de assinatura com `==` | Alta chance | Alta chance | Alta chance |
| Docstring que mente | Alta chance | Alta chance | Moderada |
| Edge case de valor negativo | Ausente | Ausente | Ausente |
| Método alucinado em ramo não exercitado | Possível | Possível | Possível |

**Conclusão:** prompts razoáveis produzem código razoável — mas não necessariamente
correto. Os defeitos desta família (off-by-one, timing attack, edge case ausente,
docstring que mente) são ortogonais à qualidade do prompt. Eles surgem porque o
modelo não tem acesso ao comportamento em produção. A revisão crítica é o que
fecha essa lacuna.
