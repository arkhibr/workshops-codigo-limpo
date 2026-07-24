# Tutorial 29 — Testes de Integração de Banco de Dados

> Referência: Martin Fowler, "IntegrationTest" e "TestPyramid" (martinfowler.com);
> documentação Python — módulo `sqlite3`; testcontainers-python (nota de evolução)

## 1. Contexto e Motivação

O Tutorial 28 verificou uma colaboração real: a aplicação e quem a consome pela rede, através do contrato HTTP. Este tutorial verifica outra colaboração igualmente real, e que costuma ficar de fora das suítes: a aplicação e o banco de dados onde ela guarda o seu estado.

Boa parte das regras de integridade de um sistema não vive no código, e sim no banco. É o banco que decide se um pedido pode apontar para um cliente que não existe, se um valor total pode ser negativo, se uma coluna obrigatória pode ficar em branco. Essas regras são expressas no schema — chaves estrangeiras, restrições `CHECK`, colunas `NOT NULL` — e são avaliadas pelo motor do banco no momento em que o SQL roda. Um teste que não executa SQL de verdade não exercita nenhuma delas.

É esse o problema de mockar a camada de persistência. Quando um teste substitui o repositório por um objeto falso, ele consegue afirmar que `inserir_pedido` foi chamado com determinados argumentos, mas não que o banco aceitaria esses argumentos. Um SQL com nome de coluna errado, uma chave estrangeira apontando para um cliente inexistente, um valor que viola um `CHECK`, uma transação que nunca é confirmada — nada disso aparece, porque nenhum SQL real chega a ser executado. O teste fica verde e o bug segue para produção.

Um teste de integração de banco existe para fechar essa lacuna. Ele roda o SQL contra um banco de verdade, deixa o motor avaliar as constraints e confere o efeito gravado consultando o próprio banco de volta. A aplicação sob teste, aqui, é o repositório de pedidos em [`exemplos/repositorio.py`](exemplos/repositorio.py), escrito sobre o módulo `sqlite3` da biblioteca padrão do Python — sem nenhuma dependência nova nesta sessão.

---

## 2. Conceito Central

### (a) Por que mockar o banco esconde bugs

Mockar a camada de persistência troca a pergunta "o banco aceitaria isso?" pela afirmação "eu programei o objeto falso para devolver isso". A segunda não é uma verificação; é uma repetição do que o próprio teste escreveu. O código abaixo, de [`exemplos/integracao_ruins.py`](exemplos/integracao_ruins.py) e [`exemplos/integracao_bons.py`](exemplos/integracao_bons.py), mostra a diferença:

```python
# ❌ Mocka o repositório — nenhum SQL roda, nenhuma constraint é avaliada
def test_inserir_pedido_chama_repositorio_mockado():
    repositorio_mock = MagicMock()
    repositorio_mock.inserir_pedido.return_value = 1
    pedido_id = repositorio_mock.inserir_pedido(conn=None, cliente_id=999, total=-50.0)
    assert pedido_id == 1  # não prova que o banco aceitaria cliente_id inexistente nem total negativo

# ✅ SQL real roda — a integridade referencial é avaliada pelo motor do banco
def test_rejeita_pedido_com_cliente_inexistente(conn):
    with pytest.raises(sqlite3.IntegrityError):
        repositorio.inserir_pedido(conn, cliente_id=999, total=10.0)
```

Três tipos de bug escapam de qualquer teste com mock e só aparecem quando o SQL roda: erro de sintaxe ou nome de coluna incorreto, que falha na primeira execução real; violação de constraint, como uma chave estrangeira inválida ou um `CHECK` que não passa; e a transação que nunca é confirmada, cujo efeito parece existir dentro do teste, mas não sobrevive a uma nova conexão.

### (b) O banco real e rápido: SQLite em memória

"Banco real" não quer dizer "banco de produção" nem "arquivo em disco". Quer dizer o sistema gerenciador de banco de dados de verdade processando o SQL, com todas as suas regras. `sqlite3.connect(":memory:")` cria uma instância completa do SQLite que roda inteiramente na memória do processo. Schema, tipos, constraints e transações se comportam exatamente como em um arquivo `.db`, com duas vantagens para um teste: a suíte inteira roda em milissegundos e nenhum arquivo é deixado no disco ao final.

Essa é a técnica que substitui o mock. Em vez de fingir o banco, o teste usa um banco verdadeiro que nasce e morre com ele.

### (c) Schema no setup, isolamento por teste e o pragma de chave estrangeira

Cada teste recebe uma conexão em memória nova, com o schema recriado do zero antes de qualquer asserção. É isso que garante que um teste não enxergue dados deixados por outro. Em bancos de produção mais pesados, como Postgres ou MySQL, recriar o schema a cada teste sairia caro, e o padrão usual é abrir uma transação no início e desfazê-la (`rollback`) no fim; com o SQLite em memória, recriar tudo é barato e ainda mais simples de entender.

```python
# ❌ Conexão e schema compartilhados por todo o módulo, em arquivo persistente
_conn_global = sqlite3.connect("teste.db")  # nunca é limpo — cada execução acumula lixo

def test_a():
    repositorio.inserir_cliente(_conn_global, "Ana")  # o dado sobra para o próximo teste

# ✅ Conexão nova por teste — a fixture recria o schema do zero e fecha no fim
@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("PRAGMA foreign_keys = ON")
    repositorio.criar_schema(c)
    yield c
    c.close()
```

O `PRAGMA foreign_keys = ON` merece uma observação à parte. No SQLite, ao contrário da maioria dos bancos, a checagem de chave estrangeira vem desligada por padrão, e precisa ser ligada explicitamente em cada nova conexão. Esquecer esse pragma faz um teste como `test_rejeita_pedido_com_cliente_inexistente` passar quando deveria falhar: o insert com chave estrangeira inválida seria aceito em silêncio, e o teste perderia justamente a constraint que se propunha a verificar.

### (d) Conferir o efeito gravado no banco

Um teste de persistência não termina no valor que a função devolve. Devolver um identificador não prova que a linha foi gravada com os campos certos, nem que ela sobrevive à transação. A confirmação vem de reler o banco e comparar o registro completo.

```python
# ❌ Confia no retorno e nunca relê o banco
def test_insere_pedido_ruim(conn):
    pedido_id = repositorio.inserir_pedido(conn, cliente_id=1, total=10.0)
    assert pedido_id == 1  # não prova que a linha está lá, nem com quais valores

# ✅ Relê o banco e confere o registro inteiro
def test_insere_e_recupera_pedido_do_cliente(conn):
    cliente_id = repositorio.inserir_cliente(conn, "Ana", vip=True)
    pedido_id = repositorio.inserir_pedido(conn, cliente_id, 90.0)
    pedido = repositorio.buscar_pedido(conn, pedido_id)
    assert pedido == {"id": pedido_id, "cliente_id": cliente_id,
                      "total": 90.0, "status": "aberto"}
```

### Nota de evolução: `testcontainers` e Postgres

O SQLite em memória cobre bem os conceitos deste tutorial: schema, constraints, isolamento e efeito gravado. Ele não é, porém, o mesmo banco que a maioria dos sistemas usa em produção. Tipos, comportamento de `CHECK`, concorrência e extensões variam entre o SQLite e o Postgres ou o MySQL. Quando a equipe precisa de paridade exata com produção, o passo seguinte é a biblioteca [`testcontainers`](https://testcontainers.com/), disponível em Python, PHP, TypeScript/Node e Java: ela sobe um container Docker efêmero do banco real por sessão ou por teste e o derruba no teardown. Não implementamos isso aqui — fica registrado como a fronteira para quando a fidelidade com produção passar a ser o risco a cobrir.

---

## 3. Ferramentas Modernas por Linguagem

| Linguagem | Framework | Instalar | Executar |
|---|---|---|---|
| Python | **pytest + `sqlite3`** (biblioteca padrão) | `pip install -r requirements.txt` | `pytest -v` |
| PHP | **PHPUnit 11 + PDO/SQLite** (extensão `pdo_sqlite`, embutida no PHP 8.1+) | `composer install` | `vendor/bin/phpunit` |
| TypeScript | **Vitest + better-sqlite3** | `npm install` | `npx vitest run` |
| ADVPL/TLPP | **PROBAT + DBAccess/TCQuery** | já incluso no ambiente TOTVS (tlppCore) | executar via AppServer com acesso a um ambiente TOTVS configurado |

Os arquivos [`equivalente.php`](exemplos/equivalente.php), [`equivalente.ts`](exemplos/equivalente.ts) e [`equivalente.tlpp`](exemplos/equivalente.tlpp), com os pares em `exercicios/`, trazem o mesmo par bom/ruim na sintaxe idiomática de cada linguagem. Eles servem de referência, não de suíte executável neste workshop: PHP e Vitest não estão instalados neste ambiente, e o PROBAT depende de um AppServer TOTVS no ar. A convenção é a mesma da Sessão 7 e do Tutorial 28 — o Python é a implementação que você executa.

Uma observação sobre ADVPL/TLPP: o DBAccess e o `TCQuery` não têm um mecanismo nativo de banco em memória, equivalente ao `sqlite3` ou ao `better-sqlite3`. Os testes de integração em TLPP costumam rodar contra um ambiente de homologação com dados de teste, ou usar tabelas de trabalho temporárias (`TCGenQry`), criadas e destruídas por teste via `@Setup`/`@Teardown`, para aproximar o isolamento. É esse o padrão que o `equivalente.tlpp` demonstra.

---

## 4. Exercício

O arquivo [`exercicios/exercicio.py`](exercicios/exercicio.py), e os equivalentes `.php`, `.ts` e `.tlpp`, trazem uma suíte de testes sobre `total_gasto_pelo_cliente(conn, cliente_id) -> float` com os mesmos três problemas estruturais de [`exemplos/integracao_ruins.py`](exemplos/integracao_ruins.py):

1. A conexão ou o repositório são mockados, de modo que nenhum SQL roda e nenhuma soma real é verificada.
2. Os testes dependem de um banco em arquivo persistente, compartilhado entre execuções e nunca limpo.
3. Não há schema isolado por teste: a suíte assume que a tabela e os dados já existem.

A [`exercicios/repositorio.py`](exercicios/repositorio.py) é uma cópia local do repositório, idêntica à de `exemplos/`. Como o repositório do workshop não permite que um arquivo importe de outro diretório, ele é replicado aqui para que o exercício rode por conta própria.

**Etapas:**

1. Execute a suíte como está. Ela passa — os problemas são de estrutura, não de execução.
2. Identifique os três problemas, comparando com a lista de `integracao_ruins.py` na seção 2(a).
3. Refatore seguindo [`exemplos/integracao_bons.py`](exemplos/integracao_bons.py): uma fixture que cria `sqlite3.connect(":memory:")` por teste, chama `criar_schema` e verifica a soma real, além do isolamento entre clientes.
4. Compare o resultado com [`exercicios/gabarito.py`](exercicios/gabarito.py), ou com o gabarito na sua linguagem.

```bash
# Rodar o exercício e o gabarito (Python)
cd exercicios
pytest exercicio.py -v
pytest gabarito.py -v
```

---

## 5. Checklist

- [ ] O teste roda SQL de verdade contra um banco real (`:memory:` ou equivalente), em vez de mockar a camada de persistência?
- [ ] Cada teste tem a própria conexão e o próprio schema, independente de dados deixados por outro teste ou execução?
- [ ] O `PRAGMA foreign_keys = ON` (ou o equivalente) está ativo, para que a integridade referencial seja avaliada de fato?
- [ ] As constraints inválidas — chave estrangeira inexistente, `CHECK` violado — são verificadas esperando a exceção correta (`sqlite3.IntegrityError` ou equivalente)?
- [ ] O teste relê o banco para conferir o efeito gravado, em vez de confiar apenas no valor de retorno?
- [ ] Nenhum arquivo `.db` ou `.sqlite` persistente é deixado no repositório depois de rodar a suíte?

---

## 6. Referências

- **FOWLER, Martin.** "IntegrationTest" (bliki).
  `https://martinfowler.com/bliki/IntegrationTest.html`
  Citado no Tutorial 28 — a mesma definição de teste de integração se aplica aqui, trocando a colaboração HTTP pela colaboração com o banco de dados.

- **FOWLER, Martin.** "TestPyramid" (bliki).
  `https://martinfowler.com/bliki/TestPyramid.html`
  O modelo de proporção entre unidade, integração e e2e — os testes de banco ficam na camada de integração, mais lentos e mais caros que os de unidade da Sessão 7.

- **Python.** Documentação oficial do módulo `sqlite3`.
  `https://docs.python.org/3/library/sqlite3.html`
  Referência da API usada em `repositorio.py`, incluindo o comportamento de `PRAGMA foreign_keys`, `row_factory` e `IntegrityError`.

- **Testcontainers.** `https://testcontainers.com/`
  Base da nota de evolução da seção 2 — containers efêmeros do banco real (Postgres, MySQL) para testes de integração com fidelidade total de produção.
