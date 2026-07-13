# Tutorial 25 — Dublês de Teste

> Referência: Martin Fowler, "Mocks Aren't Stubs"; Gerard Meszaros,
> *xUnit Test Patterns* (capítulo sobre Test Doubles)

## 1. Contexto e Motivação

O Tutorial 24 estabeleceu AAA, FIRST e nomenclatura comportamental para testes de unidade isolados. Mas a maior parte do código de produção não é feita só de funções puras — depende de gateways de pagamento, APIs externas, bancos de dados, filas, relógio do sistema. Testar esse código exige uma decisão: como isolar a unidade sendo testada das dependências que ela usa, sem perder a capacidade de verificar que ela se comporta corretamente?

A resposta é **dublê de teste** (do inglês *test double*, numa analogia direta com dublês de cinema): um objeto que substitui uma dependência real durante o teste, com comportamento controlado e previsível. O termo genérico "mock" é usado informalmente para qualquer dublê — mas Gerard Meszaros, em *xUnit Test Patterns*, formalizou uma taxonomia de cinco tipos distintos, cada um resolvendo um problema diferente. Usar o tipo errado no lugar errado é a causa mais comum de suítes de teste lentas, frágeis ou que dão falsa confiança.

Este tutorial ensina a taxonomia completa (Dummy, Stub, Fake, Spy, Mock), quando usar cada um, e dois anti-padrões que surgem do uso indiscriminado de dublês.

---

## 2. Conceito Central

### Taxonomia: Dummy, Stub, Fake, Spy, Mock

Os cinco tipos de dublê, do mais simples ao mais sofisticado, todos ilustrados em `exemplos/dubles_bons.py`:

**Dummy** — um objeto passado apenas para satisfazer uma assinatura de método, mas nunca de fato usado no caminho testado. Existe só para o código compilar/rodar.

```python
def test_dummy_notificacao_nao_e_exercitada_quando_pagamento_recusado():
    # Dummy: um objeto passado apenas para satisfazer uma assinatura,
    # nunca de fato utilizado no caminho testado aqui.
    gateway = GatewayPagamentoStub(status="recusado")
    _notificacao_dummy = object()  # nunca chamado neste teste
    resultado = gateway.cobrar(50.0)
    assert resultado.status == "recusado"
```

**Stub** — devolve uma resposta fixa e pré-programada para uma chamada, sem lógica real por trás. Um Stub nunca é usado para *verificar* que foi chamado — ele só alimenta o teste com um cenário controlado.

```python
class GatewayPagamentoStub:
    """Stub: devolve resposta fixa e pré-programada, sem verificar interação."""

    def __init__(self, status: str = "aprovado"):
        self._status = status

    def cobrar(self, valor: float) -> ResultadoPagamento:
        return ResultadoPagamento(status=self._status, valor=valor)
```

**Fake** — uma implementação funcional real, porém simplificada e inadequada para produção — tipicamente um repositório em memória no lugar de um banco de dados. Ao contrário do Stub, um Fake tem lógica de verdade (guarda e recupera dados corretamente); só não é a implementação de produção.

```python
class RepositorioPedidoFake:
    """Fake: implementação funcional leve, em memória — sem instrumentação de chamadas."""

    def __init__(self):
        self._pedidos = {}

    def salvar(self, pedido_id: str, dados: dict) -> None:
        self._pedidos[pedido_id] = dados

    def buscar(self, pedido_id: str):
        return self._pedidos.get(pedido_id)
```

**Spy** — registra as chamadas que recebe para permitir inspeção posterior, sem expectativa pré-programada sobre o que "deveria" acontecer. A diferença para o Mock é sutil, mas importante: o Spy só observa; a decisão de falhar o teste vem de um `assert` explícito depois, escrito por quem lê o teste.

```python
def test_spy_registra_chamadas_para_inspecao_posterior():
    # Spy: Mock usado sem expectativa pré-programada — só registra e é
    # inspecionado depois, ao contrário do Mock com assert_called_once_with.
    spy = Mock(wraps=RepositorioPedidoFake())
    spy.salvar("P002", {"total": 200.0})
    assert spy.salvar.call_count == 1
    assert spy.buscar("P002") == {"total": 200.0}
```

**Mock** — pré-programado com uma **expectativa** sobre como será chamado (quantas vezes, com quais argumentos), e o próprio dublê falha o teste se a expectativa não for cumprida. É o único dos cinco tipos que verifica *comportamento de interação* (que uma chamada aconteceu) em vez de *estado* (qual foi o resultado).

```python
def test_processa_pagamento_aprovado_notifica_cliente():
    gateway = GatewayPagamentoStub(status="aprovado")
    notificacao = Mock()
    processador = ProcessadorPagamento(gateway, notificacao)

    resultado = processador.processar(100.0, "cliente@teste.com")

    assert resultado.status == "aprovado"
    notificacao.enviar.assert_called_once_with("cliente@teste.com", "Pagamento aprovado")
```

Repare no par de testes em `dubles_bons.py`: `test_processa_pagamento_aprovado_notifica_cliente` usa Mock porque o comportamento esperado é uma **ação colateral** (enviar notificação) que não tem um valor de retorno para inspecionar — só dá pra verificar que a chamada aconteceu. Já `test_pagamento_recusado_nao_notifica_cliente` usa o mesmo Mock para provar a ausência de uma chamada (`assert_not_called()`), o outro lado da mesma moeda.

---

### Tabela de decisão

| Preciso de... | Uso |
|---|---|
| Resposta fixa e previsível para uma chamada | **Stub** |
| Verificar que uma interação (chamada, ordem, argumentos) aconteceu | **Mock** |
| Comportamento funcional leve, sem instrumentar chamadas | **Fake** |
| Satisfazer uma assinatura de método sem exercitar o objeto | **Dummy** |
| Registrar chamadas para inspecionar depois, sem expectativa prévia | **Spy** |

Regra prática: comece sempre pela pergunta "o que este teste precisa verificar?". Se a resposta é "o valor que a função retorna", use Stub/Fake e um `assert` de estado. Se a resposta é "que uma ação colateral aconteceu" (enviar e-mail, gravar log, chamar uma API de terceiros), aí sim use Mock ou Spy — e só nesse caso.

---

### Anti-pattern: over-mocking

Mockar objetos de valor ou funções puras é desperdício — eles já são rápidos, determinísticos e não têm efeito colateral, então não há isolamento a ganhar. Pior: um mock desnecessário adiciona ruído ao teste e ainda o acopla a detalhes de implementação.

```python
# ❌ Over-mocking: ResultadoPagamento é um dataclass imutável, sem
# I/O nem efeito colateral — mockar aqui não protege nada, só ofusca o teste
from unittest.mock import Mock

resultado_mock = Mock()
resultado_mock.status = "aprovado"
resultado_mock.valor = 100.0
assert resultado_mock.status == "aprovado"  # não testou nada de verdade

# ✅ Objeto de valor real: mais simples, mais claro, mesma garantia
resultado = ResultadoPagamento(status="aprovado", valor=100.0)
assert resultado.status == "aprovado"
```

O teste `test_processa_pagamento_com_mock_fragil`, em `exemplos/dubles_ruins.py`, ilustra a variante mais perigosa deste anti-padrão: um `MagicMock()` usado para verificar a **ordem exata** de chamadas internas (`method_calls[0][0] == "cobrar"`). Esse teste está acoplado à implementação — qualquer refatoração interna do `ProcessadorPagamento` que preserve o comportamento observável (o pagamento ainda é processado corretamente) pode quebrar esse teste sem que nenhum bug real tenha sido introduzido. Compare com `dubles_bons.py`, onde o Mock verifica apenas que `enviar()` foi chamado com os argumentos certos — uma verificação de contrato, não de implementação interna.

---

### Anti-pattern: mockar o que você não é dono

Mockar diretamente uma biblioteca de terceiros (SDK de pagamento, cliente HTTP, ORM) acopla toda a suíte de testes à API pública dessa lib. Quando a lib lança uma nova versão com uma assinatura de método diferente, os mocks continuam "passando" (porque nada os invalida automaticamente) enquanto o código de produção já está quebrado — um falso positivo caro de descobrir.

```python
# ❌ Mocka a lib de terceiros diretamente em cada teste
from unittest.mock import patch

@patch("stripe.Charge.create")
def test_cobra_com_stripe_mockado_direto(mock_create):
    mock_create.return_value = {"status": "succeeded"}
    ...  # se a assinatura de Charge.create mudar numa versão nova, este mock não avisa

# ✅ Encapsula a lib com um Adapter próprio — só o Adapter conhece a API externa
class GatewayStripe:
    def cobrar(self, valor: float) -> ResultadoPagamento:
        resposta = stripe.Charge.create(amount=int(valor * 100), currency="brl")
        status = "aprovado" if resposta["status"] == "succeeded" else "recusado"
        return ResultadoPagamento(status=status, valor=valor)

# O restante da suíte testa contra a interface do Adapter (GatewayPagamentoStub),
# não contra a API do Stripe — exatamente o padrão usado em dubles_bons.py.
```

A prática recomendada: encapsule a biblioteca externa com um **Adapter** de fronteira fina (só traduz chamadas), teste o resto do sistema contra a interface desse Adapter (com Stub/Fake, como em `dubles_bons.py`), e reserve testes de integração — não testes de unidade — para verificar que o Adapter realmente conversa bem com a lib real.

---

## 3. Ferramentas Modernas por Linguagem

| Linguagem | Ferramenta | Cria... |
|---|---|---|
| Python | `unittest.mock` (`Mock`, `MagicMock`), `pytest-mock` | Stub/Mock/Spy via `Mock()`, `Mock(wraps=...)` para Spy |
| PHP | PHPUnit 11 — `createStub()` / `createMock()` | Stub via `createStub()`; Mock com expectativas via `createMock()` + `expects()` |
| TypeScript | Vitest — `vi.fn()`, `vi.mock()`, `vi.spyOn()` | Mock simples via `vi.fn()`; Spy sobre objeto real via `vi.spyOn()`; módulo inteiro via `vi.mock()` |
| ADVPL/TLPP | nenhuma — seams manuais | Classe escrita à mão implementando o mesmo "contrato" por convenção, recebida via construtor |

Nas quatro linguagens, o **Fake** nunca vem de uma biblioteca de mocking — é sempre uma classe/estrutura escrita à mão (`RepositorioPedidoFake`, `RepositorioEnderecoFake`), porque um Fake precisa de lógica funcional real (guardar e recuperar dados), não apenas de respostas programadas.

---

## 4. Nota ADVPL

ADVPL/TLPP não tem framework de mocking equivalente a `unittest.mock`, PHPUnit ou Vitest — não há `createStub()`, `vi.fn()` ou qualquer geração automática de dublês. A prática padrão é a mesma discutida no **Tutorial 07** (código legado) sobre **seams**: expor um ponto de substituição (tipicamente um parâmetro de classe no construtor) e passar manualmente uma classe que implementa o mesmo contrato por convenção — os mesmos métodos, com a mesma assinatura, mas comportamento controlado para teste.

`exemplos/equivalente.tlpp` mostra o contraste: `ProcessarPagamentoSemSeam` instancia `GatewayPagamentoReal` internamente (sem seam, impossível testar sem infraestrutura real); `ProcessadorPagamento` recebe o gateway via construtor (seam), permitindo passar `GatewayPagamentoStub` — uma classe manual, sem nenhuma mágica de framework por trás.

---

## 5. Exercício

O arquivo `exercicios/exercicio.py` (e seus equivalentes `.php`, `.ts`, `.tlpp`) contém `ServicoEntrega`, que depende de `ApiCepReal` (chamada de rede real/simulada, lenta) e `RepositorioEnderecoReal` (banco real/simulado), ambos instanciados internamente — sem seam algum. O teste fornecido passa, mas leva ~0,5s por causa das dependências reais.

**Etapas:**

1. Rode o exercício como está e observe a lentidão (`pytest exercicios/exercicio.py -v --durations=0`).
2. Introduza um seam: `ServicoEntrega` deve receber `api_cep` e `repositorio` via construtor, em vez de instanciá-los internamente.
3. Crie um **Stub** para a API de CEP (`ApiCepStub`, resposta fixa) e um **Fake** para o repositório (`RepositorioEnderecoFake`, em memória, com um método de inspeção como `foi_salvo(pedido_id)`).
4. Reescreva os testes usando os dublês — devem rodar em milissegundos, sem `time.sleep`/delay algum.
5. Compare com `exercicios/gabarito.*` na sua linguagem.

```bash
# Rodar o exercício (Python) — lento, ~0.5s
pytest exercicios/exercicio.py -v --durations=0

# Comparar com o gabarito — rápido, sem sleep
pytest exercicios/gabarito.py -v
```

---

## 6. Checklist

- [ ] O dublê escolhido corresponde ao que o teste realmente precisa verificar (estado vs. interação)?
- [ ] Stubs são usados só para respostas fixas — nunca para verificar quantas vezes foram chamados?
- [ ] Mocks verificam apenas comportamento observável (contrato), não detalhes de implementação interna (ordem exata de chamadas privadas)?
- [ ] Fakes têm lógica funcional real (não apenas retornam valores fixos)?
- [ ] Objetos de valor e funções puras permanecem reais nos testes, sem mock desnecessário?
- [ ] Bibliotecas de terceiros são encapsuladas por um Adapter antes de qualquer double, em vez de mockadas diretamente?
- [ ] O double está isolado do teste (sem I/O real, sem `time.sleep`/delay algum)?

---

## 7. Referências

- **FOWLER, Martin.** "Mocks Aren't Stubs" (bliki).
  `https://martinfowler.com/articles/mocksArentStubs.html`
  O artigo que formalizou a distinção entre testes baseados em estado (Stub/Fake) e testes baseados em interação (Mock), e cunhou grande parte do vocabulário usado neste tutorial.

- **MESZAROS, Gerard.** *xUnit Test Patterns: Refactoring Test Code*. Addison-Wesley, 2007.
  A referência definitiva sobre padrões de teste, incluindo o capítulo que define formalmente Dummy, Stub, Fake, Spy e Mock como categorias distintas de Test Double.

- **FEATHERS, Michael.** *Working Effectively with Legacy Code*. Prentice Hall, 2004.
  Cap. 4 (*The Seam Model*) — a técnica de seams usada na Nota ADVPL (seção 4) e já apresentada no Tutorial 07 para tornar código legado testável sem framework de mocking.

- **OSHEROVE, Roy.** *The Art of Unit Testing*. 2. ed. Manning, 2013.
  Cap. 2–4 tratam diretamente de stubs e mocks, com exemplos de quando cada tipo de dublê é apropriado.
