# Prompt de Exemplo — Segurança em Código Gerado por IA

Este arquivo compara dois prompts para a mesma funcionalidade: um endpoint de consulta de cliente por ID. O contraste mostra como requisitos de segurança explícitos no prompt elevam a qualidade do ponto de partida.

---

## Prompt funcional puro

```
Cria uma função Python que recebe um ID de cliente e retorna os dados desse cliente consultando um banco de dados.
```

### Saída típica da IA

```python
DB_PASSWORD = "admin123"  # credencial hardcoded
DB_URL = "mysql://admin:admin123@localhost/clientes"

def consultar_cliente(id):
    query = f"SELECT * FROM clientes WHERE id = {id}"  # concatenação — injeção
    return executar_query(query)  # sem validação do parâmetro
```

**Problemas gerados:**
- Credencial hardcoded diretamente no código.
- Query montada por concatenação de string — vulnerável a injeção de SQL.
- Nenhuma validação do parâmetro `id` — aceita qualquer valor, inclusive strings maliciosas.
- Função sem tipo de retorno explícito, sem tratamento de ID inexistente.

---

## Prompt com requisitos de segurança

```
Contexto: sistema de gestão de clientes. Todos os identificadores em português brasileiro.

Cria uma função que consulta cliente por ID com os seguintes requisitos obrigatórios:

Segurança:
- Não use segredos ou credenciais hardcoded — leia de variáveis de ambiente (ou de um dict de configuração nomeado, para fins de demonstração).
- Parametrize a consulta — nunca concatene a entrada do usuário diretamente em strings.
- Valide a entrada: o ID deve conter apenas dígitos, de 1 a 10 caracteres. Rejeite com ValueError e mensagem clara.
- Retorne None ou levante ValueError com mensagem clara se o ID não for encontrado.

Clean Code:
- Identificadores em português brasileiro.
- Cada função tem uma única responsabilidade.
- Sem números mágicos — use constantes nomeadas.

Linguagem: Python 3.10+. Sem frameworks externos. Simule o banco de dados com um dict em memória.
```

### Saída típica da IA

```python
import re
import os

FORMATO_ID_VALIDO = re.compile(r"^\d{1,10}$")

# configuração lida de variável de ambiente (sem segredo no código)
CHAVE_API_INTERNA = os.getenv("CHAVE_API_INTERNA", "")

# banco simulado em memória
_banco_clientes: dict[str, dict] = {
    "1001": {"nome": "Ana Lima", "email": "ana@exemplo.com"},
    "2002": {"nome": "Carlos Souza", "email": "carlos@exemplo.com"},
}

def _validar_id_cliente(id_cliente: str) -> None:
    if not FORMATO_ID_VALIDO.match(id_cliente):
        raise ValueError(
            f"ID inválido: '{id_cliente}'. Esperado: até 10 dígitos numéricos."
        )

def consultar_cliente(id_cliente: str) -> dict:
    _validar_id_cliente(id_cliente)
    cliente = _banco_clientes.get(id_cliente)
    if cliente is None:
        raise ValueError(f"Cliente com ID '{id_cliente}' não encontrado.")
    return cliente
```

**Melhorias produzidas pelo prompt mais forte:**
- Nenhuma credencial no código-fonte.
- Validação explícita com regex e mensagem de erro descritiva.
- Consulta parametrizada por design (busca em dict por chave exata — sem concatenação de string).
- Identificadores em português, responsabilidades separadas.

---

## O prompt não substitui a revisão

Mesmo com um prompt forte, a saída da IA deve ser revisada com o checklist de segurança do tutorial antes de ir para o código-base. A IA pode:

- Gerar validação parcial (verifica formato mas não tamanho máximo).
- Usar uma versão antiga de uma biblioteca sugerida com CVEs conhecidos.
- Logar dados sensíveis em mensagens de erro.
- Ignorar requisitos que conflitem com a solução mais simples.

O prompt forte reduz o trabalho de revisão — não o elimina.
