# Tutorial 13 — Segurança em Código Gerado por IA

> Referência: modos de falha de segurança em código de IA; complementa o tutorial 12

---

## 1. Contexto e Motivação

A IA gera código funcional com rapidez — mas "funcional" e "seguro" não são sinônimos. Assistentes de IA foram treinados em repositórios públicos que contêm exemplos de código inseguro tanto quanto seguros. Ao gerar um endpoint que consulta dados por parâmetro, a IA tende a produzir a versão mais simples e direta — que costuma ser exatamente a mais perigosa.

O desenvolvedor que revisa código gerado por IA precisa adicionar uma camada de atenção à segurança que vai além do Clean Code convencional: nomes claros, funções pequenas e comentários bons não protegem um sistema de injeção de SQL, credenciais expostas ou entradas não validadas.

Este tutorial mapeia as **brechas que a IA produz com mais frequência**, ensina como preveni-las no próprio prompt e como identificá-las na revisão.

---

## 2. Conceito Central

### As cinco brechas mais frequentes em código gerado por IA

#### 2.1 Segredos hardcoded

A IA escreve código que funciona — e para funcionar, coloca credenciais diretamente no código.

**Gerado (inseguro):**
```python
DB_SENHA = "s3nh4_producao_2024"
API_KEY = "sk-abc123xyz789"
```

**Revisado (seguro):**
```python
import os
DB_SENHA = os.getenv("DB_SENHA")  # lida de variável de ambiente
API_KEY = os.getenv("API_KEY")
```

Por que a IA faz isso? O código de treinamento muitas vezes contém credenciais de desenvolvimento hardcoded, e a IA replica esse padrão. Um segredo no código-fonte é um segredo exposto a qualquer um com acesso ao repositório.

---

#### 2.2 Injeção (SQL, comando, template)

Ao gerar uma consulta que recebe parâmetro externo, a IA frequentemente monta a string por concatenação — a forma mais antiga e perigosa.

**Gerado (inseguro — injeção de SQL):**
```python
# entrada do usuário: "1 OR 1=1"
query = f"SELECT * FROM clientes WHERE id = {parametro}"
# resulta em: SELECT * FROM clientes WHERE id = 1 OR 1=1
# retorna TODOS os registros
```

**Revisado (seguro — consulta parametrizada):**
```python
# a mesma entrada "1 OR 1=1" é tratada como valor literal
resultado = banco.get(parametro)  # busca exata; não interpreta SQL
```

A injeção funciona porque o banco (ou o interpretador de comandos) não distingue instrução de dado quando tudo chega como texto. Consultas parametrizadas separam estrutura de dados por design.

---

#### 2.3 Falta de validação de entrada externa

A IA assume que quem chama a função é bem-intencionado e envia dados no formato correto.

**Gerado (inseguro):**
```python
def consultar_cliente(id_cliente):
    return banco[id_cliente]  # KeyError se não existir; aceita qualquer valor
```

**Revisado (seguro):**
```python
FORMATO_ID_VALIDO = re.compile(r"^\d{1,10}$")

def consultar_cliente(id_cliente: str) -> dict:
    if not FORMATO_ID_VALIDO.match(str(id_cliente)):
        raise ValueError(f"ID inválido: '{id_cliente}'. Esperado: até 10 dígitos.")
    return banco.get(id_cliente)
```

Sem validação, a entrada controla o comportamento do sistema. Com validação, o sistema recusa explicitamente entradas que não correspondem ao contrato esperado.

---

#### 2.4 Dependências vulneráveis

A IA sugere bibliotecas que conhece do treinamento — mas seu conhecimento tem data de corte. Ela pode sugerir versões antigas com CVEs conhecidos, ou bibliotecas abandonadas.

**Gerado (arriscado):**
```
pip install requests==2.18.0  # versão de 2017; CVEs conhecidos
```

**Revisado:**
```
pip install requests  # versão mais recente
# ou: especificar um range mínimo: requests>=2.28.0
```

Estratégia: sempre verificar a versão sugerida com `pip index versions <pacote>` e consultar o banco de CVEs do NIST antes de fixar uma versão antiga.

---

#### 2.5 Permissões amplas demais

A IA gera o código mais simples que atende ao pedido — o que significa usar as permissões mais amplas disponíveis.

**Gerado (arriscado):**
```python
# lê, escreve e deleta sem distinção
with open(caminho_arquivo, "r+") as arquivo:
    ...
```

**Revisado:**
```python
# abre apenas para leitura — minimiza superfície de dano
with open(caminho_arquivo, "r") as arquivo:
    ...
```

O princípio do menor privilégio: cada componente deve ter acesso apenas ao que precisa para sua função específica. Pedir mais do que o necessário é ampliar desnecessariamente o impacto de qualquer falha.

---

### Como pedir segurança no prompt

A IA responde a restrições explícitas. Adicionar requisitos de segurança ao prompt eleva o ponto de partida:

**Prompt funcional puro (arriscado como ponto de partida):**
```
Cria um endpoint que consulta cliente por ID no banco de dados.
```

**Prompt com requisitos de segurança:**
```
Cria uma função que consulta cliente por ID.
Requisitos de segurança obrigatórios:
- Não use segredos ou credenciais hardcoded — leia de variáveis de ambiente.
- Parametrize a consulta — nunca concatene entrada do usuário em strings de query.
- Valide a entrada: rejeite IDs que não sejam dígitos (1–10 caracteres).
- Retorne erro claro (exceção com mensagem) para entrada inválida ou ID não encontrado.
```

Isso não elimina a necessidade de revisão, mas reduz significativamente os anti-padrões de segurança na saída inicial.

---

## 3. Exercício

O exercício está em `exercicios/` e simula o cenário mais comum: a IA gerou uma função de busca de pedidos com brechas de segurança. Sua tarefa:

1. Tire o segredo do código (variável de configuração ou ambiente).
2. Parametrize e valide a entrada do usuário.
3. Liste todas as brechas que você encontrou antes de corrigir.

```bash
# Veja o código a ser corrigido:
python3 sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/exercicio.py

# Compare com a solução de referência:
python3 sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/gabarito.py
```

> Arquivo: [`exercicios/exercicio.py`](exercicios/exercicio.py) · [`exercicios/exercicio.ts`](exercicios/exercicio.ts)  
> Gabarito: [`exercicios/gabarito.py`](exercicios/gabarito.py) · [`exercicios/gabarito.ts`](exercicios/gabarito.ts)  
> Revisão comentada: [`exercicios/gabarito_revisao.md`](exercicios/gabarito_revisao.md)  
> Roteiro hands-on: [`exercicios/roteiro-ia.md`](exercicios/roteiro-ia.md)

---

## 4. Checklist de Segurança

Use estas perguntas ao revisar qualquer saída de IA que envolva dados externos, credenciais ou consultas:

1. **Há segredos no código?** — Procure strings que se parecem com chaves, senhas ou tokens: `password =`, `api_key =`, `sk-`, `Bearer`.
2. **As consultas são parametrizadas?** — Entradas do usuário são concatenadas em strings de query SQL, shell ou template?
3. **A entrada externa é validada?** — O código verifica formato, tamanho e tipo antes de usar o valor recebido?
4. **As permissões são mínimas?** — O código acessa arquivos, APIs ou recursos com o menor nível de permissão necessário?
5. **As dependências são confiáveis?** — Versões fixadas correspondem a releases sem CVEs conhecidos?
6. **Dados sensíveis são logados?** — CPF, senhas, tokens aparecem em mensagens de erro ou logs?

---

## 5. Referências

- **OWASP Top 10** — vulnerabilidades mais críticas em aplicações web (owasp.org/www-project-top-ten)
- **NIST National Vulnerability Database** — base de CVEs consultável por biblioteca/versão (nvd.nist.gov)
- **Clean Code**, Robert C. Martin — Capítulo 7: *Error Handling* (p. 103–112)
- Tutorial 12: [`../tutorial-12-revisao-critica-ia/checklist_revisao_ia.md`](../tutorial-12-revisao-critica-ia/checklist_revisao_ia.md)
- Arquivos de exemplo: [`exemplos/prompt.md`](exemplos/prompt.md) · [`exemplos/consulta_gerado.py`](exemplos/consulta_gerado.py) · [`exemplos/consulta_revisado.py`](exemplos/consulta_revisado.py)

---

> **Próximo tutorial:** [Tutorial 14 — Testes como Guard-Rails](../tutorial-14-testes-guard-rails/README.md) *(em breve)*
