# Prompt — Dirigir uma mudança multi-arquivo com agentes

Este arquivo demonstra **o mesmo objetivo de geração** — adicionar suporte a
cupom de desconto em dois arquivos (`carrinho` + `precificacao`) — com as
três ferramentas de fronteira.

**Objetivo:** o agente deve atualizar `precificacao` para aceitar cupom e
propagar essa mudança para todos os chamadores em `carrinho`.

---

## O prompt base (comum aos três modelos)

```
Adicione suporte a cupom de desconto ao módulo de carrinho.

Mudanças necessárias:
1. Em precificacao: adicionar @dataclass Cupom (codigo, percentual_desconto),
   constante CUPONS_VALIDOS com pelo menos 2 cupons, função resolver_cupom(codigo),
   e atualizar calcular_total para aceitar cupom como segundo argumento obrigatório.

2. Em carrinho: adicionar campo 'cupom: Optional[Cupom]' ao Carrinho,
   função aplicar_cupom, e atualizar TODOS os chamadores de calcular_total
   para passar carrinho.cupom como segundo argumento.

Antes de gerar qualquer código:
  - Liste todos os locais onde calcular_total é chamado em carrinho.
  - Confirme que cada chamador será atualizado para a nova assinatura.
```

A instrução "liste todos os chamadores e confirme" é o mecanismo que força
o agente a auditar a propagação antes de escrever código — reduzindo a chance
de deixar um chamador esquecido.

---

## Claude (Opus 4.8 / Claude Code)

Claude Code opera sobre o repositório completo via contexto de 1M tokens e
executa edições multi-arquivo de forma coordenada. O fluxo correto:

```
[em Claude Code, com o repositório aberto]

Quero adicionar suporte a cupom de desconto ao carrinho. Os arquivos envolvidos
são sessao-5/tutorial-19-multiarquivo-agentes/exemplos/revisado/precificacao.py
e carrinho.py.

Antes de editar qualquer arquivo:
1. Mostre todos os locais onde calcular_total é chamado nos dois arquivos.
2. Confirme qual será a nova assinatura completa de calcular_total.
3. Liste cada chamador que precisará de atualização.

Depois, aplique as mudanças nos dois arquivos de uma vez, mantendo cada arquivo
autocontido e com bloco if __name__ == "__main__": funcionando.
```

**Como Claude Code aplica e apresenta o diff:**

Claude Code edita os dois arquivos em uma única operação coordenada. Ao
concluir, apresenta um diff unificado mostrando `precificacao.py` e
`carrinho.py` lado a lado. A instrução de listar chamadores antes força
o modelo a verificar a propagação da mudança explicitamente.

**O que revisar no diff:**
- Conferir que a nova assinatura de `calcular_total` aparece igual nos dois arquivos.
- Verificar que toda chamada a `calcular_total` em `carrinho.py` inclui o argumento `cupom`.
- Confirmar que `carrinho.cupom` é passado — não `None` fixo ou valor omitido.

**Instrução de fallback se o diff estiver incompleto:**

```
Você atualizou a assinatura em precificacao.py mas não encontrei a atualização
do chamador em finalizar_carrinho (carrinho.py). Mostre o trecho atual dessa
função e aplique a correção.
```

---

## OpenAI (Codex — agent mode)

O Codex em agent mode itera autonomamente: lê os arquivos, propõe mudanças,
executa e verifica. Para mudanças multi-arquivo, o controle de propagação
é feito via instrução de plano explícito:

```
[mensagem de sistema / AGENTS.md]
You are a Python code agent for a Clean Code workshop (Brazilian Portuguese).
All identifiers in Portuguese. @dataclass for entities. Named constants.
Flat module structure. Each file must remain self-contained with __main__ demo.

[mensagem do usuário]
Before making any edits, output a plan with:
  1. New signature of calcular_total (full line).
  2. Every call site of calcular_total in both files (file + line).
  3. Confirmation that all call sites will be updated.

Then apply the following multi-file change:
  FILE: precificacao.py — add Cupom dataclass, CUPONS_VALIDOS constant,
    resolver_cupom function, update calcular_total signature to include cupom.
  FILE: carrinho.py — add cupom field to Carrinho, aplicar_cupom function,
    update ALL calls to calcular_total to pass carrinho.cupom.

After editing, run both files and confirm output.
```

**Como o Codex aplica e apresenta o diff:**

O Codex em agent mode mostra o plano textual antes de editar (se instruído),
depois aplica as mudanças arquivo por arquivo e exibe um diff por arquivo.
Cada diff é independente — o revisor precisa mentalmente compor os dois para
detectar inconsistências cross-file.

**Diferença relevante:** pedir o plano com a lista de chamadores antes das
edições é mais crítico no Codex do que no Claude Code, porque o Codex não
apresenta um diff unificado multi-arquivo de forma nativa. A inconsistência
cross-file é mais fácil de passar despercebida quando os diffs chegam em
janelas separadas.

---

## Gemini (Gemini CLI)

O Gemini CLI usa `GEMINI.md` como instrução permanente e aproveita a janela
de contexto ampla para receber exemplos completos. Para mudanças multi-arquivo,
cole os dois arquivos completos antes do prompt de mudança:

```
# system_instruction (em GEMINI.md):
Você é um agente de código para um workshop de Clean Code em português.
Identificadores em português. @dataclass para entidades. Constantes nomeadas.
Módulo plano sem camadas. Bloco __main__ com demo de stdout.

# prompt (cole precificacao.py e carrinho.py completos antes deste bloco):
Antes de qualquer edição, liste:
  1. Assinatura nova de calcular_total (linha completa).
  2. Todos os locais onde calcular_total é chamado nos dois arquivos.
  3. Confirmação de que cada chamador será atualizado.

Aplique a seguinte mudança multi-arquivo:
  ARQUIVO precificacao.py: adicionar @dataclass Cupom, constante CUPONS_VALIDOS,
    função resolver_cupom, atualizar calcular_total para receber cupom como
    segundo argumento obrigatório (sem valor padrão).
  ARQUIVO carrinho.py: adicionar campo cupom ao Carrinho, função aplicar_cupom,
    atualizar TODOS os chamadores de calcular_total para passar carrinho.cupom.

Após as edições, mostre o diff de cada arquivo separadamente, depois mostre
um resumo cross-file confirmando que a assinatura é consistente entre os dois.
```

**Como o Gemini CLI aplica e apresenta o diff:**

O Gemini apresenta as edições como blocos de código substituídos, normalmente
arquivo por arquivo. A instrução de "resumo cross-file" ao final força o modelo
a declarar explicitamente a consistência — e se houver inconsistência, essa
declaração falsa se torna mais fácil de detectar na revisão.

**Vantagem:** colar os arquivos completos como contexto permite que o Gemini
identifique todos os chamadores sem depender de indexação de repositório.
Útil quando o projeto não tem um `GEMINI.md` configurado ou quando os arquivos
são isolados do repositório principal.

---

## O que muda entre os modelos

| Aspecto | Claude Code | Codex (agent mode) | Gemini CLI |
|---|---|---|---|
| Como aplica a mudança | Edição coordenada dos dois arquivos | Arquivo por arquivo, iterativo | Blocos substituídos, arquivo por arquivo |
| Como apresenta o diff | Diff unificado multi-arquivo | Diffs separados por arquivo | Blocos de código + resumo textual |
| Visibilidade cross-file | Alta (diff unificado) | Baixa (diffs separados) | Média (depende da instrução de resumo) |
| Mecanismo de controle de propagação | Instrução de listar chamadores | Instrução de plano antes das edições | Instrução de resumo cross-file ao final |
| Onde a inconsistência emerge | No diff unificado, se houver | Entre os diffs separados | Na discrepância entre código e resumo |

**Conclusão:** os três modelos podem gerar a mudança corretamente com a instrução
certa. A diferença está em como cada um apresenta o resultado e o quanto o revisor
precisa compor manualmente para enxergar a inconsistência cross-file. Revisar o
diff em altitude — olhando os dois arquivos juntos — é o mecanismo mais confiável
independentemente do modelo usado.
