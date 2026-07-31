# Guia de Adoção — Clean Code na Prática

Um time que nunca praticou Clean Code não absorve 33 tutoriais de uma vez. Tenta adotar tudo ao mesmo tempo, atropela o básico e, em duas semanas, volta ao que fazia antes. Este guia existe para dar ordem: o que vem primeiro, o que cada passo compra em capacidade real, e como saber que o time está pronto para o próximo.

O guia tem duas partes.

- **Parte 1 — A estratégia de adoção.** A rota que um tech lead usa para conduzir o time do zero até o fluxo assistido por IA. É aqui que os 33 tutoriais deixam de ser uma lista e viram uma escada.
- **Parte 2 — O workbook por tutorial.** Perguntas que cada desenvolvedor responde no próprio contexto para transformar a teoria de cada tutorial em decisão registrada.

## Para quem pilota e para quem pratica

Quem conduz a adoção — tech lead, líder técnico, quem quer que seja — lê a Parte 1 e decide a sequência: em que nível o time está, qual é o próximo, o que vai medir para saber que avançou. Cada desenvolvedor lê a Parte 2 do nível atual e registra as próprias decisões.

Pular níveis não funciona. Um time que tenta aplicar SOLID (Nível 3) antes de concordar em como nomear uma variável (Nível 1) gasta o code review discutindo estilo em vez de design. A escada existe justamente para que cada degrau se apoie no anterior.

---

## Parte 1 — A estratégia de adoção

### A escada de maturidade

Cinco níveis. Cada um agrupa um conjunto de tutoriais que compram uma capacidade concreta, tem um sinal observável de que o time dominou, e um gatilho que indica a hora de subir.

| Nível | Capacidade que o time ganha | Tutoriais |
|---|---|---|
| 1 — Código Legível | Qualquer pessoa lê o código dos outros sem precisar do autor ao lado | T01–T04 |
| 2 — Revisão e Sustentação | Manter a qualidade sob prazo apertado e mexer no legado sem pânico | T05–T07 |
| 3 — Design que Resiste à Mudança | Adicionar comportamento novo sem reescrever o antigo | T08–T15 |
| 4 — Rede de Testes | Mudar o código sem medo, porque a máquina avisa o que quebrou | T24–T33 |
| 5 — Fluxo Assistido por IA | Acelerar com IA sem baixar a régua de qualidade | T16–T23 |

A ordem não é arbitrária. Cada nível é a pré-condição do seguinte, e as transições contam a história inteira:

- Código ilegível (falta o Nível 1) inviabiliza a revisão do Nível 2 — não se revisa o que não se lê.
- Sem a disciplina de revisão e a coragem para tocar no legado (Nível 2), a refatoração para bons designs (Nível 3) não tem onde acontecer.
- Design testável (Nível 3, sobretudo a inversão de dependências do SOLID) é o que permite escrever os testes de unidade do Nível 4 sem precisar de banco e e-mail reais.
- E a rede de testes do Nível 4 é o que torna seguro deixar a IA dirigir no Nível 5 — sem ela, a IA só acelera a produção de código que ninguém consegue conferir.

Uma decisão de ordem merece destaque: **testes (Nível 4) vêm depois de design (Nível 3), e IA (Nível 5) vem por último**. O Nível 4 não depende de IA em nenhum ponto — a rede de testes é a mesma com ou sem assistente. É ela, e não a IA, que dá ao time a liberdade de mudar o código. A IA entra por cima dessa rede, nunca no lugar dela.

---

### Nível 1 — Código Legível

> Tutoriais: **T01 Nomes · T02 Funções · T03 Comentários · T04 Formatação**

**A capacidade:** qualquer pessoa do time abre um arquivo que não escreveu e entende o que ele faz sem perguntar ao autor.

**Como os quatro tutoriais se encadeiam.** Nomes (T01) é a base — `quantidade_itens_pedido` no lugar de `qtd_it_ped` resolve mais dúvida do que qualquer comentário conseguiria. Funções (T02) vem logo atrás, porque nome bom não salva uma função de 200 linhas que valida, calcula e persiste ao mesmo tempo; quebrar em funções menores é o que dá a cada pedaço um nome honesto. Comentários (T03) fecha a dupla: quando o nome e a função já dizem *o quê*, o comentário sobra para explicar *o porquê* — a regra de cálculo da comissão que ninguém lembra de cabeça. Formatação (T04) torna tudo isso automático: um formatter no CI encerra a discussão de estilo de uma vez.

**Sinal de que o time dominou:** os comentários de code review deixaram de ser sobre indentação, espaçamento e nome de variável. Se ainda aparecem, ou o formatter não está no CI ou o padrão de nomes nunca foi combinado de fato.

**Gatilho para subir:** o time consegue abrir um PR e discutir o que o código faz, não como ele está escrito.

**O que fica de artefato:** um formatter configurado no CI (Black, Prettier ou php-cs-fixer) e um acordo escrito de idioma e convenção de nomes. São dois objetos concretos, não uma boa intenção — por isso sobrevivem à próxima sprint apertada.

---

### Nível 2 — Revisão e Sustentação

> Tutoriais: **T05 Code Review · T06 Dívida Técnica · T07 Código Legado**

**A capacidade:** manter a qualidade quando o prazo aperta, e mexer no código herdado sem paralisar de medo.

**Como os três tutoriais se encadeiam.** Code review (T05) transforma os quatro hábitos do Nível 1 num portão compartilhado — o checklist mínimo de revisão é literalmente nomes, funções, comentários e formatação. Dívida técnica (T06) reconhece que a revisão barra dívida nova, mas o código já está cheio de dívida antiga; a Regra do Escoteiro (deixar o arquivo um pouco melhor do que encontrou) e o registro da dívida como issue tornam esse passivo visível e redutível. Código legado (T07) chega no caso mais duro: a pior dívida é o módulo legado sem testes. A disciplina aqui é não mexer no que você não consegue caracterizar — e essa é exatamente a ponte para o Nível 4.

**Sinal de que o time dominou:** um PR que falha o checklist volta para ajuste antes do merge, e isso é tratado como rotina, não como ofensa pessoal. Magic numbers ganham nome no caminho (`STATUS_AGUARDANDO_APROVACAO` em vez de `3`).

**Gatilho para subir:** o time parou de dar merge em código que não entende, e toda mudança em legado vem com uma nota do que foi verificado.

**O que fica de artefato:** um checklist de revisão (que nasce dos quatro itens do Nível 1) e um backlog de dívida técnica que de fato é olhado.

**Conexão adiante:** a promessa do T07 — caracterizar antes de mudar — o time ainda não consegue cumprir por inteiro neste nível. A ferramenta para isso, os testes de caracterização, só chega no Nível 4. Vale deixar isso explícito para o time: aqui se estabelece a regra; lá se ganha o instrumento.

---

### Nível 3 — Design que Resiste à Mudança

> Tutoriais: **T08 SOLID · T09 Criação · T10 Estrutural · T11 Anti-patterns · T12 Strategy/Template · T13 Observer/Command · T14 Idioms · T15 Code Review por Padrões**

**A capacidade:** adicionar um comportamento novo deixa de exigir reescrever o antigo. Um novo tipo de pedido entra por uma classe nova, não por mais um `elif` espalhado em cinco arquivos.

**Como os oito tutoriais se encadeiam.** SOLID (T08) é a espinha, com destaque para o SRP (uma classe, um motivo para mudar) e o DIP (inverter dependências para que um teste de unidade não precise de banco e e-mail reais). Os padrões de criação (T09) e estruturais (T10) são o SOLID aplicado de forma concreta: Builder para o construtor de seis parâmetros, Factory para o `if/elif tipo` que cresce a cada variante, Adapter para isolar as User Functions do Protheus de modo que uma atualização do ERP toque uma classe só. Anti-patterns (T11) é o espaço negativo desse desenho — God Object, Magic Strings e Feature Envy são violações de SRP e de nomes que o time agora sabe apontar pelo nome.

No comportamento, Strategy e Template Method (T12) matam o `if/elif algoritmo`, e Observer e Command (T13) desacoplam o "pedido confirmado" que dispara três efeitos colaterais. Idioms (T14) traz os mesmos princípios na gramática de cada linguagem — `@dataclass` e context managers em Python, o equivalente em ADVPL/TLPP onde essas construções não existem. Code review orientado a padrões (T15) é a âncora: o checklist de revisão do Nível 2 ganha uma dimensão de design, e o `gabarito_patterns.md` vira catálogo de consulta em revisões reais.

**Sinal de que o time dominou:** uma variante nova entra por extensão, não por edição do código existente; e o checklist de revisão passa a pegar cheiros de design, não só de estilo.

**Gatilho para subir:** o time refatora para um padrão de propósito e consegue nomear por que aquele padrão, e não outro.

**O que fica de artefato:** um checklist de revisão ampliado (com o catálogo do T15) e um vocabulário comum — dizer "isso virou um God Object" ou "aqui cabe uma Strategy" e todo mundo entender.

**Conexão adiante:** o DIP do T08 é o que torna o código testável sem infraestrutura real. Ele é a pré-condição técnica dos dublês de teste do Nível 4. Sem inverter a dependência aqui, o teste de unidade lá vira um teste de integração disfarçado.

---

### Nível 4 — Rede de Testes

> Tutoriais: **T24 Fundamentos · T25 Dublês · T26 Massa de Dados · T27 Testes em Legado · T28 Integração de API · T29 Integração de Banco · T30 API + Banco · T31 E2E Web · T32 E2E Mobile · T33 Performance**

Este nível não depende de IA em ponto nenhum. A rede de testes é a mesma com ou sem assistente — é ela que dá ao time a liberdade de mudar o código, e é ela que torna o Nível 5 seguro.

**A capacidade:** mudar o código sem medo, porque a máquina avisa quando algo quebrou. O time refatora, o teste roda verde, e ninguém precisa clicar manualmente pela aplicação para conferir.

**Como os dez tutoriais se encadeiam — pela pirâmide de testes.** Na base, os testes de unidade: fundamentos (T24) fixa o padrão preparar–executar–verificar; dublês (T25) só funciona bem porque o DIP do Nível 3 já isolou as dependências; massa de dados (T26) cuida de dados de teste determinísticos; e testes em legado (T27) é onde a promessa do Nível 2 finalmente ganha instrumento — os testes de caracterização, que registram o que o código *faz hoje*, não o que deveria fazer, criando a rede antes de qualquer mudança.

No meio, a integração, rodando em memória (FastAPI `TestClient` e SQLite `:memory:`, sem Docker nem serviço externo): API (T28) verifica status e caminhos de erro; banco (T29) cuida do isolamento entre testes; e API mais banco (T30) fecha o fluxo ponta a ponta em memória. No topo, os testes de ponta a ponta e de carga: Maestro na web (T31) e no mobile (T32), rodando contra apps de demonstração reais; e k6 (T33) para performance, com thresholds sobre o alvo local.

A forma da pirâmide é a estratégia: muitos testes de unidade rápidos na base, menos de integração no meio, um punhado de E2E no topo. Um time que inverte isso — muito E2E lento, pouca unidade — paga em suíte instável e feedback lento.

**Sinal de que o time dominou:** uma refatoração entra verde e ninguém abre a aplicação para conferir na mão. Módulo legado ganha teste de caracterização antes de qualquer alteração.

**Gatilho para subir:** o time confia na suíte o bastante para refatorar de forma agressiva.

**O que fica de artefato:** uma suíte de testes rodando no CI e o hábito de caracterizar o legado antes de tocá-lo.

---

### Nível 5 — Fluxo Assistido por IA

> Tutoriais: **T16 Dirigir e Revisar · T17 Engenharia de Prompt · T18 Spec-first · T19 Multi-arquivo · T20 Revisão Crítica · T21 Refatoração Assistida · T22 Segurança · T23 Testes como Guard-rails**

Este nível vem por último porque consome todos os anteriores. Só dá para revisar a saída da IA contra um padrão se o padrão existe (Níveis 1 a 3), e só dá para confiar numa refatoração feita por IA se a suíte de testes (Nível 4) pega a regressão.

**A capacidade:** acelerar com IA sem baixar a régua. O código gerado passa pelo mesmo portão do código humano.

**Como os oito tutoriais se encadeiam.** Do lado da geração: dirigir e revisar (T16), engenharia de contexto e prompt (T17), spec-first (T18) e geração multi-arquivo com agentes (T19) tratam de dar ao modelo as convenções do repo — as mesmas que o time padronizou nos Níveis 1 a 3, via CLAUDE.md, AGENTS.md ou GEMINI.md — e de revisar em altitude, olhando o diff inteiro, não a função isolada.

Do lado da revisão: revisão crítica (T20), refatoração assistida (T21) e segurança (T22) apontam o code review para um autor novo. São os seis modos de falha, a API alucinada que parece real mas não existe na versão que você usa, o `WHERE` parametrizado e o `ORDER BY` interpolado na mesma função. É o code review do Nível 2 e do T15, agora contra código que ninguém digitou.

O elo final é testes como guard-rails (T23): a rede do Nível 4 é o que permite aceitar uma refatoração assistida. E há uma armadilha específica — a IA tende a escrever testes que confirmam o bug em vez de detectá-lo, porque espelham o que o código faz. É o julgamento formado no Nível 4 que pega isso.

**Sinal de que o time dominou:** PRs gerados por IA passam pelo mesmo checklist e pelo mesmo portão de testes que os PRs humanos, e são recusados pelos mesmos motivos.

**Gatilho para subir:** este é o topo. O desafio deixa de ser subir e passa a ser sustentar.

**O que fica de artefato:** uma política de uso de IA — quando usar, o que sempre dar de contexto, o que sempre revisar — ancorada no checklist e na suíte de testes que o time já tem.

---

### O mapa completo — os 33 tutoriais na escada

Nenhum tutorial fica de fora. A tabela abaixo mostra onde cada um entra e o que ele contribui para o nível.

| Nível | Tutorial | Contribuição |
|---|---|---|
| 1 | T01 Nomes | Nome que dispensa tradução |
| 1 | T02 Funções | Função pequena com nome honesto |
| 1 | T03 Comentários | Comentário que explica o porquê |
| 1 | T04 Formatação | Estilo automático no CI |
| 2 | T05 Code Review | Portão compartilhado de qualidade |
| 2 | T06 Dívida Técnica | Dívida visível e redutível |
| 2 | T07 Código Legado | Regra de não mexer no que não se caracteriza |
| 3 | T08 SOLID | SRP e DIP como espinha do design |
| 3 | T09 Criação | Builder, Factory contra construtores e `if/elif` |
| 3 | T10 Estrutural | Adapter, Facade para isolar o externo |
| 3 | T11 Anti-patterns | Vocabulário para nomear o cheiro |
| 3 | T12 Strategy/Template | Fim do `if/elif algoritmo` |
| 3 | T13 Observer/Command | Efeitos colaterais desacoplados |
| 3 | T14 Idioms | Os princípios na gramática de cada linguagem |
| 3 | T15 Code Review por Padrões | Checklist com dimensão de design |
| 4 | T24 Fundamentos | Padrão preparar–executar–verificar |
| 4 | T25 Dublês | Isolar dependências no teste |
| 4 | T26 Massa de Dados | Dados de teste determinísticos |
| 4 | T27 Testes em Legado | Caracterização como rede de segurança |
| 4 | T28 Integração de API | Status e caminhos de erro |
| 4 | T29 Integração de Banco | Isolamento entre testes |
| 4 | T30 API + Banco | Fluxo ponta a ponta em memória |
| 4 | T31 E2E Web | Fluxo real no navegador |
| 4 | T32 E2E Mobile | Paridade no emulador |
| 4 | T33 Performance | Carga e thresholds |
| 5 | T16 Dirigir e Revisar | O novo fluxo com IA |
| 5 | T17 Engenharia de Prompt | Contexto que define a qualidade |
| 5 | T18 Spec-first | Requisito verificável antes do código |
| 5 | T19 Multi-arquivo | Revisão de diff amplo |
| 5 | T20 Revisão Crítica | Os seis modos de falha |
| 5 | T21 Refatoração Assistida | Equivalência antes de aceitar |
| 5 | T22 Segurança | A vulnerabilidade onde você não olhou |
| 5 | T23 Testes como Guard-rails | A rede que autoriza aceitar a IA |

---

### Como medir o progresso

Cada nível tem um sinal observável. Progresso é passar de um sinal para o próximo, não completar tutoriais.

| Nível | O time chegou quando… |
|---|---|
| 1 | O code review parou de falar de indentação e nome de variável |
| 2 | PR que falha o checklist volta para ajuste, e isso é rotina |
| 3 | Variante nova entra por classe nova, não por `elif` novo |
| 4 | Refatoração entra verde e ninguém confere na mão |
| 5 | PR de IA passa pelo mesmo portão que PR humano |

---

### Erros comuns na adoção do zero

Pular direto para o Nível 5 porque IA é o assunto do momento. Sem a rede de testes do Nível 4, a IA acelera a produção de código que ninguém consegue revisar — o problema fica maior, mais rápido.

Tratar o Nível 1 como óbvio demais para valer esforço. Sem o formatter no CI e o acordo de nomes por escrito, a disciplina evapora na primeira entrega apertada, e o time volta à estaca zero sem perceber.

Adotar padrões (Nível 3) como meta em si. O código enche de Factory e Strategy onde um `if` simples resolvia, e a suposta melhoria de design vira mais uma camada para entender.

---

## Parte 2 — Workbook por tutorial

Responda as perguntas de cada tutorial no seu próprio contexto. Ao final, suas respostas formam o seu guia prático de adoção. Os tutoriais estão em ordem de currículo; a Parte 1 já dá a ordem estratégica de adoção.

### Meu projeto

Qual linguagem principal você usa?
> _:_

Qual o tamanho do seu time?
> _:_

Qual o maior problema de qualidade de código que você enfrenta hoje?
> _:_

Em qual nível da escada (Parte 1) você acha que o time está agora?
> _:_

---

### Tutorial 01 — Nomes Significativos · Nível 1

> Material de referência: [sessao-1/tutorial-01-nomes/README.md](sessao-1/tutorial-01-nomes/README.md)

Usar o mesmo idioma do domínio de negócio facilita a leitura — quem lê o código já conhece os termos. Português é natural quando o negócio opera em português; inglês pode fazer sentido se o time é internacional ou a base já está em inglês. Qual será a sua escolha de idioma para os identificadores?
> _:_

Nomes no plural (`pedidos`, `usuarios`) ou com sufixo (`lista_pedidos`) são convenções comuns para coleções. Qual padrão você vai adotar?
> _:_

Abreviações como `qtd_it_ped` economizam digitação mas custam compreensão. A alternativa — `quantidade_itens_pedido` — é imediata de ler. Como você vai lidar com abreviações obscuras que aparecerem no código?
> _:_

Um critério simples: se você precisa ler o contexto ao redor para entender o que uma variável faz, o nome pode melhorar. Qual será o seu critério para decidir que um nome precisa ser renomeado?
> _:_

Misturar `getUserPedidos()` com `buscar_user_orders()` cria inconsistência que acumula. Algumas equipes fazem migração gradual, outras estabelecem um padrão e aplicam dali em diante. Como você vai tratar nomes que misturam idiomas?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 02 — Funções · Nível 1

> Material de referência: [sessao-1/tutorial-02-funcoes/README.md](sessao-1/tutorial-02-funcoes/README.md)

Não existe número mágico, mas funções que não cabem na tela dificultam a compreensão. Algumas equipes usam 20 linhas como referência, outras preferem "cabe na tela sem rolar". Qual tamanho máximo você vai definir para uma função?
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

### Tutorial 03 — Comentários · Nível 1

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

### Tutorial 04 — Formatação · Nível 1

> Material de referência: [sessao-1/tutorial-04-formatacao/README.md](sessao-1/tutorial-04-formatacao/README.md)

Formatters automáticos eliminam discussões de estilo em PR e garantem consistência sem esforço manual. Para Python há o Black, para JS/TS o Prettier, para PHP o php-cs-fixer. Qual você vai configurar no seu projeto?
> _:_

O formatter pode rodar ao salvar o arquivo, como pre-commit hook, ou no CI. Salvar é imediato mas pode interferir no fluxo; CI é garantido mas o feedback vem mais tarde. Quando faz mais sentido rodar o formatter no seu fluxo de trabalho?
> _:_

A Stepdown Rule sugere colocar funções mais abstratas no topo e funções de detalhe abaixo — o leitor vai do geral para o específico. Outra abordagem é agrupar por domínio ou responsabilidade. Como você vai organizar a ordem das funções nos seus arquivos?
> _:_

Comentários de PR sobre indentação ou espaçamento são ruído que um formatter eliminaria. Se ainda aparecem, é sinal de que o formatter não está configurado ou não está no CI. O que você vai fazer quando esse tipo de comentário aparecer numa revisão?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 05 — Code Review · Nível 2

> Material de referência: [sessao-2/tutorial-05-code-review/README.md](sessao-2/tutorial-05-code-review/README.md)

Sem um checklist, revisões dependem do humor e do tempo do revisor naquele dia. Os quatro tutoriais do Nível 1 já formam um checklist natural: nomes, funções, comentários, formatação. O que você vai incluir no seu checklist mínimo de revisão?
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

### Tutorial 06 — Dívida Técnica · Nível 2

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

### Tutorial 07 — Código Legado · Nível 2

> Material de referência: [sessao-2/tutorial-07-codigo-legado/README.md](sessao-2/tutorial-07-codigo-legado/README.md)

Modificar código legado sem testes é como operar sem rede de segurança — qualquer mudança pode causar um efeito inesperado em outro lugar. Testes de caracterização documentam o comportamento atual antes de qualquer mudança. Qual será a sua regra antes de modificar código sem cobertura de testes?
> _:_

Testes de caracterização não testam o que *deveria* acontecer — testam o que *acontece hoje*, incluindo comportamentos estranhos. O objetivo é criar uma rede de segurança, não validar a lógica. Como você vai escrever esses testes para um módulo que não conhece bem? (A ferramenta para isso está no Tutorial 27, no Nível 4.)
> _:_

Refatorações grandes em código legado têm alta chance de nunca terminar ou de introduzir regressões. Mudanças incrementais — uma função por vez, um conceito por vez — são mais seguras e mais fáceis de revisar. O que você vai fazer quando precisar mexer em um módulo legado grande?
> _:_

O Strangler Fig substitui partes do sistema gradualmente, construindo a nova versão ao lado da antiga. É mais trabalhoso no curto prazo mas reduz o risco de uma mudança grande quebrar tudo. Em que situação você vai propor essa abordagem em vez de refatoração incremental?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 08 — SOLID na Prática · Nível 3

> Material de referência: [sessao-3/tutorial-08-solid/README.md](sessao-3/tutorial-08-solid/README.md)

Uma classe com muitas responsabilidades é difícil de testar e de mudar com segurança. Qual classe no seu sistema atual faz coisas demais? O que você separaria primeiro?
> _:_

Quando o seu código precisa de e-mail real e banco real para rodar um teste de unidade, o DIP está sendo violado. Esse é o mesmo DIP que torna possíveis os dublês do Tutorial 25. Como você vai inverter essa dependência no próximo módulo que escrever?
> _:_

O OCP diz que você deve poder adicionar comportamento sem alterar código existente. Pense em um `if/elif` que cresce toda vez que surge um novo tipo no seu sistema. Como você o tornaria extensível?
> _:_

O LSP é violado quando uma subclasse lança exceção que a base nunca lança, ou ignora um parâmetro obrigatório. Há alguma herança no seu código que quebra silenciosamente o contrato da classe pai?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 09 — Padrões de Criação · Nível 3

> Material de referência: [sessao-3/tutorial-09-criacao/README.md](sessao-3/tutorial-09-criacao/README.md)

Construtores com 6+ parâmetros opcionais são difíceis de ler e de chamar corretamente. Existe algum objeto no seu código que seria melhor construído com um Builder? Quais seriam os campos obrigatórios e quais os opcionais?
> _:_

Factory Method permite adicionar um novo tipo concreto sem alterar a fábrica. Em que parte do seu sistema você tem um `if/elif tipo == "X"` que cresce a cada nova variante?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 10 — Padrões Estruturais · Nível 3

> Material de referência: [sessao-3/tutorial-10-estrutural/README.md](sessao-3/tutorial-10-estrutural/README.md)

Adapter é especialmente valioso em código ADVPL/TLPP: isola as User Functions do Protheus do restante da lógica. Quando o ERP é atualizado, apenas o Adapter muda. Há alguma integração no seu código que chama diretamente funções de terceiros que poderiam mudar?
> _:_

Facade simplifica subsistemas com muitas etapas. Existe algum fluxo no seu código onde o chamador precisa conhecer 5+ subsistemas para realizar uma operação simples?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 11 — Anti-patterns Clássicos · Nível 3

> Material de referência: [sessao-3/tutorial-11-antipatterns/README.md](sessao-3/tutorial-11-antipatterns/README.md)

God Object: uma classe que faz tudo é a forma mais comum de violação de SRP em sistemas legados. Sem olhar o código agora — qual classe do seu sistema você suspeita que tem responsabilidades demais?
> _:_

Magic Strings e Magic Numbers tornam o código frágil: uma string errada em qualquer lugar quebra silenciosamente. Faça uma busca rápida por `== "` no seu código. Quantos desses são strings mágicas sem contexto?
> _:_

Feature Envy: quando um método acessa mais dados de outro objeto do que do próprio, ele está no lugar errado. Você consegue identificar um método assim no seu código atual?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 12 — Strategy e Template Method · Nível 3

> Material de referência: [sessao-4/tutorial-12-strategy-template/README.md](sessao-4/tutorial-12-strategy-template/README.md)

Strategy substitui `if/elif algoritmo == "X"` por polimorfismo. Qual função no seu código muda de comportamento dependendo de um parâmetro de tipo? Ela poderia ser uma Strategy?
> _:_

Template Method é útil quando você tem dois processos com o mesmo esqueleto mas etapas diferentes. Há duas classes no seu código com métodos quase idênticos, diferindo apenas em 1–2 passos?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 13 — Observer e Command · Nível 3

> Material de referência: [sessao-4/tutorial-13-observer-command/README.md](sessao-4/tutorial-13-observer-command/README.md)

Observer desacopla eventos de seus consumidores. Existe algum ponto no seu código onde uma ação (confirmar pedido, por exemplo) dispara 3+ efeitos colaterais diretamente? Adicionar um novo efeito exige alterar o código original?
> _:_

Command encapsula uma operação e seu estado anterior, permitindo desfazer. Existe alguma operação crítica no seu sistema que hoje não pode ser revertida? O que seria necessário para implementar um undo?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 14 — Idiom Patterns por Linguagem · Nível 3

> Material de referência: [sessao-4/tutorial-14-idioms/README.md](sessao-4/tutorial-14-idioms/README.md)

`@dataclass` com `__post_init__` elimina `__init__` manual e centraliza validação. Quais classes no seu código Python têm `__init__` com mais de 4 linhas que poderiam usar `@dataclass`?
> _:_

Context managers garantem cleanup mesmo quando há exceções — sem depender de `finally` espalhados. Há algum recurso (arquivo, conexão, lock) no seu código que é fechado manualmente em vários lugares?
> _:_

Em ADVPL/TLPP, `@dataclass` e `with` não existem. Como você vai aplicar os princípios equivalentes (validação centralizada, cleanup garantido) com as ferramentas disponíveis?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 15 — Code Review Orientado a Padrões (Âncora) · Nível 3

> Material de referência: [sessao-4/tutorial-15-code-review-padroes/README.md](sessao-4/tutorial-15-code-review-padroes/README.md)

Antes de ver o gabarito, liste os problemas que você encontrou em `codigo_para_revisar.py`. Quantas violações você identificou? Quais ficaram invisíveis na primeira leitura?
> _:_

O `gabarito_patterns.md` é um catálogo de referência para usar em code reviews reais. Quais padrões da tabela você vai adotar como critério de revisão na sua equipe a partir de agora?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 24 — Fundamentos de Testes · Nível 4

> Material de referência: [sessao-7/tutorial-24-fundamentos-testes/README.md](sessao-7/tutorial-24-fundamentos-testes/README.md)

Um teste legível segue três blocos claros: preparar o cenário, executar a ação, verificar o resultado. Como você vai estruturar os testes da sua equipe para que qualquer pessoa entenda o que está sendo verificado?
> _:_

Cobertura alta não garante qualidade — dá para cobrir 100% das linhas sem testar nenhum caso de erro. Qual vai ser o seu critério para dizer que uma função está bem testada, além do percentual de cobertura?
> _:_

Escrever o teste antes ou depois da implementação muda o desenho do código. Em que situações a sua equipe vai escrever o teste primeiro?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 25 — Dublês de Teste · Nível 4

> Material de referência: [sessao-7/tutorial-25-dubles-teste/README.md](sessao-7/tutorial-25-dubles-teste/README.md)

Dublês só funcionam bem quando a dependência já está isolada — é o DIP do Tutorial 08 pagando dividendo aqui. Qual dependência do seu código (banco, e-mail, API externa) você vai isolar primeiro para poder testar sem ela?
> _:_

Stub devolve um valor pronto; mock verifica que uma chamada aconteceu; fake é uma implementação simplificada de verdade. Como você vai decidir qual dublê usar em cada caso?
> _:_

Excesso de mocks amarra o teste à implementação — qualquer refatoração quebra o teste mesmo sem mudar o comportamento. Qual será o seu limite para não mockar demais?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 26 — Massa de Dados · Nível 4

> Material de referência: [sessao-7/tutorial-26-massa-dados/README.md](sessao-7/tutorial-26-massa-dados/README.md)

Dados de teste espalhados e repetidos tornam a suíte frágil e difícil de manter. Como você vai centralizar a criação de dados de teste (fixtures, factories) na sua equipe?
> _:_

Dados aleatórios podem esconder um bug que só aparece com um valor específico, e um teste que falha uma vez a cada dez execuções destrói a confiança na suíte. Como você vai garantir que os testes sejam determinísticos?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 27 — Testes em Código Legado · Nível 4

> Material de referência: [sessao-7/tutorial-27-testes-legado/README.md](sessao-7/tutorial-27-testes-legado/README.md)

Este tutorial entrega a ferramenta que o Tutorial 07 prometeu: o teste de caracterização, que registra o comportamento atual do código antes de qualquer mudança. Qual módulo legado do seu sistema você vai caracterizar primeiro?
> _:_

Código legado costuma não ter pontos de teste — não dá para injetar um dublê onde tudo está acoplado. Onde você vai abrir o primeiro "seam" (ponto de costura) para tornar o módulo testável?
> _:_

O teste de caracterização captura inclusive os comportamentos estranhos, porque o objetivo é a rede de segurança, não a correção. Como você vai comunicar ao time que um comportamento capturado não é necessariamente o comportamento desejado?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 28 — Integração de API · Nível 4

> Material de referência: [sessao-8/tutorial-28-integracao-api/README.md](sessao-8/tutorial-28-integracao-api/README.md)

Testes de integração de API rodam a aplicação em memória (FastAPI `TestClient`), sem subir servidor nem Docker. Como você vai montar esse tipo de teste no stack da sua equipe?
> _:_

O caminho feliz é o mais fácil e o menos revelador — os bugs moram nos status de erro (400, 404, 422). Quais caminhos de erro da sua API você sempre vai cobrir?
> _:_

Validação de entrada rejeitada com a mensagem certa é parte do contrato da API. Como você vai testar que a validação bloqueia o input inválido e responde com clareza?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 29 — Integração de Banco · Nível 4

> Material de referência: [sessao-8/tutorial-29-integracao-banco/README.md](sessao-8/tutorial-29-integracao-banco/README.md)

Testes de banco rodam em SQLite `:memory:`, isolados e rápidos, sem serviço externo. Como você vai garantir que cada teste começa com um banco limpo e não vaza estado para o próximo?
> _:_

Um teste que depende da ordem de execução de outro é uma bomba-relógio. Como você vai garantir o isolamento entre os testes que tocam o banco?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 30 — Integração de API + Banco · Nível 4

> Material de referência: [sessao-8/tutorial-30-integracao-api-banco/README.md](sessao-8/tutorial-30-integracao-api-banco/README.md)

Este teste exercita o fluxo completo — requisição, regra de negócio, persistência — ainda em memória. Qual fluxo ponta a ponta da sua aplicação vale mais a pena cobrir desse jeito?
> _:_

Quanto mais amplo o teste, mais lento e mais difícil de diagnosticar quando falha. Como você vai equilibrar cobertura ampla com feedback rápido nesse nível?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 31 — E2E Web com Maestro · Nível 4

> Material de referência: [sessao-9/tutorial-31-e2e-web-maestro/README.md](sessao-9/tutorial-31-e2e-web-maestro/README.md)

Testes de ponta a ponta são os mais caros e os mais lentos — o topo da pirâmide. Quais fluxos são críticos o bastante para justificar um teste E2E na sua aplicação?
> _:_

Um fluxo E2E que depende de seletores frágeis quebra a cada mudança de layout. Como você vai escrever fluxos Maestro que resistam a pequenas mudanças na interface?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 32 — E2E Mobile com Maestro · Nível 4

> Material de referência: [sessao-9/tutorial-32-e2e-mobile-maestro/README.md](sessao-9/tutorial-32-e2e-mobile-maestro/README.md)

O E2E mobile roda contra um emulador com o app instalado, o que exige mais infraestrutura que o E2E web. Como a sua equipe vai integrar esse tipo de teste no CI, dado o custo do emulador?
> _:_

Muitos fluxos são iguais no web e no mobile. O que você vai reaproveitar entre os dois e o que precisa ser específico da plataforma?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 33 — Performance com k6 · Nível 4

> Material de referência: [sessao-9/tutorial-33-performance-k6/README.md](sessao-9/tutorial-33-performance-k6/README.md)

Teste de performance sem um threshold definido é só um gráfico bonito. Quais limites (latência p95, taxa de erro) a sua aplicação precisa respeitar sob carga?
> _:_

Medir performance no ambiente errado engana — o alvo local não reflete produção. Onde e como a sua equipe vai rodar os testes de carga para que o número signifique algo?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 16 — O novo fluxo: dirigir e revisar · Nível 5

> Material de referência: [sessao-5/tutorial-16-novo-fluxo-ia/README.md](sessao-5/tutorial-16-novo-fluxo-ia/README.md)

O modelo não conhece seu projeto por padrão — sem contexto explícito, ele produz código genérico que não segue os padrões do repo. Quais convenções do seu repo você sempre vai dar ao modelo (via CLAUDE.md, AGENTS.md ou GEMINI.md)?
> _:_

A revisão em altitude significa olhar para além da função isolada — o nome, o estilo, a integração com o restante do módulo. Como você vai revisar a saída do modelo contra o padrão do projeto, não só contra "funciona"?
> _:_

A política de uso de IA define expectativas para o time inteiro: quando usar, o que sempre dar de contexto, o que sempre revisar. Qual será a política de uso de IA da sua equipe?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 17 — Engenharia de contexto e prompt para gerar código · Nível 5

> Material de referência: [sessao-5/tutorial-17-engenharia-de-prompt/README.md](sessao-5/tutorial-17-engenharia-de-prompt/README.md)

Um bom prompt inclui mais do que o pedido — contexto, domínio, exemplos, assinatura-alvo e restrições determinam a qualidade do ponto de partida. Quais elementos você vai incluir no template de prompt da sua equipe?
> _:_

Iterar o prompt é mais eficiente do que corrigir o código — uma mudança no prompt pode resolver vários problemas de uma vez, enquanto corrigir a saída acumula patches. Quando vale refinar o prompt em vez de aceitar e ajustar a saída?
> _:_

Mesmo um prompt excelente não elimina a revisão — o modelo pode gerar algo funcionalmente plausível mas semanticamente errado para o seu domínio. O que você sempre vai verificar antes de aceitar um resultado de geração de código?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 18 — Spec-first: do requisito ao código verificável · Nível 5

> Material de referência: [sessao-5/tutorial-18-spec-first/README.md](sessao-5/tutorial-18-spec-first/README.md)

Exigências implícitas não entram no código sozinhas — o modelo gera o que o prompt descreve, não o que a equipe pressupõe. Qual o seu processo para transformar um requisito em spec antes de pedir o código ao modelo?
> _:_

A spec é mais barata de corrigir do que o código — ajustar uma linha de especificação custa segundos; reescrever a função gerada custa minutos e revisão. Como você vai fixar e comunicar as exigências implícitas antes de gerar?
> _:_

Testes como contrato no pedido ajudam o modelo a gerar o comportamento certo — exemplos concretos de entrada e saída eliminam ambiguidade que palavras deixam em aberto. Como você vai usar exemplos de entrada/saída como contrato no prompt?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 19 — Geração multi-arquivo com agentes · Nível 5

> Material de referência: [sessao-5/tutorial-19-multiarquivo-agentes/README.md](sessao-5/tutorial-19-multiarquivo-agentes/README.md)

Um agente que edita vários arquivos de uma vez é poderoso e perigoso — o risco não está só no arquivo editado, mas no efeito sobre os arquivos que ele toca indiretamente. Como você vai revisar um diff multi-arquivo — o que procura além do arquivo editado?
> _:_

Inconsistências cross-file só aparecem na revisão em altitude — nomes duplicados, importações fantasma, estilos divergentes no mesmo módulo escapam quando você olha arquivo por arquivo. Qual será o seu checklist de revisão de diff multi-arquivo?
> _:_

Às vezes é melhor parar e re-dirigir do que aceitar — um agente que derivou do objetivo original custa mais para corrigir do que reiniciar com um prompt melhor. Quando você vai interromper o agente e reformular o pedido?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 20 — Revisão crítica de código gerado por IA · Nível 5

> Material de referência: [sessao-6/tutorial-20-revisao-critica-ia/README.md](sessao-6/tutorial-20-revisao-critica-ia/README.md)

O perigo não é o código feio, é o código confiante com um defeito sutil — compila, o caminho feliz passa, mas um caso de borda silencioso está errado. Qual será o seu checklist mínimo de revisão de código de IA (os seis modos de falha)?
> _:_

Uma API alucinada parece real — o nome é coerente com o padrão da biblioteca, a assinatura faz sentido, mas o método simplesmente não existe na versão que você usa. Como você vai confirmar que um método ou endpoint sugerido pelo modelo realmente existe na versão da lib que você usa?
> _:_

Um comentário que mente é pior do que nenhum — o leitor confia na docstring e raciocina sobre um comportamento que o código não implementa. Como você vai tratar a "confiança enganosa" (docstring que afirma algo que o código não faz)?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 21 — Refatoração assistida avançada · Nível 5

> Material de referência: [sessao-6/tutorial-21-refatoracao-avancada/README.md](sessao-6/tutorial-21-refatoracao-avancada/README.md)

Uma refatoração que parece equivalente pode deslocar um limite de faixa — a lógica principal funciona, mas um caso de borda de fronteira mudou silenciosamente. Como você vai verificar que a refatoração assistida preservou o comportamento, inclusive nas bordas?
> _:_

Verificação de equivalência é mais eficaz que revisão visual — pedir à IA para construir um harness de teste antes da refatoração detecta diferenças que o olho não pega. Como você vai construir (ou pedir à IA) uma verificação de equivalência antes de aceitar a refatoração?
> _:_

Refatorações em passos são mais seguras — cada passo é pequeno o suficiente para ser entendido e revertido se necessário. Qual o tamanho máximo de mudança assistida que você aceita revisar de uma vez?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 22 — Segurança em código gerado · Nível 5

> Material de referência: [sessao-6/tutorial-22-seguranca-ia/README.md](sessao-6/tutorial-22-seguranca-ia/README.md)

O `WHERE` pode estar parametrizado e o `ORDER BY` interpolado na mesma função — a vulnerabilidade fica exatamente onde você não olhou porque o resto parecia correto. Qual será o seu checklist de segurança para código de IA, além do óbvio?
> _:_

Uma regex de validação pode aceitar exatamente o que deveria barrar — a expressão parece restritiva, mas um caso de borda específico passa. Como você vai testar que a validação realmente bloqueia o input malicioso?
> _:_

"Parece seguro" é o estado mais perigoso — a confiança gerada pela aparência de correção reduz o escrutínio exatamente onde ele é mais necessário. O que você sempre vai questionar antes de aceitar uma função de validação ou acesso a dados gerada por IA?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

### Tutorial 23 — Testes como guard-rails e manutenibilidade · Nível 5

> Material de referência: [sessao-6/tutorial-23-testes-manutenibilidade/README.md](sessao-6/tutorial-23-testes-manutenibilidade/README.md)

Caracterizar antes é mais barato que regredir depois — uma rede de testes de caracterização custa horas; uma regressão descoberta em produção custa dias. O que você vai fazer antes de deixar o agente mexer em código sem testes?
> _:_

A IA pode escrever testes que confirmam o bug em vez de detectá-lo — se o modelo gera a implementação e os testes, os testes tendem a espelhar o que o código faz, não o que deveria fazer. Como você vai garantir que os testes da IA cobrem as bordas e não só o caminho feliz?
> _:_

O diff é a fonte da verdade, não a saída isolada — revisar só o arquivo novo deixa escapar o que foi removido, deslocado ou quebrado nos outros arquivos. Qual será o seu ritual de revisão de diff após uma mudança assistida?
> _:_

**Minha decisão para este tutorial:**
> _:_

---

## Meu plano de adoção

Preencha a decisão principal de cada tutorial. A coluna do nível liga cada decisão à escada da Parte 1.

### Nível 1 — Código Legível

| Tutorial | Minha decisão principal |
|---|---|
| 01 — Nomes | |
| 02 — Funções | |
| 03 — Comentários | |
| 04 — Formatação | |

### Nível 2 — Revisão e Sustentação

| Tutorial | Minha decisão principal |
|---|---|
| 05 — Code Review | |
| 06 — Dívida Técnica | |
| 07 — Código Legado | |

### Nível 3 — Design que Resiste à Mudança

| Tutorial | Minha decisão principal |
|---|---|
| 08 — SOLID | |
| 09 — Padrões de Criação | |
| 10 — Padrões Estruturais | |
| 11 — Anti-patterns | |
| 12 — Strategy e Template Method | |
| 13 — Observer e Command | |
| 14 — Idiom Patterns | |
| 15 — Code Review por Padrões | |

### Nível 4 — Rede de Testes

| Tutorial | Minha decisão principal |
|---|---|
| 24 — Fundamentos de Testes | |
| 25 — Dublês | |
| 26 — Massa de Dados | |
| 27 — Testes em Legado | |
| 28 — Integração de API | |
| 29 — Integração de Banco | |
| 30 — API + Banco | |
| 31 — E2E Web | |
| 32 — E2E Mobile | |
| 33 — Performance | |

### Nível 5 — Fluxo Assistido por IA

| Tutorial | Minha decisão principal |
|---|---|
| 16 — Dirigir e revisar | |
| 17 — Engenharia de prompt | |
| 18 — Spec-first | |
| 19 — Multi-arquivo com agentes | |
| 20 — Revisão crítica de código de IA | |
| 21 — Refatoração assistida | |
| 22 — Segurança em código gerado | |
| 23 — Testes como guard-rails | |
