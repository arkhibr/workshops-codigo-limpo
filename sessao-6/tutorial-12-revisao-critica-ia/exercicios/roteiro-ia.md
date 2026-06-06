# Exercício — Gerar, Revisar e Registrar

> Este exercício fecha o loop completo: você gera código com uma IA, aplica o checklist
> de revisão na saída e mede quantos itens foram violados.

---

## Opção A — Gere seu próprio código (recomendada)

### Passo 1: Peça à IA um trecho similar

Use o assistente de IA da sua preferência e envie um prompt como:

```
Crie um módulo Python de integração com um gateway de boleto bancário.
O módulo deve ter as funções:
- emitir_boleto(valor, cpf_pagador, data_vencimento, descricao)
- consultar_boleto(codigo_barras)
- cancelar_boleto(codigo_barras, motivo)

O gateway tem uma API REST com autenticação Bearer.
```

**Importante:** envie este prompt *sem* adicionar restrições de segurança, edge cases
ou instruções sobre como ler a chave de API. Queremos observar o que a IA produz
com um prompt razoável, mas incompleto — exatamente como o `prompt_original.md` deste tutorial.

### Passo 2: Aplique o checklist

Abra `checklist_revisao_ia.md` e percorra cada item sobre o código que você recebeu.

Para cada item que encontrar violado, anote:
- A **linha** onde o problema aparece
- A **categoria** do checklist (Correção, Segurança, Edge cases, etc.)
- O que está errado e como corrigir

### Passo 3: Registre os resultados

Preencha a tabela abaixo no seu caderno ou em um arquivo local:

| # | Categoria | Linha | Problema encontrado | Presente no código gerado? |
|---|---|---|---|---|
| 1 | Segurança | ? | Chave de API hardcoded | Sim / Não |
| 2 | Segurança | ? | URL por concatenação | Sim / Não |
| 3 | Correção | ? | Lógica invertida | Sim / Não |
| 4 | Dependências | ? | Método inexistente (alucinação) | Sim / Não |
| 5 | Edge cases | ? | Valor zero/negativo sem validação | Sim / Não |
| 6 | Legibilidade e Coesão | ? | Comentário que mente | Sim / Não |

### Passo 4: Avalie

- **5–6 itens presentes:** a IA reproduziu os padrões de falha típicos com um prompt incompleto.
  Isso demonstra por que a revisão crítica é necessária, não opcional.
- **3–4 itens presentes:** o comportamento da IA variou. Compare com o checklist completo
  e verifique se há problemas que você não mapeou para as categorias acima.
- **0–2 itens presentes:** o prompt pode ter sido interpretado de forma mais cautelosa pela IA,
  ou a ferramenta adicionou salvaguardas próprias. Anote isso — é uma observação válida.

---

## Opção B — Revisão do código deste tutorial (fallback)

Se não tiver acesso a um assistente de IA agora, use `codigo_gerado_por_ia.py` (ou `.ts`)
como material de revisão.

1. Leia o código do início ao fim como se fosse um PR.
2. Anote cada problema que encontrar — linha, categoria, problema, sugestão.
3. Compare com `gabarito_review.md` para ver quais você acertou e quais perdeu.

**Meta:** encontrar todos os 6 problemas plantados antes de abrir o gabarito.

---

## Reflexão final

Independentemente da opção escolhida, responda para si mesmo:

1. Quais categorias do checklist o código violou com mais frequência?
2. Algum problema era difícil de perceber sem o checklist como guia?
3. Como você adaptaria o prompt original para reduzir esses problemas na próxima geração?

> Não existe resposta única — o objetivo é calibrar o olhar crítico para código de IA,
> não memorizar uma lista de defeitos.
