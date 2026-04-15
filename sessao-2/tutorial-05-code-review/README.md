# Tutorial 05 — Code Review Simulado

> **Sessão 2 · Exercício Âncora · 30 min**
> Este exercício integra todos os tutoriais anteriores em uma revisão real de código.

---

## Objetivo

Code review é onde o Clean Code vira trabalho em equipe. A qualidade do código de um time é, em grande parte, determinada pela qualidade das revisões que o time faz — não pelo brilhantismo individual.

Neste exercício você vai **simular um code review completo**: ler o arquivo `codigo_para_revisar.py` como se fosse um Pull Request e escrever comentários como faria para um colega de trabalho. O gabarito (`gabarito_review.md`) mostra o que um revisor experiente observaria no mesmo código.

O objetivo não é decorar os comentários do gabarito — é desenvolver o **olhar treinado** para identificar problemas de nomenclatura, função, comentários e formatação ao mesmo tempo.

---

## Como Fazer

1. **Leia o código** em [`codigo_para_revisar.py`](codigo_para_revisar.py) do começo ao fim, como se fosse um PR real.

2. **Abra um arquivo pessoal** (pode ser um `.md` ou `.txt`) e anote cada problema que encontrar. Para cada um, escreva:
   - A **linha** onde está o problema
   - O **problema** identificado
   - Uma **sugestão** de melhoria

3. **Rode o código** para confirmar que funciona antes de revisar:
   ```bash
   python codigo_para_revisar.py
   ```

4. **Compare com o gabarito** em [`gabarito_review.md`](gabarito_review.md). Veja quais problemas você acertou, quais perdeu e quais identificou a mais.

---

## O que Olhar — Checklist de Review

Use este checklist como guia durante a revisão:

### Nomes
- [ ] Variáveis, parâmetros e atributos revelam intenção sem precisar de comentário?
- [ ] Existem abreviações ou nomes de 1-2 letras que não sejam convenção (`i`, `e` em `except`)?
- [ ] As constantes têm nomes em `SCREAMING_SNAKE_CASE` que explicam o que representam?
- [ ] Os métodos têm nomes verbais que descrevem o que fazem?

### Funções
- [ ] Cada função faz uma única coisa?
- [ ] Os métodos longos poderiam ser divididos em funções menores e nomeadas?
- [ ] Existem parâmetros com nomes genéricos (`cpd`, `t`, `v`) que confundem?
- [ ] Há magic numbers soltos (valores numéricos sem constante nomeada)?

### Comentários
- [ ] Existem comentários que apenas repetem o que o código já diz?
- [ ] Existem TODOs sem rastreabilidade (sem ticket, responsável, prazo)?
- [ ] Há código comentado sem contexto?
- [ ] Há comentários de diário de bordo que deveriam estar no git?

### Formatação
- [ ] Os imports estão organizados (stdlib → terceiros → locais)?
- [ ] Há múltiplos imports na mesma linha?
- [ ] Existem linhas com mais de 88 caracteres?
- [ ] Os métodos estão separados por linhas em branco?

---

## O que é um Bom Comentário de Review?

Um comentário de review construtivo tem três partes: **o problema**, **o porquê é um problema** e **a sugestão**. Evite julgamentos vagos ou tom impositivo.

| Comentário | Qualidade |
|---|---|
| "Isso está errado." | Inútil — não diz o que está errado nem como corrigir |
| "Variável ruim." | Vago — não aponta o problema específico |
| "`self.p` não revela o que armazena. Sugiro renomear para `self._itens_do_pedido_atual` para deixar claro que são os itens do pedido em aberto." | Concreto, específico e com sugestão acionável |

### Regras de Tom

- **Específico:** aponte a linha e o elemento exato, não o arquivo inteiro
- **Construtivo:** sempre ofereça uma sugestão; crítica sem direção não ajuda
- **Impessoal:** comente o código, não o autor — "este nome não revela intenção" em vez de "você usou nome ruim"
- **Gradual:** diferencie blockers (problemas que impedem o merge) de suggestions (melhorias desejáveis mas opcionais)
- **Breve:** um comentário por problema; não misture vários problemas numa mesma anotação

---

## Como Comparar com o Gabarito

O gabarito tem **15 comentários** distribuídos em 4 categorias. Ao comparar:

- Se você encontrou **10 ou mais**, o olhar está bem calibrado
- Se você encontrou **5 a 9**, revise a categoria onde perdeu mais e releia o tutorial correspondente
- Se você encontrou **menos de 5**, considere refazer a leitura do código linha a linha usando o checklist acima como guia

> Não existe problema em ter encontrado problemas que o gabarito não tem — boas revisões são colaborativas, não têm uma única resposta correta.

---

> **Próximo tutorial:** [Tutorial 06 — Dívida Técnica](../tutorial-06-divida-tecnica/README.md)
