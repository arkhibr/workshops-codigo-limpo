# Tutorial 28 — Testes de Integração de API

> Referência: Martin Fowler, "IntegrationTest" e "TestPyramid" (martinfowler.com);
> documentação FastAPI — TestClient; Kent C. Dodds, "Write tests. Not too many. Mostly integration."

## 1. Contexto e Motivação

Sessão 7 tratou de testes de unidade: unidades isoladas, sem I/O, rodando em milissegundos, no topo da confiança-por-esforço mas na base da pirâmide de testes (unit >> integration > e2e). Uma suíte de unidade perfeita ainda não prova que o sistema funciona **como um todo** — ela prova que cada peça, isolada, se comporta como esperado quando você mesmo prepara as entradas.

Testes de **integração** verificam a colaboração entre componentes reais: o handler HTTP, a serialização de request/response, os códigos de status, a validação declarada no schema. Em vez de chamar uma função Python diretamente, um teste de integração de API sobe (ou simula, em memória) o servidor inteiro e faz requisições HTTP de verdade contra ele — exercitando a camada de transporte que o teste de unidade nunca toca.

O que muda, na prática:
- **HTTP entra na equação:** métodos, rotas, status codes, headers.
- **Serialização entra na equação:** o corpo vai e volta como JSON — um bug de serialização (campo renomeado, tipo trocado) só aparece aqui, nunca num teste de unidade que chama a função Python diretamente.
- **O contrato observável é a resposta HTTP**, não o valor de retorno de uma função.

Este tutorial usa como SUT (`exemplos/app.py`) uma API de pedidos em FastAPI — a mesma que o Tutorial 30 (Sessão 9) vai reaproveitar, agora com persistência real. Os testes aqui usam `TestClient` (em memória, sem subir um processo de servidor), que já é suficiente para caracterizar um teste de integração: ele passa pela camada HTTP/serialização completa, só não abre uma porta de rede.

---

## 2. Conceito Central

### (a) Test client em memória vs. servidor real

`TestClient` (FastAPI/Starlette) monta as requisições e as processa via ASGI diretamente em memória — sem abrir socket, sem porta, sem processo separado. Isso mantém o teste rápido (milissegundos) e ainda assim exercita rotas, validação de schema e serialização de verdade. Um teste contra um **servidor real** (processo `uvicorn` rodando, requisições via rede/`localhost`) vai além: também verifica configuração de processo, timeouts, e é o que os equivalentes PHP (Guzzle) e TLPP (FWRest) deste tutorial fazem, por serem os padrões idiomáticos dessas linguagens. Ambos são testes de integração legítimos; `TestClient` é a opção mais rápida e é a recomendada como padrão neste tutorial.

### (b) Contrato completo, não só o status

Um teste que verifica só `status_code == 200` pode passar mesmo que o corpo da resposta esteja completamente errado — total calculado errado, campo faltando, tipo trocado. "Verde" nesse caso não significa "correto", só significa "não caiu".

```python
# ❌ Só confirma que a rota respondeu — não confirma o que ela respondeu
def test_cria_pedido(cliente):
    resposta = cliente.post("/pedidos", json={...})
    assert resposta.status_code == 201

# ✅ Verifica o contrato completo: status + campos do corpo
def test_cria_pedido_retorna_201_com_total_calculado(cliente):
    resposta = cliente.post("/pedidos", json={...})
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["total"] == 60.0
    assert corpo["status"] == "aberto"
```

### (c) Isolamento de estado — factory + fixture por teste

`app.py` expõe `criar_app()`, uma **factory**: cada chamada devolve uma instância nova do FastAPI com seu próprio dicionário de pedidos em memória. Se um teste guardasse o app (ou o `TestClient`) num escopo compartilhado do módulo, o estado criado por um teste (um pedido com id=1, por exemplo) vazaria para o próximo teste — a ordem de execução passaria a importar, e rodar um teste isolado (`pytest -k test_x`) quebraria.

```python
# ❌ TestClient global — todos os testes do módulo compartilham o mesmo app
cliente = TestClient(criar_app())

def test_cria_pedido():
    cliente.post("/pedidos", json={...})  # cria id=1

def test_busca_pedido_criado_anteriormente():
    cliente.get("/pedidos/1")  # só funciona se o teste acima já rodou antes

# ✅ Fixture por teste — cada teste recebe um app novo e isolado
@pytest.fixture
def cliente() -> TestClient:
    return TestClient(criar_app())

def test_cria_pedido_retorna_201_com_total_calculado(cliente):
    ...
```

### (d) Testar caminhos de erro (404 / 409 / 422)

Uma suíte de integração que só testa o caminho feliz (criar pedido, pagar pedido) deixa a maior parte do contrato da API sem cobertura: o que acontece quando o pedido não existe? Quando ele já foi pago? Quando o corpo da requisição é inválido? `app.py` define três desses caminhos explicitamente — `404` (pedido não encontrado), `409` (pedido já pago) e `422` (validação do Pydantic: itens vazio ou quantidade não positiva) — e a suíte-alvo (`integracao_bons.py`) cobre os três.

---

## 3. Ferramentas Modernas por Linguagem

| Linguagem | Framework | Instalar | Executar |
|---|---|---|---|
| Python | **pytest + FastAPI TestClient** | `pip install -r requirements.txt` | `pytest -v` |
| PHP | **PHPUnit 11 + Guzzle** (contra servidor real) | `composer install` | `vendor/bin/phpunit` |
| TypeScript | **Vitest + supertest** | `npm install` | `npx vitest run` |
| ADVPL/TLPP | **PROBAT + FWRest/HttpGet** | já incluso no ambiente TOTVS (tlppCore) | executar via AppServer com o endpoint publicado |

**Nota sobre PHP/TypeScript/TLPP:** os arquivos `equivalente.php`, `equivalente.ts` e `equivalente.tlpp` (e seus pares em `exercicios/`) são paridade **ilustrativa** — mostram o mesmo padrão bom/ruim na sintaxe idiomática de cada linguagem, mas não são executados neste workshop (PHP e Vitest não estão instalados neste ambiente; PROBAT exige um AppServer TOTVS no ar). Isso segue a mesma convenção da Sessão 7.

---

## 4. Exercício

O arquivo `exercicios/exercicio.py` (e seus equivalentes `.php`, `.ts`, `.tlpp`) contém uma suíte de testes sobre a rota `POST /pedidos/{id}/pagar` com os mesmos 3 problemas estruturais de `exemplos/integracao_ruins.py`:

1. `TestClient` global compartilhado entre os testes (estado vaza — a ordem passa a importar).
2. Só verifica `status_code` (nunca olha o corpo da resposta).
3. Ordem dependente — um teste assume que o pedido criado por outro teste ainda existe, com o id que ele espera.

**Nota sobre autocontenção:** `exercicios/app.py` é uma cópia local do SUT (idêntico a `exemplos/app.py`) — o repositório não permite que um arquivo importe de outro diretório, então o app é replicado aqui para que o exercício rode de forma independente.

**Etapas:**

1. Rode a suíte como está — ela passa, mas os problemas são estruturais, não de execução.
2. Identifique os 3 problemas (compare com a lista de `integracao_ruins.py`, seção 2 acima).
3. Refatore aplicando os padrões de `integracao_bons.py`: fixture pytest que cria um `TestClient(criar_app())` novo por teste, nomes comportamentais, e asserções sobre o contrato completo (status + corpo).
4. Compare com `exercicios/gabarito.*` na sua linguagem.

```bash
# Rodar o exercício e o gabarito (Python)
cd exercicios
pytest exercicio.py -v
pytest gabarito.py -v
```

---

## 5. Checklist

- [ ] O teste verifica o contrato completo da resposta (status **e** corpo), não só o status?
- [ ] Cada teste tem seu próprio estado isolado (factory + fixture por teste), sem depender de execução anterior?
- [ ] Os caminhos de erro (404, 409, 422) estão cobertos, não só o caminho feliz?
- [ ] O teste não depende de I/O de rede externa (chamadas a serviços de terceiros pela internet)? Se depender, está isolado/marcado como tal (`@pytest.mark.skip`) e documentado?
- [ ] O nome do teste descreve o comportamento e o resultado esperado, sem precisar olhar o corpo?

**Nota sobre `integracao_ruins.py`:** o teste que ilustra dependência de rede real (`test_consulta_servico_externo`) está marcado `@pytest.mark.skip(reason="depende de rede real — anti-padrão ilustrado")` para não quebrar a suíte em CI/ambientes offline. O defeito estrutural que ele demonstra (lentidão, flakiness, não-repetibilidade) existe independentemente de o teste estar rodando ou não — é por isso que esse padrão deve ser evitado em produção, não movido para trás de um `skip` permanente.

---

## 6. Referências

- **FOWLER, Martin.** "IntegrationTest" (bliki).
  `https://martinfowler.com/bliki/IntegrationTest.html`
  Define o que caracteriza um teste de integração e por que a fronteira entre "unidade" e "integração" costuma ser mais sobre isolamento do que sobre o número de componentes envolvidos.

- **FOWLER, Martin.** "TestPyramid" (bliki).
  `https://martinfowler.com/bliki/TestPyramid.html`
  O modelo de proporção entre unidade, integração e e2e já apresentado na Sessão 7 — a base conceitual para decidir quanto investir em cada camada.

- **FastAPI.** "Testing" — documentação oficial sobre `TestClient`.
  `https://fastapi.tiangolo.com/tutorial/testing/`
  Referência oficial do padrão de teste usado neste tutorial (TestClient em memória via ASGI).

- **DODDS, Kent C.** "Write tests. Not too many. Mostly integration." (blog).
  Argumento da variação "trophy" de testes (já citada na Sessão 7) — relevante aqui porque testes de integração de API são exatamente a camada que essa variação recomenda enfatizar.
