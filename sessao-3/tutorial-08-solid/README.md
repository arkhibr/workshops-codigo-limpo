# Tutorial 08 — SOLID na Prática

> Referência: Robert C. Martin, *Clean Code* Cap. 1 + *Agile Software Development* Cap. 7–11 (SOLID papers, 2000–2003)

---

## 1. Contexto e Motivação

Nos tutoriais anteriores você aprendeu a nomear bem, escrever funções coesas e formatar código para legibilidade. Esses princípios operam no nível da linha. Os princípios **SOLID** operam no nível da **arquitetura de classes**: eles definem como responsabilidades devem ser distribuídas entre os componentes do sistema.

Um sistema que respeita SOLID tem uma propriedade específica: você consegue modificar um comportamento **sem abrir e reeditar código que já funcionava**. Isso reduz o risco de regressão, acelera onboarding e torna testes mais baratos — porque cada classe tem uma única razão para existir e suas dependências são visíveis no construtor.

O custo de ignorar SOLID aparece de forma gradual: começa com funções longas (já visto no tutorial-02), evolui para classes que fazem tudo, e termina em módulos onde qualquer mudança se propaga de forma imprevisível por todo o sistema.

> **Nota sobre nomenclatura:** interfaces e protocolos usam `PascalCase` simples — `Formatador`, não `IFormatador`. O prefixo `I` é uma convenção do C#/.NET que não se aplica a Python, PHP 8 ou TypeScript. (Referência: tutorial-04, seção de convenções de nomenclatura.)

**Contra-exemplos:**
- Uma classe que valida, persiste e envia e-mail tem três razões distintas para mudar. Qualquer alteração pode introduzir bugs nas outras responsabilidades.
- Um método com `if/elif` por tipo de relatório precisa ser reaberto cada vez que um novo tipo é adicionado.
- Uma subclasse que lança `NotImplementedError` onde a base nunca lança quebra código existente de forma silenciosa em runtime.
- Uma interface/classe virtual complexa de 10 métodos força implementações que usam apenas 2 a carregar código morto.
- Uma classe que instancia `new EmailSmtp()` internamente não pode ser testada com um dublê de e-mail sem alterar o código de produção.

O SOLID é um conjunto de princípios de design de código que busca endereçar esses e outros pontos e garantir a você um código robusto e manutenível ao longo do tempo.

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/334edf0c-bb1a-4689-ba05-27056360c24d" />



---

## 2. S — Single Responsibility Principle (SRP)

> *"Uma classe deve ter apenas uma razão para mudar."*
> — Robert C. Martin

"Razão para mudar" é definida por **ator**: qual equipe ou papel de negócio solicitaria alteração nessa classe? Uma classe que valida pedidos interessa à equipe de regras de negócio. Uma classe que envia e-mail interessa à equipe de infraestrutura. Quando ambas estão na mesma classe, uma mudança de infraestrutura (trocar SMTP por SES) abre risco de introduzir bugs na validação.

### O problema

```python
class GeradorRelatorioPedidos:
    def __init__(self) -> None:
        self.db    = BancoDadosSQLite()   # acoplado a implementação concreta
        self.email = EmailSmtp()          # acoplado a implementação concreta

    def validar_pedido(self, pedido):     # responsabilidade: regras de negócio
        return bool(pedido.itens) and bool(pedido.cliente_id)

    def calcular_total(self, pedido):     # responsabilidade: financeiro
        return sum(i.preco * i.quantidade for i in pedido.itens)

    def salvar_pedido(self, pedido):      # responsabilidade: persistência
        self.db.salvar("pedidos", {"id": pedido.id, "status": pedido.status})

    def enviar_confirmacao(self, pedido): # responsabilidade: notificação
        self.email.enviar(pedido.cliente_id, f"Pedido {pedido.id} confirmado")

    def gerar(self, tipo, pedido):        # responsabilidade: formatação
        ...
```

Essa classe tem **cinco** razões para mudar. Qualquer das cinco mudanças abre risco de quebrar as outras quatro.

### A solução

```python
class ValidadorPedido:
    """Razão para mudar: mudança nas regras de validação de negócio."""
    def validar(self, pedido: Pedido) -> bool:
        if not pedido.itens:
            return False
        if not pedido.cliente_id:
            return False
        if any(i.preco <= 0 for i in pedido.itens):
            return False
        return True

class CalculadorTotal:
    """Razão para mudar: mudança nas alíquotas ou regras de cálculo."""
    TAXA_IMPOSTO = 0.10

    def calcular(self, pedido: Pedido) -> float:
        subtotal = sum(i.preco * i.quantidade for i in pedido.itens)
        return round(subtotal * (1 + self.TAXA_IMPOSTO), 2)

    def calcular_subtotal(self, pedido: Pedido) -> float:
        return round(sum(i.preco * i.quantidade for i in pedido.itens), 2)

class RepositorioPedido:
    """Razão para mudar: mudança no mecanismo de persistência."""
    def salvar(self, pedido: Pedido) -> None:
        ...  # escreve no banco

class NotificadorEmail:
    """Razão para mudar: mudança no canal de notificação."""
    def notificar(self, destinatario: str, mensagem: str) -> None:
        ...  # envia e-mail
```

Cada classe agora tem um único motivo para ser aberta e editada.

> **Sinal de alerta:** nomes compostos com "e" são uma bandeira vermelha. `SalvaEEnvia`, `ValidaECalcula`, `BuscaEFormata` — o "e" no nome geralmente revela duas responsabilidades na mesma classe.

---

> **📝 Reflita:** No código da sua equipe, qual classe tem mais "e" escondidos no comportamento — valida, calcula, salva e notifica? Escreva os quatro atores que precisariam ser consultados antes de modificá-la.

---

## 3. O — Open/Closed Principle (OCP)

> *"Entidades de software devem ser abertas para extensão, mas fechadas para modificação."*
> — Bertrand Meyer / Robert C. Martin

Este princípio já foi introduzido no **tutorial-02** no contexto de funções com `switch`. O mesmo raciocínio se aplica ao nível de classes: quando um novo "tipo" é adicionado ao sistema, você não deveria precisar abrir nenhuma classe existente.

O sinal de violação é direto: toda vez que o negócio pede um novo tipo de relatório (ou desconto, ou exportação, ou canal de notificação), você precisa editar um método que já funcionava.

### O problema

```python
def gerar(self, tipo: str, pedido: Pedido) -> str:
    total = self.calcular_total(pedido)
    if tipo == "vendas":
        return f"Relatório Vendas | Pedido {pedido.id} | Total: R${total:.2f}"
    elif tipo == "financeiro":
        return f"Relatório Financeiro | Receita: R${total:.2f}"
    elif tipo == "estoque":                    # ← inserido quando negócio pediu
        return f"Relatório Estoque | {len(pedido.itens)} item(ns)"
    # próxima demanda: abrir este método novamente e adicionar mais um elif
    else:
        raise ValueError(f"Tipo desconhecido: {tipo}")
```

Cada novo tipo de relatório exige reabrir e reeditar esse método — arriscando quebrar os tipos que já funcionavam.

### A solução

```python
from typing import Protocol

class Formatador(Protocol):
    """Contrato que qualquer formatador deve honrar."""
    def formatar(self, pedido: Pedido, total: float) -> str: ...

class FormatadorVendas:
    def formatar(self, pedido: Pedido, total: float) -> str:
        itens = ", ".join(f"{i.descricao} x{i.quantidade}" for i in pedido.itens)
        return f"[Vendas] Pedido {pedido.id} | {itens} | Total: R${total:.2f}"

class FormatadorFinanceiro:
    def formatar(self, pedido: Pedido, total: float) -> str:
        return f"[Financeiro] Pedido {pedido.id} | Total: R${total:.2f}"

class FormatadorEstoque:
    def formatar(self, pedido: Pedido, total: float) -> str:
        linhas = [f"  • {i.descricao}: {i.quantidade} un" for i in pedido.itens]
        return "[Estoque] Movimentação:\n" + "\n".join(linhas)

# FormatadorNFe adicionado sem alterar nenhuma das classes acima
class FormatadorNFe:
    def formatar(self, pedido: Pedido, total: float) -> str:
        return f"[NF-e] Nr: {pedido.id} | Dest: {pedido.cliente_id} | R${total:.2f}"
```

`GeradorRelatorio` recebe um `Formatador` e nunca precisa saber quantos tipos existem:

```python
class GeradorRelatorio:
    def __init__(self, formatador: Formatador, ...) -> None:
        self._formatador = formatador

    def processar(self, pedido: Pedido) -> str:
        total = self._calculador.calcular(pedido)
        return self._formatador.formatar(pedido, total)  # sem if — polimorfismo resolve
```

> **Quando NÃO abstrair:** espere o segundo caso concreto antes de introduzir o protocolo. Uma única implementação não justifica a abstração — a generalização prematura é tão custosa quanto a duplicação.

---

> **📝 Reflita:** Qual é o `if tipo == ...` mais longo do seu código atual? Quantos `elif` ele tem? Quantas vezes por trimestre alguém abre esse método para adicionar um novo caso?

---

## 4. L — Liskov Substitution Principle (LSP)

> *"Se S é subtipo de T, objetos do tipo T podem ser substituídos por objetos do tipo S sem alterar as propriedades desejáveis do programa."*
> — Barbara Liskov (1987)

Em termos práticos: se uma função aceita um `Pedido`, ela deve funcionar corretamente com qualquer subtipo de `Pedido` — sem surpresas em runtime. Uma subclasse que lança exceções que a base nunca lança, ou que silenciosamente ignora o comportamento esperado, quebra o contrato.

### O problema

```python
class Pedido:
    def confirmar(self) -> None:
        self.status = "confirmado"   # pós-condição: status sempre vira "confirmado"

class PedidoAmostra(Pedido):
    def confirmar(self) -> None:
        raise NotImplementedError("PedidoAmostra não pode ser confirmado")
        # quebra a pós-condição da base — código que usa Pedido explode em runtime
```

Qualquer código que processa uma lista de `Pedido` e chama `confirmar()` explodirá silenciosamente quando receber um `PedidoAmostra`.

### A solução

```python
class PedidoAmostra(Pedido):
    def calcular_total_especial(self) -> float:
        return 0.0          # amostras têm custo zero
    # confirmar() herdado sem alteração — pós-condição da base garantida

class PedidoPrioritario(Pedido):
    def __init__(self, *args, prioridade: int = 1, **kwargs):
        super().__init__(*args, **kwargs)
        self.prioridade = prioridade

    def confirmar(self) -> None:
        super().confirmar()   # honra o contrato: status = "confirmado"
        print(f"  [Fila] Pedido {self.id} com prioridade {self.prioridade}")
        # estende o comportamento sem violar a pós-condição

def confirmar_e_exibir(pedido: Pedido) -> None:
    pedido.confirmar()
    assert pedido.status == "confirmado"   # invariante garantida para qualquer subtipo
    print(f"  {pedido.id} → {pedido.status}")
```

`confirmar_e_exibir` funciona com `Pedido`, `PedidoAmostra` e `PedidoPrioritario` — nenhuma surpresa.

> **Herança vs. composição:** quando uma subclasse precisa *restringir* o comportamento da base (ex.: "esse tipo não pode ser confirmado"), isso é um sinal de que herança é o mecanismo errado. Use composição: `PedidoAmostra` não é um `Pedido` que confirma — é um objeto à parte que pode *conter* dados de um pedido.

---

> **📝 Reflita:** Na sua base de código, existe algum `NotImplementedError` em uma subclasse que substitui um método da classe pai? Esse método é chamado por código que não sabe qual subtipo vai receber?

---

## 5. I — Interface Segregation Principle (ISP)

> *"Clientes não devem ser forçados a depender de interfaces que não usam."*
> — Robert C. Martin

Interfaces grandes forçam implementações a carregar código morto: métodos que retornam valores vazios (`return ""`, `return b""`), lançam `NotImplementedError`, ou simplesmente fazem `pass`. Código morto é ruído — e ruído cria bugs.

### O problema

```python
class Processador:
    """Interface com 6 métodos — qualquer implementação precisa de todos."""
    def validar(self)      -> bool:  raise NotImplementedError
    def calcular(self)     -> float: raise NotImplementedError
    def notificar(self)    -> None:  raise NotImplementedError
    def arquivar(self)     -> None:  raise NotImplementedError
    def exportar_csv(self) -> str:   raise NotImplementedError
    def exportar_pdf(self) -> bytes: raise NotImplementedError

class ProcessadorSimples(Processador):
    """Precisa apenas de validar e calcular — mas é forçado a implementar tudo."""
    def validar(self)      -> bool:  return True
    def calcular(self)     -> float: return 0.0
    def notificar(self)    -> None:  pass          # código morto
    def arquivar(self)     -> None:  pass          # código morto
    def exportar_csv(self) -> str:   return ""     # código morto
    def exportar_pdf(self) -> bytes: return b""    # código morto
```

`ProcessadorSimples` carrega quatro métodos que nunca serão chamados. Quando `exportar_pdf` mudar de assinatura, `ProcessadorSimples` precisará ser alterado — mesmo que nunca exporte PDFs.

### A solução

```python
from typing import Protocol

class Validavel(Protocol):
    def validar(self) -> bool: ...

class Calculavel(Protocol):
    def calcular(self) -> float: ...

class Arquivavel(Protocol):
    def arquivar(self) -> None: ...
    def exportar_csv(self) -> str: ...

class ExportavelEmPDF(Protocol):
    def exportar_pdf(self) -> bytes: ...


class ProcessadorSimples:
    """Implementa apenas Validavel e Calculavel — zero código morto."""
    def __init__(self, pedido: Pedido) -> None:
        self._pedido = pedido

    def validar(self) -> bool:
        return bool(self._pedido.itens) and bool(self._pedido.cliente_id)

    def calcular(self) -> float:
        return round(sum(i.preco * i.quantidade for i in self._pedido.itens), 2)


class ProcessadorCompleto:
    """Exportador completo — implementa todas as interfaces necessárias."""
    def __init__(self, pedido: Pedido) -> None:
        self._pedido = pedido

    def validar(self) -> bool:
        return bool(self._pedido.itens) and bool(self._pedido.cliente_id)

    def calcular(self) -> float:
        return round(sum(i.preco * i.quantidade for i in self._pedido.itens), 2)

    def arquivar(self) -> None:
        print(f"  [Arquivo] Pedido {self._pedido.id} arquivado em storage frio")

    def exportar_csv(self) -> str:
        linhas = ["produto_id,descricao,preco,quantidade"]
        for i in self._pedido.itens:
            linhas.append(f"{i.produto_id},{i.descricao},{i.preco},{i.quantidade}")
        return "\n".join(linhas)

    def exportar_pdf(self) -> bytes:
        conteudo = f"PEDIDO {self._pedido.id}\nCliente: {self._pedido.cliente_id}"
        return conteudo.encode("utf-8")
```

`ProcessadorSimples` não sabe que `exportar_pdf` existe. Uma mudança em `ExportavelEmPDF` não o afeta.

> **Nota ADVPL/TLPP:** interfaces não existem em AdvPL clássico e TLPP 4.0+ tem classes mas sem interfaces formais. Simule ISP com grupos de codeblocks: um grupo para validação, outro para exportação. Quem precisa de validação recebe apenas o codeblock de validação.

---

> **📝 Reflita:** Existe alguma interface ou classe base no seu código com mais de 4 métodos? Quantos desses métodos cada implementação concreta realmente usa? Qual o percentual de código morto nas implementações?

---

## 6. D — Dependency Inversion Principle (DIP)

> *"Módulos de alto nível não devem depender de módulos de baixo nível. Ambos devem depender de abstrações."*
> — Robert C. Martin

Uma classe que instancia suas dependências no construtor está acoplada a implementações concretas. Isso tem dois problemas imediatos: (1) você não consegue testar a classe sem invocar todas as suas dependências reais (banco, SMTP, S3); (2) trocar uma dependência exige abrir e editar a classe de alto nível.

### O problema

```python
class GeradorRelatorioPedidos:
    def __init__(self) -> None:
        self.db    = BancoDadosSQLite()   # acoplado — impossível substituir em teste
        self.email = EmailSmtp()          # acoplado — impossível substituir em teste
```

Para testar `GeradorRelatorioPedidos` você precisa de um banco SQLite real e um servidor SMTP real. Não há como passar um dublê de teste sem modificar o código de produção.

### A solução

```python
# Abstrações (protocolos) — definidas no módulo de alto nível
class RepositorioDePedido(Protocol):
    def salvar(self, pedido: Pedido) -> None: ...
    def buscar(self, pedido_id: str) -> Optional[dict]: ...

class Notificador(Protocol):
    def notificar(self, destinatario: str, mensagem: str) -> None: ...


# Implementações concretas de produção
class RepositorioPedido:
    def salvar(self, pedido: Pedido) -> None:
        print(f"  [BD] salvo: {pedido.id} → {pedido.status}")
    def buscar(self, pedido_id: str) -> Optional[dict]:
        ...

class NotificadorEmail:
    def notificar(self, destinatario: str, mensagem: str) -> None:
        print(f"  [Email] → {destinatario}: {mensagem}")


# Implementações de teste — sem banco real, sem SMTP
class RepositorioEmMemoria:
    def __init__(self) -> None:
        self._dados: dict = {}
    def salvar(self, pedido: Pedido) -> None:
        self._dados[pedido.id] = {"id": pedido.id, "status": pedido.status}
    def buscar(self, pedido_id: str) -> Optional[dict]:
        return self._dados.get(pedido_id)

class NotificadorLog:
    def notificar(self, destinatario: str, mensagem: str) -> None:
        print(f"  [Log] {destinatario}: {mensagem}")


# Módulo de alto nível — depende das abstrações, não das implementações
class GeradorRelatorio:
    def __init__(
        self,
        repo:        RepositorioDePedido,  # abstração
        notificador: Notificador,          # abstração
        formatador:  Formatador,           # abstração
        calculador:  CalculadorTotal,      # sem efeitos externos — concreta aceitável
    ) -> None:
        self._repo        = repo
        self._notificador = notificador
        self._formatador  = formatador
        self._calculador  = calculador

    def processar(self, pedido: Pedido) -> str:
        total = self._calculador.calcular(pedido)
        self._repo.salvar(pedido)
        self._notificador.notificar(pedido.cliente_id, f"Total: R${total:.2f}")
        return self._formatador.formatar(pedido, total)


# Em produção:
gerador = GeradorRelatorio(RepositorioPedido(), NotificadorEmail(), FormatadorVendas(), CalculadorTotal())

# Em teste — sem banco, sem SMTP:
gerador_teste = GeradorRelatorio(RepositorioEmMemoria(), NotificadorLog(), FormatadorVendas(), CalculadorTotal())
```

Para adicionar notificação por SMS: crie `NotificadorSms` e injete-o no construtor. `GeradorRelatorio` não precisa ser tocado.

> **DIP em ADVPL/TLPP:** simule injeção de dependência com codeblocks. O codeblock é passado como parâmetro e pode ser substituído sem alterar a função receptora:
>
> ```advpl
> // Produção:
> bNotificador := {|cId, cMsg| NotificarEmail(cId, cMsg)}
> ProcessarComFormatador(cPedId, aItens, cCliId, bFmtVendas, bNotificador, bRepo)
>
> // Teste — mesmo código, outro codeblock:
> bNotificadorTeste := {|cId, cMsg| ConOut("[Log] " + cId + ": " + cMsg)}
> ProcessarComFormatador(cPedId, aItens, cCliId, bFmtVendas, bNotificadorTeste, bRepo)
> ```

---

> **📝 Reflita:** No código da equipe, quantas classes instanciam conexões de banco ou clientes HTTP no próprio construtor (`new PDO(...)`, `new HttpClient()`)? Qual seria o custo de escrever um teste unitário para uma dessas classes hoje?

---

## 7. Os Cinco Princípios em Conjunto

Os cinco princípios se reforçam mutuamente. A `GeradorRelatorio` final satisfaz todos:

| Princípio | Como é respeitado em `GeradorRelatorio` |
|---|---|
| **SRP** | Faz apenas uma coisa: orquestra o fluxo de processamento. Não valida, não calcula, não formata. |
| **OCP** | Recebe `Formatador` pelo construtor. Adicionar `FormatadorNFe` não exige alterar `GeradorRelatorio`. |
| **LSP** | Aceita qualquer implementação de `RepositorioDePedido` e `Notificador`. `RepositorioEmMemoria` é substituível por `RepositorioPedido` sem surpresas. |
| **ISP** | Depende de `Formatador` (1 método), `Notificador` (1 método), `RepositorioDePedido` (2 métodos). Nenhum contrato força métodos desnecessários. |
| **DIP** | Recebe todas as dependências pelo construtor. O módulo de alto nível nunca instancia módulos de baixo nível. |

Quando você viola um princípio, geralmente viola outros. Uma classe que instancia suas dependências (DIP) também tende a acumular responsabilidades (SRP) e a resistir à extensão (OCP).

---

## 8. Armadilhas Comuns

### "Apliquei SOLID e o código ficou mais complexo"

SOLID aumenta o número de classes. Se o problema for pequeno, o overhead não se paga. Aplique quando:
- Existe mais de um "ator" que pedirá mudanças
- Existe mais de um "tipo" que será adicionado com o tempo
- O componente precisa ser testado isoladamente

### "Criei uma interface para cada classe"

Uma interface usada por uma única implementação provavelmente é prematura. Espere o segundo caso de uso antes de extrair a abstração.

### "Prefixei interfaces com I para deixar claro que é interface"

O prefixo `I` é uma convenção do C#. Em Python, PHP 8 e TypeScript a convenção é `PascalCase` simples — o tipo da declaração (`class`, `interface`, `Protocol`, `ABC`) já torna a natureza da entidade explícita. (Tutorial-04, seção de nomenclatura.)

### "Injetei todas as dependências mas não testei nada"

A injeção de dependência cria a *possibilidade* de testar com dublês — mas o valor só se realiza quando você efetivamente escreve os testes. Sem testes, DIP é overhead puro.

---

## 9. Regras de Ouro

- **SRP:** se você precisar de "e" para descrever o que a classe faz, ela tem responsabilidades demais
- **OCP:** antes de abrir um método existente para adicionar um novo tipo, verifique se um protocolo resolve
- **LSP:** subclasses estendem, não restringem — se precisar restringir, use composição
- **ISP:** interfaces com mais de 3–4 métodos são candidatas à segregação
- **DIP:** `new ConcreteService()` no construtor é o cheiro de DIP violado
- **Nomeação:** `PascalCase` sem prefixo — `Formatador`, não `IFormatador`; `Calculavel`, não `ICalculavel`
- **Ordem de aplicação:** SRP primeiro — classes com responsabilidade única são mais fáceis de estender (OCP), substituir (LSP) e compor (DIP)

---

## 10. Checklist — SOLID na revisão de código

- [ ] Esta classe tem mais de uma razão para mudar? → SRP
- [ ] Adicionar um novo tipo exige editar código existente? → OCP
- [ ] Esta subclasse pode substituir a base sem surpresas em runtime? → LSP
- [ ] Esta interface força implementar métodos que não serão usados? → ISP
- [ ] Esta classe instancia suas dependências com `new` no construtor? → DIP
- [ ] Algum nome de interface tem prefixo `I`? → convenção (tutorial-04)
- [ ] Algum método da subclasse lança `NotImplementedError` onde a base não lança? → LSP

---

## 11. Exercício

Arquivo: `exercicios/exercicio.py` (equivalentes: `.php`, `.ts`, `.tlpp`)

A classe `GeradorFatura` viola SRP e DIP:
- Valida, calcula, persiste e envia e-mail na mesma classe.
- Instancia `EmailSMTP` diretamente no construtor.

**Tarefa:**
1. Separe em classes com responsabilidade única: `ValidadorFatura`, `CalculadorFatura`, `RepositorioFatura`.
2. Crie o protocolo `Notificador` (sem prefixo `I`) e injete-o no construtor de `ProcessadorFatura`.
3. Verifique que o arquivo executa sem erros após a refatoração.

```bash
python3 exercicios/exercicio.py   # estado inicial com violações
python3 exercicios/gabarito.py    # solução refatorada
```

Gabarito: `exercicios/gabarito.py`

---

## 12. Equivalentes em Outras Linguagens

Os mesmos 5 princípios são demonstrados nos arquivos de exemplo com as convenções de cada linguagem:

| Linguagem | Abstração | Convenção |
|---|---|---|
| **Python** | `Protocol` (duck typing estrutural) | `PascalCase` simples |
| **PHP 8.1+** | `interface` + `implements` | `PascalCase` simples (PSR-1) |
| **TypeScript** | `interface` ou `type` | `PascalCase` simples (ESLint community) |
| **ADVPL/TLPP** | codeblocks para DIP; funções separadas para SRP | prefixo de tipo obrigatório para variáveis (`c`, `n`, `a`, `l`) |

> Arquivos: `exemplos/solid_ruins.py` · `exemplos/solid_bons.py` · `exemplos/equivalente.php` · `exemplos/equivalente.ts` · `exemplos/equivalente.tlpp`

---

## 13. Para se Aprofundar

Martin, R. C. (2008). Clean code: A handbook of agile software craftsmanship. Prentice Hall. https://www.pearson.com/en-us/subject-catalog/p/clean-code/P200000009528

Martin, R. C. (2000). Design principles and design patterns. Object Mentor. http://www.objectmentor.com/resources/articles/Principles_and_Patterns.pdf

Martin, R. C. (2003). The Single Responsibility Principle. Object Mentor. http://www.objectmentor.com/resources/articles/srp.pdf

Martin, R. C. (2003). The Open-Closed Principle. Object Mentor. http://www.objectmentor.com/resources/articles/ocp.pdf

Martin, R. C. (2003). The Liskov Substitution Principle. Object Mentor. http://www.objectmentor.com/resources/articles/lsp.pdf

Martin, R. C. (2003). The Interface Segregation Principle. Object Mentor. http://www.objectmentor.com/resources/articles/isp.pdf

Martin, R. C. (2003). The Dependency Inversion Principle. Object Mentor. http://www.objectmentor.com/resources/articles/dip.pdf

Martin, R. C. (2003). Agile software development: Principles, patterns, and practices. Prentice Hall. https://www.pearson.com/en-us/subject-catalog/p/agile-software-development-principles-patterns-and-practices/P200000003420

---

> **Próximo tutorial:** [Tutorial 09 — Padrões de Criação](../tutorial-09-criacao/README.md)
