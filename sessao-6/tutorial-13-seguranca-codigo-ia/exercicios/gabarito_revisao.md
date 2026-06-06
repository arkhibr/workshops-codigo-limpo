# Gabarito de Revisão — Busca de Pedidos

> Este documento descreve cada brecha encontrada no `exercicio.py` / `exercicio.ts`, a correção aplicada e o item do checklist de segurança correspondente.

---

## Brecha 1 — Chave de integração hardcoded

**Onde:** linha com `CHAVE_INTEGRACAO = "tok-pedidos-abc987xyz"`

**Problema:**  
A chave de integração está literal no código-fonte. Qualquer desenvolvedor com acesso ao repositório — incluindo histórico de commits — pode ler essa credencial. Em um repositório público, a exposição é imediata.

**Correção aplicada:**

```python
# exercicio.py (inseguro)
CHAVE_INTEGRACAO = "tok-pedidos-abc987xyz"

# gabarito.py (seguro)
import os
CHAVE_INTEGRACAO = os.getenv("CHAVE_INTEGRACAO", "<não configurado>")
```

```typescript
// exercicio.ts (inseguro)
const CHAVE_INTEGRACAO = "tok-pedidos-abc987xyz";

// gabarito.ts (seguro) — em produção, configuracaoAmbiente seria process.env
const CHAVE_INTEGRACAO = configuracaoAmbiente["CHAVE_INTEGRACAO"];
```

**Checklist:** "Há segredos no código? Tokens/chaves são lidos de variáveis de ambiente?"

---

## Brecha 2 — Filtro montado por concatenação de string

**Onde:** linha com `filtro = "SELECT * FROM pedidos WHERE cliente = '" + nome_cliente + "'"`

**Problema:**  
A entrada do usuário é inserida diretamente em uma string de query SQL por concatenação. Em um banco real, uma entrada como `Ana Lima' OR '1'='1` altera a estrutura da query e pode retornar todos os registros da tabela — ou pior, executar comandos destrutivos.

O exercício demonstra isso: com aspas simples na entrada, a simulação retorna todos os pedidos em vez dos pedidos do cliente solicitado.

**Correção aplicada:**  
Eliminar completamente a concatenação. Em vez de montar uma string de query, o gabarito usa filtragem direta por comparação de valor:

```python
# gabarito.py
return [p for p in _pedidos if p["cliente"] == nome_cliente]
```

```typescript
// gabarito.ts
return pedidos.filter(p => p.cliente === nomeCliente);
```

A entrada nunca é interpretada como instrução — apenas como valor a comparar.

**Checklist:** "As consultas são parametrizadas? Entradas do usuário são concatenadas em strings de query SQL?"

---

## Brecha 3 — Sem validação do parâmetro de entrada

**Onde:** função `buscar_pedidos` / `buscarPedidos` — nenhuma verificação antes de usar o valor.

**Problema:**  
O código aceita qualquer string sem verificar formato, tamanho ou conteúdo. Isso permite:
- Entradas com caracteres especiais (aspas, hifens duplos) que alteram o comportamento.
- Entradas vazias que retornam lista vazia silenciosamente sem indicar erro.
- Entradas excessivamente longas que podem causar comportamento inesperado.

**Correção aplicada:**

```python
# gabarito.py
FORMATO_NOME_VALIDO = re.compile(r"^[A-Za-zÀ-ÿ\s]{2,80}$")

def _validar_nome_cliente(nome_cliente: str) -> None:
    if not FORMATO_NOME_VALIDO.match(nome_cliente):
        raise ValueError(
            f"Nome inválido: '{nome_cliente}'. "
            "Esperado: letras e espaços, entre 2 e 80 caracteres."
        )
```

A validação é feita em função separada (responsabilidade única) e executa **antes** de qualquer operação de busca.

**Checklist:** "A entrada externa é validada? O código verifica formato, tamanho e tipo antes de usar o valor?"

---

## Checklist de Segurança — Aplicado a Este Caso

| # | Pergunta | exercicio | gabarito |
|---|----------|-----------|---------|
| 1 | Há segredos no código? | ✗ Sim — `CHAVE_INTEGRACAO` hardcoded | ✓ Lida de `os.getenv` / `process.env` |
| 2 | As consultas são parametrizadas? | ✗ Não — concatenação de string | ✓ Comparação direta por valor |
| 3 | A entrada externa é validada? | ✗ Não — aceita qualquer valor | ✓ Regex com tamanho máximo |
| 4 | As permissões são mínimas? | ✓ Sem acesso a recursos externos | ✓ Sem acesso a recursos externos |
| 5 | As dependências são confiáveis? | ✓ Sem dependências externas | ✓ Sem dependências externas |
| 6 | Dados sensíveis são logados? | Parcial — a query (com dados do usuário) é impressa | ✓ Apenas contagem e resultado limpo |

---

## Resumo

As três brechas do exercício são as mais frequentes em código gerado por IA:  
a credencial hardcoded aparece porque a IA quer fazer o código funcionar imediatamente;  
a concatenação de string aparece porque é a forma mais simples de montar um filtro;  
a ausência de validação aparece porque a IA assume entradas bem-comportadas.

A correção segue um padrão consistente: **configuração fora do código, validação antes de qualquer uso, e parametrização por design (sem concatenação).**
