# Guia de Adoção — Clean Code na Prática

Responda as perguntas abaixo no seu próprio contexto. Ao final, suas respostas formam o seu guia prático de adoção.

---

## Meu Projeto

Qual linguagem principal você usa?
> _:_

Qual o tamanho do seu time?
> _:_

Qual o maior problema de qualidade de código que você enfrenta hoje?
> _:_

---

## Tutorial 01 — Nomes Significativos

> Material de referência: [sessao-1/tutorial-01-nomes/README.md](sessao-1/tutorial-01-nomes/README.md)

Usar o mesmo idioma do domínio de negócio facilita a leitura — quem lê o código já conhece os termos. Português é natural quando o negócio opera em português; inglês pode fazer sentido se o time é internacional ou a base de código já está em inglês. Qual será a sua escolha de idioma para os identificadores?
> _:_

Nomes no plural (`pedidos`, `usuarios`) ou com sufixo (`lista_pedidos`) são convenções comuns para coleções. Qual padrão você vai adotar?
> _:_

Abreviações como `qtd_it_ped` economizam digitação mas custam compreensão. A alternativa — `quantidade_itens_pedido` — é imediata de ler. Como você vai lidar com abreviações obscuras que aparecerem no código?
> _:_

Um critério simples: se você precisa ler o contexto ao redor para entender o que uma variável faz, o nome pode melhorar. Qual será o seu critério para decidir que um nome precisa ser renomeado?
> _:_

Misturar `getUserPedidos()` com `buscar_user_orders()` cria inconsistência que acumula. Algumas equipes fazem uma migração gradual, outras estabelecem um padrão e aplicam dali em diante. Como você vai tratar nomes que misturam idiomas?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Tutorial 02 — Funções

> Material de referência: [sessao-1/tutorial-02-funcoes/README.md](sessao-1/tutorial-02-funcoes/README.md)

Não existe um número mágico, mas funções que não cabem na tela dificultam a compreensão. Algumas equipes usam 20 linhas como referência, outras preferem "cabe na tela sem rolar". Qual tamanho máximo você vai definir para uma função?
> _:_

Uma função que valida, calcula e salva ao mesmo tempo é difícil de testar e de reusar. Dividir em funções menores torna cada uma mais simples e mais fácil de nomear. Como você vai tratar uma função que claramente faz mais de uma coisa?
> _:_

`processar(enviar_email=True)` é uma função disfarçada de duas — o booleano controla comportamentos diferentes. A alternativa é criar `processar()` e `processar_e_notificar()`. O que você vai fazer quando encontrar esse padrão?
> _:_

Funções que mudam estado e também retornam valor são difíceis de compor e de testar. Separar em `salvar()` + `buscar_id()` é mais previsível do que `salvar_e_retornar_id()`. Como você vai aplicar essa separação no seu código?
> _:_

Funções com muitos parâmetros são difíceis de chamar e de lembrar a ordem. Agrupar parâmetros relacionados em um objeto ou dataclass é uma solução comum. O que você vai fazer quando uma lista de parâmetros crescer demais?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Tutorial 03 — Comentários

> Material de referência: [sessao-1/tutorial-03-comentarios/README.md](sessao-1/tutorial-03-comentarios/README.md)

Comentários que explicam *o quê* o código faz tendem a ficar desatualizados. Comentários que explicam *por que* uma decisão foi tomada — uma regra de negócio não óbvia, um workaround para um bug externo — têm valor duradouro. O que você vai usar como critério para decidir quando comentar?
> _:_

Código comentado cria ruído e dúvida: foi deixado de propósito? pode ser apagado? O histórico do Git preserva tudo que já foi escrito. O que você vai fazer quando encontrar código comentado no projeto?
> _:_

`# TODO: refatorar isso` sem contexto raramente é resolvido — ninguém sabe quem criou, quando, ou se ainda é relevante. Formatos como `# TODO [#123]: refatorar após migração` ligam o TODO a um item rastreável. Qual formato você vai adotar?
> _:_

Quando um trecho é difícil de entender, a solução pode ser um comentário explicativo ou um código melhor — nome mais claro, função extraída. Como você vai decidir entre comentar e refatorar?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Tutorial 04 — Formatação

> Material de referência: [sessao-1/tutorial-04-formatacao/README.md](sessao-1/tutorial-04-formatacao/README.md)

Formatters automáticos eliminam discussões de estilo em PR e garantem consistência sem esforço manual. Para Python há o Black, para JS/TS o Prettier, para PHP o php-cs-fixer. Qual você vai configurar no seu projeto?
> _:_

O formatter pode rodar ao salvar o arquivo, como pre-commit hook, ou no CI. Salvar é imediato mas pode interferir no fluxo; CI é garantido mas o feedback vem mais tarde. Quando faz mais sentido rodar o formatter no seu fluxo de trabalho?
> _:_

A Stepdown Rule sugere colocar funções mais abstratas no topo e funções de detalhe abaixo — o leitor vai do geral para o específico. Outra abordagem é agrupar por domínio ou responsabilidade. Como você vai organizar a ordem das funções nos seus arquivos?
> _:_

Comentários de PR sobre indentação ou espaçamento são ruído que um formatter eliminaria. Se ainda aparecem, é um sinal de que o formatter não está configurado ou não está no CI. O que você vai fazer quando esse tipo de comentário aparecer numa revisão?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Tutorial 05 — Code Review

> Material de referência: [sessao-2/tutorial-05-code-review/README.md](sessao-2/tutorial-05-code-review/README.md)

Sem um checklist, revisões dependem do humor e do tempo do revisor naquele dia. Os 4 tutoriais anteriores já formam um checklist natural: nomes, funções, comentários, formatação. O que você vai incluir no seu checklist mínimo de revisão?
> _:_

Aprovações em menos de 2 minutos raramente envolvem análise real. Um tempo mínimo não é sobre ser lento — é sobre garantir que a revisão de fato aconteceu. Qual compromisso de tempo mínimo você vai assumir por revisão?
> _:_

Feedback como "esse código está confuso" é subjetivo e difícil de agir. "Essa função faz validação e persistência — vale separar em duas" é concreto e acionável. Como você vai estruturar seus comentários de revisão?
> _:_

Discordâncias técnicas em revisão podem travar PRs ou gerar conflito. Algumas equipes usam prefixos como `nit:` para sugestão menor e `blocker:` para o que não pode entrar assim. Como você vai tratar discordâncias técnicas numa revisão?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Tutorial 06 — Dívida Técnica

> Material de referência: [sessao-2/tutorial-06-divida-tecnica/README.md](sessao-2/tutorial-06-divida-tecnica/README.md)

A Regra do Escoteiro diz: deixe o código melhor do que encontrou. Não precisa ser uma refatoração grande — renomear uma variável ou extrair uma constante já conta. Qual será a sua regra de melhoria incremental em cada PR que você tocar?
> _:_

Dívida não registrada se torna dívida invisível — ninguém sabe que existe até que cause um problema. Criar um issue ou card com o problema e o impacto estimado torna a dívida visível e gerenciável. Como você vai documentar dívida técnica que não pode resolver agora?
> _:_

`if status == 3` não comunica nada. `if status == STATUS_AGUARDANDO_APROVACAO` é autoexplicativo. Extrair magic numbers e strings literais para constantes nomeadas é uma das melhorias mais rápidas e de maior impacto. O que você vai fazer quando encontrar esse padrão?
> _:_

Melhorias incrementais não resolvem tudo — às vezes um módulo está tão comprometido que precisa de atenção dedicada. Como você vai identificar esse momento e propor a priorização para o time?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Tutorial 07 — Código Legado

> Material de referência: [sessao-2/tutorial-07-codigo-legado/README.md](sessao-2/tutorial-07-codigo-legado/README.md)

Modificar código legado sem testes é como operar sem rede de segurança — qualquer mudança pode causar um efeito inesperado em outro lugar. Testes de caracterização documentam o comportamento atual antes de qualquer mudança. Qual será a sua regra antes de modificar código sem cobertura de testes?
> _:_

Testes de caracterização não testam o que *deveria* acontecer — testam o que *acontece hoje*, incluindo comportamentos estranhos. O objetivo é criar uma rede de segurança, não validar a lógica. Como você vai escrever esses testes para um módulo que não conhece bem?
> _:_

Refatorações grandes em código legado têm alta chance de nunca terminar ou de introduzir regressões. Mudanças incrementais — uma função por vez, um conceito por vez — são mais seguras e mais fáceis de revisar. O que você vai fazer quando precisar mexer em um módulo legado grande?
> _:_

O Strangler Fig substitui partes do sistema gradualmente construindo a nova versão ao lado da antiga. É mais trabalhoso no curto prazo mas reduz o risco de uma mudança grande quebrar tudo. Em que situação você vai propor essa abordagem em vez de refatoração incremental?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Meu Plano de Adoção

| Tutorial | Minha decisão principal |
|---|---|
| 01 — Nomes | |
| 02 — Funções | |
| 03 — Comentários | |
| 04 — Formatação | |
| 05 — Code Review | |
| 06 — Dívida Técnica | |
| 07 — Código Legado | |
