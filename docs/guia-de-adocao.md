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

### Recomendação forte

1. **Comentários explicam o *porquê*, não o *o quê*** — o código já diz o que faz. Se precisar explicar o que faz, melhore o código.
2. **Código comentado é lixo** — delete-o. O histórico do Git guarda o passado; o arquivo não precisa guardar.
3. **TODOs têm dono e rastreabilidade** — `# TODO: refatorar isso` sem contexto nunca será resolvido. Use `# TODO [#123]: refatorar após migração de schema`.

### Sinais do seu contexto

- O arquivo tem blocos de código comentado que ninguém toca? → Delete-os no próximo PR.
- Os comentários descrevem o que o código faz em vez de por que ele faz? → Substitua pelo nome correto da função ou variável.
- Há TODOs sem número de issue no projeto? → Eles nunca serão feitos ou nunca deveriam ser feitos — decida qual.

### Primeiro passo esta semana

No próximo arquivo que você abrir, delete todo o código comentado. Se sentir insegurança, lembre: o Git tem tudo.

---

## Tutorial 04 — Formatação

### Recomendação forte

1. **Formatter automático, sem debate** — configure o formatter padrão da sua linguagem e ative-o no CI. Discussão de estilo em PR é tempo desperdiçado.
2. **Funções relacionadas ficam próximas** — quem lê o código não deve pular entre arquivos ou entre o início e o fim do arquivo para entender um fluxo.
3. **Abstrações de cima para baixo** — a função mais geral aparece antes das funções de detalhe que ela chama. (Stepdown Rule)

### Sinais do seu contexto

- PRs têm comentários sobre indentação, aspas simples vs. duplas ou espaçamento? → Instale um formatter e elimine essa classe de comentário para sempre.
- É difícil seguir o fluxo de uma função porque ela chama outras definidas 200 linhas acima? → Reorganize com a Stepdown Rule.

### Primeiro passo esta semana

Configure o formatter padrão da sua linguagem principal e rode-o no projeto:
- Python: `black .`
- TypeScript/JavaScript: `prettier --write .`
- PHP: `php-cs-fixer fix`

Se o projeto já tem formatter, verifique se ele está ativo no CI.

---

## Tutorial 05 — Code Review

### Recomendação forte

1. **"LGTM" sem análise não é revisão** — toda aprovação deve ter pelo menos uma observação genuína sobre o código.
2. **Checklist mínimo antes de aprovar:** nomes revelam intenção? funções fazem uma coisa? comentários desnecessários removidos? formatter aplicado?
3. **Feedback no código, não na pessoa** — "essa função pode ser dividida em duas" é acionável. "Você escreveu isso de forma confusa" não é.

### Sinais do seu contexto

- PRs são aprovadas em menos de 2 minutos sem comentários? → O processo de revisão precisa de estrutura.
- Os mesmos problemas aparecem repetidamente nas revisões? → Transforme-os em um checklist compartilhado pelo time.
- Revisores ficam em dúvida sobre o que verificar? → O checklist dos 4 primeiros tutoriais é o ponto de partida.

### Primeiro passo esta semana

No próximo PR que você revisar, aplique os critérios dos tutoriais 01 a 04 como checklist explícito e deixe pelo menos 2 observações concretas — mesmo que seja para elogiar uma boa escolha de nome.

---

## Tutorial 06 — Dívida Técnica

### Recomendação forte

1. **Regra do Escoteiro em todo PR** — deixe o código melhor do que encontrou. Não precisa ser muito: renomear uma variável ou extrair uma constante já conta.
2. **Dívida não documentada acumula juros invisíveis** — quando não puder pagar agora, registre: crie um issue ou card descrevendo o problema e o impacto estimado.
3. **Magic numbers são dívida técnica visível** — `if status == 3` não diz nada. `if status == STATUS_AGUARDANDO_APROVACAO` diz tudo. Extraia para constantes nomeadas.

### Sinais do seu contexto

- Há módulos que ninguém quer tocar com medo de quebrar algo? → Esses módulos têm dívida técnica crítica acumulada. Não ignore — registre e planeje.
- As estimativas de prazo sempre incluem uma margem para "consertar antes de entregar"? → A dívida está controlando o ritmo do time.
- O mesmo bloco de código aparece em mais de dois lugares? → Duplicação é dívida técnica. Extraia para uma função compartilhada.

### Primeiro passo esta semana

No próximo PR, encontre um magic number ou string literal espalhado pelo código e extraia para uma constante com nome que revele intenção. Uma mudança pequena, mas que melhora a leitura imediatamente.

---

## Tutorial 07 — Código Legado

<!-- placeholder — preenchido na Task 9 -->
