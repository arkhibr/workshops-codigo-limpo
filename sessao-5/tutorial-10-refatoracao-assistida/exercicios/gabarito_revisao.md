# Gabarito de Revisão — Importação de Catálogo de Produtos

> Este documento lista os problemas de coesão do `exercicio.py` / `exercicio.ts` e a sequência de passos de refatoração sugerida.

---

## Problemas de coesão identificados

### 1. Função com nome genérico fazendo cinco coisas

A função `processar` não tem nome descritivo e acumula cinco responsabilidades distintas:

| Responsabilidade                          | Onde aparece                              |
|-------------------------------------------|-------------------------------------------|
| Leitura e divisão das linhas do CSV       | `data.strip().split("\n")[1:]`            |
| Validação de número de campos             | `if len(cols) != 4: continue`             |
| Validação de campos obrigatórios          | `if not nm or not cat: continue`          |
| Conversão de tipos (`float`, `int`)       | `preco = float(pr)` / `qtd = int(qt)`     |
| Aplicação de regra de negócio (filtro)    | `if preco <= 0 or qtd < 0: continue`      |

O sinal claro: para nomear a função com precisão, precisaríamos de "ler *e* validar *e* converter *e* filtrar *e* acumular".

### 2. Nomes de variáveis sem intenção

| Identificador | Problema                          | Solução                |
|---------------|-----------------------------------|------------------------|
| `data`        | Genérico demais                   | `conteudo_csv`         |
| `res`         | Abreviação de resultado de quê?   | `produtos`             |
| `rows`        | Inglês                            | `linhas`               |
| `r`           | Uma letra sem contexto            | `linha`                |
| `cols`        | Inglês                            | `campos`               |
| `nm`          | Abreviação                        | `nome`                 |
| `cat`         | Abreviação                        | `categoria`            |
| `pr`          | Abreviação                        | `preco_str`            |
| `qt`          | Abreviação                        | `quantidade_str`       |

> `preco_str` / `quantidade_str` são nomes úteis durante a refatoração. Na versão final do gabarito, a conversão acontece direto (`float(campos[INDICE_PRECO].strip())`), eliminando a variável intermediária — uma simplificação que surge naturalmente quando a função já está coesa.

### 3. Índices mágicos de acesso a lista

`cols[0]`, `cols[1]`, `cols[2]`, `cols[3]` não dizem o que estão acessando. A versão revisada usa constantes nomeadas: `INDICE_NOME`, `INDICE_CATEGORIA`, `INDICE_PRECO`, `INDICE_QUANTIDADE`.

### 4. Regra de negócio misturada com conversão de dados

A verificação `preco <= 0 or qtd < 0` é uma regra de negócio (o que constitui um produto válido para importar), mas está no mesmo bloco que a conversão de tipos. Mudar a regra exige tocar no código de conversão.

### 5. `any[]` / tipo implícito sem contrato

O tipo de retorno `any[]` (TS) ou a ausência de tipo (Python) não documenta o contrato. Um `Produto` / `dict` tipado explicita o que o chamador pode esperar.

---

## Sequência de passos de refatoração

### Passo 1 — Extrair a leitura

Crie `ler_linhas(conteudo_csv)` que divide o conteúdo e descarta o cabeçalho. A função principal passa a chamar `ler_linhas` em vez de fazer o split inline.

**Verifique:** rode o arquivo. A saída deve ser idêntica.

---

### Passo 2 — Extrair a validação

Crie `validar_produto(campos)` que verifica o número de campos, os campos obrigatórios e a conversibilidade de tipos. A função principal passa a chamar `validar_produto` e pular linhas inválidas.

**Verifique:** rode o arquivo. A saída deve ser idêntica.

---

### Passo 3 — Extrair a conversão

Crie `converter_produto(campos)` que converte os campos para os tipos corretos e monta o dicionário/objeto. A função principal passa a chamar `converter_produto` em vez de fazer as conversões inline.

**Verifique:** rode o arquivo. A saída deve ser idêntica.

---

### Passo 4 — Extrair o filtro de negócio

Crie `filtrar_produto(produto)` que aplica as regras de negócio (preço positivo, quantidade não negativa). A função principal passa a chamar `filtrar_produto` após a conversão.

**Verifique:** rode o arquivo. A saída deve ser idêntica.

---

### Passo 5 — Renomear e tipar

Renomeie `processar` para `importar_produtos` e adicione tipos explícitos aos parâmetros e retornos. Renomeie as variáveis locais de abreviações para nomes descritivos.

**Verifique:** rode o arquivo. A saída deve ser idêntica.

---

## Resultado esperado

Após os cinco passos, a função `importar_produtos` deve ter este formato:

```python
def importar_produtos(conteudo_csv: str) -> list[dict]:
    produtos = []
    for linha in ler_linhas(conteudo_csv):
        campos = linha.split(SEPARADOR_CSV)
        if not validar_produto(campos):
            continue
        produto = converter_produto(campos)
        if filtrar_produto(produto):
            produtos.append(produto)
    return produtos
```

Cada função auxiliar é testável isoladamente. A orquestradora não contém lógica de negócio — apenas chama funções nomeadas que revelam sua intenção.
