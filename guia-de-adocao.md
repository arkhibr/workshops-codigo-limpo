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

## Tutorial 08 — Clean Code no Contexto Real com IA

> Material de referência: [sessao-5/tutorial-08-clean-code-com-ia/README.md](sessao-5/tutorial-08-clean-code-com-ia/README.md)

Um prompt fraco produz código genérico: nomes abreviados, números mágicos, idioma misturado. Especificar domínio, padrão de nomenclatura e restrições no prompt eleva o ponto de partida antes da revisão. O que você vai incluir sempre num prompt para código — domínio, idioma, restrições?
> _:_

A IA não conhece o contexto do seu sistema — ela produz o que parece razoável dado o prompt. O que você vai revisar sempre antes de aceitar uma saída de IA no seu projeto?
> _:_

Há trechos onde a IA prejudica mais do que ajuda: lógica de negócio complexa com invariantes implícitas, código de segurança crítico, partes que exigem conhecimento do histórico do sistema. Quando você vai optar por escrever sem assistência de IA?
> _:_

A política de uso de IA define expectativas para o time inteiro: quando usar, o que sempre revisar, o que nunca aceitar sem verificação. **Qual será a política de uso de IA da sua equipe?**
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Tutorial 09 — Engenharia de Prompt para Código Limpo

> Material de referência: [sessao-5/tutorial-09-engenharia-de-prompt/README.md](sessao-5/tutorial-09-engenharia-de-prompt/README.md)

Um template de prompt inclui os elementos que você sempre precisa: contexto do domínio, idioma dos identificadores, restrições de dependências, formato de retorno esperado. Qual será o template de prompt padrão da sua equipe para gerar código?
> _:_

A IA não sabe que o seu módulo usa snake_case em português ou que certas libs são proibidas — a menos que você diga. Como você vai fornecer à IA o contexto dos padrões já existentes no projeto?
> _:_

Às vezes a saída está próxima do esperado e uma iteração no prompt resolve; outras vezes é mais rápido ajustar na mão. Quando vale a pena iterar o prompt em vez de corrigir a saída diretamente?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Tutorial 10 — Refatoração Assistida: Coesão e Legibilidade

> Material de referência: [sessao-5/tutorial-10-refatoracao-assistida/README.md](sessao-5/tutorial-10-refatoracao-assistida/README.md)

Pedir "melhore esse código" de uma vez entrega uma reescrita difícil de auditar; pedir um passo por vez — extraia essa função, renomeie essa variável — mantém cada mudança rastreável. Qual será sua regra ao usar IA para refatoração: passos pequenos ou de uma vez?
> _:_

Uma refatoração assistida pode alterar o comportamento sem aviso — a saída parece igual, mas um edge case mudou. Como você vai verificar que o comportamento foi preservado após uma refatoração assistida?
> _:_

Diffs grandes aumentam a chance de uma regressão passar despercebida na revisão. Qual é o tamanho máximo de mudança que você aceita revisar de uma vez antes de pedir que a IA divida em passos?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Tutorial 11 — Tratamento de Erros com IA

> Material de referência: [sessao-5/tutorial-11-tratamento-de-erros/README.md](sessao-5/tutorial-11-tratamento-de-erros/README.md)

`except Exception: pass` e `catch {}` vazio fazem o caminho feliz funcionar enquanto escondem falhas reais. O dado corrompido só aparece na ponta, longe da origem. O que você vai fazer ao encontrar esse padrão numa saída de IA?
> _:_

Serviços externos — banco de dados, APIs, filas — falham. Se essas falhas não são propagadas ou logadas, o sistema segue como se nada tivesse acontecido. Como você vai garantir que falhas externas não sejam silenciadas no código que aceitar?
> _:_

`ValueError`, `ConexaoRecusadaError`, `LimiteExcedidoError` — exceções com nome revelam o que falhou e onde. Que exceções específicas do seu domínio de negócio precisam existir como tipos próprios?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Tutorial 12 — Revisão Crítica de Código Gerado por IA

> Material de referência: [sessao-6/tutorial-12-revisao-critica-ia/README.md](sessao-6/tutorial-12-revisao-critica-ia/README.md)

Código de IA é confiante e plausível — compila, o nome parece razoável, o caminho feliz funciona. Exatamente por isso a revisão exige critérios explícitos. Qual será o seu checklist mínimo de revisão de código gerado por IA?
> _:_

A IA inventa métodos coerentes com o padrão da biblioteca que simplesmente não existem. O código compila mas quebra em runtime na primeira chamada. Como você vai confirmar que uma API ou método sugerido pela IA realmente existe?
> _:_

Comentários que descrevem o que o código faz mas contradizem o que o código realmente faz criam uma falsa sensação de clareza — o leitor confia no comentário e erra a lógica. Como você vai tratar essa "confiança enganosa" numa revisão?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Tutorial 13 — Segurança em Código Gerado por IA

> Material de referência: [sessao-6/tutorial-13-seguranca-codigo-ia/README.md](sessao-6/tutorial-13-seguranca-codigo-ia/README.md)

A IA hardcoda credenciais porque o prompt não disse como obtê-las — e o código funcional com segredo exposto é pior do que código que não funciona. Como você vai tratar segredos em código sugerido por IA antes de aceitar?
> _:_

Concatenação de parâmetros na query é a forma mais simples e mais perigosa de construir consultas. A IA escolhe o caminho de menor resistência se o prompt não restringe. Como você vai garantir consultas parametrizadas e validação de entrada no código que revisar?
> _:_

A IA pode sugerir uma dependência nova sem saber que a stdlib resolve o mesmo problema ou que a lib tem histórico de vulnerabilidades. Qual será o seu critério para aceitar ou rejeitar uma dependência nova sugerida pela IA?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Tutorial 14 — Testes como Guard-Rails para Mudanças Assistidas

> Material de referência: [sessao-6/tutorial-14-testes-guard-rails/README.md](sessao-6/tutorial-14-testes-guard-rails/README.md)

Mexer em código sem testes com auxílio de IA é acelerar sem freios — a regressão silenciosa só aparece quando o cliente reclama. Antes de deixar a IA modificar código sem cobertura de testes, o que você vai fazer primeiro?
> _:_

A IA pode escrever um teste que apenas confirma o comportamento que ela mesma implementou — inclusive comportamentos com bug. Como você vai evitar que os testes gerados só confirmem a implementação em vez de especificar o comportamento esperado?
> _:_

Rodar antes e depois garante que uma mudança assistida não quebrou nenhum caso existente. Qual será o seu ritual de verificação antes e depois de cada mudança assistida por IA?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Tutorial 15 — Manutenibilidade e Trabalho com Agentes

> Material de referência: [sessao-6/tutorial-15-manutenibilidade-agentes/README.md](sessao-6/tutorial-15-manutenibilidade-agentes/README.md)

Sem contexto dos padrões existentes, a IA introduz deriva: dois estilos de nomenclatura no mesmo arquivo, uma função quase idêntica a outra já existente, uma lib nova onde a stdlib bastava. Como você vai garantir que a IA siga os padrões já estabelecidos no seu código?
> _:_

Quando a IA edita vários arquivos de uma vez, olhar apenas para a saída nova é insuficiente — o diff inteiro revela duplicações, importações removidas, estilos divergentes introduzidos. Você vai revisar o diff completo ou só a saída isolada? Qual é o seu compromisso?
> _:_

A IA puxa dependências quando não sabe que o problema já está resolvido na stdlib ou em código existente. Ao longo do tempo, isso infla o projeto. Como você vai evitar que dependências desnecessárias se acumulem com o uso de IA?
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
| 08 — Clean Code com IA | |
| 09 — Engenharia de Prompt | |
| 10 — Refatoração Assistida | |
| 11 — Tratamento de Erros com IA | |
| 12 — Revisão Crítica de IA | |
| 13 — Segurança com IA | |
| 14 — Testes Guard-Rails | |
| 15 — Manutenibilidade com IA | |
