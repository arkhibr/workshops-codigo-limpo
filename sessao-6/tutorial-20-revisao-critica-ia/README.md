# Tutorial 20 — Revisão Crítica de Código Gerado por IA

> Tutorial âncora do tema — revisar saída confiante e polida de modelos de fronteira.

---

## 1. Contexto e Motivação

Este tutorial tem o mesmo papel na Sessão 6 que o Tutorial 05 tem na Sessão 2:
integrar o tema em um exercício de revisão completo. Antes, você revisava código
escrito por um humano com vícios visíveis — nomes ruins, funções longas, comentários
de diário de bordo. Aqui você revisa código gerado por um modelo de fronteira.

O perigo não é o mesmo. **O perigo é a superfície limpa.**

Em 2026, Claude Opus 4.8, GPT-4o e Gemini 2.0 geram código tipado, idiomático,
com docstrings profissionais e constantes nomeadas. O código parece revisado.
Ele passa na leitura rápida. É exatamente por isso que a revisão crítica é
necessária: **os defeitos se escondem atrás da aparência de qualidade**.

Os modos de falha mudaram. O modelo não usa nomes de uma letra nem deixa
`except: pass`. Ele alucina métodos com nomes plausíveis, escreve docstrings
que prometem o que o código não entrega, e passa silenciosamente por edge cases
que nunca apareceram nos dados de treinamento.

> *"A segunda leitura quase sempre encontra algo que o autor não viu — não por
> incompetência, mas porque o autor tem o contexto que o leitor não tem."*
>
> — Robert C. Martin, *Clean Code*

Esse princípio vale ainda mais quando o autor é um modelo: ele não tem contexto
de produção, não conhece a versão exata da SDK, e não sabe o que acontece quando
alguém chama `cobrar(cobranca)` com valor negativo às 23h47 em produção.

---

## 2. Conceito Central — Os 6 Modos de Falha

Código gerado por IA de fronteira falha de formas previsíveis. Conhecer os
padrões é o que separa uma revisão que encontra os problemas de uma que apenas
confirma que o código compila.

### Modo 1 — API/método alucinado

O modelo gera chamadas a métodos que parecem existir mas não existem na versão
da biblioteca usada. O nome é plausível e bem formado. A alucinação não aparece
em tempo de compilação quando está em um ramo não exercitado.

```python
# Plausível, mas verificar_idempotencia não existe na SDK 3.x
_gateway.verificar_idempotencia(transacao_id)
```

**Sinal de alerta:** método chamado em ramo de guarda que o caminho feliz não exercita.

### Modo 2 — Lógica confiante-mas-errada

O modelo reproduz um padrão correto-looking com um detalhe errado. Off-by-one
em ranges, condição de comparação invertida (`<` vs `<=`), arredondamento que
perde 1 centavo. O código ao redor está impecável — o defeito se camufla.

```python
for numero in range(1, num_parcelas):   # off-by-one: gera n-1 parcelas
```

**Sinal de alerta:** loops com limites numéricos, comparações em condições de guarda.

### Modo 3 — Segurança sutil

Não um segredo hardcoded em texto plano — isso o modelo evita. O defeito é mais
sutil: comparar tokens com `==` em vez de constant-time, montar parte de uma
query por concatenação, logar um campo que contém dado sensível.

```python
return assinatura_esperada == assinatura_recebida   # timing side-channel
```

**Sinal de alerta:** qualquer comparação de tokens, assinaturas ou senhas.

> O Tutorial 14 aprofunda segurança em código gerado por IA — este é o primeiro contato.

### Modo 4 — Edge case ausente

O modelo não testa o código que gera. Valores zero, negativos, listas vazias e
timeouts são os candidatos mais comuns. A função está tipada e documentada — ela
simplesmente não defende a entrada.

```python
def cobrar(cobranca: Cobranca) -> ResultadoCobranca:
    # valor <= 0 não é validado; executa sem erro
    resposta = _gateway.cobrar(cobranca.valor, ...)
```

**Sinal de alerta:** funções que recebem valores numéricos ou coleções sem guarda explícita.

### Modo 5 — Over-engineering

O modelo infere que um sistema real teria mais camadas e as adiciona sem ser
pedido. Uma factory/strategy para algo trivial, uma camada de cache sem
invalidação, um repositório abstrato para dados em memória. O código compila e
roda — mas viola o princípio de não adicionar complexidade antes de precisar.

```python
class ProcessadorDePagamento:   # o pedido era: três funções livres
    def processar(self, cobranca):
        ...
```

**Sinal de alerta:** classes de infraestrutura (Factory, Repository, Strategy, Cache)
que não foram solicitadas.

### Modo 6 — Docstring que mente

O modelo escreve o que deveria fazer, não o que faz. A docstring promete
validação de CPF e idempotência. O corpo não valida nada. Em produção, alguém
lê a docstring, acredita na promessa e não adiciona a guarda que deveria estar lá.

```python
def cobrar(cobranca: Cobranca) -> ResultadoCobranca:
    """
    Valida o CPF do cliente e garante idempotência via pedido_id
    antes de submeter ao gateway.
    """
    # ... corpo que não valida CPF nem garante idempotência
```

**Sinal de alerta:** qualquer docstring que mencione validação, garantia ou segurança.

---

## 3. Exercício

### O que fazer

1. **Leia** `codigo_gerado_por_ia.py` do início ao fim como se fosse um Pull Request real.

2. **Rode** o código para confirmar que o caminho feliz funciona:
   ```bash
   python3 codigo_gerado_por_ia.py
   npx ts-node codigo_gerado_por_ia.ts
   ```

3. **Anote** cada problema encontrado com: linha, categoria do checklist, problema, sugestão.

4. **Compare** com `gabarito_review.md` (Python) ou `gabarito_review_ts.md` (TypeScript).

5. **Faça o roteiro hands-on** em `exercicios/roteiro-ia.md` — inclui a trilha de gerar
   código real nos três modelos e comparar.

### Critério de calibração

- **6 defeitos encontrados:** olhar totalmente calibrado para código de fronteira
- **4–5 defeitos:** bom — revisar as categorias onde perdeu
- **2–3 defeitos:** reler a seção "Conceito Central" e refazer a leitura com o checklist
- **0–1 defeitos:** o código está cumprindo seu papel de ensino — é polido o suficiente para iludir

---

## 4. Checklist de Revisão

O `checklist_revisao_ia.md` é a ferramenta reutilizável deste tutorial.
Use-o em qualquer revisão de código gerado por IA, não apenas neste exercício.

Categorias:
1. Correção
2. Segurança
3. Edge Cases
4. Legibilidade e Coesão
5. Dependências e Alucinação
6. A IA entendeu o pedido?

---

## 5. Referências

- *Clean Code* — Robert C. Martin (Cap. 3 e 4: funções e comentários)
- *Working Effectively with Legacy Code* — Michael Feathers (Cap. 8: detecção de efeitos colaterais)
- Tutorial 05 — Code Review Simulado (Sessão 2): estrutura análoga com código humano
- Tutorial 17 — Engenharia de Contexto e Prompt: como o prompt afeta os defeitos gerados
- Tutorial 22 — Segurança em Código Gerado (Sessão 6): aprofundamento do Modo 3

---

> **Próximo tutorial:** [Tutorial 21 — Refatoração Assistida Avançada](../tutorial-21-refatoracao-avancada/README.md)
