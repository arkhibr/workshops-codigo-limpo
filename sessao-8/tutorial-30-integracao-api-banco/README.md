# Tutorial 30 — Integração ponta-a-ponta API+Banco ⭐ (âncora Sessão 8)

> Referência: Martin Fowler, "IntegrationTest" e "TestPyramid" (martinfowler.com);
> documentação FastAPI — TestClient; módulo `sqlite3`;
> Kent C. Dodds, "Write tests. Not too many. Mostly integration."

## 1. Contexto e Motivação

Os Tutoriais 28 e 29 isolaram, cada um, uma das duas colaborações que uma suíte de integração costuma cobrir: o 28 exercitou HTTP e serialização contra uma API em memória; o 29 exercitou SQL e constraints contra um banco real. Nenhum dos dois, sozinho, prova que o sistema funciona **como um todo**: o 28 usava um app com estado em dicionário Python, sem tocar banco nenhum; o 29 chamava funções de repositório diretamente, sem passar por HTTP.

Este tutorial é o **âncora** da Sessão 8: uma request HTTP de verdade percorre a stack inteira — rota FastAPI, validação Pydantic, SQL contra um SQLite real — até ser persistida, e o teste confirma que ela chegou lá. É um teste de integração **vertical**: em vez de isolar uma camada por vez (horizontal), ele atravessa todas as camadas que uma requisição de produção atravessaria, com a única simplificação sendo o SQLite `:memory:` no lugar do banco de produção (a mesma simplificação já justificada no Tutorial 29).

O SUT (`exemplos/app.py`) combina os dois tutoriais anteriores: a mesma API de pedidos do Tutorial 28, agora com `criar_app(conn: sqlite3.Connection)` — a conexão sqlite é **injetada**, não criada internamente. Isso é o que permite ao teste passar um `sqlite3.connect(":memory:")` próprio e inspecionar o banco diretamente depois da chamada HTTP, exatamente como o Tutorial 29 fazia com o repositório.

---

## 2. Conceito Central

### (a) Teste vertical: a request percorre a stack real até o banco

Um teste de integração vertical não para na resposta HTTP — ele confirma que o efeito esperado (a linha inserida, o status atualizado) está de fato no banco, na mesma conexão que a rota usou para gravar.

```python
def test_post_pedido_persiste_no_banco(contexto):
    cliente, conn = contexto
    resposta = cliente.post("/pedidos", json={
        "cliente": "Ana",
        "itens": [{"produto": "Livro", "quantidade": 3, "preco_unitario": 10.0}],
    })
    assert resposta.status_code == 201
    pedido_id = resposta.json()["id"]
    # a request HTTP grava no banco — e o teste confere os dois lados
    linha = conn.execute("SELECT cliente, total FROM pedidos WHERE id = ?",
                         (pedido_id,)).fetchone()
    assert tuple(linha) == ("Ana", 30.0)
```

### (b) Onde parar: integração ≠ E2E de UI

"Vertical" aqui significa API → validação → SQL → banco — a stack de **backend** completa, num único processo, sem rede real nem interface. Isso não é a mesma coisa que um teste E2E (Sessões 9): E2E dirige a aplicação pela interface que o usuário final usa (browser, app), sobe processos reais (servidor + banco + eventualmente um front-end), e paga o custo de lentidão e flakiness que vem disso. Este tutorial fica deliberadamente aquém dessa fronteira — é o teto de confiança que dá para comprar sem sair do nível de integração. A fronteira exata (o que passa a ser E2E) é retomada nos Tutoriais 31/32.

### (c) Verificar os dois lados — o ponto pedagógico central

O erro mais comum ao "testar a stack inteira" é parar na primeira confirmação que aparece — o `status_code` da resposta — e nunca voltar para confirmar o efeito colateral que a stack deveria ter produzido. Os dois lados são perguntas diferentes:

- **"A API respondeu certo?"** → confere `resposta.status_code` e `resposta.json()`.
- **"O efeito realmente aconteceu?"** → confere `conn.execute(...)` de volta.

Um bug de persistência real — commit esquecido, coluna errada, `UPDATE` que não roda — pode devolver uma resposta HTTP perfeita (o handler monta o dicionário de retorno manualmente, sem reler o banco) e ainda assim nunca ter gravado nada. Só a segunda pergunta pega esse bug.

```python
# ❌ Só confere a resposta HTTP — nunca relê o banco
def test_pagar_pedido_muda_status_para_pago(contexto):
    cliente, conn = contexto
    criado = cliente.post("/pedidos", json={...}).json()
    resposta = cliente.post(f"/pedidos/{criado['id']}/pagar")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "pago"  # não prova que foi persistido

# ✅ Confere os DOIS lados: resposta HTTP e estado persistido
def test_pagar_pedido_persiste_status_pago_no_banco(contexto):
    cliente, conn = contexto
    criado = cliente.post("/pedidos", json={...}).json()
    resposta = cliente.post(f"/pedidos/{criado['id']}/pagar")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "pago"
    linha = conn.execute("SELECT status FROM pedidos WHERE id = ?",
                         (criado["id"],)).fetchone()
    assert tuple(linha) == ("pago",)  # ✅ prova que foi persistido
```

### (d) "Integração vertical falsa" — o que não mockar neste nível

O anti-padrão central deste tutorial-âncora é mockar exatamente a camada que o teste se propõe a exercitar: a conexão com o banco. `exemplos/integracao_ruins.py` injeta um `MagicMock()` no lugar do `sqlite3.Connection` em `criar_app(conn)` — a suíte parece testar HTTP → app → banco (usa o mesmo SUT real, a mesma factory, o mesmo formato de chamada), mas nenhum SQL roda de verdade. Isso é mais enganoso do que mockar em um teste de unidade, porque a estrutura do teste (fixture, `TestClient`, `criar_app`) é idêntica à do teste bom — só a conexão foi substituída por um dublê que devolve exatamente o que foi programado para devolver.

```python
# ❌ "Integração vertical falsa": o banco é o próprio dublê
def test_post_pedido_com_banco_mockado():
    conn_mock = MagicMock()
    conn_mock.execute.return_value.lastrowid = 1
    cliente = TestClient(criar_app(conn_mock))
    resposta = cliente.post("/pedidos", json={...})
    assert resposta.status_code == 201  # "verde", mas nenhum SQL rodou
```

Regra prática: no nível de integração vertical, o próprio banco (ou API, dependendo de qual colaboração está sendo testada) é o que está sob teste — mocká-lo devolve a suíte para o nível de unidade, mas com a aparência estrutural (fixtures, nomes, `TestClient`) de um teste de integração. É a mentira mais cara de detectar em code review, porque "parece" certo.

### (e) A "trophy" de testes revisitada — por que integração vertical rende tanto

A "trophy" de Kent C. Dodds (citada na Sessão 7 e no Tutorial 28) argumenta por investir a maior fatia do esforço de teste em integração, não em unidade. Este tutorial é o exemplo mais concreto do porquê: um único teste vertical (`test_post_pedido_persiste_no_banco`) exercita, numa passada, a validação Pydantic, o roteamento FastAPI, a serialização JSON, o SQL de `INSERT`, a constraint `CHECK (total >= 0)` e o commit da transação — sete unidades de risco cobertas por uma suíte de dois testes. Cobrir a mesma superfície só com testes de unidade exigiria mockar cada colaboração (validação, roteamento, repositório) separadamente, multiplicando o número de testes sem necessariamente multiplicar a confiança — porque cada mock introduz a mesma pergunta do item (d): "isso prova que a peça real se comporta assim, ou só que eu disse que o mock devolve isso?".

---

## 3. Ferramentas Modernas por Linguagem

| Linguagem | Framework | Instalar | Executar |
|---|---|---|---|
| Python | **pytest + FastAPI TestClient + `sqlite3`** | `pip install -r requirements.txt` | `pytest -v` |
| PHP | **PHPUnit 11 + Guzzle + PDO/SQLite** (contra servidor real) | `composer install` | `vendor/bin/phpunit` |
| TypeScript | **Vitest + supertest + better-sqlite3** | `npm install` | `npx vitest run` |
| ADVPL/TLPP | **PROBAT + FWRest + DBAccess/TCQuery** | já incluso no ambiente TOTVS (tlppCore) | executar via AppServer com o endpoint publicado |

**Nota sobre PHP/TypeScript/TLPP:** os arquivos `equivalente.php`, `equivalente.ts` e `equivalente.tlpp` (e seus pares em `exercicios/`) são paridade **ilustrativa** — mostram o mesmo padrão vertical bom/ruim na sintaxe idiomática de cada linguagem, mas não são executados neste workshop (PHP e Vitest não estão instalados neste ambiente; PROBAT exige um AppServer TOTVS no ar). Isso segue a mesma convenção da Sessão 7 e dos Tutoriais 28/29.

---

## 4. Exercício

O arquivo `exercicios/exercicio.py` (e seus equivalentes `.php`, `.ts`, `.tlpp`) contém um teste sobre a rota `POST /pedidos/{id}/pagar` — adicionada ao SUT do exercício (`exercicios/app.py`) especificamente para este tutorial — com o mesmo problema estrutural de `exemplos/integracao_ruins.py` (anti-padrão "só verifica a resposta"):

1. O teste confirma `resposta.status_code == 200` e `resposta.json()["status"] == "pago"`, mas nunca relê o banco. Um bug em `pagar_pedido()` que devolvesse a resposta certa sem de fato persistir o `UPDATE` (ou sem commitar) passaria despercebido.

**Nota sobre autocontenção:** `exercicios/app.py` é uma cópia local do SUT (idêntico a `exemplos/app.py`, com a rota adicional `POST /pedidos/{id}/pagar`) — o repositório não permite que um arquivo importe de outro diretório, então o app é replicado aqui para que o exercício rode de forma independente.

**Etapas:**

1. Rode o teste como está — ele passa, mas o problema é estrutural, não de execução.
2. Identifique o problema: o teste verifica só um lado (a resposta HTTP).
3. Refatore aplicando o padrão de `exemplos/integracao_bons.py`: depois de chamar a rota, releia o pedido via `conn.execute(...)` e confirme que o status `"pago"` está persistido — não só presente na resposta.
4. Compare com `exercicios/gabarito.*` na sua linguagem.

```bash
# Rodar o exercício e o gabarito (Python)
cd exercicios
pytest exercicio.py -v
pytest gabarito.py -v
```

---

## 5. Checklist

- [ ] O teste percorre a stack real (rota → validação → SQL → banco), sem mockar a própria colaboração que está sob teste?
- [ ] Cada teste verifica **os dois lados**: a resposta HTTP (status + corpo) **e** o estado persistido, relendo o banco diretamente?
- [ ] A conexão (`conn`) é injetada via `criar_app(conn)` e criada nova (`:memory:`) por teste — sem estado vazando entre testes?
- [ ] Nenhuma camada dentro do escopo do teste (banco, no caso deste tutorial) está mockada — se estivesse, o teste teria voltado a ser um teste de unidade disfarçado de integração?
- [ ] O teste sabe onde parar: não sobe browser/UI real (isso é E2E — Tutoriais 31/32), fica no nível de backend vertical?

---

## 6. Referências

- **FOWLER, Martin.** "IntegrationTest" (bliki).
  `https://martinfowler.com/bliki/IntegrationTest.html`
  Já citado nos Tutoriais 28 e 29 — aqui, as duas colaborações (HTTP e persistência) são exercitadas juntas na mesma suíte.

- **FOWLER, Martin.** "TestPyramid" (bliki).
  `https://martinfowler.com/bliki/TestPyramid.html`
  A camada de integração deste tutorial fica entre a unidade (Sessão 7) e o E2E (Sessão 9) — o ponto de maior retorno por esforço, segundo o modelo.

- **FastAPI.** "Testing" — documentação oficial sobre `TestClient`.
  `https://fastapi.tiangolo.com/tutorial/testing/`
  Base do padrão de teste em memória usado neste tutorial, agora combinado com persistência sqlite real.

- **Python.** Documentação oficial do módulo `sqlite3`.
  `https://docs.python.org/3/library/sqlite3.html`
  Referência da API usada em `app.py` — inclui `row_factory`, `Connection.execute` e o comportamento de conexões `:memory:` injetadas.

- **DODDS, Kent C.** "Write tests. Not too many. Mostly integration." (blog).
  Já citada no Tutorial 28 — este tutorial é o exemplo mais direto do argumento: um teste vertical cobre, numa passada, mais superfície de risco do que várias unidades mockadas cobririam separadamente (seção 2e acima).
