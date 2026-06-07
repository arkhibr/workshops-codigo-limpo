# Roteiro Hands-on — Revisão Crítica de Código Gerado por IA

> Tutorial 20 — âncora do tema.
> Aplique o `checklist_revisao_ia.md` em saída real de três modelos e compare.

---

## Objetivo

Desenvolver o olhar para identificar defeitos sutis em código polido e confiante
gerado por modelos de fronteira. O exercício tem dois caminhos: **trilha real**
(gerar e revisar) e **trilha de fallback** (revisar o código deste tutorial).

---

## Trilha Real — Gerar e Revisar (recomendada)

### Passo 1 — Gerar o mesmo módulo em três modelos

Use o prompt base abaixo com Claude, ChatGPT (GPT-4o ou Codex) e Gemini.
Envie exatamente o mesmo texto para os três — sem ajustes:

```
Crie um módulo Python de integração com um gateway de pagamento.
O módulo deve expor três funções: cobrar, estornar, consultar_status.

Use identificadores em português, dataclasses e tipagem estática.
O gateway pode ser simulado em memória — sem rede real.
Inclua parcelamento com juros compostos de 1,99% ao mês.
Bloco if __name__ == "__main__": com demo de cobrança parcelada em 3x.
```

Salve cada saída em um arquivo separado:
- `saida_claude.py`
- `saida_openai.py`
- `saida_gemini.py`

### Passo 2 — Rodar os três arquivos

```bash
python3 saida_claude.py
python3 saida_openai.py
python3 saida_gemini.py
```

Confirme que todos rodam sem erro. Observe a saída de parcelamento — se o
número de parcelas geradas não bate com o solicitado, você já encontrou um defeito.

### Passo 3 — Aplicar o checklist em cada saída

Para cada arquivo, percorra `checklist_revisao_ia.md` seção por seção:

1. **Correção** — O parcelamento gera o número correto de parcelas? Trace manualmente.
2. **Segurança** — A validação de webhook usa constant-time? Há dado sensível em log?
3. **Edge cases** — Valor negativo é tratado? Lista vazia de parcelas funciona?
4. **Legibilidade/Coesão** — As docstrings descrevem o que o código faz?
5. **Dependências/Alucinação** — Todos os métodos chamados existem?
6. **A IA entendeu o pedido?** — Há camadas que não foram pedidas?

### Passo 4 — Registrar e comparar

Para cada saída, anote em uma tabela quantos itens do checklist foram violados:

| Categoria | Claude | OpenAI | Gemini |
|---|---|---|---|
| Correção | | | |
| Segurança | | | |
| Edge cases | | | |
| Legibilidade/Coesão | | | |
| Dependências/Alucinação | | | |
| A IA entendeu o pedido? | | | |
| **Total** | | | |

**Perguntas para reflexão:**
- Qual modelo produziu mais defeitos? Em quais categorias?
- Algum defeito apareceu nos três modelos? O que isso diz sobre o prompt?
- O código de algum modelo passaria sem ressalvas em um code review rápido?

---

## Trilha de Fallback — Revisar o Código do Tutorial

Se não tiver acesso aos modelos, use os arquivos deste tutorial diretamente:

```bash
# Rode o Python para ver a demo
python3 ../codigo_gerado_por_ia.py

# Rode o TypeScript
npx ts-node ../codigo_gerado_por_ia.ts
```

**Instrução:** leia `codigo_gerado_por_ia.py` do início ao fim como se fosse
um Pull Request real. Para cada problema encontrado, anote:
- A linha exata
- A categoria do checklist
- O problema e uma sugestão de correção

Depois confira com `gabarito_review.md`. O objetivo é encontrar os **6 defeitos
plantados** — mas itens adicionais que você identificar também são válidos.

**Critério de avaliação:**
- 5–6 defeitos encontrados: olhar bem calibrado para código de IA
- 3–4 defeitos: revisar as categorias onde perdeu e reler o tutorial
- 1–2 defeitos: refazer a leitura linha a linha com o checklist em mãos

---

## Variante em Par

Faça a revisão com um colega:
1. Um lê o código em voz alta, linha por linha
2. O outro acompanha o checklist e sinaliza quando algo parece suspeito
3. Troquem de papel na metade do arquivo

Alucinações e edge cases são significativamente mais fáceis de detectar quando
alguém está descrevendo o código para outra pessoa em tempo real.
