# Tutorial 07 — Gestão de Código Legado

## 1. Contexto e Motivação

> *"To me, legacy code is simply code without tests."*
> — Michael Feathers, *Working Effectively with Legacy Code*, p. xvi

A definição de Feathers é deliberadamente provocadora. Código legado não é sinônimo de código antigo. Um módulo escrito ontem, sem testes e sem clareza de intenção, já é código legado — porque você não consegue verificar que uma mudança não vai quebrar nada.

O problema central não é técnico. É psicológico. Ninguém quer tocar em código que pode quebrar silenciosamente. Sem testes, qualquer modificação é um salto no escuro: você altera uma função, o sistema compila, os logs não mostram nada — e três semanas depois um cliente reporta que os valores de um relatório estão errados. O medo paralisa. O código cresce ao redor do núcleo problemático, nunca dentro dele.

> [!Tip]
> Robert C. Martin descreve a **Regra do Escoteiro** em *Clean Code* (p. 14): *"Leave the campground cleaner than you found it."* 
Aplicada ao código, a regra é simples: cada vez que você toca um arquivo, deixe-o um pouco mais limpo do que estava — um nome melhor, uma função extraída, um magic number nomeado. Não é preciso um "sprint de refatoração". O progresso acontece de forma incremental, commit a commit, ao longo de meses.

Esses dois princípios — testes como pré-requisito para mudança, e melhoria incremental a cada toque — formam a base deste tutorial.

---

## 2. Conceito Central

### O que torna código difícil de mudar

| Problema | Por que dificulta mudanças |
|---|---|
| **Acoplamento oculto** | Dependências não declaradas: uma função acessa um banco de dados sem que o chamador saiba. Para testar, você precisa de infraestrutura real. |
| **Estado global mutável** | Uma variável global modificada em um lugar afeta comportamento em outro. Impossível testar em isolamento — o estado anterior vaza entre chamadas. |
| **Funções que fazem muitas coisas** | Não dá para testar o cálculo de imposto sem acionar também a gravação no banco e o envio de e-mail. A única opção é testar tudo junto. |
| **Ausência de testes** | Sem testes, você não tem como verificar que uma mudança não quebrou nada. O medo bloqueia a refatoração, que poderia criar os testes. Ciclo vicioso. |

---

### O modelo de Seams (Costuras)

Um **seam** é um ponto no código onde você pode substituir um comportamento sem precisar editar aquele código. É o conceito central de Feathers: antes de refatorar, você precisa criar ao menos uma abertura pela qual os testes possam entrar.

O problema concreto: o código abaixo não tem seams. Para testar `processar_pedido`, você precisa de um banco de dados real e de um servidor SMTP real — porque a função os instancia diretamente.

```python
# ❌ Sem seams — impossível testar sem infraestrutura real
class ProcessadorDePedidos:
    def processar_pedido(self, pedido_id: str) -> None:
        db = ConexaoBanco("host=prod user=app")   # instanciado aqui dentro
        mailer = ServicoDeEmail("smtp.empresa.com") # instanciado aqui dentro
        pedido = db.buscar(pedido_id)
        total = pedido["valor"] * 1.12
        db.salvar({"id": pedido_id, "total": total, "status": "processado"})
        mailer.enviar(pedido["email"], f"Pedido {pedido_id} confirmado: R$ {total}")
```

Para testar a regra `valor * 1.12`, você é obrigado a subir banco e SMTP. Se a conexão falhar no CI, o teste falha — por um motivo que nada tem a ver com a lógica de negócio.

#### Seam 1 — Injeção de Dependência

A solução mais direta: em vez de instanciar colaboradores internamente, recebê-los como parâmetro. Agora o chamador decide o que passar — em produção, as implementações reais; nos testes, objetos falsos.

```python
# ✅ Seam via injeção de dependência
class ProcessadorDePedidos:
    def __init__(self, banco: BancoInterface, mailer: MailerInterface) -> None:
        self._banco = banco
        self._mailer = mailer

    def processar_pedido(self, pedido_id: str) -> None:
        pedido = self._banco.buscar(pedido_id)
        total = pedido["valor"] * 1.12
        self._banco.salvar({"id": pedido_id, "total": total, "status": "processado"})
        self._mailer.enviar(pedido["email"], f"Pedido {pedido_id} confirmado: R$ {total}")

# No teste — sem banco, sem SMTP
class BancoFake:
    def buscar(self, id): return {"valor": 1000.0, "email": "x@y.com"}
    def salvar(self, dados): self.ultimo_salvo = dados

class MailerFake:
    def enviar(self, dest, msg): self.ultima_mensagem = msg

banco = BancoFake()
processador = ProcessadorDePedidos(banco, MailerFake())
processador.processar_pedido("P001")
assert banco.ultimo_salvo["total"] == 1120.0
```

O seam está no construtor: é ali que o comportamento pode ser substituído sem tocar na lógica de `processar_pedido`.

#### Seam 2 — Herança para Override

Quando você não consegue injetar dependências porque o código legado instancia tudo internamente e não tem como mudar o construtor agora, uma alternativa é criar uma subclasse que sobrescreve apenas o método problemático.

```python
# Classe legada — não dá para mudar o construtor agora
class RelatorioLegado:
    def gerar(self, periodo: str) -> float:
        dados = self._buscar_dados(periodo)   # acessa banco diretamente
        return sum(d["valor"] for d in dados) * 0.9

    def _buscar_dados(self, periodo: str) -> list:
        return ConexaoBanco().query(f"SELECT * FROM vendas WHERE periodo='{periodo}'")

# ✅ Subclasse de teste — sobrescreve apenas o que acessa infraestrutura
class RelatorioLegadoTestavel(RelatorioLegado):
    def _buscar_dados(self, periodo: str) -> list:
        return [{"valor": 500.0}, {"valor": 300.0}]  # dados fixos, sem banco

relatorio = RelatorioLegadoTestavel()
assert relatorio.gerar("2024-01") == 720.0  # (500 + 300) * 0.9
```

A lógica de negócio em `gerar` foi testada sem alterar uma linha do código legado. O seam é o método `_buscar_dados`, que a subclasse pode sobrescrever.

#### Seam 3 — Parâmetros em vez de estado global

Estado global é o inimigo dos testes: o valor de uma variável global depende de tudo que aconteceu antes na execução. A solução é transformar o estado global em parâmetro explícito.

```python
# ❌ Lê estado global — resultado depende de quem chamou antes
_taxa_cambio = 5.20

def converter_valor(valor_usd: float) -> float:
    return valor_usd * _taxa_cambio  # acoplado ao estado global

# ✅ Recebe o valor como parâmetro — sem dependência de estado externo
def converter_valor(valor_usd: float, taxa_cambio: float) -> float:
    return valor_usd * taxa_cambio

assert converter_valor(100.0, 5.20) == 520.0
assert converter_valor(100.0, 4.80) == 480.0
```

O seam é o parâmetro `taxa_cambio`: o chamador controla o valor, sem precisar manipular variáveis globais.

---

### Testes de Caracterização

O paradoxo do código legado: para refatorar com segurança, você precisa de testes. Mas para escrever testes, você precisa entender o que o código faz — e o código é difícil de entender justamente porque não tem testes.

Os **testes de caracterização** resolvem esse paradoxo. Em vez de perguntar "o que o código *deveria* fazer?", você pergunta "o que o código *faz* agora?". O teste documenta o comportamento atual, mesmo que esse comportamento seja questionável.

**O fluxo em quatro passos:**

**Passo 1 — Chame o código e imprima o resultado sem assert.**
```python
resultado = calc.calc_comm("V001", 10000, "STD", 8000)
print(resultado)   # → 812.0
```

**Passo 2 — Use o valor que saiu como expected no assert.**
```python
resultado = calc.calc_comm("V001", 10000, "STD", 8000)
assert resultado == 812.0  # você não sabe por que é 812, mas é o que sai
```

**Passo 3 — Rode o teste. Ele deve passar.**
Se falhar, você cometeu um erro ao copiar o valor. Corrija e rode de novo até ficar verde.

**Passo 4 — Repita para mais entradas e casos de borda.**
```python
# Cobre as ramificações do código
assert calc.calc_comm("V001", 10000, "STD", 8000) == 812.0   # caso base
assert calc.calc_comm("V001", 500,   "STD", 8000) == 37.5    # valor baixo
assert calc.calc_comm("V002", 10000, "PREM", 8000) == 950.0  # tipo diferente
assert calc.calc_comm("V001", 10000, "STD", 0)    == 650.0   # meta zerada
```

Agora você tem uma rede de segurança. Qualquer refatoração que altere um desses valores vai fazer um teste falhar — e você decide: foi intencional ou foi uma regressão?

> **Nota importante:** o valor `812.0` pode estar errado do ponto de vista do negócio. Isso não importa agora. Primeiro você protege o comportamento atual; depois, em um commit separado, você corrige o bug — e o teste vai falhar de propósito, aí você atualiza o expected para o valor correto.

---

### Técnicas de Refatoração Segura

#### Extrair Função (Extract Method)

É a técnica mais usada e mais segura. Você identifica um bloco de código dentro de uma função longa, move esse bloco para uma função nova com nome descritivo, e faz a função original chamar a nova. O comportamento externo não muda — você só reorganizou onde o código vive.

```python
# ❌ Antes: método de 40 linhas com lógica fiscal embutida
def processar_fatura(self, dados: dict) -> dict:
    cliente = self._db.buscar_cliente(dados["cli_id"])
    valor = dados["valor"]

    # bloco de cálculo fiscal — 15 linhas misturadas com o resto
    if cliente["tipo"] == "PJ":
        if valor > 5000:
            imposto = valor * 0.12
        else:
            imposto = valor * 0.065
        if len(dados["itens"]) > 10:
            imposto *= 1.15
    else:
        imposto = valor * 0.075 if valor > 2000 else valor * 0.03
        imposto += 150

    fatura = {"valor": valor, "imposto": imposto, "total": valor + imposto}
    self._db.salvar_fatura(fatura)
    self._mailer.notificar(cliente["email"], fatura)
    return fatura
```

```python
# ✅ Depois: Extract Method isola o cálculo fiscal
def processar_fatura(self, dados: dict) -> dict:
    cliente = self._db.buscar_cliente(dados["cli_id"])
    imposto = self._calcular_imposto(dados["valor"], cliente["tipo"], len(dados["itens"]))
    fatura = {"valor": dados["valor"], "imposto": imposto, "total": dados["valor"] + imposto}
    self._db.salvar_fatura(fatura)
    self._mailer.notificar(cliente["email"], fatura)
    return fatura

def _calcular_imposto(self, valor: float, tipo_cliente: str, qtd_itens: int) -> float:
    if tipo_cliente == "PJ":
        aliquota = 0.12 if valor > 5000 else 0.065
        imposto = valor * aliquota
        return imposto * 1.15 if qtd_itens > 10 else imposto
    imposto = valor * 0.075 if valor > 2000 else valor * 0.03
    return imposto + 150
```

Agora `_calcular_imposto` pode ser testada diretamente, sem banco e sem e-mail:
```python
assert processador._calcular_imposto(8000, "PJ", 2) == 960.0
assert processador._calcular_imposto(3000, "PJ", 2) == 195.0
assert processador._calcular_imposto(1000, "PF", 2) == 180.0
```

**Regra de ouro do Extract Method:** faça um passo de cada vez. Extraia uma função, rode os testes de caracterização, veja que estão verdes, commit. Extraia outra, rode, commit. Nunca extraia três funções de uma vez antes de verificar que nada quebrou.

#### Substituição Gradual (Strangler Fig Pattern)

O nome vem da figueira-estranguladora, uma planta que cresce em volta de uma árvore hospedeira. A nova planta usa a árvore como suporte enquanto ainda é fraca. Com o tempo, a nova planta cobre totalmente a árvore. A árvore original apodrece dentro, mas o sistema nunca parou.

É exatamente assim que funciona a migração de um módulo legado: a nova implementação cresce ao redor da antiga, coexistindo via uma interface compartilhada. Um roteador decide qual usar. Quando a nova cobre todos os casos, a antiga é removida — sem nenhum "dia de corte" de risco alto.

```python
# Interface compartilhada — ambas as implementações a honram
class ProcessadorDePedidosInterface:
    def processar(self, pedido_id: str) -> dict: ...

# Implementação legada — continua funcionando, não é tocada
class ProcessadorLegado(ProcessadorDePedidosInterface):
    def processar(self, pedido_id: str) -> dict:
        # 200 linhas de código legado, intocadas
        ...

# Nova implementação — limpa, testável, construída em paralelo
class ProcessadorNovo(ProcessadorDePedidosInterface):
    def __init__(self, banco, mailer, calculador):
        ...
    def processar(self, pedido_id: str) -> dict:
        # implementação nova, com testes
        ...

# Roteador — decide qual usar sem que o chamador saiba
class RoteadorDePedidos(ProcessadorDePedidosInterface):
    def __init__(self, legado, novo, percentual_novo: float = 0.0):
        self._legado = legado
        self._novo = novo
        self._percentual_novo = percentual_novo  # começa em 0%, sobe gradualmente

    def processar(self, pedido_id: str) -> dict:
        import random
        if random.random() < self._percentual_novo:
            return self._novo.processar(pedido_id)
        return self._legado.processar(pedido_id)
```

A migração acontece em semanas: 0% → 5% → 20% → 50% → 100% → remove legado. Se algo der errado a qualquer momento, você volta o percentual para 0% — sem rollback de deploy.

#### Wrapper

Quando o código legado tem uma interface caótica (parâmetros posicionais obscuros, retornos inconsistentes, side effects misturados), o Wrapper cria uma camada com interface limpa ao redor dele. O código legado permanece **completamente intocado** — o wrapper apenas traduz.

```python
# Função legada — parâmetros posicionais sem nome, retorno misterioso
def calc_comm(vid, val, tp, meta, fl=0):
    # 80 linhas de código legado — não vamos tocar aqui
    ...
    # retorna uma tupla (comissao, bonus, flag_atingiu_meta) em alguns casos
    # e um float em outros, dependendo de fl
    ...

# ✅ Wrapper com interface clara
class CalculadorDeComissao:
    def calcular(
        self,
        vendedor_id: str,
        valor_venda: float,
        tipo_plano: str,
        meta_mensal: float,
    ) -> float:
        resultado = calc_comm(vendedor_id, valor_venda, tipo_plano, meta_mensal, 0)
        # normaliza o retorno inconsistente da função legada
        return resultado if isinstance(resultado, float) else resultado[0]
```

Agora o resto do sistema usa `CalculadorDeComissao.calcular()` — com parâmetros nomeados, retorno previsível — e os testes de caracterização ficam sobre o wrapper. A função `calc_comm` fica congelada; ninguém a chama diretamente mais.

---

### A Regra do Escoteiro na prática

- Antes de adicionar uma feature: melhorar os nomes na área que você vai tocar
- Antes de fazer commit: verificar se o arquivo tem pelo menos um problema a menos do que quando você abriu
- Não precisa refatorar tudo de uma vez — progresso incremental acumula ao longo de semanas

---

## 3. O Problema na Prática

Fragmento de `exemplos/legado_antes.py`:

```python
_db = {"faturas": {}, "clientes": {...}}  # estado global mutável
_ultimo_erro = None

class FaturaProcessor:
    # Processa faturas de pessoa física apenas
    # (mentira: processa PF e PJ, mas o comentário nunca foi atualizado)

    def process(self, data):
        global _ultimo_erro
        cli_id = data["cli"]          # nome obscuro
        v = data["val"]               # nome obscuro
        tp = cliente["tipo"]

        if tp == "PJ":
            if v > 5000:              # magic number: o que significa 5000?
                imp = v * 0.12        # magic number: qual imposto é 12%?
            else:
                imp = v * 0.065
            if len(data["it"]) > 10:
                imp = imp * 1.15      # magic number: por que 15% a mais?
        else:
            if v > 2000:
                imp = v * 0.075
            else:
                imp = v * 0.03
            imp = imp + 150           # magic number: o que é essa taxa de R$ 150?

        # ... mais 30 linhas: persistência, e-mail, log
        print(f"EMAIL -> {cliente['email']}: ...")  # efeito colateral incontrolável
```

**Por que é difícil modificar:**

1. **Não há como testar o cálculo de imposto em isolamento.** Para verificar se `0.065` está correto para PJ abaixo de R$ 5.000, você precisa fornecer um cliente válido no `_db`, fornecer dados completos, aceitar que um e-mail será "enviado" (print), e lidar com o estado global `_ultimo_erro`. O teste de uma regra fiscal exige montar toda a infraestrutura.

2. **O estado global `_db` vaza entre testes.** Se você chamar `process` duas vezes no mesmo processo, a segunda fatura recebe id `F0002` porque `_db["faturas"]` já tem um registro. Testes dependentes de ordem são testes não confiáveis.

3. **A lógica de cálculo está duplicada em `reprocess`.** Quando a regra fiscal mudar, é obrigatório atualizar dois lugares — e nada no código sinaliza isso. O próximo desenvolvedor vai atualizar `process` e esquecer `reprocess`.

4. **O comentário mente.** `# Processa faturas de pessoa física apenas` — o código claramente trata PJ também. Comentários desatualizados são mais perigosos do que ausência de comentários: induzem quem lê a confiar em uma descrição errada.

---

## 4. A Solução

Fragmento de `exemplos/legado_depois.py`:

```python
# Constantes nomeadas — sem magic numbers espalhados pelo código
ALIQUOTA_PJ_ALTA = 0.12       # ISS sobre serviços PJ acima do limiar
ALIQUOTA_PJ_BAIXA = 0.065
LIMIAR_PJ = 5000.0
TAXA_FIXA_PF = 150.0          # Taxa administrativa — contrato câmara de compensação (dez/2022)

class CalculadorDeImpostos:
    def calcular(self, valor: float, tipo_cliente: str, quantidade_itens: int) -> float:
        if tipo_cliente == "PJ":
            return self._imposto_pj(valor, quantidade_itens)
        return self._imposto_pf(valor)

    def _imposto_pj(self, valor: float, quantidade_itens: int) -> float:
        aliquota = ALIQUOTA_PJ_ALTA if valor > LIMIAR_PJ else ALIQUOTA_PJ_BAIXA
        imposto = valor * aliquota
        if quantidade_itens > LIMITE_MUITOS_ITENS:
            imposto *= ADICIONAL_MUITOS_ITENS
        return imposto

class ProcessadorDeFaturas:
    def __init__(self, clientes, repositorio, calculador, validador, notificador):
        # Todas as dependências injetadas — cada uma pode ser substituída em testes
        ...
```

**Decisões de design:**

- `CalculadorDeImpostos` recebe valores e retorna um número. Sem banco, sem e-mail, sem estado. Pode ser testado com uma linha: `assert calc.calcular(8000, "PJ", 2) == 960.0`.
- `ProcessadorDeFaturas` orquestra, mas não implementa nenhuma regra. Se a lógica de cálculo mudar, apenas `CalculadorDeImpostos` muda.
- `NotificadorDeFaturas` pode ser substituído por um fake em testes — sem nenhum print, sem alterar o processador.
- Constantes no topo do arquivo: quando a alíquota mudar, há um único lugar para alterar, com contexto de negócio documentado.

---

## 5. Equivalentes em Outras Linguagens

### PHP — Seam via Injeção de Dependência

Arquivo: `exemplos/equivalente.php`

O problema clássico em PHP legado: `new Mailer()` e `new Repository()` instanciados diretamente dentro do método. Não há seam — não há como substituir por fakes sem editar a classe.

A solução não altera a lógica de negócio: apenas a forma como os colaboradores chegam à classe muda, do construtor. Interfaces são definidas para `RepositorioFaturaInterface` e `MailerInterface`. Em produção, as implementações reais são injetadas. Em testes, fakes que armazenam chamadas em arrays — sem banco, sem SMTP.

### TypeScript — Strangler Fig Pattern

Arquivo: `exemplos/equivalente.ts`

Uma interface `ProcessadorDePedidos` é extraída do código legado. A nova implementação honra a mesma interface. Um `RoteadorDePedidos` decide qual usar baseado em critério configurável (valor do pedido, feature flag, etc.). O `ClienteCheckout` só enxerga a interface — não sabe que existe um roteador. A migração acontece gradualmente, sem big bang.

### ADVPL/TLPP — Extração de Function em código Protheus

Arquivo: `exemplos/equivalente.tlpp`

Em Protheus, o equivalente do Extract Method é extrair sub-Functions globais. A Function `CALCPED` original tinha ~80 linhas cobrindo validação, cálculo fiscal, geração de ID, gravação e log. Após refatoração, `CALCPED` mantém a mesma assinatura (nenhum chamador quebra) e delega para `VALIDA_DADOS_PED`, `CALC_IMPOSTO_PED`, `GERA_NUM_PEDIDO`, `GRAVA_PEDIDO` e `REGISTRA_LOG_PEDIDO`.

O benefício imediato: `CALC_IMPOSTO_PED` pode ser chamada em testes unitários sem conectar ao banco Protheus ou abrir área SC5. O comentário no arquivo mostra como escrever uma `U_TESTE_IMPOSTO` com asserts diretos.

---

## 6. Regras de Ouro

- **A Regra do Escoteiro**: a cada commit, deixe o arquivo com pelo menos um problema a menos — um nome melhor, uma constante extraída, um comentário removido. Progresso incremental acumula.

- **Teste de caracterização antes de refatorar**: documente o comportamento atual com asserts antes de tocar uma linha. Se os asserts quebrarem depois da refatoração, você mudou o comportamento — decida se foi intencional.

- **Refatore em pequenos passos verificáveis**: cada extração de função deve deixar os testes verdes. Nunca refatore e adicione funcionalidade ao mesmo tempo — fica impossível saber o que quebrou.

- **Não reescreva código legado — refatore gradualmente**: reescritas totais têm histórico de falhar. O código existente acumula décadas de casos de borda não documentados. O Strangler Fig preserva esse conhecimento enquanto melhora a estrutura.

- **Seams permitem testar sem reescrever**: identificar e expor seams (injeção de dependência, parâmetros em vez de estado global) é frequentemente suficiente para criar os primeiros testes sem alterar a lógica de negócio.

- **Dívida técnica em código legado tem juros compostos**: cada nova feature adicionada sobre código sem testes é mais difícil de testar do que a anterior. O custo de mudança cresce exponencialmente; o custo de criar os primeiros testes cresce linearmente.

---

## 7. Exercício

O arquivo `exercicios/exercicio.py` contém um módulo legado de cálculo de comissões com os seguintes problemas clássicos: parâmetros obscuros, magic numbers, lógica duplicada, estado global modificado dentro de método, e comentário que contradiz o código.

**Etapas:**

1. **Testes de caracterização**: rode o arquivo e observe os valores retornados. Escreva asserts que documentam esses valores no bloco `if __name__ == "__main__":`. Rode novamente — todos os asserts devem passar.

2. **Identificar smells**: anote `# SMELL:` em cada problema encontrado. Não corrija ainda — apenas marque.

3. **Refatorar**: aplique as técnicas do tutorial — constantes nomeadas, classes com responsabilidade única, eliminar estado global, eliminar lógica duplicada.

4. **Verificar**: rode seus testes de caracterização sobre a versão refatorada. Se algum assert falhar, você alterou o comportamento — investigue se foi intencional.

```bash
# Rodar o exercício
python3 exercicios/exercicio.py

# Comparar com o gabarito
python3 exercicios/gabarito.py
```

---

## 8. Para se Aprofundar

- **FEATHERS, Michael.** *Working Effectively with Legacy Code*. Prentice Hall, 2004.
  Especialmente Cap. 1 (*Changing Software*) e Cap. 4 (*The Seam Model*). O livro que definiu o vocabulário moderno para trabalhar com código legado. Cada capítulo apresenta uma técnica específica para tornar código não-testável em testável, sem reescrever do zero.

- **MARTIN, Robert C.** *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall, 2008.
  Cap. 1, especialmente a Regra do Escoteiro (p. 14). O livro inteiro é sobre as decisões micro de código que determinam se um sistema vai envelhecer bem ou se tornar legado.

- **FOWLER, Martin.** *Refactoring: Improving the Design of Existing Code*. 2. ed. Addison-Wesley, 2018.
  Catálogo de refatorações seguras com pré e pós-condições. Extract Method, Move Method, Replace Magic Number with Symbolic Constant — cada um com passos detalhados para aplicar sem quebrar o comportamento.

- **Strangler Fig Application — Martin Fowler** (bliki).
  `https://martinfowler.com/bliki/StranglerFigApplication.html`
  O artigo original que nomeou o padrão, com a analogia da figueira-estranguladora e exemplos de aplicação em sistemas web.
