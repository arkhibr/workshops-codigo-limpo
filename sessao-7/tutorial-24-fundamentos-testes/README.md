# Tutorial 24 — Fundamentos de Testes de Unidade

> Referência: Kent Beck, *Test-Driven Development: By Example*; Roy Osherove,
> *The Art of Unit Testing*; Martin Fowler, "TestPyramid" (martinfowler.com)

## 1. Contexto e Motivação

Até aqui, o workshop tratou de como escrever código legível — nomes, funções pequenas, comentários necessários, formatação consistente. A partir deste tutorial, a pergunta muda: como você **prova** que esse código faz o que deveria fazer, e continua fazendo depois da próxima alteração?

A resposta não é "testando manualmente antes do deploy". Testes manuais são lentos, inconsistentes entre execuções e não sobrevivem à próxima mudança — ninguém reexecuta o roteiro de teste manual completo a cada commit. A resposta é escrever **testes de unidade**: pequenos programas que chamam seu código com entradas conhecidas e verificam que a saída é a esperada, executados em segundos, toda vez que algo muda.

Sessão 2 já apresentou testes de caracterização como ferramenta para proteger código legado antes de refatorar. Esta sessão vai além: como estruturar testes de unidade *bem escritos* desde o início, para qualquer código — novo ou legado —, usando os frameworks reais que equipes profissionais usam em produção (pytest, PHPUnit, Vitest, PROBAT).

**Diferença importante em relação às sessões anteriores deste workshop:** até agora, todo código era autocontido e verificado via `print`/stdout, sem framework de testes. A partir daqui, os arquivos usam sintaxe **real** de framework de testes e são verificados **executando o framework** (`pytest -v`, não `python3 arquivo.py`). Essa é uma exceção documentada e intencional — faz sentido ensinar testes de unidade com as ferramentas que existem para isso.

---

## 2. Conceito Central

### O que é uma unidade e o que é isolamento

Uma **unidade** é a menor porção de comportamento que faz sentido testar isoladamente — normalmente uma função pura ou um método de uma classe. "Isolamento" significa que o teste de uma unidade não depende de outras unidades, de infraestrutura externa (banco de dados, rede, sistema de arquivos) nem do resultado de outros testes.

Isso não significa que sistemas não tenham dependências — significa que, ao testar `calcular_desconto`, você não quer que uma falha de conexão com um banco de dados, ou a ordem em que os testes rodam, decida se o teste passa ou falha. Se `calcular_desconto` está isolada, o teste roda em milissegundos, sempre com o mesmo resultado, em qualquer máquina.

```python
# ❌ Não é uma unidade isolada: depende de banco real
def calcular_desconto_ruim(cliente_id):
    cliente = banco.buscar(cliente_id)  # I/O externo
    return 100.0 * 0.9 if cliente["vip"] else 100.0

# ✅ Unidade isolada: só depende dos parâmetros recebidos
def calcular_desconto(valor: float, cliente_vip: bool) -> float:
    return valor * 0.9 if cliente_vip else valor
```

A segunda versão pode ser testada com uma linha, sem subir nenhuma infraestrutura. Isolamento é o que torna um teste **rápido** e **confiável** — os dois primeiros atributos que vamos formalizar com FIRST, adiante.

---

### AAA — Arrange-Act-Assert

Todo teste de unidade bem estruturado segue (implícita ou explicitamente) três fases:

| Fase | O que faz | Exemplo |
|---|---|---|
| **Arrange** | Prepara os dados e o estado necessários para o teste | `valor = 100.0` |
| **Act** | Executa o comportamento sendo testado — idealmente uma única chamada | `resultado = calcular_desconto(valor, cliente_vip=True)` |
| **Assert** | Verifica que o resultado é o esperado | `assert resultado == 90.0` |

```python
def test_aplica_10_porcento_para_cliente_vip():
    # Arrange
    valor = 100.0
    # Act
    resultado = calcular_desconto(valor, cliente_vip=True)
    # Assert
    assert resultado == 90.0
```

O valor de nomear as três fases (mesmo com comentários simples) é forçar disciplina: se você não consegue separar claramente "preparar", "executar" e "verificar", provavelmente o teste está fazendo coisas demais. Um teste com múltiplos blocos Act intercalados com Assert geralmente está testando mais de um comportamento — sinal de que deveria ser dividido.

---

### FIRST — Fast, Independent, Repeatable, Self-validating, Timely

FIRST é um acrônimo (popularizado por Tim Ottinger e Jeff Langr) que resume as cinco qualidades que um bom teste de unidade deve ter. Cada letra, com contraste bom/ruim:

**F — Fast (Rápido)**
Um teste de unidade deve rodar em milissegundos. Se a suíte inteira leva minutos, ninguém vai rodá-la a cada alteração — e o valor do teste desaparece.
```python
# ❌ Lento: dorme de propósito, ou faz I/O real
def test_processa_pedido():
    time.sleep(2)
    resultado = requests.get("https://api-real.com/pedido/1")
    assert resultado.status_code == 200

# ✅ Rápido: puramente em memória
def test_calcula_total_do_pedido():
    assert calcular_total([10.0, 20.0]) == 30.0
```

**I — Independent (Independente)**
A ordem de execução não pode importar. Um teste não pode depender de estado deixado por outro.
```python
# ❌ Depende de ordem: se test_b rodar antes de test_a, quebra
_carrinho = []
def test_a():
    _carrinho.append("item")
    assert len(_carrinho) == 1

# ✅ Cada teste monta seu próprio estado
def test_adiciona_item_ao_carrinho_vazio():
    carrinho = []
    carrinho.append("item")
    assert len(carrinho) == 1
```

**R — Repeatable (Repetível)**
O mesmo teste, rodado em qualquer ambiente (sua máquina, CI, máquina de outro dev), deve produzir o mesmo resultado — sem depender de rede, hora do sistema ou ordem de arquivos no disco.
```python
# ❌ Não repetível: depende do relógio real
def test_desconto_de_segunda():
    hoje = datetime.now()
    resultado = calcular_desconto(100.0, hoje.weekday() == 0)
    assert resultado >= 0  # assert fraco pra "sempre passar"

# ✅ Repetível: a condição vem como parâmetro explícito
def test_aplica_desconto_quando_e_segunda(self):
    resultado = calcular_desconto_do_dia(100.0, dia_da_semana=0)
    assert resultado == 90.0
```

**S — Self-validating (Autoverificável)**
O teste deve terminar em pass/fail automático — sem exigir que um humano leia um log e decida se passou.
```python
# ❌ Exige inspeção manual
def test_calculo():
    print(calcular_desconto(100.0, True))  # "vai que dá 90.0, confere aí"

# ✅ Autoverificável: o assert decide
def test_calculo():
    assert calcular_desconto(100.0, True) == 90.0
```

**T — Timely (Oportuno)**
Testes devem ser escritos junto com o código de produção — não meses depois. Escrito tarde demais, o teste tende a ser moldado pela implementação (em vez de guiar o design) e frequentemente nunca é escrito.

---

### Pirâmide de testes (unit >> integration > e2e)

A pirâmide de testes (Mike Cohn, *Succeeding with Agile*) é um modelo de proporção: você quer **muitos** testes de unidade (rápidos, baratos, isolados), **menos** testes de integração (verificam a colaboração entre componentes reais) e **poucos** testes end-to-end (lentos, caros, cobrem o sistema inteiro via interface).

```
        /\
       /e2e\          poucos — lentos, caros, frágeis
      /------\
     /integra-\        alguns — verificam integração real
    /   ção    \
   /------------\
  /   unidade    \    muitos — rápidos, baratos, isolados
 /----------------\
```

A lógica: um bug de regra de negócio pode ser pego por um teste de unidade em milissegundos. O mesmo bug, pego só por um teste e2e, custa minutos de execução e um diagnóstico muito mais difícil (a falha pode estar em qualquer camada do sistema).

> **Nota:** existe uma variação moderna e discutível chamada **"trophy" de testes** (Kent C. Dodds), que sugere investir mais pesado em testes de integração do que a pirâmide clássica recomenda — argumento: testes de integração dão mais confiança por esforço em sistemas com muita integração de UI/API. É um debate legítimo da comunidade, não um consenso; o modelo de pirâmide continua sendo o ponto de partida mais ensinado, e é o que este workshop adota como base.

---

### Nomenclatura comportamental

Nomes de teste devem descrever **comportamento esperado**, não a implementação testada. Um bom nome de teste, lido isoladamente (sem olhar o corpo), já diz o que o sistema deve fazer.

```python
# ❌ Nome não diz nada sobre o que é verificado
def test1(): ...
def test_calculo(): ...
def test_desconto(): ...

# ✅ Nome descreve comportamento — lido como uma frase
def test_aplica_10_porcento_para_cliente_vip(): ...
def test_nao_aplica_desconto_para_cliente_comum(): ...
def test_frete_gratis_acima_de_200(): ...
```

Um padrão comum (não obrigatório, mas útil): `test_<resultado_esperado>_quando_<condicao>`. Quando um teste falha, o nome sozinho no relatório de CI já indica qual regra de negócio quebrou — sem precisar abrir o arquivo.

---

## 3. Ferramentas Modernas por Linguagem

| Linguagem | Framework | Instalar | Executar |
|---|---|---|---|
| Python | **pytest** | `pip install pytest` | `pytest -v` |
| PHP | **PHPUnit 11** (+ nota abaixo sobre Pest) | `composer require --dev phpunit/phpunit` | `vendor/bin/phpunit` |
| TypeScript | **Vitest** | `npm install -D vitest` | `npx vitest run` |
| ADVPL/TLPP | **PROBAT** (parte do tlppCore, TOTVS) | já incluso no ambiente TOTVS (tlppCore) | executar via AppServer/TDS com suporte a PROBAT |

**Nota sobre Pest:** [Pest](https://pestphp.com/) é uma camada de sintaxe mais enxuta sobre o PHPUnit (funções `test()`/`it()` em vez de classes), cada vez mais popular na comunidade PHP moderna. Ele roda sobre o mesmo motor do PHPUnit — os testes deste tutorial em PHPUnit são 100% compatíveis com o ecossistema Pest, caso a equipe prefira essa sintaxe.

**Nota sobre PROBAT:** ao contrário de pytest/PHPUnit/Vitest, PROBAT **não tem parametrização nativa** (equivalente a `@pytest.mark.parametrize`, `#[DataProvider]` ou `it.each`). Para cobrir múltiplas variações de entrada, repita o método de teste com dados diferentes e nomes descritivos, ou itere um array dentro do próprio corpo do teste.

---

## 4. Exercício

O arquivo `exercicios/exercicio.py` (e seus equivalentes `.php`, `.ts`, `.tlpp`) contém uma suíte de testes sobre `calcular_comissao(valor_venda, meta_batida)` — 8% de comissão se a meta foi batida, 3% caso contrário — com os mesmos 4 problemas estruturais de `exemplos/testes_ruins.py`:

1. Nomes que não dizem o que é testado (`test1`, `test2`, `test_comissao`)
2. Um teste verificando comportamentos não relacionados
3. Estado global/compartilhado entre testes (a ordem de execução importa)
4. Dependência do relógio real (não-determinístico)

**Etapas:**

1. Rode a suíte como está — ela passa, mas os problemas são estruturais, não de execução.
2. Identifique os 4 problemas (compare com a lista de `testes_ruins.py`, na seção anterior).
3. Refatore aplicando AAA, FIRST e nomes comportamentais. Use a parametrização nativa da linguagem (`@pytest.mark.parametrize`, `#[DataProvider]`, `it.each`) para cobrir as variações de valor e meta — em PROBAT, repita o método de teste.
4. Compare com `exercicios/gabarito.*` na sua linguagem.

```bash
# Rodar o exercício (Python)
pytest exercicios/exercicio.py -v

# Comparar com o gabarito
pytest exercicios/gabarito.py -v
```

---

## 5. Checklist

- [ ] O nome do teste descreve o comportamento esperado, sem olhar o corpo?
- [ ] O teste segue AAA — uma preparação, uma ação, uma verificação?
- [ ] O teste verifica **um único** comportamento (não dois ou mais combinados)?
- [ ] O teste roda em milissegundos, sem I/O real (rede, banco, disco)?
- [ ] O teste passa/falha da mesma forma em qualquer ordem de execução?
- [ ] O teste produz o mesmo resultado em qualquer máquina e a qualquer hora (sem `datetime.now()`, `random()` sem seed, etc.)?
- [ ] Variações de entrada estão parametrizadas, em vez de copiadas e coladas?

---

## 6. Referências

- **BECK, Kent.** *Test-Driven Development: By Example*. Addison-Wesley, 2002.
  O livro que formalizou o ciclo Red-Green-Refactor e popularizou testes de unidade como ferramenta de design, não apenas de verificação.

- **OSHEROVE, Roy.** *The Art of Unit Testing*. 2. ed. Manning, 2013.
  Referência prática sobre isolamento, uso de test doubles e organização de suítes de teste em sistemas reais.

- **FOWLER, Martin.** "TestPyramid" (bliki).
  `https://martinfowler.com/bliki/TestPyramid.html`
  O artigo que consolidou o modelo de pirâmide de testes como heurística de proporção entre unidade, integração e e2e.

- **OTTINGER, Tim; LANGR, Jeff.** "FIRST principles" — referenciado em *Clean Code* (Martin), cap. 9.
  A origem do acrônimo FIRST usado neste tutorial.

- **DODDS, Kent C.** "Write tests. Not too many. Mostly integration." (blog).
  Argumento por trás da variação "trophy" de testes mencionada na seção 2.
