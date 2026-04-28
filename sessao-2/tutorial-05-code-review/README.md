# Tutorial 05 — Code Review Simulado

> Este exercício integra todos os tutoriais anteriores em uma revisão real de código.

---

## Objetivo

Code review é onde o Clean Code vira trabalho em equipe. A qualidade do código de um time é, em grande parte, determinada pela qualidade das revisões que o time faz — não pelo brilhantismo individual.

Neste exercício você vai **simular um code review completo**: ler o arquivo `codigo_para_revisar.py` como se fosse um Pull Request e escrever comentários como faria para um colega de trabalho. O gabarito (`gabarito_review.md`) mostra o que um revisor experiente observaria no mesmo código.

O objetivo não é decorar os comentários do gabarito — é desenvolver o **olhar treinado** para identificar problemas de nomenclatura, função, comentários e formatação ao mesmo tempo.

---

## O que é Code Review?

Code review tem dois propósitos principais que se reforçam mutuamente:

**1. Qualidade técnica:** encontrar bugs, violações de padrões, problemas de segurança e dívida técnica introduzida antes que o código chegue à main. Uma segunda leitura quase sempre encontra algo que o autor não viu — não por incompetência, mas porque o autor tem o contexto que o leitor não tem.

**2. Transferência de conhecimento:** quem revisa aprende sobre a área alterada; quem escreve recebe uma perspectiva externa sobre clareza e design. Com o tempo, o time inteiro passa a conhecer partes do sistema que antes eram território de uma só pessoa.

Estudos de engenharia de software mostram que inspeções de código encontram entre **60 e 90% dos bugs** antes de qualquer teste automatizado (Capers Jones, *Applied Software Measurement*, 2008). Testes automatizados e review se complementam: review encontra problemas de design e clareza que testes não detectam; testes encontram problemas de comportamento em produção que review pode perder.

---

## Como fazer um bom comentário de review

Um comentário de review precisa ser acionável. Crítica sem direção obriga o autor a adivinhar o que fazer.

**Seja específico:** aponte a linha e o elemento exato.
> "Linha 42: esta função valida o e-mail E envia a confirmação — considere extrair o envio em função separada (`enviar_email_confirmacao`)."

É melhor que:
> "Esta função está grande."

**Seja construtivo com perguntas:** perguntas convidam o autor a pensar, em vez de impor uma solução.
> "O que acontece se `usuario` for `None` aqui? Precisa de uma guarda antes da linha 58?"

**Distinga severidade com prefixos:**
- `[blocker]` — problema que impede o merge (bug, falha de segurança, violação de contrato de API)
- `[sugestão]` — melhoria relevante mas o PR pode ser mergeado sem ela
- `[nitpick]` — questão estética ou de preferência; baixíssima prioridade

**Comente o código, não a pessoa:** "este trecho" em vez de "você fez". A frase "este nome não revela intenção" é objetiva; "você usou nome ruim" é pessoal e gera defensividade desnecessária.

| Comentário | Qualidade |
|---|---|
| "Isso está errado." | Inútil — não diz o que está errado nem como corrigir |
| "Variável ruim." | Vago — não aponta o problema específico |
| "`self.p` não revela o que armazena. Sugiro renomear para `self._itens_do_pedido_atual` para deixar claro que são os itens do pedido em aberto." | Concreto, específico e com sugestão acionável |

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

## Como Comparar com o Gabarito

O gabarito tem **15 comentários** distribuídos em 4 categorias. Ao comparar:

- Se você encontrou **10 ou mais**, o olhar está bem calibrado
- Se você encontrou **5 a 9**, revise a categoria onde perdeu mais e releia o tutorial correspondente
- Se você encontrou **menos de 5**, considere refazer a leitura do código linha a linha usando o checklist acima como guia

> Não existe problema em ter encontrado problemas que o gabarito não tem — boas revisões são colaborativas, não têm uma única resposta correta.

---

> **Próximo tutorial:** [Tutorial 06 — Dívida Técnica](../tutorial-06-divida-tecnica/README.md)
