# Tutorial 29 — Testes de Integração de Banco de Dados

> Referência: Martin Fowler, "IntegrationTest" e "TestPyramid" (martinfowler.com);
> documentação Python — módulo `sqlite3`; testcontainers-python (nota de evolução)

## 1. Contexto e Motivação

O Tutorial 28 tratou de testes de integração de API: HTTP, serialização e o contrato completo de uma resposta. Este tutorial cobre a outra colaboração real que uma suíte de integração costuma verificar — a camada de persistência. Em vez de chamar uma função Python diretamente ou mockar o acesso a dados, os testes aqui rodam contra um banco SQLite de verdade: o SQL é executado, as constraints do schema (chave estrangeira, `CHECK`) são avaliadas pelo motor do banco, e o efeito colateral gravado é conferido consultando o próprio banco de volta.

Isso importa porque a camada de persistência é onde regras de integridade *vivem* — não no código Python. Um teste que mocka o repositório (`unittest.mock.MagicMock`) pode "provar" que `inserir_pedido` foi chamado com os argumentos certos, mas não prova nada sobre se o banco aceitaria esses argumentos: um SQL mal escrito, uma constraint violada (cliente inexistente, total negativo) ou uma transação que nunca comita passam batido, porque nenhum SQL real roda no teste.

Este tutorial usa como SUT (`exemplos/repositorio.py`) um repositório de pedidos sobre `sqlite3` (biblioteca padrão do Python — sem dependências novas nesta sessão). O SQLite `:memory:` é o banco real e rápido: ele não é um mock, é o próprio SGBD rodando em memória, então schema, constraints e transações se comportam como em produção — só que sem tocar disco.

---

## 2. Conceito Central

### (a) Por que mockar o banco esconde bugs

Mockar a camada de persistência troca "o banco vai aceitar isso?" por "eu disse que o mock devolve isso". As duas perguntas parecem parecidas, mas só a primeira é verificável — a segunda é uma tautologia.

```python
# ❌ Mocka o repositório — nenhum SQL roda, nenhuma constraint é avaliada
def test_inserir_pedido_chama_repositorio_mockado():
    repositorio_mock = MagicMock()
    repositorio_mock.inserir_pedido.return_value = 1
    pedido_id = repositorio_mock.inserir_pedido(conn=None, cliente_id=999, total=-50.0)
    assert pedido_id == 1  # ❌ não prova que o banco aceitaria cliente_id inexistente

# ✅ SQL real roda — a constraint de integridade referencial é avaliada de verdade
def test_rejeita_pedido_com_cliente_inexistente(conn):
    with pytest.raises(sqlite3.IntegrityError):
        repositorio.inserir_pedido(conn, cliente_id=999, total=10.0)
```

Os bugs concretos que um mock nunca pega: SQL com erro de sintaxe ou nome de coluna errado (só aparece na primeira execução real), violação de constraint (FK inválida, `CHECK` falhando), e uma transação que nunca é commitada (o efeito parece ter acontecido dentro do teste, mas não sobrevive a uma nova conexão).

### (b) Banco real vs. in-memory — `:memory:` como banco real e rápido

"Banco real" não significa "banco em produção" ou "arquivo em disco" — significa "o SGBD de verdade processando o SQL". `sqlite3.connect(":memory:")` cria uma instância completa do SQLite, rodando inteiramente em RAM: todas as regras de schema, tipos, constraints e transações funcionam exatamente como em um arquivo `.db`, só que a suíte inteira roda em milissegundos e não deixa nenhum artefato no disco.

```python
# ✅ Banco real, mas rápido — SQLite completo, em memória, por teste
@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("PRAGMA foreign_keys = ON")
    repositorio.criar_schema(c)
    yield c
    c.close()
```

### (c) Schema no setup e isolamento por teste

Cada teste recebe uma conexão `:memory:` **nova**, com o schema recriado do zero (`criar_schema`) antes de qualquer asserção. Isso é o que garante que um teste não veja dados deixados por outro — a alternativa mais simples ao padrão "transação + rollback" usado em bancos de produção mais pesados (Postgres, MySQL), onde recriar o schema a cada teste seria caro demais.

```python
# ❌ Conexão e schema compartilhados entre todos os testes do módulo
_conn_global = sqlite3.connect("teste.db")  # arquivo persistente, nunca limpo

def test_a():
    repositorio.inserir_cliente(_conn_global, "Ana")  # deixa lixo para o próximo teste

# ✅ Conexão nova por teste — fixture recria o schema do zero
@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    repositorio.criar_schema(c)
    yield c
    c.close()
```

`PRAGMA foreign_keys = ON` merece atenção à parte: no SQLite, ao contrário da maioria dos SGBDs, a checagem de chave estrangeira vem **desligada por padrão** em cada nova conexão — é preciso ligar explicitamente, por conexão, toda vez. Esquecer esse pragma faz `test_rejeita_pedido_com_cliente_inexistente` falhar silenciosamente (o insert com FK inválida seria aceito).

### (d) Verificar efeitos colaterais no banco, não só o retorno

Um teste de integração de persistência não termina no valor de retorno da função chamada — ele deve confirmar que o dado realmente foi gravado (ou rejeitado) consultando o banco de volta.

```python
# ❌ Confia no retorno, nunca relê o banco
def test_insere_pedido_ruim(conn):
    pedido_id = repositorio.inserir_pedido(conn, cliente_id=1, total=10.0)
    assert pedido_id == 1  # não prova que o registro está lá com os campos certos

# ✅ Relê o banco e confere o registro completo
def test_insere_e_recupera_pedido_do_cliente(conn):
    cliente_id = repositorio.inserir_cliente(conn, "Ana", vip=True)
    pedido_id = repositorio.inserir_pedido(conn, cliente_id, 90.0)
    pedido = repositorio.buscar_pedido(conn, pedido_id)
    assert pedido == {"id": pedido_id, "cliente_id": cliente_id,
                      "total": 90.0, "status": "aberto"}
```

### Nota de evolução: `testcontainers` + Postgres

SQLite `:memory:` é suficiente para ensinar os conceitos deste tutorial (schema, constraints, isolamento, efeitos colaterais), mas não é o mesmo SGBD que a maioria dos sistemas usa em produção — tipos, comportamento de `CHECK`, concorrência e extensões variam entre SQLite e Postgres/MySQL. Para fidelidade total de produção, a evolução natural é a biblioteca [`testcontainers`](https://testcontainers.com/) (disponível em Python, PHP, TypeScript/Node e Java): ela sobe um container Docker efêmero do SGBD real (ex.: Postgres) por sessão ou por teste, e derruba no teardown. Isso não é implementado neste tutorial — é a fronteira citada para quando a equipe precisar de paridade exata com produção.

---

## 3. Ferramentas Modernas por Linguagem

| Linguagem | Framework | Instalar | Executar |
|---|---|---|---|
| Python | **pytest + `sqlite3`** (biblioteca padrão) | `pip install -r requirements.txt` | `pytest -v` |
| PHP | **PHPUnit 11 + PDO/SQLite** (extensão `pdo_sqlite`, embutida no PHP 8.1+) | `composer install` | `vendor/bin/phpunit` |
| TypeScript | **Vitest + better-sqlite3** | `npm install` | `npx vitest run` |
| ADVPL/TLPP | **PROBAT + DBAccess/TCQuery** | já incluso no ambiente TOTVS (tlppCore) | executar via AppServer com acesso a um ambiente TOTVS configurado |

**Nota sobre PHP/TypeScript/TLPP:** os arquivos `equivalente.php`, `equivalente.ts` e `equivalente.tlpp` (e seus pares em `exercicios/`) são paridade **ilustrativa** — mostram o mesmo padrão bom/ruim na sintaxe idiomática de cada linguagem, mas não são executados neste workshop (PHP e Vitest não estão instalados neste ambiente; PROBAT exige um AppServer TOTVS no ar). Isso segue a mesma convenção da Sessão 7 e do Tutorial 28.

**Nota sobre TLPP:** DBAccess/`TCQuery` não têm um mecanismo nativo de mocking de banco (equivalente a um driver in-memory como `sqlite3`/`better-sqlite3`). Testes de integração em ADVPL/TLPP tipicamente rodam contra um ambiente de homologação com dados de teste, ou usam tabelas de trabalho temporárias (`TCGenQry`, criadas e destruídas por teste via `@Setup`/`@Teardown`) para aproximar o isolamento — é o padrão que `equivalente.tlpp` demonstra.

---

## 4. Exercício

O arquivo `exercicios/exercicio.py` (e seus equivalentes `.php`, `.ts`, `.tlpp`) contém uma suíte de testes sobre `total_gasto_pelo_cliente(conn, cliente_id) -> float` com os mesmos 3 problemas estruturais de `exemplos/integracao_ruins.py`:

1. Mocka a conexão/repositório — nenhum SQL roda, nenhuma soma real é verificada.
2. Depende de um banco em arquivo persistente e compartilhado entre execuções (nunca limpo).
3. Sem schema isolado por teste — assume que a tabela e os dados já existem.

**Nota sobre autocontenção:** `exercicios/repositorio.py` é uma cópia local do SUT (idêntico a `exemplos/repositorio.py`) — o repositório não permite que um arquivo importe de outro diretório, então o repositório é replicado aqui para que o exercício rode de forma independente.

**Etapas:**

1. Rode a suíte como está — ela passa, mas os problemas são estruturais, não de execução.
2. Identifique os 3 problemas (compare com a lista de `integracao_ruins.py`, seção 2 acima).
3. Refatore aplicando os padrões de `exemplos/integracao_bons.py`: fixture pytest que cria `sqlite3.connect(":memory:")` novo por teste, chama `criar_schema`, e verifica a soma real (e o isolamento entre clientes).
4. Compare com `exercicios/gabarito.*` na sua linguagem.

```bash
# Rodar o exercício e o gabarito (Python)
cd exercicios
pytest exercicio.py -v
pytest gabarito.py -v
```

---

## 5. Checklist

- [ ] O teste roda SQL de verdade contra um banco real (`:memory:` ou equivalente), sem mockar a camada de persistência?
- [ ] Cada teste tem sua própria conexão/schema isolado, sem depender de dados deixados por outro teste ou execução anterior?
- [ ] `PRAGMA foreign_keys = ON` (ou equivalente) está ativo, para que constraints de integridade referencial sejam avaliadas de verdade?
- [ ] Constraints inválidas (FK inexistente, `CHECK` violado) são verificadas esperando a exceção correta (`sqlite3.IntegrityError` ou equivalente), não ignoradas?
- [ ] O teste relê o banco para conferir o efeito colateral gravado, em vez de confiar apenas no valor de retorno?
- [ ] Nenhum arquivo `.db`/`.sqlite` persistente é deixado no repositório após rodar a suíte?

---

## 6. Referências

- **FOWLER, Martin.** "IntegrationTest" (bliki).
  `https://martinfowler.com/bliki/IntegrationTest.html`
  Já citado no Tutorial 28 — a mesma definição de teste de integração se aplica aqui, trocando a colaboração HTTP pela colaboração com o SGBD.

- **FOWLER, Martin.** "TestPyramid" (bliki).
  `https://martinfowler.com/bliki/TestPyramid.html`
  O modelo de proporção entre unidade, integração e e2e — testes de banco ficam na camada de integração, mais lentos e mais caros que os de unidade da Sessão 7.

- **Python.** Documentação oficial do módulo `sqlite3`.
  `https://docs.python.org/3/library/sqlite3.html`
  Referência oficial da API usada em `repositorio.py` — inclui o comportamento de `PRAGMA foreign_keys`, `row_factory` e `IntegrityError`.

- **Testcontainers.** `https://testcontainers.com/`
  Base da "nota de evolução" da seção 2 — containers efêmeros do SGBD real (Postgres, MySQL) para testes de integração com fidelidade total de produção.
