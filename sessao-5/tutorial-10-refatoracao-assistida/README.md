# Tutorial 10 — Refatoração Assistida: Coesão e Legibilidade

> Referência: *Clean Code*, Cap. 3 (Funções)

---

## 1. Contexto e Motivação

Quando a IA gera código funcional mas monolítico, o instinto é aceitar — o resultado roda, o teste passa, o prazo fecha. O problema aparece três semanas depois, quando alguém precisa corrigir a validação e quebra inadvertidamente a leitura do arquivo, porque estavam na mesma função.

A refatoração assistida inverte a lógica: em vez de pedir à IA "melhora esse código" e aceitar a reescrita inteira, você pede **um passo por vez** — extraia essa função, renomeie essa variável, separe essa responsabilidade. Entre cada passo você roda o arquivo e confirma que o comportamento foi preservado.

Essa abordagem tem duas vantagens concretas:

1. **Rastreabilidade:** cada passo produz uma mudança pequena e verificável. Se algo quebra, você sabe exatamente onde.
2. **Aprendizado:** você entende o que está sendo alterado — em vez de receber código novo que você não escreveu e não consegue explicar.

---

## 2. Conceito Central

### Coesão: uma função, uma responsabilidade

Uma função com baixa coesão faz várias coisas ao mesmo tempo. O sinal mais claro é quando você não consegue nomeá-la sem usar "e":

```python
# Baixa coesão — nome com "e"
def importar_e_validar_e_converter(arquivo):
    ...

# Alta coesão — cada função nomeia uma coisa
def ler_linhas(conteudo_csv):     ...
def validar_cliente(linha):       ...
def converter_cliente(linha):     ...
def importar_clientes(conteudo):  ...
```

A função monolítica não é errada porque é grande — é errada porque mistura responsabilidades que mudam por motivos diferentes. A regra de validação pode mudar sem afetar a leitura; o formato de saída pode mudar sem afetar a validação.

### Refatorar em passos pequenos e verificáveis

O ciclo de um passo de refatoração:

```
1. Identifique uma responsabilidade na função grande.
2. Peça à IA: "Extraia [responsabilidade X] para uma função própria. Não altere mais nada."
3. Rode o arquivo. Confirme que a saída é idêntica.
4. Repita para a próxima responsabilidade.
```

Compare com o prompt aberto:

```
# Prompt aberto (arriscado)
"Melhora esse código"

# Prompt dirigido (seguro)
"Extraia apenas a parte que lê as linhas do CSV para uma função chamada
ler_linhas. Mantenha o resto exatamente igual. Não renomeie variáveis
fora dessa função."
```

O prompt aberto pode reestruturar o código inteiro de uma vez — você perde rastreabilidade e pode não perceber que o comportamento mudou em um caso de borda.

### Fragmentos antes e depois

Versão gerada (monolítica):

```python
def importar(csv):
    r = []
    for l in csv.strip().split("\n")[1:]:
        p = l.split(",")
        if len(p) != 3:
            continue
        n, e, c = p[0].strip(), p[1].strip(), p[2].strip()
        if not n or not e or "@" not in e:
            continue
        r.append({"nome": n, "email": e, "cidade": c})
    return r
```

Versão revisada (coesa):

```python
def ler_linhas(conteudo_csv: str) -> list[str]:
    linhas = conteudo_csv.strip().split("\n")
    return linhas[1:]  # descarta cabeçalho

def validar_cliente(campos: list[str]) -> bool:
    if len(campos) != 3:
        return False
    nome, email, _ = campos
    return bool(nome.strip()) and bool(email.strip()) and "@" in email

def converter_cliente(campos: list[str]) -> dict:
    nome, email, cidade = campos
    return {"nome": nome.strip(), "email": email.strip(), "cidade": cidade.strip()}

def importar_clientes(conteudo_csv: str) -> list[dict]:
    clientes = []
    for linha in ler_linhas(conteudo_csv):
        campos = linha.split(",")
        if validar_cliente(campos):
            clientes.append(converter_cliente(campos))
    return clientes
```

A saída é idêntica. O que mudou foi a capacidade de testar, corrigir e entender cada parte separadamente.

---

## 3. Exercício

O exercício está em `exercicios/` e tem duas partes:

**Parte estática** (`exercicio.py` / `exercicio.ts`): função monolítica que importa um catálogo de produtos fazendo tudo junto — leitura, validação, conversão e acumulação. Sua tarefa:
1. Refatore em passos pequenos, extraindo uma responsabilidade por vez.
2. Rode o arquivo após cada passo para confirmar que a saída é preservada.
3. Liste as responsabilidades que você separou.

```bash
# Veja o código a ser refatorado:
python3 sessao-5/tutorial-10-refatoracao-assistida/exercicios/exercicio.py

# Compare com a solução de referência:
python3 sessao-5/tutorial-10-refatoracao-assistida/exercicios/gabarito.py
```

**Parte hands-on** (`roteiro-ia.md`): use o seu assistente de IA com prompts dirigidos para refatorar passo a passo, rodando o arquivo após cada passo para confirmar o comportamento.

> Arquivo: [`exercicios/exercicio.py`](exercicios/exercicio.py) · [`exercicios/exercicio.ts`](exercicios/exercicio.ts)
> Gabarito: [`exercicios/gabarito.py`](exercicios/gabarito.py) · [`exercicios/gabarito.ts`](exercicios/gabarito.ts)
> Revisão comentada: [`exercicios/gabarito_revisao.md`](exercicios/gabarito_revisao.md)
> Roteiro hands-on: [`exercicios/roteiro-ia.md`](exercicios/roteiro-ia.md)

---

## 4. Checklist de Refatoração Assistida

Use estas perguntas a cada passo de refatoração:

1. **Pedi um passo por vez?** — O prompt especificou exatamente uma extração ou renomeação, sem permitir mudanças além disso?
2. **Rodei o arquivo após cada passo?** — A saída foi idêntica antes e depois da alteração?
3. **O comportamento foi preservado?** — Nenhum caso de borda foi silenciosamente alterado?
4. **Cada função tem uma única responsabilidade?** — É possível nomear a função sem usar "e" (ler *e* validar)?
5. **Os nomes revelam intenção?** — `ler_linhas`, `validar_cliente` e `converter_cliente` dizem o que fazem sem precisar de comentário?
6. **A função principal ficou mais curta?** — A orquestradora deve apenas chamar as funções, sem conter lógica de negócio diretamente.

---

## 5. Referências

- **Clean Code**, Robert C. Martin — Capítulo 3: *Functions* (p. 31–52), especialmente *"Do One Thing"* (p. 35) e *"One Level of Abstraction per Function"* (p. 36)
- Arquivos de exemplo: [`exemplos/prompt.md`](exemplos/prompt.md) · [`exemplos/importacao_gerado.py`](exemplos/importacao_gerado.py) · [`exemplos/importacao_revisado.py`](exemplos/importacao_revisado.py)

---

> **Tutorial anterior:** [Tutorial 09 — Engenharia de Prompt para Código Limpo](../tutorial-09-engenharia-de-prompt/README.md)
