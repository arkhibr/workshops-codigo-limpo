# Prompt Aberto vs. Prompt Dirigido — Refatoração Passo a Passo

> Um prompt de refatoração aberto reescreve o código inteiro de uma vez. Um prompt dirigido extrai uma responsabilidade e para — permitindo verificação após cada passo.

---

## Prompt Aberto

```
melhora esse código
```

**Por que é arriscado:** a IA pode renomear variáveis, reorganizar fluxos, extrair funções e alterar o tratamento de casos de borda — tudo ao mesmo tempo, em uma única resposta. Você perde rastreabilidade: se o comportamento mudar em algum caso de borda, não saberá qual passo causou o problema.

**Resultado típico:** código mais legível, mas com diferenças sutis que só aparecem em produção — um `continue` removido aqui, um default diferente ali.

> Arquivo de exemplo: `importacao_gerado.py` / `importacao_gerado.ts`

---

## Prompt Dirigido (em passos)

Em vez de um único prompt, use uma sequência — um por responsabilidade:

### Passo 1 — Extrair a leitura

```
Tenho a função abaixo. Extraia APENAS a parte que lê as linhas do CSV
(descarta o cabeçalho e divide por "\n") para uma função chamada
ler_linhas(conteudo_csv: str) -> list[str].

Não altere nada mais — não renomeie variáveis, não mova lógica de
validação ou conversão. Mantenha o comportamento exatamente igual.

[cole o código aqui]
```

**Verifique:** rode o arquivo. A saída deve ser idêntica.

---

### Passo 2 — Extrair a validação

```
Agora extraia APENAS a verificação que descarta linhas inválidas
para uma função chamada validar_cliente(campos: list[str]) -> bool.

A função deve retornar True se os campos forem válidos, False caso
contrário. Não mova nem altere a lógica de conversão. Mantenha o
comportamento exatamente igual.

[cole o código do passo 1 aqui]
```

**Verifique:** rode o arquivo. A saída deve ser idêntica.

---

### Passo 3 — Extrair a conversão

```
Agora extraia APENAS a montagem do dicionário de cliente para uma
função chamada converter_cliente(campos: list[str]) -> dict.

Não altere a lógica de validação nem o loop principal. Mantenha o
comportamento exatamente igual.

[cole o código do passo 2 aqui]
```

**Verifique:** rode o arquivo. A saída deve ser idêntica.

---

## O que muda na prática

| Dimensão              | Prompt aberto                          | Prompt dirigido (passos)                    |
|-----------------------|----------------------------------------|---------------------------------------------|
| Escopo por resposta   | Todo o código reescrito de uma vez     | Uma responsabilidade extraída               |
| Verificabilidade      | Difícil isolar regressões              | Roda após cada passo; regressão localizada  |
| Rastreabilidade       | Não sabe o que mudou exatamente        | Cada passo tem uma mudança identificada     |
| Confiança no resultado | Depende de revisão completa           | Comportamento confirmado passo a passo      |
| Risco de regressão    | Alto — a IA pode alterar casos de borda | Baixo — mudança mínima e verificada        |

**Conclusão:** o prompt dirigido não é mais trabalhoso — é mais seguro. Cada verificação intermediária leva 10 segundos (`python3 arquivo.py`). A alternativa é uma revisão completa do código reescrito para encontrar mudanças sutis que talvez só apareçam em produção.
