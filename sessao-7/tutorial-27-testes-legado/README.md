# Tutorial 27 — Testes de Unidade em Código Legado ⭐ (Âncora)

> Referência: Michael Feathers, *Working Effectively with Legacy Code*
> (caracterização, seams); Martin Fowler, "Mocks Aren't Stubs"

## 1. Contexto e Motivação

O Tutorial 07 (Sessão 2) apresentou o problema central deste workshop sobre código legado: **código sem seams é impossível de testar em isolamento**. Um seam é um ponto onde você pode substituir um comportamento — tipicamente uma dependência instanciada dentro de um construtor — sem editar o código que a usa. Sem esse ponto de substituição, testar uma unidade exige acionar toda a infraestrutura real que ela toca por baixo: banco de dados, serviço externo, fila, relógio do sistema.

`exemplos/legado_ruins.py` reencena esse problema com um caso novo: `GerenciadorEstoque` instancia `ConexaoBancoReal` e `ServicoPrecoExternoReal` diretamente no construtor, e ainda mantém um cache de preços em um atributo de classe — estado global mutável, compartilhado por todas as instâncias. Não há como testar `recalcular_estoque` sem um banco e um serviço de preço reais. O único teste possível neste arquivo, `test_impossivel_testar_sem_infraestrutura_real`, documenta exatamente isso: ele passa porque confirma a exceção de conexão — a impossibilidade de testar é o próprio ponto pedagógico, não um teste "quebrado" a ser corrigido.

Este tutorial é a **âncora** da Sessão 7: ele não introduz teoria nova, mas junta em um único fluxo tudo que as três sessões anteriores já ensinaram — o modelo de seams (Tutorial 07), a taxonomia de dublês de teste (Tutorial 25) e o Test Data Builder (Tutorial 26) — aplicado ao cenário mais comum na prática: um módulo de produção real, sem testes, que precisa ganhar uma rede de segurança antes de qualquer refatoração.

---

## 2. Conceito Central

### O ciclo completo: seam → double → caracterização → suíte de regressão

Testar código legado com segurança segue sempre a mesma sequência de decisões — nunca comece pela refatoração:

1. **Seam.** Sem um ponto de substituição, nada mais é possível. `exemplos/legado_bons.py` introduz o seam mais simples e mais comum: injeção via construtor. `GerenciadorEstoque(banco, servico_precos, cache_precos=None)` recebe as dependências em vez de instanciá-las — o cache de preços, antes estado global escondido, também vira um parâmetro explícito (por instância, não mais compartilhado).

2. **Double.** Com o seam aberto, escolha o tipo certo de dublê por dependência (Tutorial 25). `ServicoPrecoStub` é um **Stub**: devolve um preço fixo e pré-programado, e ainda conta `chamadas` para permitir verificar reaproveitamento de cache. `BancoEstoqueFake` é um **Fake**: mantém estoques em memória com lógica funcional real (`buscar_estoque`/`atualizar_estoque` se comportam como um banco de verdade, só que sem I/O) — e, seguindo o Test Data Builder do Tutorial 26, o próprio Fake atua como builder do estado inicial via `com_estoque(produto_id, quantidade)`, encadeável e legível no Arrange do teste.

3. **Caracterização.** Antes de julgar ou corrigir qualquer coisa, documente o comportamento *atual* como oráculo. `test_caracterizacao_recalculo_com_estoque_suficiente` é o primeiro teste em `legado_bons.py` — ele não pergunta "isso está certo?", pergunta "o que o código faz agora?". O segundo teste, `test_recalculo_com_venda_maior_que_estoque_gera_saldo_negativo`, documenta um caso de borda descoberto durante a caracterização (o legado não valida estoque insuficiente) sem tentar corrigi-lo: decidir se isso é um bug é uma decisão de produto, não deste teste.

4. **Suíte de regressão.** Uma vez caracterizado, o comportamento vira uma rede de segurança. `test_recalculo_reaproveita_preco_em_cache_na_segunda_chamada` prova que o cache funciona como esperado — e, a partir daqui, qualquer refatoração futura (extrair uma função, renomear um parâmetro, mudar a estrutura interna) tem uma suíte verde para confirmar que nada mudou de comportamento. Só depois desse ciclo completo (seam → double → caracterização → suíte) é que faz sentido melhorar o design do código.

### Passo a passo replicável

O mesmo ciclo, como checklist de execução para aplicar em qualquer módulo legado real:

1. **Identificar dependências ocultas** — o que a classe/função instancia ou acessa internamente que não é passado como parâmetro (banco, serviço externo, relógio, estado global)?
2. **Introduzir seam** — normalmente injeção via construtor; em casos onde o construtor não pode mudar, considere as alternativas do Tutorial 07 (herança para override, parâmetro em vez de estado global).
3. **Escolher o double certo por dependência** — Stub para resposta fixa (`ServicoPrecoStub`), Fake para comportamento funcional leve em memória (`BancoEstoqueFake`), Mock quando o que importa é verificar uma interação/efeito colateral (Tutorial 25).
4. **Escrever a caracterização antes de qualquer refatoração** — rode o código, observe o valor de saída, use esse valor como `expected` no assert. O primeiro teste da suíte deve sempre ser um teste de caracterização, não um teste de "comportamento correto assumido".
5. **Só então melhorar o código** — com a suíte verde protegendo o comportamento observável, agora sim: extrair funções, renomear, eliminar duplicação, remover o estado global. Cada passo de refatoração deve manter a suíte verde; se um teste quebrar, foi uma mudança de comportamento — decida se foi intencional.

---

## 3. Ferramentas Modernas por Linguagem

| Linguagem | Seam | Double | Framework de teste |
|---|---|---|---|
| Python | injeção via construtor (`__init__`) | classes manuais (`ServicoPrecoStub`, `BancoEstoqueFake`) | pytest |
| PHP | injeção via construtor + `interface` | classes manuais implementando a interface | PHPUnit 11 |
| TypeScript | injeção via construtor + `interface` | classes manuais implementando a interface | Vitest |
| ADVPL/TLPP | parâmetro de classe no construtor (`:new(oBanco, oServicoPrecos, ...)`) | classe manual seguindo o mesmo contrato por convenção | PROBAT |

Em ADVPL/TLPP não há framework de mocking (`createStub()`, `vi.fn()`), a mesma limitação já discutida no Tutorial 25: o double é sempre uma classe escrita à mão que implementa os mesmos métodos, com a mesma assinatura, mas comportamento controlado — `exemplos/equivalente.tlpp` segue exatamente esse padrão para `GatewayPagamentoStub`/`BancoEstoqueFake` e para a auditoria do exercício.

---

## 4. Checklist "código legado sob teste"

- [ ] Toda dependência externa (banco, serviço, relógio, estado global) chega via parâmetro/construtor, em vez de ser instanciada internamente?
- [ ] O primeiro teste escrito sobre o código legado é de **caracterização** (documenta o comportamento atual), não uma suposição de comportamento correto?
- [ ] Casos de borda encontrados durante a caracterização foram documentados como teste, mesmo que o comportamento pareça questionável — sem "corrigir" antes de decidir se é intencional?
- [ ] O double escolhido corresponde ao que cada dependência precisa (Stub para resposta fixa, Fake para lógica funcional em memória)?
- [ ] A suíte de caracterização roda antes de qualquer refatoração, e continua verde depois de cada passo pequeno de melhoria?
- [ ] Nenhum teste depende de infraestrutura real (banco, rede) para rodar em milissegundos?

---

## 5. Exercício

O arquivo `exercicios/exercicio.py` (e seus equivalentes `.php`, `.ts`, `.tlpp`) contém `ProcessadorReembolso`, com o mesmo problema estrutural de `legado_ruins.py`: instancia `GatewayPagamentoReal` e `ServicoAuditoriaReal` diretamente no construtor, sem seam algum, e sem nenhum teste. Ambas as dependências reais lançam um erro indicando que não estão disponíveis neste ambiente.

**Etapas:**

1. Introduza seams: `ProcessadorReembolso` deve receber `gateway` e `auditoria` via construtor.
2. Crie um **Stub** para o gateway de pagamento (`GatewayPagamentoStub`, resposta fixa `{"status": "estornado", "valor": ...}`).
3. Crie um **Fake** para o serviço de auditoria (`ServicoAuditoriaFake`, guardando os eventos registrados em uma lista, para inspeção).
4. Escreva um teste de **caracterização** como primeiro teste (`test_caracterizacao_processa_reembolso_com_sucesso`), seguido de um segundo teste que verifica o efeito colateral observado no Fake (`test_reembolso_registra_evento_de_auditoria`).
5. Compare com `exercicios/gabarito.*` na sua linguagem.

```bash
# O exercício não tem testes ainda — é esperado "no tests ran"
pytest exercicios/exercicio.py -v

# Comparar com o gabarito — 2 testes passando
pytest exercicios/gabarito.py -v
```

---

## 6. Referências

- **FEATHERS, Michael.** *Working Effectively with Legacy Code*. Prentice Hall, 2004.
  Cap. 4 (*The Seam Model*) e o conceito de teste de caracterização, já apresentados no Tutorial 07 e retomados aqui como síntese aplicada com dublês modernos.

- **FOWLER, Martin.** "Mocks Aren't Stubs" (bliki).
  `https://martinfowler.com/articles/mocksArentStubs.html`
  A distinção entre Stub e Fake usada em `legado_bons.py` — `ServicoPrecoStub` devolve resposta fixa, `BancoEstoqueFake` tem lógica funcional real em memória.

- **Tutorial 07 — Gestão de Código Legado** (Sessão 2 deste workshop).
  O modelo de seams e os quatro passos do teste de caracterização, aqui aplicados de ponta a ponta com Stub/Fake (Tutorial 25) e Test Data Builder (Tutorial 26).
