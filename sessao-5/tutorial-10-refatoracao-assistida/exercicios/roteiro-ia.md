# Roteiro Hands-on — Refatoração Assistida Passo a Passo

> Duração estimada: 25–35 minutos
> Pré-requisito: acesso a um assistente de IA (ChatGPT, Claude, Gemini, Copilot ou similar)

---

## Objetivo

Refatorar a função monolítica do exercício usando a IA como parceira — pedindo **um passo por vez** e rodando o arquivo após cada passo para confirmar que o comportamento foi preservado.

---

## Passo a Passo

### 1. Leia o exercício e liste as responsabilidades

Abra `exercicio.py` (ou `exercicio.ts`) e rode localmente:

```bash
python3 sessao-5/tutorial-10-refatoracao-assistida/exercicios/exercicio.py
```

Anote a saída — você vai comparar com ela após cada passo. Em seguida, leia o código e liste pelo menos **quatro responsabilidades** que a função `processar` acumula. Use as categorias do Tutorial 10:

- Lê e divide as linhas do CSV?
- Valida número de campos?
- Valida campos obrigatórios?
- Converte tipos?
- Aplica regra de negócio?

---

### 2. Extraia a leitura (Passo 1)

Envie para a IA:

```
Tenho a função abaixo que importa produtos de um CSV. Extraia APENAS
a parte que lê as linhas do CSV (divide por "\n" e descarta o cabeçalho)
para uma função chamada ler_linhas(conteudo_csv: str) -> list[str].

Não altere nada mais — não mova validações, conversões nem regras de
negócio. Mantenha o comportamento exatamente igual.

[cole o código do exercicio.py aqui]
```

Copie o código gerado para `exercicio.py`, substitua o conteúdo e rode:

```bash
python3 sessao-5/tutorial-10-refatoracao-assistida/exercicios/exercicio.py
```

**Verifique:** a saída deve ser idêntica à do Passo 1. Se não for, identifique o que mudou antes de continuar.

---

### 3. Extraia a validação (Passo 2)

Envie para a IA:

```
Agora extraia APENAS a verificação que descarta linhas inválidas
para uma função chamada validar_produto(campos: list[str]) -> bool.

A função deve retornar True se o número de campos for correto, os
campos obrigatórios estiverem preenchidos e os valores numéricos
forem convertíveis. Não mova nem altere a lógica de conversão nem
a regra de negócio de preço/quantidade. Mantenha o comportamento
exatamente igual.

[cole o código do passo anterior aqui]
```

Substitua e rode novamente. Confirme que a saída é idêntica.

---

### 4. Extraia a conversão (Passo 3)

Envie para a IA:

```
Agora extraia APENAS a montagem do dicionário de produto para uma
função chamada converter_produto(campos: list[str]) -> dict.

A função deve converter os tipos e retornar o dicionário com nome,
categoria, preco (float) e quantidade (int). Não altere a validação
nem a regra de negócio. Mantenha o comportamento exatamente igual.

[cole o código do passo anterior aqui]
```

Substitua e rode. Confirme que a saída é idêntica.

---

### 5. Extraia o filtro de negócio (Passo 4)

Envie para a IA:

```
Agora extraia APENAS a regra de negócio que descarta produtos
inválidos (preço não positivo ou quantidade negativa) para uma
função chamada filtrar_produto(produto: dict) -> bool.

Não altere nenhuma outra parte do código. Mantenha o comportamento
exatamente igual.

[cole o código do passo anterior aqui]
```

Substitua e rode. Confirme que a saída é idêntica.

---

### 6. Renomeie e compare com o gabarito

Peça à IA:

```
Renomeie a função principal de processar para importar_produtos e
renomeie as variáveis locais de abreviações para nomes descritivos
em português (res → produtos, rows → linhas, cols → campos, etc.).
Não altere a lógica. Mantenha o comportamento exatamente igual.

[cole o código do passo anterior aqui]
```

Rode uma última vez e compare com o gabarito:

```bash
python3 sessao-5/tutorial-10-refatoracao-assistida/exercicios/gabarito.py
```

As saídas devem ser idênticas.

---

### 7. Reflexão

Responda para cada critério abaixo:

| # | Critério                                                              | Atendido? |
|---|-----------------------------------------------------------------------|-----------|
| 1 | Pedi um passo por vez, sem permitir outras mudanças?                  |           |
| 2 | Rodei o arquivo após cada passo?                                      |           |
| 3 | O comportamento foi preservado em todos os passos?                    |           |
| 4 | Cada função tem uma única responsabilidade?                           |           |
| 5 | É possível nomear cada função sem usar "e"?                           |           |
| 6 | A função principal ficou apenas orquestrando, sem lógica inline?      |           |

---

## Aviso — Fallback sem IA

Se você não tiver acesso a um assistente de IA no momento, refatore diretamente o `exercicio.py` / `exercicio.ts` seguindo os passos acima manualmente. O objetivo é a **prática da refatoração em passos verificáveis** — a IA é uma ferramenta, não o foco. Use o `gabarito_revisao.md` como referência para a sequência de passos.

---

## Reflexão final

> Refatorar com IA em passos pequenos não é mais lento do que pedir a reescrita inteira — é mais seguro. Cada verificação intermediária leva 10 segundos. A alternativa é uma revisão completa de um código que você não escreveu, em busca de mudanças sutis que talvez só apareçam em produção.

Discuta com o grupo: em que situação você ainda usaria o prompt aberto "melhora esse código"? Quando o risco é aceitável?
