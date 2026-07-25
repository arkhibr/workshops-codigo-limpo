# Tutorial 26 — Massa de Dados para Testes

> Referência: Gerard Meszaros, *xUnit Test Patterns*; documentação de
> `factory_boy`, `Hypothesis`, `fast-check`

## 1. Contexto e Motivação

### Mystery Guest e duplicação de setup

Os Tutoriais 24 e 25 resolveram como estruturar um teste (AAA, FIRST, nomenclatura comportamental) e como isolar uma unidade das suas dependências (dublês de teste). Falta resolver um terceiro problema, tão comum quanto os outros dois: como preparar os **dados** de entrada de um teste sem que essa preparação vire, ela mesma, uma fonte de acoplamento e ruído.

O sintoma mais comum é o **Mystery Guest** (Meszaros, *xUnit Test Patterns*): um teste que depende de um objeto de dados grande, montado por inteiro, cujos detalhes irrelevantes ao cenário sendo testado ficam escondidos no meio de dezenas de campos. Quem lê o teste não consegue responder rapidamente "o que este teste realmente precisa que seja verdade para passar?" — porque a resposta está soterrada num literal de cliente, endereço, forma de pagamento e cupom, quando só o cupom importa.

[`exemplos/massa_ruins.py`](exemplos/massa_ruins.py) mostra o padrão: dois testes que aplicam um cupom de desconto, cada um recriando um pedido inteiro (cliente, itens, endereço de entrega, forma de pagamento, datas) só para variar o campo `cupom_desconto`. Além do Mystery Guest, há duplicação — se o formato de `endereco_entrega` mudar (um novo campo obrigatório, por exemplo), toda a suíte de testes que monta pedidos manualmente precisa ser editada, mesmo que nenhum desses testes verifique nada sobre endereço.

```python
# ❌ Mystery Guest: 8 campos montados à mão, mas só "cupom_desconto" importa
def test_cupom_aplica_desconto():
    pedido = {
        "id": "P001",
        "cliente": {"id": "C1", "nome": "Maria Silva", "email": "maria@teste.com", "cpf": "111.111.111-11"},
        "itens": [{"produto": "Notebook", "preco": 3000.0, "quantidade": 1}],
        "endereco_entrega": {"rua": "Rua A", "numero": "100", "cidade": "SP", "cep": "01000-000"},
        "forma_pagamento": "cartao",
        "cupom_desconto": "PROMO10",
        "data_criacao": "2026-01-01",
        "status": "pendente",
    }
    resultado = aplicar_cupom(pedido, "PROMO10")
    assert resultado["itens"][0]["preco"] == 2700.0
```

A solução não é "escrever menos dados" — é **centralizar a montagem dos dados de teste** num único lugar que aplica valores padrão sensatos, deixando cada teste declarar apenas o que é relevante para ele. Esse é o papel dos padrões apresentados a seguir: Object Mother, Test Data Builder e Factories.

---

## 2. Conceito Central

### Object Mother vs. Test Data Builder

Ambos os padrões resolvem o mesmo problema — centralizar a criação de massa de dados de teste — mas equilibram de forma diferente a simplicidade e a escala.

**Object Mother** é uma classe (ou módulo) com métodos de fábrica nomeados para cenários fixos e conhecidos: `Pedidos.pedidoComCupomValido()`, `Pedidos.pedidoVIPSemDesconto()`, `Clientes.clienteInadimplente()`. Cada método já devolve o objeto pronto, sem parâmetros de configuração (ou com poucos). É extremamente simples de ler e usar — o nome do método já documenta o cenário.

O problema do Object Mother aparece quando o número de combinações cresce: se você precisa de "pedido com cupom, cliente VIP, endereço internacional, pagamento em boleto", ou você cria um método para cada combinação (explosão combinatória de nomes) ou o método passa a aceitar tantos parâmetros opcionais que perde a vantagem de simplicidade que o padrão prometia.

**Test Data Builder** resolve exatamente esse ponto fraco: em vez de métodos fixos, uma classe builder aplica valores padrão sensatos no construtor e expõe métodos encadeáveis (fluent interface) para sobrescrever só o que o teste precisar — `com_item(...)`, `com_cupom(...)`. Cada combinação de cenário é uma composição de chamadas, não um novo método.

```python
class PedidoBuilder:
    """Test Data Builder: valores padrão sensatos, sobrescreve só o relevante."""

    def __init__(self):
        self._pedido = Pedido()

    def com_item(self, produto: str, preco: float, quantidade: int = 1) -> "PedidoBuilder":
        self._pedido.itens = [{"produto": produto, "preco": preco, "quantidade": quantidade}]
        return self

    def com_cupom(self, codigo: str) -> "PedidoBuilder":
        self._pedido.cupom_desconto = codigo
        return self

    def construir(self) -> Pedido:
        return self._pedido


def test_cupom_aplica_10_por_cento_de_desconto():
    pedido = PedidoBuilder().com_item("Notebook", preco=3000.0).com_cupom("PROMO10").construir()
    resultado = aplicar_cupom(pedido, "PROMO10")
    assert resultado.itens[0]["preco"] == 2700.0
```

Compare com [`massa_ruins.py`](exemplos/massa_ruins.py): o teste acima declara só o item e o cupom — os oito campos irrelevantes (cliente, endereço, forma de pagamento, datas) ficam escondidos dentro do `PedidoBuilder`, com valores padrão que ninguém precisa repetir.

**Trade-off resumido:** Object Mother é mais simples de ler para um número pequeno e estável de cenários fixos ("preciso sempre destes 3 ou 4 tipos de pedido"); Test Data Builder escala melhor quando o número de combinações de campos relevantes cresce, porque cada teste compõe só os métodos que precisa, sem multiplicar nomes de método.

---

### Factories

Uma **Factory** (no sentido usado por bibliotecas como `factory_boy` e `fishery`) resolve um problema adjacente: gerar rapidamente um objeto de dados **plausível e válido**, sem que o teste precise se importar com os detalhes de cada campo — normalmente usando um gerador de dados falsos (Faker) por trás.

A diferença conceitual entre Factory e Builder está em **quem decide o quê**: a Factory decide **o que construir** — ela sabe montar um `Cliente` válido do início ao fim, e o teste só pede "me dê um cliente" ou "me dê um cliente com este e-mail específico". O Builder decide **como montar passo a passo** — ele expõe as etapas de construção (`com_item`, `com_cupom`) para que o teste componha o objeto incrementalmente, controlando cada aspecto relevante.

```python
class ClienteFactory(factory.Factory):
    class Meta:
        model = dict

    nome = factory.LazyFunction(fake.name)
    email = factory.LazyFunction(fake.email)
    cpf = factory.LazyFunction(fake.cpf)


def test_cliente_gerado_pela_factory_tem_email_valido():
    cliente = ClienteFactory()
    assert "@" in cliente["email"]
```

Na prática, os dois padrões convivem bem: uma Factory frequentemente usa um Builder internamente (ou vice-versa), e é comum usar Factory para dados "de apoio" que o teste não precisa controlar em detalhe (um cliente qualquer, com nome e e-mail plausíveis) e Builder para a entidade central do cenário, cujos campos relevantes o teste precisa declarar explicitamente.

---

### Testes baseados em propriedade (property-based testing)

Todos os padrões até aqui ainda exigem que **você** escolha os valores de exemplo — `preco=3000.0`, `aliquota=0.18`. Testes baseados em propriedade invertem essa lógica: em vez de escrever exemplos, você declara uma **propriedade** que deve valer para qualquer entrada dentro de um espaço definido, e a ferramenta (Hypothesis, em Python; fast-check, em TypeScript) gera centenas de casos automaticamente, incluindo valores-limite que ninguém pensaria em escrever à mão (zero, negativos, números muito grandes, strings vazias, unicode).

```python
@given(st.floats(min_value=0, max_value=100_000, allow_nan=False, allow_infinity=False))
def test_aplicar_cupom_nunca_gera_preco_negativo(preco):
    pedido = PedidoBuilder().com_item("Item", preco=preco).com_cupom("PROMO10").construir()
    resultado = aplicar_cupom(pedido, "PROMO10")
    assert resultado.itens[0]["preco"] >= 0
```

Esse teste único, com um `@given`, substitui dezenas de testes exemplificados manualmente (`preco=0`, `preco=0.01`, `preco=99999.99`...) — e quando o Hypothesis encontra uma falha, ele automaticamente faz *shrinking*: reduz o caso que falhou ao menor exemplo possível que ainda reproduz o bug, facilitando o diagnóstico.

**O que se ganha:** cobertura de casos-limite que a intuição humana normalmente não considera — é comum um teste baseado em propriedade encontrar um bug de arredondamento, overflow ou codificação que nenhum exemplo manual jamais cobriria, porque ninguém pensou em testar aquele valor específico.

**O que custa:** é mais difícil depurar uma falha do que num teste exemplificado — o caso que falhou não foi escrito por você, então entender *por que* aquele valor específico quebra a lógica exige investigação adicional (embora o shrinking do Hypothesis reduza bastante esse custo). Também exige mais disciplina para escrever a propriedade certa: propriedades fracas demais (`resultado >= 0` quando o esperado seria uma igualdade exata) dão falsa confiança, e propriedades fortes demais podem ser difíceis de expressar ou até calcular no próprio teste.

Property-based testing não substitui os testes exemplificados — ele complementa: use exemplos concretos para documentar comportamento esperado em casos de negócio conhecidos (a Factory/Builder ajudam aqui), e propriedades para varrer o espaço de entradas em busca de casos-limite que a intuição não cobre.

---

## 3. Ferramentas Modernas por Linguagem

| Linguagem | Ferramentas | Papel de cada uma |
|---|---|---|
| Python | `factory_boy` + `Faker` + `Hypothesis` | `factory_boy` implementa Factories (`factory.Factory`); `Faker` gera dados falsos plausíveis (nomes, e-mails, CPF); `Hypothesis` implementa testes baseados em propriedade (`@given`) |
| PHP | `fakerphp/faker` | Gera dados falsos plausíveis; Builders são classes fluentes escritas à mão (`PedidoBuilder`), já que o PHP não tem um equivalente direto ao `factory_boy` amplamente adotado |
| TypeScript | `fishery` + `@faker-js/faker` | `fishery` implementa Factories tipadas (`Factory.define<T>()`); `@faker-js/faker` gera dados falsos plausíveis; `fast-check` (mencionado nas referências) implementa testes baseados em propriedade |
| ADVPL/TLPP | builders manuais | Sem lib de dados fake nem de Factory — o builder é sempre uma função/classe escrita à mão (`MontarPedidoPadrao(aOverrides)`) que centraliza os valores padrão e aplica overrides |

Em todas as quatro linguagens, o princípio é o mesmo independentemente de haver ou não uma biblioteca por trás: **centralizar valores padrão em um único lugar, e deixar cada teste declarar só o que é relevante para o cenário**. As bibliotecas (`factory_boy`, `fishery`, `fakerphp/faker`) automatizam a geração de dados plausíveis; onde elas não existem (ADVPL/TLPP), o mesmo resultado é alcançado escrevendo o builder manualmente — mais verboso, mas com o mesmo efeito sobre a legibilidade dos testes.

---

## 4. Exercício

O arquivo [`exercicios/exercicio.py`](exercicios/exercicio.py) (e seus equivalentes `.php`, `.ts`, `.tlpp`) contém `NotaFiscal`, com o mesmo problema de [`massa_ruins.py`](exemplos/massa_ruins.py): cada teste duplica um literal gigante (número, emitente, destinatário, itens, alíquota, chave de acesso), mudando só a alíquota entre um teste e outro.

**Etapas:**

1. Rode o exercício como está e confirme que os dois testes passam, apesar da duplicação.
2. Extraia um `NotaFiscalBuilder` (ou, em ADVPL/TLPP, uma função `MontarNotaFiscalPadrao(aOverrides)`) com valores padrão sensatos para emitente, destinatário e item.
3. Exponha `com_item(descricao, valor)` e `com_aliquota(valor)` (ou os overrides equivalentes) para sobrescrever só o que cada teste precisa.
4. Reescreva os dois testes usando o builder — cada um deve declarar apenas a alíquota que varia, sem repetir emitente/destinatário/item.
5. Compare com `exercicios/gabarito.*` na sua linguagem.

```bash
# Rodar o exercício (Python)
pytest exercicios/exercicio.py -v

# Comparar com o gabarito
pytest exercicios/gabarito.py -v
```

---

## 5. Checklist

- [ ] Cada teste declara apenas os campos relevantes para o cenário que está verificando (sem Mystery Guest)?
- [ ] Valores padrão sensatos estão centralizados num único lugar (Object Mother, Builder ou Factory), não duplicados em cada teste?
- [ ] Ao escolher entre Object Mother e Test Data Builder, a escolha reflete o número de combinações de cenário (poucos fixos → Object Mother; muitas combinações → Builder)?
- [ ] Dados "de apoio" (que o teste não precisa controlar em detalhe) usam Factory/Faker, em vez de literais fixos e repetitivos?
- [ ] Testes baseados em propriedade são usados para propriedades gerais (invariantes), não como substituto de exemplos concretos de regra de negócio?
- [ ] Uma falha de teste baseado em propriedade foi investigada usando o caso reduzido (shrinking), não o caso aleatório original?
- [ ] Em ADVPL/TLPP, o builder manual está centralizado numa única função/classe, evitando que a montagem de dados se espalhe pelos testes?

---

## 6. Referências

- **MESZAROS, Gerard.** *xUnit Test Patterns: Refactoring Test Code*. Addison-Wesley, 2007.
  Define formalmente Object Mother e Test Data Builder, além do anti-padrão Mystery Guest discutido na seção 1.

- **Documentação oficial do `factory_boy`.**
  `https://factoryboy.readthedocs.io/`
  Referência da biblioteca de Factories usada em [`massa_bons.py`](exemplos/massa_bons.py), incluindo `LazyFunction` e integração com `Faker`.

- **Documentação oficial do `Hypothesis`.**
  `https://hypothesis.readthedocs.io/`
  Referência da biblioteca de testes baseados em propriedade para Python, incluindo o mecanismo de *shrinking* mencionado na seção 2.

- **Documentação oficial do `fast-check`.**
  `https://fast-check.dev/`
  Equivalente ao Hypothesis para o ecossistema TypeScript/JavaScript — testes baseados em propriedade com shrinking automático.

- **Documentação oficial do `fishery`.**
  `https://github.com/thoughtbot/fishery`
  Biblioteca de Factories tipadas para TypeScript usada em [`exemplos/equivalente.ts`](exemplos/equivalente.ts).

- **FEATHERS, Michael.** *Working Effectively with Legacy Code*. Prentice Hall, 2004.
  Contexto complementar sobre por que dados de teste bem estruturados facilitam a introdução de testes de caracterização em código legado (Sessão 2 deste workshop).
