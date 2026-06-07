# Tutorial 19 — Geração multi-arquivo com agentes

> Referência: dirigir e revisar mudanças multi-arquivo com agentes

---

## 1. Contexto e Motivação

Em 2026, modelos de fronteira não apenas geram funções isoladas — eles editam
múltiplos arquivos em uma única instrução, propagando mudanças de interface
através do repositório. Claude Code, Codex e Gemini CLI operam sobre o
codebase completo, aplicando diffs coordenados que tocam dezenas de arquivos.

Essa capacidade traz um risco específico: **a inconsistência cross-file**.

Quando um agente altera a assinatura de uma função em um arquivo, ele precisa
atualizar todos os chamadores em todos os outros arquivos. Se um chamador for
esquecido, cada arquivo roda sua própria demo sem erro — a inconsistência só
aparece quando os dois arquivos são executados juntos.

> *"The first step in fixing a bug is to make the bug visible."*
> — Robert C. Martin, *Clean Code*, Cap. 3

O problema é que a inconsistência cross-file não aparece em nenhum arquivo
isolado — ela está no espaço *entre* os arquivos. Uma revisão arquivo por arquivo
não é suficiente. É preciso revisar o diff em altitude: olhando todos os arquivos
da mudança como um todo.

**O risco em 2026 é proporcional à velocidade.** Agentes que editam 10 arquivos
em 30 segundos têm mais oportunidade de deixar um chamador esquecido do que um
desenvolvedor que edita um arquivo por vez, compilando e testando a cada passo.
A habilidade de revisar o diff em altitude é o que mantém a consistência.

---

## 2. Conceito Central

### Mudanças multi-arquivo: o agente edita, você revisa

O fluxo com um agente de código é:

```
1. Você descreve a mudança (ex.: "adicionar cupom de desconto")
2. O agente lê os arquivos, planeja e aplica as edições
3. O agente apresenta o diff
4. Você revisa o diff — em altitude — e aceita ou corrige
```

A etapa crítica é a 4. Não a 2.

---

### O que é "revisar em altitude"

Revisar em altitude significa olhar o diff dos múltiplos arquivos **juntos**,
não um por vez:

```
REVISÃO ISOLADA (insuficiente):
  - precificacao.py: assinatura nova com 'cupom' ✓
  - carrinho.py: campo novo, função nova ✓
  → Aprovado ← (inconsistência não detectada)

REVISÃO EM ALTITUDE (suficiente):
  - precificacao.py declara: calcular_total(itens, cupom)  ← 2 args
  - carrinho.py chama:       calcular_total(itens)         ← 1 arg
  → INCONSISTÊNCIA DETECTADA ← TypeError em produção
```

A diferença não está no que cada arquivo faz internamente — está na interface
entre eles.

---

### O fragmento de diff com a inconsistência

O diff abaixo é a mudança real de `gerado/` (adicionar cupom ao carrinho).
Revise-o como você receberia de um agente:

```diff
# precificacao.py

+ @dataclass
+ class Cupom:
+     codigo:              str
+     percentual_desconto: float

  def calcular_total(
      itens: list[ItemCarrinho],
+     cupom: Optional[Cupom],   # ← NOVO parâmetro — sem valor padrão
  ) -> float:
      ...

# carrinho.py

  @dataclass
  class Carrinho:
      id:    str
      itens: list[ItemCarrinho] = field(default_factory=list)
+     cupom: Optional[Cupom]   = None

+ def aplicar_cupom(carrinho: Carrinho, cupom: Cupom) -> None:
+     carrinho.cupom = cupom

  def finalizar_carrinho(carrinho: Carrinho) -> dict:
      ...
-     total = calcular_total(carrinho.itens)
      total = calcular_total(carrinho.itens)         ← linha NÃO foi alterada
      return {
          ...
+         "cupom": carrinho.cupom.codigo if carrinho.cupom else None,
      }
```

**Pergunta de revisão:** a assinatura mudou em `precificacao.py` — o chamador em
`finalizar_carrinho` (carrinho.py) foi atualizado para os 2 argumentos?

Resposta: não. A linha `calcular_total(carrinho.itens)` não foi alterada. O agente
atualizou as linhas ao redor mas esqueceu esta. O cupom está no dict de retorno
mas nunca chega ao cálculo — inconsistência cross-file silenciosa.

Veja `exemplos/diff-comentado.md` para o diff completo com análise.

---

### Quando parar e re-dirigir o agente

Três sinais de que você deve interromper antes de aceitar o diff:

**1. A assinatura mudou mas você não viu a atualização dos chamadores**

```
Assinatura nova: calcular_total(itens, cupom)
Chamada em carrinho.py: calcular_total(itens)  ← não atualizado
```

Ação: "Você atualizou a assinatura de calcular_total mas finalizar_carrinho
ainda chama calcular_total(itens). Corrija este chamador."

**2. Um campo novo aparece no objeto mas não chega à lógica de cálculo**

```
Carrinho.cupom = cupom_aplicado   ← campo existe
total = calcular_total(itens)     ← cupom não entra no cálculo
```

Ação: "O campo cupom está no Carrinho mas não é passado para calcular_total.
Isso significa que o desconto nunca será aplicado. Corrija."

**3. O diff toca mais arquivos do que o necessário**

Se o agente propõe refatorar funções não relacionadas à mudança pedida,
pare e re-direcione: "Faça apenas a mudança de cupom. Nada mais."

---

## 3. Exercício

**Contexto:** os arquivos `exercicios/exercicio_carrinho.*` e
`exercicios/exercicio_precificacao.*` contêm uma mudança análoga — adicionar
cálculo de frete ao pedido. O agente atualizou `exercicio_precificacao` corretamente
(nova assinatura com `regiao`), mas `exercicio_carrinho` tem um chamador não atualizado.

**Tarefas:**

1. Execute os dois arquivos separadamente e observe que ambos rodam sem erro:
   ```bash
   python3 sessao-5/tutorial-19-multiarquivo-agentes/exercicios/exercicio_precificacao.py
   python3 sessao-5/tutorial-19-multiarquivo-agentes/exercicios/exercicio_carrinho.py
   ```

2. Revise os dois arquivos **juntos** como se fossem um diff de agente. Use o
   checklist abaixo. Identifique onde está a inconsistência cross-file.

3. Corrija o chamador inconsistente e confirme que o total agora inclui o frete
   (nordeste: R$ 29,90; total esperado: R$ 219,60).

4. Compare com `gabarito_carrinho.py` e `gabarito_revisao.md`.

**Referência:** `exercicios/roteiro-ia.md` contém o roteiro para os três modelos.

---

## 4. Checklist — Revisão de mudança multi-arquivo em altitude

Use estas perguntas sempre que receber um diff de agente que toca múltiplos arquivos:

- [ ] **Revisei o diff inteiro?** — olhei todos os arquivos modificados juntos, não um por vez?
- [ ] **A assinatura mudou e todos os chamadores acompanharam?** — se a função ganhou um parâmetro, cada chamada nos outros arquivos foi atualizada?
- [ ] **Campo novo → lógica nova?** — se um objeto ganhou um campo, esse campo chega até o ponto de cálculo ou é apenas exibido?
- [ ] **Rodei os dois arquivos juntos após a mudança?** — não só cada um isoladamente?
- [ ] **A mudança ficou coesa entre arquivos?** — a feature está completa em todos os arquivos envolvidos, sem partes esquecidas?
- [ ] **O diff é minimal?** — o agente não refatorou nada além do que foi pedido?

---

## 5. Referências

- Martin, Robert C. *Clean Code: A Handbook of Agile Software Craftsmanship*. Cap. 3 — Functions.
- Feathers, Michael. *Working Effectively with Legacy Code*. Cap. 8 — How Do I Add a Feature?
- Documentação Claude Code: [Claude Code e edições multi-arquivo](https://docs.anthropic.com/claude-code)
- OpenAI Codex: [Agent mode e AGENTS.md](https://platform.openai.com/docs/agents)
- Gemini CLI: [GEMINI.md e contexto amplo](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- Exemplos do repositório:
  - `sessao-5/tutorial-19-multiarquivo-agentes/exemplos/diff-comentado.md`
  - `sessao-5/tutorial-19-multiarquivo-agentes/exemplos/gerado/carrinho.py`
  - `sessao-5/tutorial-19-multiarquivo-agentes/exemplos/revisado/carrinho.py`
