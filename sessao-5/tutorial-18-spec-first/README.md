# Tutorial 18 — Spec-first: do requisito ao código verificável

> Referência: spec-first / plan-first na geração de código com modelos de fronteira

---

## 1. Contexto e Motivação

Em 2026, modelos de fronteira geram código idiomático, tipado e bem estruturado a
partir de um parágrafo em linguagem natural. O problema não está na qualidade técnica
do código — está na completude da especificação que o orienta.

Um requisito informal tem lacunas. Quem desenvolve a regra de negócio preenche essas
lacunas mentalmente, sem perceber. O modelo de IA preenche as mesmas lacunas com a
inferência estatisticamente mais provável — que pode ser diferente da intenção real.

> *"What is the programmer's role? We must extract the requirements from the
> chaos of the software factory."*
> — Robert C. Martin, *Clean Code*, Cap. 1

O resultado é código que passa nos casos do caminho principal mas silenciosamente
ignora um requisito implícito — algo que "todo mundo sabia" mas ninguém escreveu.
Em código gerado manualmente, esse gap aparece na revisão porque o desenvolvedor
que conhece o domínio reconhece a ausência. Em código gerado por IA em alta
velocidade, o gap passa desapercebido porque o código *parece* correto.

**A solução não é revisar mais código — é escrever a spec antes de gerá-lo.**

Revisar a spec custa menos do que revisar o código: é mais curta, mais legível e
não requer contexto de implementação para detectar o que falta. Se a spec estiver
errada, você corrige uma linha de texto — não uma função já integrada.

---

## 2. Conceito Central

### Spec-first: as quatro fases do SDD

O GitHub Spec Kit — toolkit de referência para SDD com agentes de IA — estrutura o
fluxo em **quatro fases distintas**. A revisão acontece nas três primeiras, não na última:

```
1. Specify   →  spec de comportamento: user stories, requisitos, critérios de aceitação
2. Plan      →  plano técnico: arquitetura, modelos de dados, contratos de API (OpenAPI)
3. Tasks     →  breakdown em tarefas ordenadas por dependência, testáveis isoladamente
4. Implement →  agente executa tarefas em ordem, test-first, com verificação por fase
```

| Fase | Artefato produzido | Quem revisa |
|---|---|---|
| **Specify** | Feature spec (o quê e por quê — sem prescrever implementação) | Negócio + tech |
| **Plan** | Plano técnico + contratos de API (OpenAPI) + modelos de dados | Tech lead |
| **Tasks** | Lista de tarefas ordenadas, cada uma com critério de "done" | Dev / agente |
| **Implement** | Código gerado + testes (test-first) + verificação automatizada | Agente + dev |

Antes das quatro fases, o Spec Kit define uma **Constitution** — documento de princípios
arquiteturais imutáveis que governa todas as specs do projeto (convenções, restrições de
stack, padrões de segurança). Quando requisitos mudam, a spec é atualizada primeiro;
o código se regenera a partir dela (*Specification Evolution*).

A spec não é burocracia — é o contrato entre a intenção humana e o modelo. Ela transforma
um parágrafo ambíguo em uma fonte de verdade inequívoca que atravessa todas as quatro fases.

---

### Por que a exigência implícita é perdida

Todo requisito informal tem exigências que "vão sem dizer":

- Um sistema de agendamento *obviamente* não deve aceitar dois eventos simultâneos
  no mesmo recurso — mas "óbvio" para o desenvolvedor não é explícito para o modelo.
- O modelo vê a parte escrita: "crie uma reserva com sala, horário início e fim".
  Ele gera um sistema que cria reservas. Isso é o que foi pedido.

O fragmento abaixo ilustra o gap:

**Prompt sem spec firme:**

```
Crie um sistema de reservas de sala. Cada reserva tem sala, data, horário de
início e fim, e nome do responsável. Implemente as operações de criar e listar.
```

**Saída típica (polida, mas incompleta):**

```python
def criar_reserva(sala, inicio, fim, responsavel):
    reserva = Reserva(sala=sala, inicio=inicio, fim=fim, responsavel=responsavel)
    repositorio.append(reserva)   # ← aceita qualquer reserva, inclusive sobrepostas
    return reserva
```

O código é limpo. Cria a reserva. Nunca verifica sobreposição — porque o prompt
nunca exigiu isso explicitamente.

**Com spec estruturada (exigência implícita fixada):**

```
REGRA: Não permitir reserva sobreposta no mesmo recurso.
  Se sala X está reservada das 14h às 16h, uma nova reserva para sala X das 15h
  às 17h deve ser rejeitada com ReservaSobrepostaError.
CONTRATO: criar_reserva("Sala A", 14h, 16h, "Ana") → OK
           criar_reserva("Sala A", 15h, 17h, "Bob") → ReservaSobrepostaError
```

**Saída resultante (polida e correta):**

```python
def criar_reserva(sala, inicio, fim, responsavel):
    for reserva in repositorio:
        if reserva.sala == sala and reservas_sobrepostas(reserva, inicio, fim):
            raise ReservaSobrepostaError(sala, inicio, fim)
    ...   # ← rejeita a sobreposição antes de aceitar
```

---

### Testes como contrato no pedido

A técnica mais eficaz para fixar exigências implícitas é incluir **exemplos de
entrada→saída esperada** diretamente na spec/prompt. Esses exemplos funcionam
como testes antes do código existir — são o contrato verificável que ancora
o comportamento esperado.

No Spec Kit, esses exemplos evoluem para **testes reais gerados antes do código de
produção** dentro da fase Implement (test-first): o agente escreve o teste, confirma
que ele falha, implementa a lógica mínima, e verifica que passa — na ordem TDD clássica,
mas conduzida pelo agente a partir dos critérios de aceitação da spec.

```
EXEMPLOS (contrato):
  criar_reserva("Sala A", "10:00", "11:00", "Ana")  → reserva criada, id=1
  criar_reserva("Sala A", "10:30", "12:00", "Bob")  → ReservaSobrepostaError  ← sobrepõe
  criar_reserva("Sala A", "11:00", "12:00", "Bob")  → reserva criada, id=2    ← adjacente é OK
  criar_reserva("Sala B", "10:30", "12:00", "Bob")  → reserva criada, id=3    ← sala diferente OK
```

Esses casos de fronteira (sobreposição parcial, adjacência, sala diferente) forçam
o modelo a implementar a lógica de detecção corretamente — porque os exemplos
já especificam o comportamento esperado para cada cenário.

---

### Revisar a spec é mais barato que revisar o código

| Etapa de revisão | O que você revisa | Custo de correção |
|---|---|---|
| Na spec (antes do código) | Texto estruturado, 20–30 linhas | Editar uma linha de texto |
| No código gerado | Código completo, lógica e integração | Refatorar função + testes |
| Em produção | Comportamento, dados corrompidos | Hotfix + comunicação |

A spec não é burocracia — é o ponto mais barato para detectar o requisito que falta.

---

### Abordagens mais robustas de SDD

O que praticamos aqui — spec em linguagem estruturada com exemplos de contrato — é o
ponto de entrada do espectro SDD. Equipes que precisam de maior rigor dispõem de
abordagens progressivamente mais formais:

| Abordagem | Mecanismo | Quando usar |
|---|---|---|
| **Spec estruturada + exemplos** *(este tutorial)* | Texto + tabelas de entrada→saída | Geração de código com IA; alinhamento rápido de equipe |
| **BDD — Behavior-Driven Development** | Cenários Gherkin (`Given / When / Then`) executados por Cucumber ou pytest-bdd | Quando spec precisa ser inteligível por negócio e executável como teste |
| **Property-based testing** | Invariantes e propriedades verificadas contra entradas aleatórias (Hypothesis/Python, fast-check/TS) | Quando o espaço de entrada é amplo e exemplos manuais cobrem só o caminho feliz |
| **Design by Contract (DbC)** | Pré-condições, pós-condições e invariantes declarados no código (`icontract`, `deal` em Python; Eiffel, Kotlin Contracts) | Quando a API pública tem restrições críticas que devem ser verificadas em runtime |
| **Schema-first / Contract-first** | OpenAPI / JSON Schema geram stubs de servidor e cliente antes de qualquer implementação — **artefato central da fase Plan no Spec Kit**, não apenas uma abordagem alternativa | Serviços HTTP e mensageria; contratos entre equipes autônomas |
| **Verificação formal** | Modelagem matemática com TLA+, Alloy ou Coq — provas de propriedades | Protocolos distribuídos, algoritmos de consenso, sistemas de segurança crítica |

**Qual escolher?** A regra prática é usar o nível mais leve que ainda detecta o
problema relevante. Para a maioria dos fluxos de domínio, spec estruturada + BDD
eliminam 80% dos gaps sem a curva de adoção das ferramentas formais. Property-based
testing vale quando o domínio tem lógica de validação complexa com muitas fronteiras.
DbC e verificação formal aparecem quando o custo de falha é alto o suficiente para
justificar a formalidade.

O ponto comum a todas as abordagens: **a spec existe antes do código e é a fonte de
verdade que orienta, verifica e documenta o comportamento esperado**.

---

## 3. Exercício

**Contexto:** o arquivo `exercicios/exercicio.py` (e `.ts`) contém um módulo de
cancelamento de reserva gerado por um modelo de fronteira — limpo e tipado, com
tratamento de erro correto. Mas foi gerado sem a especificação de uma exigência
implícita: **o cancelamento só é permitido com antecedência mínima de 2 horas**.
O código aceita cancelamentos a qualquer momento, inclusive nos últimos minutos
antes do horário — o que violaria a política da empresa.

**Tarefas:**

1. Execute o exercício e observe o resultado:
   ```bash
   python3 sessao-5/tutorial-18-spec-first/exercicios/exercicio.py
   ```

2. Identifique qual caso demonstra a exigência implícita que falta (dica: tente
   cancelar 30 minutos antes do início).

3. Escreva a spec que fixa a exigência, incluindo exemplos de contrato
   (entrada→saída esperada para os casos-limite).

4. Corrija o código (ou use a spec revisada em um modelo) e compare com `gabarito.py`.

**Referência:** `exercicios/gabarito_revisao.md` contém a exigência implícita
identificada, a spec com os exemplos de contrato, e o roteiro para os três modelos.

---

## 4. Checklist — As quatro fases antes de gerar código

### Fase 1 — Specify
- [ ] Escrevi a **spec de comportamento** — o quê e por quê, sem prescrever implementação?
- [ ] **Fixei as exigências implícitas** — o que "vai sem dizer" para mim mas não aparece no texto?
- [ ] Incluí **critérios de aceitação** com exemplos de contrato (entrada→saída) para os casos de fronteira?
- [ ] A spec foi **revisada por negócio e tech** antes de avançar?

### Fase 2 — Plan
- [ ] Existe um **plano técnico** separado da spec de comportamento — arquitetura, modelos, API?
- [ ] Os **contratos de API** (OpenAPI ou equivalente) estão definidos antes de gerar código?
- [ ] Restrições de stack, segurança e padrões do projeto (Constitution) estão refletidos no plano?

### Fase 3 — Tasks
- [ ] O plano foi quebrado em **tarefas ordenadas por dependência**, cada uma com critério de "done"?
- [ ] Cada tarefa é **testável isoladamente** — pequena o suficiente para verificação focada?

### Fase 4 — Implement
- [ ] O agente escreveu **testes antes do código de produção** (test-first)?
- [ ] Posso executar o resultado e ver o comportamento esperado nos exemplos do contrato?
- [ ] Se o requisito mudou: **atualizei a spec primeiro** e deixei o código se regenerar a partir dela?

---

## 5. Referências

- Martin, Robert C. *Clean Code: A Handbook of Agile Software Craftsmanship*. Cap. 1–2.
- Feathers, Michael. *Working Effectively with Legacy Code*. Cap. 2 — Working with Feedback.
- **GitHub Spec Kit** (toolkit de referência para SDD): [github/spec-kit](https://github.com/github/spec-kit)
- GitHub Blog — lançamento do Spec Kit: [Spec-driven development with AI](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- GitHub Copilot Academy — workshop SDD: [Spec-Driven Development](https://copilot-academy.github.io/workshops/immersive-experience/spec_driven_development)
- Microsoft Learn — Implementar SDD com Spec Kit: [Módulo de treinamento](https://learn.microsoft.com/en-us/training/modules/spec-driven-development-github-spec-kit-enterprise-developers/)
- Documentação Claude Code: [Claude Code e CLAUDE.md](https://docs.anthropic.com/claude-code)
- OpenAI Codex: [AGENTS.md e system instructions](https://platform.openai.com/docs/agents)
- Gemini CLI: [GEMINI.md e system instructions](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- Exemplos do repositório:
  - `sessao-5/tutorial-17-engenharia-de-prompt/exemplos/prompt.md`
  - `sessao-5/tutorial-18-spec-first/exemplos/spec.md`
  - `sessao-5/tutorial-18-spec-first/exemplos/reserva_revisado.py`
