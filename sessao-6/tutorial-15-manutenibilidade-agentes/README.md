# Tutorial 15 — Manutenibilidade e Trabalho com Agentes ao Longo do Tempo

> Referência: *Clean Code*, Cap. 1 e 17; Regra do Escoteiro (Sessão 2)

---

## 1. Contexto e Motivação

Uma feature adicionada por IA em uma tarde pode ser limpa e funcional. Dez features adicionadas ao longo de dois meses, cada uma por um prompt diferente, sem contexto do que já existia — esse é o cenário que cria entropia silenciosa.

Cada contribuição de IA, isolada, parece plausível: o código compila, os testes passam, o comportamento está correto. O problema aparece quando você olha para a base inteira: duas funções que fazem quase a mesma coisa com nomes em estilos diferentes, uma dependência que foi puxada porque a IA não sabia que a stdlib resolvia o problema, formatação que diverge bloco a bloco.

Isso é **deriva de consistência** — e ela corrói a manutenibilidade mesmo sem introduzir bugs.

**Manutenibilidade sustenta a velocidade ao longo do tempo.** Uma base consistente permite que qualquer membro da equipe (ou qualquer agente de IA futuro) entenda, altere e estenda o código com previsibilidade. Uma base com deriva alta aumenta o custo cognitivo de cada mudança — e esse custo se acumula.

---

## 2. Conceito Central

### Consistência com padrões existentes

A IA não conhece as suas convenções a menos que você as forneça. Se o seu módulo usa `calcular_total_pedido`, e você pede uma nova função sem dar esse contexto, a IA pode gerar `calcTotal` — e agora você tem dois estilos convivendo no mesmo arquivo.

A solução é dar contexto de padrão no prompt:

```
# Prompt sem contexto → gera deriva
"adiciona uma função que aplica desconto de fidelidade"

# Prompt com contexto → respeita o padrão
"no módulo relatorio_vendas.py, que usa snake_case em português,
adiciona uma função calcular_desconto_fidelidade(pontos) seguindo
o mesmo estilo das funções existentes. Sem novas dependências."
```

### Revisar o diff, não só a saída isolada

Quando você pede à IA uma nova função e ela gera 30 linhas limpas, a tentação é olhar apenas para as 30 linhas novas. Mas um agente que edita vários arquivos de uma vez pode ter introduzido duplicação, removido uma importação necessária em outro lugar, ou reforçado um estilo divergente.

**Revisão do diff inteiro é inegociável quando a IA edita múltiplos arquivos.** O diff revela o que mudou em relação ao que existia — a saída isolada revela apenas o que foi adicionado.

```
# Antes de aceitar qualquer mudança de agente:
git diff        # o que mudou exatamente?
git diff --stat # quantos arquivos foram tocados?
```

### Documentar o porquê

A IA comenta o *quê* — não o *porquê*. Se uma função tem uma restrição de negócio não óbvia (ex.: desconto não se aplica a pedidos com mais de 90 dias), esse conhecimento precisa estar no código como comentário de intenção — ou a próxima rodada de IA vai "corrigir" o comportamento achando que é um bug.

```python
# Regra de negócio: pedidos com mais de PRAZO_MAX_DIAS_DESCONTO dias
# não são elegíveis para desconto, independente dos pontos acumulados.
# Histórico: decisão do time comercial em jan/2026.
if dias_desde_pedido > PRAZO_MAX_DIAS_DESCONTO:
    return 0.0
```

### Evitar inchaço de dependências

A IA frequentemente resolve um problema puxando uma biblioteca quando a stdlib seria suficiente. Uma dependência desnecessária é:
- Um vetor de vulnerabilidade de segurança.
- Um item a mais no `requirements.txt` que futuros mantenedores precisam entender.
- Um sinal de que o contexto não foi dado adequadamente.

Antes de aceitar uma nova dependência sugerida pela IA, pergunte: **a stdlib (ou o código que já existe no módulo) resolve isso?**

### Regra do Escoteiro com IA

A Regra do Escoteiro — *deixe o código mais limpo do que você o encontrou* — se aplica ao trabalho com agentes: cada sessão de IA é uma oportunidade não só de adicionar a feature pedida, mas de consolidar uma duplicação que a IA anterior criou, ou de uniformizar um nome que ficou inconsistente.

Sem essa disciplina ativa, cada contribuição de IA deixa a base ligeiramente pior — individualmente tolerável, cumulativamente problemático.

### Trabalho com agentes de múltiplos arquivos

Quando a IA edita múltiplos arquivos de uma vez (como agentes autônomos fazem), revisar o diff e ter guard-rails (testes) passa a ser inegociável. Um agente pode:

- Introduzir uma função duplicada em um arquivo diferente do que você estava revisando.
- Alterar uma constante compartilhada sem perceber que ela é usada em outros contextos.
- Remover código que parecia "morto" mas era necessário em um caminho menos comum.

A convenção de testes do Tutorial 14 (funções `verificar_*` que imprimem `OK` ou `FALHOU`) é o seu detector de regressão para essas situações.

### Fragmento: antes e depois da consolidação

**Antes — dois caminhos para o mesmo cálculo:**

```python
def calcTotal(vendas):                          # nome em inglês; camelCase
    return sum(v["valor"] for v in vendas)

def calcular_total_geral(lista_vendas):          # nome em português; snake_case
    total = 0
    for venda in lista_vendas:
        total += venda["valor"]
    return total
```

**Depois — uma função, um estilo:**

```python
def calcular_total_vendas(vendas: list[dict]) -> float:
    """Retorna a soma dos valores de todas as vendas da lista."""
    return sum(v["valor"] for v in vendas)
```

---

## 3. Exercício

O exercício está em `exercicios/` e tem duas partes:

**Parte estática** (`exercicio.py` / `exercicio.ts`): módulo de dashboard que acumulou sinais de deriva por contribuições de IA. Sua tarefa:

1. Identifique os sinais de deriva (duplicação, estilos divergentes, dependência supérflua).
2. Consolide o módulo mantendo o comportamento observável.
3. Liste o que foi unificado.

```bash
# Veja o módulo com deriva:
python3 sessao-6/tutorial-15-manutenibilidade-agentes/exercicios/exercicio.py

# Compare com a versão consolidada:
python3 sessao-6/tutorial-15-manutenibilidade-agentes/exercicios/gabarito.py
```

**Parte hands-on** (`roteiro-ia.md`): experimente pedir uma feature nova dando o contexto do padrão existente, revise o diff e compare com pedir a mesma feature sem contexto.

> Arquivo: [`exercicios/exercicio.py`](exercicios/exercicio.py) · [`exercicios/exercicio.ts`](exercicios/exercicio.ts)
> Gabarito: [`exercicios/gabarito.py`](exercicios/gabarito.py) · [`exercicios/gabarito.ts`](exercicios/gabarito.ts)
> Revisão comentada: [`exercicios/gabarito_revisao.md`](exercicios/gabarito_revisao.md)
> Roteiro hands-on: [`exercicios/roteiro-ia.md`](exercicios/roteiro-ia.md)

---

## 4. Checklist — Manutenibilidade com Agentes

Use estas perguntas ao revisar qualquer mudança gerada por IA em um módulo existente:

1. **A contribuição segue os padrões do módulo?** — Idioma, estilo de nomes (snake_case/camelCase), granularidade de funções — a nova parte parece ter sido escrita pelo mesmo time?
2. **Revisei o diff inteiro, não só a parte nova?** — Se a IA editou múltiplos arquivos, cada arquivo tocado foi inspecionado?
3. **Alguma dependência nova foi introduzida sem necessidade?** — A stdlib ou o código já existente no módulo resolvia o problema?
4. **Documentei o porquê das decisões não óbvias?** — Regras de negócio, restrições de prazo, decisões de design — estão em comentários de intenção?
5. **Há duplicação que a IA criou (ou que já existia e ficou)?** — Duas funções que fazem a mesma coisa com nomes ou estilos diferentes?
6. **Deixei a base mais limpa do que encontrei?** — Apliquei a Regra do Escoteiro: consolidei pelo menos uma inconsistência que não era o objetivo da sessão?

---

## 5. Referências

- **Clean Code**, Robert C. Martin — Capítulo 1: *Clean Code* (p. 1–14); Capítulo 17: *Smells and Heuristics* (p. 285–313)
- Regra do Escoteiro — Tutorial 07, Sessão 2: [`sessao-2/tutorial-07-divida-tecnica/README.md`](../../sessao-2/tutorial-07-divida-tecnica/README.md)
- Tutorial 14 — Testes como Guard-Rails: [`sessao-6/tutorial-14-testes-guard-rails/README.md`](../tutorial-14-testes-guard-rails/README.md)
- Arquivos de exemplo: [`exemplos/prompt.md`](exemplos/prompt.md) · [`exemplos/relatorio_gerado.py`](exemplos/relatorio_gerado.py) · [`exemplos/relatorio_revisado.py`](exemplos/relatorio_revisado.py)

---

> **Este é o tutorial final do workshop.** Parabéns por chegar até aqui — você percorreu os fundamentos de Clean Code, revisão crítica, segurança, testes como guard-rails e, agora, manutenibilidade ao longo do tempo com agentes de IA.
