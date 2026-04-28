# Tutorial 02 — Funções

> Referência: *Clean Code*, Capítulo 3 — Functions

---

## 1. Contexto e Motivação

Se nomes são a menor unidade de código legível, funções são a primeira unidade de comportamento. Uma função bem escrita é uma **promessa**: o nome diz o que ela faz, e o corpo cumpre exatamente essa promessa — sem surpresas.

O problema mais comum em bases de código legadas não é código incorreto, é código correto que ninguém mais consegue modificar com segurança. Funções longas que fazem muita coisa são a principal causa desse problema.

Martin usa a metáfora do jornal para descrever como funções devem ser organizadas — a **Stepdown Rule** (Clean Code p. 37): um artigo de jornal começa com o título, depois o parágrafo de abertura com o resumo, depois os detalhes, e finalmente os detalhes dos detalhes. Da mesma forma, o código deve ser lido de cima para baixo, com funções de alto nível primeiro e implementações detalhadas depois. Quem lê o código consegue parar quando entendeu o suficiente — sem precisar descer até o último nível de detalhe.

---

## 2. Conceito Central

### A regra do "faz uma coisa"

> *"Functions should do one thing. They should do it well. They should do it only."*  
> — Robert C. Martin, Clean Code, p. 35

"Uma coisa" é mais rigoroso do que parece. Uma função que valida, calcula e formata está fazendo três coisas. O teste prático: você consegue extrair alguma lógica dela em outra função com um nome significativo? Se sim, ela está fazendo mais de uma coisa.

### A Stepdown Rule — nível de abstração consistente

Dentro de uma função, todos os comandos devem estar no mesmo nível de abstração. Misturar alto nível com detalhes é o que torna funções difíceis de ler:

```python
# ❌ Mistura de níveis: alto nível + detalhe de implementação na mesma função
def processar_checkout(carrinho):
    validar_usuario(carrinho.usuario_id)          # alto nível
    total = sum(i["preco"] * i["qtd"] for i in carrinho.itens)  # detalhe
    enviar_email_confirmacao(carrinho.usuario_id)  # alto nível
```

```python
# ✅ Mesmo nível de abstração — os detalhes ficam nas funções delegadas
def processar_checkout(carrinho):
    validar_usuario(carrinho.usuario_id)
    total = calcular_total_carrinho(carrinho.itens)   # detalhe encapsulado
    enviar_email_confirmacao(carrinho.usuario_id)
```

### O Princípio Aberto/Fechado (OCP)

> *"Software entities should be open for extension, but closed for modification."*
> — Bertrand Meyer / Robert C. Martin

Um módulo respeita o OCP quando é possível **estendê-lo** para suportar novos comportamentos **sem modificar** o código existente. O sinal de que o princípio está sendo violado é simples: toda vez que o sistema precisa de um novo "tipo", você precisa abrir e editar funções que já funcionavam.

```python
# ❌ Viola OCP: cada novo tipo de desconto exige modificar esta função
def calcular_desconto(tipo: str, valor: float) -> float:
    if tipo == "black_friday":
        return valor * 0.30
    elif tipo == "fidelidade":
        return valor * 0.10
    # Adicionar "estudante" = abrir esta função e inserir mais um elif
```

```python
# ✅ Respeita OCP: adicionar "estudante" = criar nova classe, sem tocar no resto
from abc import ABC, abstractmethod  # abc = módulo "Abstract Base Classes" da biblioteca padrão

class Desconto(ABC):
    @abstractmethod
    def calcular(self, valor: float) -> float: ...

class DescontoBlackFriday(Desconto):
    def calcular(self, valor: float) -> float:
        return valor * 0.30

class DescontoFidelidade(Desconto):
    def calcular(self, valor: float) -> float:
        return valor * 0.10

class DescontoEstudante(Desconto):  # extensão sem modificar nada acima
    def calcular(self, valor: float) -> float:
        return valor * 0.15

def aplicar_desconto(desconto: Desconto, valor: float) -> float:
    return valor - desconto.calcular(valor)  # sem if — contrato resolve
```

O OCP não elimina toda modificação — ele direciona onde o código cresce: em novas classes, não em funções existentes.

### Switch statements — quando são e não são aceitáveis

Switch statements (ou if/elif em cascata) violam o OCP quando aparecem em múltiplos lugares do código (Clean Code p. 37–38). O sintoma: toda vez que um novo tipo é adicionado, você precisa localizar e editar N funções diferentes.

```python
# ❌ O if se duplica a cada operação — calcular, exibir, exportar, auditar...
def calcular_salario(funcionario):
    if funcionario.tipo == "CLT":
        return funcionario.salario_base * 1.20
    elif funcionario.tipo == "PJ":
        return funcionario.valor_hora * funcionario.horas_mes

def gerar_relatorio(funcionario):
    if funcionario.tipo == "CLT":
        return f"Regime CLT — {funcionario.nome}"
    elif funcionario.tipo == "PJ":
        return f"Regime PJ — CNPJ: {funcionario.cnpj}"

# Consequência: adicionar "Estágio" exige editar calcular_salario,
# gerar_relatorio, exibir_perfil, exportar_xml... cada um com seu if.
```

A solução em duas partes: **(1)** hierarquia polimórfica — cada subclasse sabe como se comportar; **(2)** factory — o único `if` que cria o objeto certo a partir de um dado bruto.

```python
# ✅ Hierarquia: cada tipo encapsula seu próprio comportamento
from abc import ABC, abstractmethod  # abc = módulo "Abstract Base Classes" da biblioteca padrão

class Funcionario(ABC):
    @abstractmethod
    def calcular_salario(self) -> float: ...

    @abstractmethod
    def gerar_relatorio(self) -> str: ...

class FuncionarioCLT(Funcionario):
    def __init__(self, nome: str, salario_base: float):
        self.nome = nome
        self.salario_base = salario_base

    def calcular_salario(self) -> float:
        return self.salario_base * 1.20

    def gerar_relatorio(self) -> str:
        return f"Regime CLT — {self.nome}"

class FuncionarioPJ(Funcionario):
    def __init__(self, nome: str, cnpj: str, valor_hora: float, horas_mes: int):
        self.nome = nome
        self.cnpj = cnpj
        self.valor_hora = valor_hora
        self.horas_mes = horas_mes

    def calcular_salario(self) -> float:
        return self.valor_hora * self.horas_mes

    def gerar_relatorio(self) -> str:
        return f"Regime PJ — CNPJ: {self.cnpj}"

# ✅ Factory: o if existe UMA única vez — na criação do objeto
def criar_funcionario(dados: dict) -> Funcionario:
    tipo = dados["tipo"]
    if tipo == "CLT":
        return FuncionarioCLT(dados["nome"], dados["salario_base"])
    elif tipo == "PJ":
        return FuncionarioPJ(dados["nome"], dados["cnpj"], dados["valor_hora"], dados["horas_mes"])
    raise ValueError(f"Tipo de funcionário desconhecido: {tipo}")

# ✅ Todos os chamadores usam o contrato — sem nenhum if
def processar_folha(funcionarios: list[Funcionario]) -> None:
    for f in funcionarios:
        salario = f.calcular_salario()   # sem if — polimorfismo resolve
        relatorio = f.gerar_relatorio()  # sem if — polimorfismo resolve
        print(f"{relatorio}: R$ {salario:.2f}")
```

Adicionar "Estágio" agora exige apenas: criar `FuncionarioEstagio` e adicionar um `elif` na factory — as funções que consomem `Funcionario` não precisam ser tocadas.

### Command Query Separation (CQS)

Funções que fazem algo OU retornam algo — nunca ambos (Clean Code p. 45):

```python
# ❌ Violação de CQS: modifica estado E retorna resultado
def adicionar_usuario(usuario):
    self.usuarios.append(usuario)
    return len(self.usuarios)  # efeito colateral + valor de retorno misturados

# ✅ CQS respeitado: comando separado da consulta
def adicionar_usuario(usuario):
    self.usuarios.append(usuario)

def contar_usuarios():
    return len(self.usuarios)
```

O problema de violar CQS: o chamador não sabe se está invocando um comando ou uma consulta — e isso cria acoplamento implícito entre leitura e escrita.

### Prefira exceções a códigos de erro

Retornar `-1`, `None` ou um dict `{"erro": "..."}` como sinal de falha obriga o chamador a checar o retorno antes de usar o valor (Clean Code p. 46). Isso distribui a lógica de tratamento de erro por todo o código:

```python
# ❌ Código de erro: lógica condicional se espalha pelo chamador
resultado = buscar_usuario(id)
if resultado == -1:
    ...
elif resultado is None:
    ...
else:
    usar(resultado)

# ✅ Exceção: o fluxo feliz é linear; erros são tratados onde fazem sentido
try:
    usuario = buscar_usuario(id)  # lança UsuarioNaoEncontrado se não existir
    usar(usuario)
except UsuarioNaoEncontrado:
    tratar_ausencia()
```

### DRY no nível de função

Duplicação é a raiz de toda dívida técnica de lógica. Quando a mesma sequência de operações aparece em dois lugares, qualquer mudança na regra de negócio precisa ser feita em dois lugares — e uma das cópias sempre fica para trás. Extraia funções não apenas por clareza, mas para criar um único ponto de mudança.

### Princípios fundamentais


| Princípio                              | Descrição                                                             |
| -------------------------------------- | --------------------------------------------------------------------- |
| **Tamanho pequeno**                    | Funções devem ter raramente mais de 20 linhas                         |
| **Um nível de abstração**              | Não misture lógica de alto nível com detalhes de implementação        |
| **Sem flags booleanas**                | `formatar(nome, True)` — o `True` não diz nada; crie duas funções     |
| **Sem efeitos colaterais**             | A função só faz o que o nome promete                                  |
| **Máximo 2 argumentos**                | Mais que isso, considere um objeto/dataclass                          |
| **CQS**                                | Funções fazem algo OU retornam algo, não ambos                        |
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

> Arquivo completo: `[exemplos/funcoes_ruins.py](exemplos/funcoes_ruins.py)`

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

> Arquivo completo: `[exemplos/funcoes_boas.py](exemplos/funcoes_boas.py)`

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

> Arquivos completos: `[exemplos/equivalente.php](exemplos/equivalente.php)` · `[exemplos/equivalente.ts](exemplos/equivalente.ts)` · `[exemplos/equivalente.tlpp](exemplos/equivalente.tlpp)`

---

## 6. Aprofundamento: Funções como Contratos

A assinatura de uma função é um **contrato** com o chamador:

- **Parâmetros** são os inputs esperados — o chamador promete fornecer valores válidos dentro do tipo e semântica esperados.
- **Retorno** é o output prometido — a função promete devolver algo no formato e semântica declarados.
- **Exceções** são os casos esperados, não surpresas — `UsuarioNaoEncontrado` faz parte do contrato; `NullPointerException` não.

Quando uma função viola seu contrato — recebe um parâmetro que silenciosamente ignora, retorna `None` de vez em quando sem documentar, lança exceções não declaradas — o chamador não consegue confiar nela. Desconfiança gera código defensivo; código defensivo gera ruído; ruído gera bugs.

A consequência direta: **nomes e assinaturas de funções devem ser honestos**. Se uma função pode não encontrar o usuário, o contrato deve expressar isso — seja pelo tipo de retorno (`Optional[Usuario]`), seja pela exceção documentada (`raises UsuarioNaoEncontrado`).

---

> **👉 ATIVIDADE:** Identifique a função mais longa do código da equipe. Quantas responsabilidades ela tem? Escreva uma lista com uma linha por responsabilidade identificada.

---

## 7. Regras de Ouro

- **Uma função, uma responsabilidade** — se você precisar de "e" para descrever o que ela faz, ela faz coisas demais
- **Funções pequenas permitem nomes precisos** — funções grandes demais não cabem num nome honesto
- **Nunca use flag booleana como parâmetro** — crie duas funções com nomes distintos
- **Efeitos colaterais são mentiras** — se a função modifica estado além do que o nome promete, corrija o nome ou extraia o efeito
- **Prefira exceções a retornos especiais** — retornar `None` ou `-1` como erro distribui a lógica de tratamento pelo código todo
- **CQS** — uma função faz algo OU retorna algo; misturar os dois cria acoplamento implícito
- **Stepdown Rule** — o leitor deve conseguir parar de ler quando entendeu o suficiente, sem descer a todos os detalhes

---

## 8. Exercício

**Tarefa:** Refatore as três funções do arquivo de exercício aplicando os princípios acima. Não altere o comportamento externo.

```bash
# Rode para ver o output esperado:
python exercicios/exercicio.py

# Compare com o gabarito:
python exercicios/gabarito.py
```

> Arquivo: `[exercicios/exercicio.py](exercicios/exercicio.py)`  
> Gabarito: `[exercicios/gabarito.py](exercicios/gabarito.py)`

---

## 9. Para se Aprofundar

- **Clean Code**, Robert C. Martin — Capítulo 3: *Functions* (p. 31–52)
- **Refactoring**, Martin Fowler — *Extract Function* (p. 106), *Replace Flag with Explicit Methods*
- **Principles of Object-Oriented Design**, Robert C. Martin — Open/Closed Principle (relevante para a discussão de switch statements)
- Ferramenta: `[radon](https://radon.readthedocs.io/)` mede complexidade ciclomática de funções Python

---

> **Próximo tutorial:** [Tutorial 03 — Comentários](../tutorial-03-comentarios/README.md)