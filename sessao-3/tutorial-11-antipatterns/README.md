# Tutorial 11 — Anti-patterns Clássicos

> Referência: Martin, Robert C. *Clean Code*, Cap. 17 — Smells and Heuristics; Fowler, Martin. *Refactoring*, Cap. 3 — Bad Smells in Code

## 1. Contexto e Motivação

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/9e58f6d9-0830-4697-92d1-8b0db7aa6cbb" />


Anti-patterns surgem de decisões pragmáticas sob pressão — é mais rápido adicionar um método a uma classe existente do que criar uma nova. O problema acumula: uma classe que começa com 3 métodos tem 15 depois de 6 meses, e cada mudança toca a mesma classe.

O custo real não é a classe grande. É o efeito cascata: testes difíceis de escrever, mudanças que quebram comportamentos não relacionados, e nenhum lugar óbvio para colocar código novo.

---

## 2. Conceito Central

### God Object

**O que é:** uma classe que concentra responsabilidades de domínios distintos — persistência, validação, cálculo, notificação, relatório — em um único lugar.

**Como surge:** cada nova feature vai para a classe que "parece mais próxima". Sem revisão, a classe cresce sem limite.

**Como identificar:**
- Mais de 5–6 métodos cobrindo domínios completamente diferentes
- Nome vago: `Gestor`, `Manager`, `Handler`, `Utils`, `Helper`
- Dificuldade de testar um método sem instanciar dependências de outros

**Como refatorar:** aplicar SRP (Single Responsibility Principle). Cada classe tem uma razão para mudar.

```python
# ❌ Ruim: GestorClientePedido com 12 métodos
class GestorClientePedido:
    def buscar_cliente(self, ...): ...
    def salvar_cliente(self, ...): ...
    def validar_cpf(self, ...): ...
    def calcular_total(self, ...): ...
    def enviar_email(self, ...): ...
    def gerar_boleto(self, ...): ...
    def atualizar_estoque(self, ...): ...
    def gerar_relatorio(self, ...): ...
    # ... mais 4 métodos

# ✅ Bom: cada classe tem uma responsabilidade
class RepositorioCliente:     ...  # persistência
class ValidadorDocumento:     ...  # validação de CPF
class ServicoNotificacao:     ...  # emails
class ServicoCobranca:        ...  # boletos
class GeradorRelatorio:       ...  # relatórios e CSV
```

**Custo de não corrigir:** qualquer mudança em notificação toca a mesma classe que persiste clientes — aumentando o risco de regressão e o tamanho dos PRs.

---

### Magic Strings e Magic Numbers

**O que são:** literais de string ou número inline, sem nome, representando estados ou regras de negócio.

**Como surgem:** o desenvolvedor sabe o que `"A"` significa agora. Seis meses depois, outro desenvolvedor não sabe — e não tem como buscar no código.

**Como identificar:**
- `if status == "A"` — o que é "A"?
- `if valor > 1500` — por que 1500? qual regra?
- `prazo = 30` — 30 dias corridos? úteis? horas?

**Como corrigir:** enums para estados de negócio, constantes nomeadas para limites.

```python
# ❌ Ruim
if status == "A" and tipo == "P" and valor > 1500:
    prazo = 30

# ✅ Bom
class StatusPedido(str, Enum):
    ATIVO   = "ativo"
    INATIVO = "inativo"

class TipoPedido(str, Enum):
    PREMIUM = "premium"
    NORMAL  = "normal"

LIMITE_FRETE_GRATIS:  float = 1500.0
PRAZO_PAGAMENTO_DIAS: int   = 30

if status == StatusPedido.ATIVO and tipo == TipoPedido.PREMIUM and valor > LIMITE_FRETE_GRATIS:
    prazo = PRAZO_PAGAMENTO_DIAS
```

**Custo de não corrigir:** renomeação manual em N lugares, erros de digitação silenciosos (`"Ativo"` vs `"ativo"`), busca impossível em IDEs.

---

### Feature Envy

**O que é:** um método que acessa dados de outra classe mais do que da própria. É um sinal de que o método está no lugar errado.

**Como identificar:** o método recebe um objeto como parâmetro e acessa 3 ou mais atributos dele — mais do que usa da própria classe.

**Como refatorar:** mover o método para a classe onde os dados vivem (Fowler: *Move Method*).

```python
# ❌ Ruim: Pedido sabe mais sobre Cliente do que sobre si mesmo
class Pedido:
    def calcular_desconto_fidelidade(self, cliente: Cliente) -> float:
        base  = cliente.historico_compras * 0.05   # dado de Cliente
        bonus = cliente.pontos_acumulados * 0.001  # dado de Cliente
        anos  = 2026 - int(cliente.data_cadastro[:4])  # dado de Cliente
        return min(base + bonus + anos * 2.0, 200.0)

# ✅ Bom: método na classe onde os dados vivem
class Cliente:
    def calcular_desconto_fidelidade(self) -> float:
        base  = self.historico_compras * 0.05
        bonus = self.pontos_acumulados * 0.001
        anos  = 2026 - int(self.data_cadastro[:4])
        return min(base + bonus + anos * 2.0, 200.0)
```

**Custo de não corrigir:** acoplamento espúrio entre classes, lógica de negócio espalhada onde não pertence.

---

### Copy-Paste Inheritance

**O que é:** subclasses que copiam lógica idêntica (ou quase) de cálculo ou comportamento, diferindo apenas em um detalhe mínimo.

**Como identificar:** mesma função `calcular_total()` em `PedidoNormal`, `PedidoUrgente`, `PedidoAgendado` — diferindo só em um ajuste de valor.

**Como refatorar:** Template Method. A lógica base fica na superclasse; a variação mínima vai para um método abstrato.

```python
# ❌ Ruim: calcular_total() copiado em 3 subclasses
class PedidoNormal:
    def calcular_total(self, itens): return round(sum(...), 2)
class PedidoUrgente:
    def calcular_total(self, itens): return round(sum(...) * 1.15, 2)  # copiado
class PedidoAgendado:
    def calcular_total(self, itens): return round(sum(...) + 5.0, 2)   # copiado

# ✅ Bom: lógica base na superclasse, variação nas subclasses
class PedidoBase(ABC):
    def calcular_total(self, itens: List[ItemPedido]) -> float:
        base = sum(i.preco * i.quantidade for i in itens)
        return round(base + self._adicional(base), 2)

    @abstractmethod
    def _adicional(self, base: float) -> float: ...

class PedidoNormal(PedidoBase):
    def _adicional(self, base: float) -> float: return 0.0

class PedidoUrgente(PedidoBase):
    def _adicional(self, base: float) -> float: return base * 0.15

class PedidoAgendado(PedidoBase):
    def _adicional(self, base: float) -> float: return 5.0
```

**Custo de não corrigir:** um bug na lógica base precisa ser corrigido em N lugares. A chance de esquecer um é alta.

---

## 3. Exercício

**Domínio:** sistema de RH / folha de pagamento.

O arquivo `exercicios/exercicio.py` apresenta `GestorFolhaPagamento` com 12 métodos cobrindo CRUD, cálculo de INSS/FGTS, notificação, relatório e validação — além de magic strings (`"C"`, `"P"`, `"E"`) e magic numbers (`1412`, `0.075`, `0.08`).

**Objetivo:**
1. Quebrar o God Object em classes especializadas: `RepositorioFuncionario`, `CalculadorInss`, `CalculadorFgts`, `ServicoNotificacao`, `GeradorRelatorioRH`.
2. Substituir magic strings pela `enum CategoriaCargo` e magic numbers por constantes nomeadas (`SALARIO_MINIMO_2026`, `ALIQUOTA_FGTS` etc.).

Equivalentes em PHP, TypeScript e ADVPL/TLPP na mesma pasta.

---

## 4. Checklist — Anti-patterns na revisão de código

- [ ] Esta classe tem mais de 5 métodos cobrindo domínios diferentes? (→ God Object)
- [ ] Existem strings ou números sem nome representando estados de negócio? (→ Magic Strings/Numbers)
- [ ] Este método usa mais dados de outra classe do que da própria? (→ Feature Envy)
- [ ] Lógica idêntica (ou quase) aparece em 2+ subclasses? (→ Copy-Paste Inheritance)

---

## 5. Referências

- Martin, Robert C. *Clean Code*. Cap. 17 — Smells and Heuristics.
- Fowler, Martin. *Refactoring: Improving the Design of Existing Code*. Cap. 3 — Bad Smells in Code.
- Fowler, Martin. *Refactoring*. Catálogo: Move Method, Replace Magic Literal with Symbolic Constant, Extract Class.
