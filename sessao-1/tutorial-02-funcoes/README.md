# Tutorial 02 — Funções

> **Sessão 1 · Bloco 2 · 25 min de teoria + 15 min de exercício**
> Referência: *Clean Code*, Capítulo 3 — Functions

---

## 1. Contexto e Motivação

Se nomes são a menor unidade de código legível, funções são a primeira unidade de comportamento. Uma função bem escrita é uma **promessa**: o nome diz o que ela faz, e o corpo cumpre exatamente essa promessa — sem surpresas.

O problema mais comum em bases de código legadas não é código incorreto, é código correto que ninguém mais consegue modificar com segurança. Funções longas que fazem muita coisa são a principal causa desse problema.

---

## 2. Conceito Central

### A regra do "faz uma coisa"

> *"Functions should do one thing. They should do it well. They should do it only."*
> — Robert C. Martin, Clean Code, p. 35

"Uma coisa" é mais rigoroso do que parece. Uma função que valida, calcula e formata está fazendo três coisas. O teste prático: você consegue extrair alguma lógica dela em outra função com um nome significativo? Se sim, ela está fazendo mais de uma coisa.

### Princípios fundamentais

| Princípio | Descrição |
|---|---|
| **Tamanho pequeno** | Funções devem ter raramente mais de 20 linhas |
| **Um nível de abstração** | Não misture lógica de alto nível com detalhes de implementação |
| **Sem flags booleanas** | `formatar(nome, True)` — o `True` não diz nada; crie duas funções |
| **Sem efeitos colaterais** | A função só faz o que o nome promete |
| **Máximo 2 argumentos** | Mais que isso, considere um objeto/dataclass |
| **Prefira exceções a códigos de erro** | Retornar `-1` ou `None` como sinal de erro obriga o chamador a checar |

---

## 3. O Problema na Prática

```python
# Esta função faz quatro coisas: valida, calcula, aplica desconto e salva
def processar_pedido(pedido_id, usuario_id, itens, cupom, endereco):
    if not usuario_id:
        return {"erro": "usuário inválido"}          # 1. valida

    total = 0
    for item in itens:
        total += item["preco"] * item["quantidade"]  # 2. calcula

    if cupom == "DESCONTO10":
        total = total * 0.90                         # 3. aplica desconto
    elif cupom == "DESCONTO20":
        total = total * 0.80

    print(f"[DB] Salvando pedido {pedido_id}...")   # 4. persiste
    return {"pedido_id": pedido_id, "total": total}
```

**Problema adicional — flag booleana:**
```python
# O que significa `True` aqui? Só dá pra saber lendo a implementação.
formatar_nome("João", True)
```

> Arquivo completo: [`exemplos/funcoes_ruins.py`](exemplos/funcoes_ruins.py)

---

## 4. A Solução

```python
# Cada função tem uma única responsabilidade e um nome que a descreve

def validar_usuario(usuario_id):
    if not usuario_id:
        raise ValueError("ID de usuário não pode ser vazio")

def calcular_total_itens(itens):
    return sum(item["preco"] * item["quantidade"] for item in itens)

def aplicar_cupom(total, cupom):
    multiplicador = CUPONS.get(cupom, 1.0)
    return total * multiplicador

def processar_pedido(pedido_id, usuario_id, itens, cupom, endereco):
    validar_usuario(usuario_id)                          # delega validação
    total = calcular_total_itens(itens)                  # delega cálculo
    total_com_desconto = aplicar_cupom(total, cupom)     # delega desconto
    salvar_pedido(pedido_id, usuario_id, total_com_desconto, endereco)
    return {"pedido_id": pedido_id, "total": total_com_desconto}
```

**Solução para flag booleana:**
```python
# Duas funções, intenção imediatamente clara na chamada
formatar_nome_informal("João")
formatar_nome_formal("João")
```

> Arquivo completo: [`exemplos/funcoes_boas.py`](exemplos/funcoes_boas.py)

---

## 5. Equivalentes em Outras Linguagens

### PHP

```php
// ❌ Flag booleana
function formatarNome(string $nome, bool $formal): string { ... }

// ✅ Duas funções
function formatarNomeInformal(string $nome): string { return $nome; }
function formatarNomeFormal(string $nome): string   { return "Sr(a). $nome"; }
```

### TypeScript

```typescript
// ✅ Objeto em vez de lista longa de parâmetros
interface DadosUsuario { nome: string; email: string; perfil: string; ativo: boolean; }

function criarUsuario(dados: DadosUsuario): DadosUsuario { return { ...dados }; }
```

### ADVPL/TLPP

```advpl
// ❌ Function que faz tudo
Function ProcessarPedido( cPedidoId, cUsuarioId, aPedidoItens, cCupom, aEndereco )

// ✅ Responsabilidades separadas
Function CalcularTotalItens( aPedidoItens )
Function AplicarCupom( nTotal, cCupom )
Function FormatarEndereco( aEndereco )
```

> Arquivos completos: [`exemplos/equivalente.php`](exemplos/equivalente.php) · [`exemplos/equivalente.ts`](exemplos/equivalente.ts) · [`exemplos/equivalente.tlpp`](exemplos/equivalente.tlpp)

---

## 6. Regras de Ouro

- **Uma função, uma responsabilidade** — se você precisar de "e" para descrever o que ela faz, ela faz coisas demais
- **Funções pequenas permitem nomes precisos** — funções grandes demais não cabem num nome honesto
- **Nunca use flag booleana como parâmetro** — crie duas funções com nomes distintos
- **Efeitos colaterais são mentiras** — se a função modifica estado além do que o nome promete, corrija o nome ou extraia o efeito
- **Prefira exceções a retornos especiais** — retornar `None` ou `-1` como erro distribui a lógica de tratamento pelo código todo

---

## 7. Exercício

**Tarefa:** Refatore as três funções do arquivo de exercício aplicando os princípios acima. Não altere o comportamento externo.

```bash
# Rode para ver o output esperado:
python exercicios/exercicio.py

# Compare com o gabarito:
python exercicios/gabarito.py
```

> Arquivo: [`exercicios/exercicio.py`](exercicios/exercicio.py)
> Gabarito: [`exercicios/gabarito.py`](exercicios/gabarito.py)

---

## 8. Para se Aprofundar

- **Clean Code**, Robert C. Martin — Capítulo 3: *Functions* (p. 31–52)
- **Refactoring**, Martin Fowler — *Extract Function* (p. 106), *Replace Flag with Explicit Methods*
- Ferramenta: [`radon`](https://radon.readthedocs.io/) mede complexidade ciclomática de funções Python

---

> **Próximo tutorial:** [Tutorial 03 — Comentários](../tutorial-03-comentarios/README.md)
