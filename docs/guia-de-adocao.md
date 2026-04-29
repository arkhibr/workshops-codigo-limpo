# Guia de Adoção — Clean Code na Prática

Este guia ajuda você a transformar o que aprendeu no workshop em ações concretas no seu trabalho. Ele não é um resumo do material — é uma ferramenta de decisão.

**Como usar:**
- **Logo após o workshop:** leia a tabela de prioridades e escolha o que aplicar primeiro
- **Nos próximos meses:** volte à seção do tutorial relevante quando um tema aparecer no seu trabalho

---

## Tabela de Prioridades

| Tutorial | Aplique sempre | Aplique se… |
|---|---|---|
| **01 — Nomes** | Nomes que revelam intenção; idioma consistente no projeto | …o time demora para entender o que uma variável ou função faz |
| **02 — Funções** | Uma função faz uma coisa; sem parâmetros booleanos | …funções têm mais de 20 linhas ou fazem duas coisas distintas |
| **03 — Comentários** | Comentar só o *porquê*; TODOs com número de issue ou card | …o código herdado tem comentários enganosos ou código comentado |
| **04 — Formatação** | Formatter automático ativo no projeto | …ainda não há formatter configurado ou PRs têm ruído de espaçamento |
| **05 — Code Review** | Checklist mínimo antes de aprovar qualquer PR | …revisões hoje são informais ou os mesmos problemas se repetem |
| **06 — Dívida Técnica** | Regra do Escoteiro em cada PR — deixe melhor do que encontrou | …há módulos que ninguém quer tocar com medo de quebrar algo |
| **07 — Código Legado** | Testes de caracterização antes de qualquer mudança em código sem testes | …vai refatorar código sem cobertura de testes |

---

## Tutorial 01 — Nomes Significativos

### Recomendação forte

1. **Nomes revelam intenção** — se precisar de um comentário para explicar o que uma variável faz, renomeie-a.
2. **Idioma consistente** — se o domínio do negócio está em português, use português em todos os identificadores. Misturar idiomas cria fricção desnecessária.
3. **Sem abreviações inventadas** — `qtd_it_ped` não é mais rápido de ler do que `quantidade_itens_pedido`. É apenas mais difícil.

### Sinais do seu contexto

- Alguém do time perguntou o que uma variável significa? → Esse nome precisa mudar agora.
- Você abriu um arquivo e não conseguiu entender o que a função principal faz em menos de 30 segundos? → Comece pelos nomes das funções.
- O código mistura inglês e português nos identificadores? → Escolha um idioma e aplique como padrão de equipe.

### Primeiro passo esta semana

No próximo arquivo que você tocar, renomeie as 3 primeiras variáveis cujo propósito não é imediatamente óbvio pelo nome. Não é necessário pedir aprovação — renomear uma variável é a mudança mais segura que existe.

---

## Tutorial 02 — Funções

### Recomendação forte

1. **Uma função faz uma coisa** — se precisar de "e" para descrever o que ela faz, divida-a em duas.
2. **Sem parâmetros booleanos** — `processar(enviar_email=True)` é uma função disfarçada de duas. Crie `processar()` e `processar_e_notificar()`.
3. **Comando ou consulta, nunca os dois** — funções que mudam estado não retornam valor; funções que retornam valor não têm efeitos colaterais. (CQS: Command-Query Separation)

### Sinais do seu contexto

- A função tem mais de 20 linhas? → Provavelmente está fazendo mais de uma coisa.
- Você precisa rolar a tela para ver o início e o fim de uma função? → Divida-a.
- A função tem um parâmetro chamado `modo`, `tipo` ou `flag`? → Esse parâmetro está pedindo para virar duas funções.

### Primeiro passo esta semana

Encontre uma função que faz mais de uma coisa e extraia a segunda responsabilidade para uma nova função com nome próprio. Comece pela menor extração possível — não precisa refatorar tudo de uma vez.

---

## Tutorial 03 — Comentários

<!-- placeholder — preenchido na Task 5 -->

---

## Tutorial 04 — Formatação

<!-- placeholder — preenchido na Task 6 -->

---

## Tutorial 05 — Code Review

<!-- placeholder — preenchido na Task 7 -->

---

## Tutorial 06 — Dívida Técnica

<!-- placeholder — preenchido na Task 8 -->

---

## Tutorial 07 — Código Legado

<!-- placeholder — preenchido na Task 9 -->
