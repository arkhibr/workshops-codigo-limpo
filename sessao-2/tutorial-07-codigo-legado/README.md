# Tutorial 07 — Gestão de Código Legado

## 1. Contexto e Motivação

> *"To me, legacy code is simply code without tests."*
> — Michael Feathers, *Working Effectively with Legacy Code*, p. xvi

A definição de Feathers é deliberadamente provocadora. Código legado não é sinônimo de código antigo. Um módulo escrito ontem, sem testes e sem clareza de intenção, já é código legado — porque você não consegue verificar que uma mudança não vai quebrar nada.

O problema central não é técnico. É psicológico. Ninguém quer tocar em código que pode quebrar silenciosamente. Sem testes, qualquer modificação é um salto no escuro: você altera uma função, o sistema compila, os logs não mostram nada — e três semanas depois um cliente reporta que os valores de um relatório estão errados. O medo paralisa. O código cresce ao redor do núcleo problemático, nunca dentro dele.

Robert C. Martin descreve a **Regra do Escoteiro** em *Clean Code* (p. 14): *"Leave the campground cleaner than you found it."* Aplicada ao código, a regra é simples: cada vez que você toca um arquivo, deixe-o um pouco mais limpo do que estava — um nome melhor, uma função extraída, um magic number nomeado. Não é preciso um "sprint de refatoração". O progresso acontece de forma incremental, commit a commit, ao longo de meses.

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

### O modelo de Seams (Costuras) — Michael Feathers

Um **seam** é um ponto no código onde você pode substituir um comportamento sem editar aquele código. É o que torna código testável.

Exemplo concreto: se uma classe instancia seu colaborador com `new Mailer()`, não há seam — você não consegue substituir o Mailer por um fake sem editar a classe. Se a classe recebe o Mailer como parâmetro no construtor (injeção de dependência), há um seam — você pode passar qualquer objeto que honre a interface.

Tipos de seams:

- **Injeção de dependência**: receber colaboradores como parâmetro em vez de instanciá-los internamente
- **Herança para override**: criar subclasse que sobrescreve o método problemático nos testes
- **Parâmetros de função**: passar dados como argumento em vez de ler de estado global

### Testes de Caracterização

Antes de refatorar código legado, escreva testes que documentam o comportamento **atual** — mesmo que esse comportamento seja questionável. O objetivo não é testar se o comportamento está correto. É garantir que você não vai mudá-lo acidentalmente.

```python
# Teste de caracterização: o que o código FAZ, não o que deveria fazer
resultado = calc.calc_comm("V001", 10000, "STD", 8000)
assert resultado == 812.0  # documentando o comportamento existente
```

São testes de "rede de segurança". Eles falham quando você introduz uma regressão — e só então você decide se a mudança foi intencional ou um bug.

### Técnicas de Refatoração Segura

**Extrair função (Extract Method)**
Isolar lógica em uma função com nome descritivo, sem alterar o comportamento externo. A função original continua existindo e chamando a nova. É a técnica mais segura porque o diff é pequeno e reversível.

```python
# Antes: lógica de imposto embutida em um método de 60 linhas
# Depois: método original chama _calcular_imposto_pj(valor, qtd_itens)
```

**Substituição gradual (Strangler Fig Pattern)**
Criar uma nova implementação que coexiste com a antiga via interface compartilhada. Um roteador decide qual usar — por feature flag, por percentual do tráfego, por tipo de pedido. Quando a nova implementação estiver estável e cobrir todos os casos, a antiga é removida. Não há big bang, não há dia de corte arriscado.

**Wrapper**
Envolver o código legado em uma nova classe com interface limpa. A classe legada permanece intocada; o wrapper traduz entre a interface velha e a nova.

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
