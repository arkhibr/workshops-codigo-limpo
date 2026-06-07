# Tutorial 16 — SOLID na Prática
> Referência: Robert C. Martin, *Clean Code* Cap. 1 + SOLID papers (2000–2003)

---

## 1. Contexto e Motivação

Código que cresce sem princípios acumula dívida técnica de forma exponencial: classes com dezenas de razões para mudar, hierarquias que quebram silenciosamente, dependências que tornam testes impossíveis. Os princípios SOLID são um conjunto de cinco diretrizes que, aplicadas em conjunto, reduzem o custo cognitivo de leitura, o risco de regressão ao modificar código e o tempo para integrar novos membros à equipe.

**Por que importa na prática:**
- Uma classe que valida, persiste e envia e-mail tem três razões distintas para mudar. Qualquer alteração pode introduzir bugs nas outras responsabilidades.
- Um método com `if/elif` por tipo de relatório precisa ser reaberto cada vez que um novo tipo é adicionado.
- Uma subclasse que lança `NotImplementedError` onde a base nunca lança quebra código existente de forma silenciosa em runtime.
- Uma interface de 6 métodos força implementações que usam apenas 2 a carregar código morto.
- Uma classe que instancia `new EmailSmtp()` internamente não pode ser testada com um dublê de e-mail sem alterar o código de produção.

---

## 2. Conceito Central

### S — Single Responsibility Principle (SRP)

> "Uma classe deve ter apenas uma razão para mudar."

Cada classe deve encapsular uma única responsabilidade de negócio. "Razão para mudar" significa: qual ator (equipe de negócio, DBA, equipe de infraestrutura) solicitaria alteração nessa classe?

**❌ Ruim — múltiplas responsabilidades em uma classe:**

```python
class GeradorRelatorioPedidos:
    def validar_pedido(self, pedido):  ...  # responsabilidade: regra de negócio
    def calcular_total(self, pedido):  ...  # responsabilidade: cálculo financeiro
    def salvar_pedido(self, pedido):   ...  # responsabilidade: persistência
    def enviar_confirmacao(self, pedido): ...  # responsabilidade: notificação
```

**✅ Bom — responsabilidades separadas:**

```python
class ValidadorPedido:
    def validar(self, pedido): ...

class CalculadorTotal:
    def calcular(self, pedido): ...

class RepositorioPedido:
    def salvar(self, pedido): ...

class NotificadorEmail:
    def notificar(self, destinatario, mensagem): ...
```

**Quando aplicar:** sempre que uma classe tiver mais de um "ator" que poderia solicitar mudanças. Sinal de alerta: nomes com "e" (`SalvaEEnvia`, `ValidaECalcula`).

---

### O — Open/Closed Principle (OCP)

> "Entidades de software devem ser abertas para extensão, mas fechadas para modificação."

Adicionar novo comportamento deve ser possível sem alterar código que já funciona.

**❌ Ruim — cada novo tipo exige alterar o método:**

```python
def gerar(self, tipo: str, pedido: Pedido) -> str:
    if tipo == "vendas":
        return f"Relatório Vendas | ..."
    elif tipo == "financeiro":
        return f"Relatório Financeiro | ..."
    elif tipo == "estoque":          # <- nova linha adicionada aqui
        return f"Relatório Estoque | ..."
    else:
        raise ValueError(f"Tipo desconhecido: {tipo}")
```

**✅ Bom — polimorfismo via protocolo:**

```python
class IFormatador(Protocol):
    def formatar(self, pedido: Pedido, total: float) -> str: ...

class FormatadorVendas:
    def formatar(self, pedido, total): return f"Relatório Vendas | ..."

class FormatadorEstoque:              # novo tipo: sem alterar GeradorRelatorio
    def formatar(self, pedido, total): return f"Relatório Estoque | ..."
```

**Quando aplicar:** quando a regra de extensão é previsível. Não abstraia prematuramente — espere o segundo caso concreto antes de introduzir o protocolo.

---

### L — Liskov Substitution Principle (LSP)

> "Se S é subtipo de T, objetos de T podem ser substituídos por objetos de S sem alterar as propriedades desejáveis do programa."

Uma subclasse deve honrar o contrato da classe base: mesmas pré-condições, pós-condições e sem exceções que a base nunca lança.

**❌ Ruim — subclasse quebra o contrato:**

```python
class Pedido:
    def confirmar(self) -> None:
        self.status = "confirmado"

class PedidoAmostra(Pedido):
    def confirmar(self) -> None:
        raise NotImplementedError("PedidoAmostra não pode ser confirmado")
        # código que usa Pedido explode em runtime com PedidoAmostra
```

**✅ Bom — subclasse estende sem quebrar contrato:**

```python
class PedidoAmostra(Pedido):
    def calcular_total_especial(self) -> float:
        return 0.0
    # confirmar() herdado sem alteração — contrato mantido
```

**Quando aplicar:** ao modelar hierarquias de herança. Prefira composição quando a subclasse precisar restringir o comportamento da base.

---

### I — Interface Segregation Principle (ISP)

> "Clientes não devem ser forçados a depender de interfaces que não usam."

Interfaces grandes devem ser divididas em interfaces menores e coesas. Cada cliente depende apenas do que precisa.

**❌ Ruim — interface gorda:**

```python
class IProcessador:
    def validar(self)      -> bool:  ...
    def calcular(self)     -> float: ...
    def notificar(self)    -> None:  ...
    def arquivar(self)     -> None:  ...
    def exportar_csv(self) -> str:   ...
    def exportar_pdf(self) -> bytes: ...
```

```python
class ProcessadorSimples(IProcessador):
    # precisa apenas de validar e calcular
    # mas é forçado a implementar os outros 4 métodos
    def exportar_pdf(self) -> bytes: return b""  # código morto
```

**✅ Bom — interfaces segregadas:**

```python
class IValidavel(Protocol):
    def validar(self) -> bool: ...

class ICalculavel(Protocol):
    def calcular(self) -> float: ...

class IExportavel(Protocol):
    def exportar_csv(self) -> str: ...
    def exportar_pdf(self) -> bytes: ...
```

> **Nota ADVPL:** Em AdvPL clássico, interfaces não existem nativamente. TLPP 4.0+ tem classes e herança, mas sem interfaces formais — use protocolos implícitos por convenção de nomenclatura (ex: prefixo `I` em funções relacionadas, como `INotificar_Email`, `INotificar_Log`).

**Quando aplicar:** quando implementações de uma interface deixam métodos vazios ou lançam `NotImplementedError`. Sinal de que a interface está fazendo demais.

---

### D — Dependency Inversion Principle (DIP)

> "Módulos de alto nível não devem depender de módulos de baixo nível. Ambos devem depender de abstrações."

Classes não devem instanciar suas dependências — devem recebê-las via construtor (injeção de dependência).

**❌ Ruim — dependência concreta instanciada internamente:**

```python
class GeradorRelatorioPedidos:
    def __init__(self) -> None:
        self.db    = BancoDadosSQLite()   # impossível substituir em testes
        self.email = EmailSmtp()          # impossível substituir em testes
```

**✅ Bom — dependências injetadas via construtor:**

```python
class GeradorRelatorio:
    def __init__(
        self,
        repo:        IRepositorioPedido,   # abstração
        notificador: INotificador,         # abstração
        formatador:  IFormatador,
        calculador:  CalculadorTotal,
    ) -> None:
        self._repo        = repo
        self._notificador = notificador
        ...
```

Em ADVPL, simule DIP com codeblocks:
```advpl
bNotificador := {|cId, cMsg| NotificarCliente(cId, cMsg)}
Eval(bNotificador, "CLI-100", "pedido confirmado")
// bNotificador pode ser substituído por outro codeblock sem alterar o chamador
```

**Quando aplicar:** sempre que uma classe tiver `new ConcreteService()` no construtor. Extraia a abstração e injete via parâmetro.

---

## 3. Exercício

Arquivo: `exercicios/exercicio.py` (equivalentes: `.php`, `.ts`, `.tlpp`)

A classe `GeradorFatura` viola SRP e DIP:
- Valida, calcula, persiste e envia e-mail na mesma classe.
- Instancia `EmailSMTP` diretamente no construtor.

**Tarefa:**
1. Separe em classes com responsabilidade única: `ValidadorFatura`, `CalculadorFatura`, `RepositorioFatura`.
2. Crie o protocolo `INotificador` e injete-o no construtor de `GeradorFatura`.
3. Verifique que o arquivo ainda executa sem erros após a refatoração.

Gabarito: `exercicios/gabarito.py`

---

## 4. Checklist — SOLID na revisão de código

- [ ] Esta classe tem mais de uma razão para mudar? (SRP)
- [ ] Adicionar um novo tipo exige alterar código existente? (OCP)
- [ ] Esta subclasse pode substituir a base sem surpresas em runtime? (LSP)
- [ ] Esta interface força implementar métodos não usados? (ISP)
- [ ] Esta classe instancia suas dependências internamente com `new`? (DIP)

---

## 5. Referências

- Martin, Robert C. *Clean Code*. Cap. 1.
- Martin, Robert C. SOLID papers (2000–2003): SRP, OCP, LSP, ISP, DIP.
- Martin, Robert C. *Agile Software Development, Principles, Patterns, and Practices*. Cap. 7–11.
