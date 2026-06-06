# Roteiro Hands-on — Manutenibilidade com Agentes de IA

> Duração estimada: 20–30 minutos
> Pré-requisito: acesso a um assistente de IA (ChatGPT, Claude, Gemini, Copilot ou similar)

---

## Objetivo

Experimentar como dar contexto de padrão ao agente reduz a deriva no diff — e praticar a revisão do diff inteiro como hábito de manutenibilidade.

---

## Passo a Passo

### 1. Escolha o módulo base

Use o `gabarito.py` (ou `gabarito.ts`) como ponto de partida — ele é o módulo consolidado, com estilo uniforme. Copie o conteúdo para um arquivo temporário (`meu_dashboard.py`).

```bash
cp sessao-6/tutorial-15-manutenibilidade-agentes/exercicios/gabarito.py meu_dashboard.py
```

---

### 2. Peça a feature SEM contexto de padrão

Cole o prompt abaixo no seu assistente:

```
Adiciona ao módulo abaixo uma função que calcula o ranking das 3 vendas
de maior valor e exibe o resultado.

[cole o conteúdo de meu_dashboard.py aqui]
```

Salve a saída em `meu_dashboard_sem_contexto.py` e rode:

```bash
python3 meu_dashboard_sem_contexto.py
```

---

### 3. Revise o diff — busque sinais de deriva

Compare a versão sem contexto com o original:

```bash
diff gabarito.py meu_dashboard_sem_contexto.py
```

Examine o diff linha a linha e marque cada sinal de deriva encontrado:

| # | Pergunta                                                                 | ✓ / ✗ |
|---|--------------------------------------------------------------------------|-------|
| 1 | A nova função usa o mesmo idioma (snake_case PT) das existentes?         |       |
| 2 | A nova função reutilizou `calcular_total_periodo` ou duplicou a lógica?  |       |
| 3 | Alguma dependência nova foi adicionada?                                  |       |
| 4 | A formatação (espaçamento, type hints) é consistente com o restante?     |       |
| 5 | A nova função parece ter sido escrita pelo mesmo time?                   |       |

---

### 4. Peça a mesma feature COM contexto de padrão

Cole o prompt abaixo — desta vez com o contexto de manutenibilidade embutido:

```
No módulo abaixo:
- Todos os identificadores estão em português, snake_case, com type hints.
- Funções de cálculo existentes: calcular_total_periodo(), calcular_percentual_meta().
  Reutilize — não duplique.
- Formatação de moeda: formatar_reais() já existe — use-a.
- Sem dependências externas — apenas stdlib.

Adiciona a função exibir_ranking_vendas(vendas: list[dict], top_n: int = 3) -> None
que:
1. Ordena as vendas pelo valor em ordem decrescente.
2. Exibe as top_n vendas com posição, descrição e valor formatado (formatar_reais).
3. Segue a formatação (espaçamento, docstring) das funções existentes.

[cole o conteúdo de meu_dashboard.py aqui]
```

Salve em `meu_dashboard_com_contexto.py` e rode:

```bash
python3 meu_dashboard_com_contexto.py
```

---

### 5. Compare os dois diffs

```bash
diff gabarito.py meu_dashboard_sem_contexto.py  > diff_sem_contexto.txt
diff gabarito.py meu_dashboard_com_contexto.py  > diff_com_contexto.txt
```

Responda:

1. Qual diff é menor? Por quê?
2. A versão com contexto ainda introduziu alguma deriva? Qual?
3. O comportamento (saída) é o mesmo nas duas versões?

---

### 6. Aplique a Regra do Escoteiro

Ao aceitar a versão com contexto, faça pelo menos uma melhoria adicional que não estava no pedido original — um nome mais descritivo, um comentário de intenção que faltava, uma docstring incompleta.

Isso é a Regra do Escoteiro com IA: a sessão termina com a base ligeiramente melhor do que você a encontrou.

---

## Aviso — Fallback sem IA

Se você não tiver acesso a um assistente no momento, use o `exercicio.py` como se fosse a saída de uma IA que recebeu um prompt sem contexto. O objetivo é a **revisão do diff**, não a geração em si. Aplique o checklist do Passo 3 comparando `exercicio.py` com `gabarito.py`.

---

## Reflexão final

> Cada sessão de IA sem contexto de padrão é uma aposta de que a IA vai adivinhar as suas convenções. A deriva acumulada não quebra o código — ela corrói a manutenibilidade. O antídoto é simples: dar contexto antes, revisar o diff depois.

Discuta com o grupo: qual foi o sinal de deriva mais comum na saída da IA neste exercício?
