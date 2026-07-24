# Tutorial 28 — Testes de Integração de API

> Referência: Martin Fowler, "IntegrationTest" e "TestPyramid" (martinfowler.com);
> documentação FastAPI — TestClient; Kent C. Dodds, "Write tests. Not too many. Mostly integration."

## 1. Contexto e Motivação

Um teste de unidade verifica uma parte pequena do sistema em isolamento. Ele confirma, por exemplo, que uma função calcula corretamente o total de um pedido quando recebe itens e descontos conhecidos. As dependências que não fazem parte daquela lógica — banco de dados, rede, relógio, filas ou serviços externos — são normalmente substituídas, controladas ou simplesmente não utilizadas.

Isso é valioso, mas não responde a outra pergunta: as partes do sistema se conectam corretamente quando trabalham juntas? Um teste de integração existe para responder a essa pergunta. Ele inclui componentes reais em uma mesma execução e verifica a fronteira entre eles.

Em uma API, essa fronteira não é apenas a regra de negócio. Ela inclui o contrato que a aplicação oferece a quem a consome: endereço da rota, método HTTP, parâmetros, headers, corpo da requisição, validação dos dados, código de status e formato da resposta. Um aplicativo mobile, uma página web ou outro sistema não chama diretamente a função Python que cria um pedido. Ele envia uma requisição para `POST /pedidos` e interpreta a resposta recebida.

É por isso que uma suíte de testes unitários pode estar inteiramente verde e, ainda assim, a API estar quebrada para seus consumidores. Imagine que a lógica de negócio continue calculando corretamente o campo `total`, mas alguém altere a resposta pública da API para devolver `valor_total`. O teste unitário da função de cálculo continuará passando: internamente, o valor está certo. O aplicativo mobile, porém, poderá falhar porque seu contrato esperava receber o campo `total` no JSON.

Um teste de integração de API encontra esse tipo de problema porque testa a aplicação a partir do ponto de vista de um consumidor. Em vez de chamar uma função interna, ele envia uma requisição para a rota e examina a resposta produzida. Não basta confirmar que a rota respondeu com `201 Created`; o teste precisa verificar também os campos que constituem o contrato, como o identificador criado, o status inicial e o valor total.

---

## 2. Conceito Central

### (a) Duas formas de executar o teste: em processo ou contra um servidor real

Há mais de uma forma de executar esse teste, e a diferença entre elas está no escopo da integração. Em uma abordagem, o teste cria uma requisição com método, URL, headers e corpo HTTP, mas a entrega diretamente à aplicação, dentro do mesmo processo. Ele verifica o contrato HTTP da aplicação, mas não abre uma conexão de rede. Em outra, o teste inicia — ou se conecta a — um servidor real e envia a requisição por `localhost`. Nesse caso, ele verifica também a infraestrutura de execução: processo do servidor, porta, conexão TCP e alguns comportamentos de timeout.

As duas abordagens são testes de integração legítimos. A primeira integra os componentes que implementam a API; a segunda acrescenta a integração entre a aplicação e o ambiente em que ela é servida. A escolha depende do risco que se deseja cobrir. Para testar muitas rotas a cada alteração de código, a abordagem em processo tende a ser mais rápida e estável. Para verificar se a aplicação sobe e responde como serviço de rede, testes contra um servidor real complementam a suíte.

### (b) A tecnologia: FastAPI, ASGI e o `TestClient`

Neste tutorial, aplicaremos essa ideia a uma API de pedidos escrita em FastAPI, disponível em [`exemplos/app.py`](exemplos/app.py). FastAPI é um framework Python para construir APIs web. Em uma execução normal, um servidor como o Uvicorn recebe requisições HTTP da rede e as encaminha para a aplicação FastAPI. A interface usada nessa comunicação é chamada ASGI.

Os testes usarão o `TestClient`, fornecido pelo FastAPI/Starlette. Ao executar `cliente.post("/pedidos", json=dados)`, o teste monta uma requisição como a que seria enviada por um consumidor real, mas a encaminha diretamente à aplicação por ASGI. Não é necessário iniciar o Uvicorn, abrir uma porta ou criar uma conexão TCP.

Mesmo sem rede, a rota é executada de verdade. O FastAPI identifica `POST /pedidos`, lê e valida o JSON recebido, executa dependências e *middlewares*, chama o código da rota, define o status HTTP, monta os headers e serializa a resposta. O `TestClient` não é um simulador da API: ele testa a API real, retirando apenas a camada de servidor e transporte de rede.

Isso também delimita o que esse teste não garante. Ele não confirma que o Uvicorn inicia corretamente, que a porta está disponível ou que os timeouts de rede estão bem configurados. Além disso, ele não transforma automaticamente banco de dados, filas ou serviços externos em dependências falsas: se a rota estiver configurada para acessá-los, o teste poderá acessá-los também. Quando for necessário isolá-los, será preciso substituí-los explicitamente no ambiente de teste.

### (c) Verificar o contrato completo, campo a campo

A seção anterior descreveu o que verificar; esta mostra o código. A diferença entre um teste que dá confiança e um que apenas parece dar está em quanto da resposta ele examina. Um teste que confere só o código de status passa mesmo quando o corpo está errado — o total calculado incorretamente, um campo ausente, o status inicial trocado. Os dois testes abaixo vêm de [`exemplos/integracao_ruins.py`](exemplos/integracao_ruins.py) e [`exemplos/integracao_bons.py`](exemplos/integracao_bons.py):

```python
# ❌ Confirma apenas que a rota respondeu — não confirma o que ela respondeu
def test_cria_pedido():
    resposta = cliente.post("/pedidos", json={
        "cliente": "Ana",
        "itens": [{"produto": "Livro", "quantidade": 2, "preco_unitario": 30.0}],
    })
    assert resposta.status_code == 201

# ✅ Confere os campos do contrato: total calculado (2 × 30,00 = 60,00) e status inicial "aberto"
def test_cria_pedido_retorna_201_com_total_calculado(cliente):
    resposta = cliente.post("/pedidos", json={
        "cliente": "Ana",
        "itens": [{"produto": "Livro", "quantidade": 2, "preco_unitario": 30.0}],
    })
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["total"] == 60.0
    assert corpo["status"] == "aberto"
    assert corpo["id"] >= 1
```

O primeiro teste sobreviveria a um bug que devolvesse o total como `0.0`. O segundo falharia, que é exatamente o que se espera dele.

### (d) Isolamento de estado entre testes

Um bom teste depende apenas do que ele mesmo prepara. Quando vários testes compartilham o mesmo estado — o mesmo dicionário de pedidos, a mesma aplicação já povoada por execuções anteriores —, a ordem em que rodam passa a influenciar o resultado. Um teste pode passar porque outro rodou antes dele e deixou um pedido no lugar certo, e falhar quando executado sozinho. Suítes assim são difíceis de confiar e impossíveis de paralelizar.

A forma de garantir o isolamento é dar a cada teste o seu próprio estado. A aplicação em [`exemplos/app.py`](exemplos/app.py) foi escrita para permitir isso: em vez de expor uma instância pronta, ela oferece a função `criar_app()`, chamada de *factory*. Cada chamada devolve uma aplicação nova, com um dicionário de pedidos vazio. Uma fixture do pytest chama essa função uma vez para cada teste, entregando a ele um `TestClient` sobre uma aplicação limpa.

```python
# ❌ TestClient global no módulo: todos os testes compartilham a mesma aplicação e o mesmo estado
cliente = TestClient(criar_app())

def test_cria_pedido():
    cliente.post("/pedidos", json={...})            # cria o pedido id=1

def test_busca_pedido_criado_anteriormente():
    cliente.get("/pedidos/1")                        # só passa se o teste acima rodou antes

# ✅ Fixture: cada teste recebe uma aplicação nova, com estado zerado
@pytest.fixture
def cliente() -> TestClient:
    return TestClient(criar_app())

def test_cria_pedido_retorna_201_com_total_calculado(cliente):
    ...
```

### (e) Cobrir os caminhos de erro: 404, 409 e 422

O contrato de uma API não descreve apenas o que acontece quando tudo dá certo. Ele descreve também como a aplicação responde quando algo sai do esperado, e é justamente aí que costuma estar o comportamento menos testado. Uma suíte que exercita só o caminho feliz — criar um pedido, pagar um pedido — deixa boa parte do contrato sem cobertura. A aplicação de exemplo define três caminhos de erro, cada um com um significado próprio.

O primeiro é o pedido inexistente. Uma requisição `GET /pedidos/999` para um pedido que nunca foi criado recebe `404 Not Found`. O código de status é o meio pelo qual o consumidor entende o que ocorreu sem precisar interpretar o corpo, e `404` afirma algo específico: o recurso não existe. Isso é diferente de uma falha do servidor (`500`). Um cliente bem construído reage de formas distintas a cada caso — no `404`, informa que o pedido não foi encontrado; no `500`, tenta novamente ou aciona o monitoramento.

O segundo é o conflito de estado. Pagar um pedido que já está pago não é um dado mal formado; é uma operação incompatível com o estado atual do recurso. A resposta correta é `409 Conflict`, e não `400 Bad Request`, porque a requisição em si está bem formada — o que impede a operação é a situação do pedido. Essa distinção orienta a reação do consumidor, que tratará um `409` como "este pedido já foi pago", e não como "corrija os dados enviados".

O terceiro é o corpo inválido, e aqui entra o Pydantic. Em FastAPI, o formato esperado do corpo é declarado como uma classe — no caso, `NovoPedido`, que contém uma lista de `ItemPedido`. Antes de o código da rota executar, o FastAPI valida o corpo recebido contra essa classe e, se ele não corresponde, responde `422 Unprocessable Entity` por conta própria. A aplicação vai além do formato e declara duas regras de negócio como validação: a lista de itens não pode ser vazia e a quantidade precisa ser positiva. Uma requisição com `itens: []` é recusada com `422` antes de se tornar um pedido.

A suíte [`exemplos/integracao_bons.py`](exemplos/integracao_bons.py) dedica um teste a cada um desses caminhos. Cada resposta de erro é uma parte do contrato que o consumidor vai encontrar em produção, e cobri-las é o que permite dizer que a suíte descreve a API, e não apenas o trecho que já se sabia funcionar.

---

## 3. Ferramentas Modernas por Linguagem

| Linguagem | Framework | Instalar | Executar |
|---|---|---|---|
| Python | **pytest + FastAPI TestClient** | `pip install -r requirements.txt` | `pytest -v` |
| PHP | **PHPUnit 11 + Guzzle** (contra servidor real) | `composer install` | `vendor/bin/phpunit` |
| TypeScript | **Vitest + supertest** | `npm install` | `npx vitest run` |
| ADVPL/TLPP | **PROBAT + FWRest/HttpGet** | já incluso no ambiente TOTVS (tlppCore) | executar via AppServer com o endpoint publicado |

Os arquivos [`equivalente.php`](exemplos/equivalente.php), [`equivalente.ts`](exemplos/equivalente.ts) e [`equivalente.tlpp`](exemplos/equivalente.tlpp) — com os pares em `exercicios/` — trazem o mesmo par bom/ruim na sintaxe idiomática de cada linguagem. Os exemplos em PHP (com Guzzle) e em ADVPL/TLPP (com FWRest) adotam a variante contra servidor real descrita na seção 2(a). Eles servem de referência, não de suíte executável neste workshop: PHP e Vitest não estão instalados neste ambiente, e o PROBAT depende de um AppServer TOTVS no ar. O Python é a implementação que você executa; as outras três mostram como o mesmo padrão se traduz.

---

## 4. Exercício

O arquivo [`exercicios/exercicio.py`](exercicios/exercicio.py), e os equivalentes `.php`, `.ts` e `.tlpp`, trazem uma suíte de testes sobre a rota `POST /pedidos/{id}/pagar` com os mesmos três problemas estruturais de [`exemplos/integracao_ruins.py`](exemplos/integracao_ruins.py):

1. Um `TestClient` global, compartilhado entre os testes, pelo qual o estado vaza de um para o outro e a ordem de execução passa a importar.
2. Verificação restrita ao `status_code`, sem examinar o corpo da resposta.
3. Dependência de ordem: um teste assume que o pedido criado por outro ainda existe, com o identificador que ele espera.

A [`exercicios/app.py`](exercicios/app.py) é uma cópia local da aplicação, idêntica à de `exemplos/`. Como o repositório não permite que um arquivo importe de outro diretório, a aplicação é replicada aqui para que o exercício rode por conta própria.

**Etapas:**

1. Execute a suíte como está. Ela passa — os problemas são de estrutura, não de execução.
2. Identifique os três problemas, comparando com a lista de `integracao_ruins.py` na seção 2(d).
3. Refatore seguindo [`exemplos/integracao_bons.py`](exemplos/integracao_bons.py): uma fixture que cria um `TestClient(criar_app())` por teste, nomes que descrevem o comportamento esperado e asserções sobre os campos do corpo, além do status.
4. Compare o resultado com [`exercicios/gabarito.py`](exercicios/gabarito.py), ou com o gabarito na sua linguagem.

```bash
# Rodar o exercício e o gabarito (Python)
cd exercicios
pytest exercicio.py -v
pytest gabarito.py -v
```

---

## 5. Checklist

- [ ] O teste examina os campos do corpo da resposta, além do código de status?
- [ ] Cada teste monta o próprio estado, por meio de uma factory e de uma fixture por teste, e roda independente da ordem?
- [ ] Os caminhos de erro 404, 409 e 422 têm, cada um, o seu teste?
- [ ] O teste evita I/O de rede externa? Quando precisa chamar um serviço de terceiros, ele está isolado, marcado com `@pytest.mark.skip` e documentado?
- [ ] O nome do teste descreve o comportamento e o resultado esperado, sem exigir a leitura do corpo do teste?

O teste que ilustra dependência de rede real em `integracao_ruins.py` (`test_consulta_servico_externo`) está marcado com `@pytest.mark.skip(reason="depende de rede real — anti-padrão ilustrado")`, para não quebrar a suíte em CI ou em ambientes offline. O defeito que ele demonstra — lentidão, instabilidade e falha quando a rede cai — continua existindo independentemente de o teste rodar. O `skip` serve à didática; em produção, a resposta certa é não escrever o teste dessa forma, e não escondê-lo atrás de um `skip` permanente.

---

## 6. Referências

- **FOWLER, Martin.** "IntegrationTest" (bliki).
  `https://martinfowler.com/bliki/IntegrationTest.html`
  Define o que caracteriza um teste de integração e por que a fronteira entre "unidade" e "integração" costuma ser mais sobre isolamento do que sobre o número de componentes envolvidos.

- **FOWLER, Martin.** "TestPyramid" (bliki).
  `https://martinfowler.com/bliki/TestPyramid.html`
  O modelo de proporção entre unidade, integração e e2e apresentado na Sessão 7 — a base para decidir quanto investir em cada camada.

- **FastAPI.** "Testing" — documentação oficial sobre `TestClient`.
  `https://fastapi.tiangolo.com/tutorial/testing/`
  Referência oficial do padrão usado neste tutorial: o TestClient em memória, via ASGI.

- **DODDS, Kent C.** "Write tests. Not too many. Mostly integration." (blog).
  O argumento por trás da variação "trophy" de testes, citada na Sessão 7 — relevante aqui porque os testes de integração de API são a camada que essa variação recomenda enfatizar.
