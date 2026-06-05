# Tutorial 09 — Engenharia de Prompt para Código Limpo

> Referência: *Clean Code*, Cap. 2–3; engenharia de contexto em prompts de código

---

## 1. Contexto e Motivação

O tutorial anterior mostrou que um **prompt forte produz código melhor** do que um prompt vago. Agora vamos entender *por que* isso acontece e como construir sistematicamente um prompt de qualidade.

A IA não conhece o seu domínio, as suas convenções de nomenclatura, as dependências que você quer evitar nem o padrão de retorno que o restante do sistema espera. Quando você não especifica isso, ela preenche as lacunas com defaults genéricos — inglês, abreviações, magic numbers, funções que fazem três coisas ao mesmo tempo.

Engenharia de prompt é a disciplina de traduzir suas expectativas de Clean Code em linguagem que a IA possa seguir **antes** de gerar o código — não depois, na revisão.

---

## 2. Conceito Central

### Os cinco elementos de um prompt estruturado

Um prompt de qualidade contém cinco elementos, todos presentes explicitamente:

| Elemento          | O que especifica                                          | Exemplo                                     |
|-------------------|-----------------------------------------------------------|---------------------------------------------|
| **Contexto**      | Domínio do negócio, arquitetura existente, idioma        | "sistema de vendas, identificadores em PT"  |
| **Linguagem de domínio** | Os termos que o negócio usa — não sinônimos genéricos | "ItemPedido, não Product nem Item"          |
| **Restrições**    | O que a IA *não* deve fazer                              | "sem libs externas, responsabilidade única" |
| **Exemplo (few-shot)** | Uma amostra do padrão desejado                      | trecho de código com o estilo esperado      |
| **Formato de saída** | O contrato de retorno esperado                        | "retorna `float`, lança `ValueError` se…"  |

### O mesmo pedido com e sem contexto

```
# Prompt fraco
calcula o preço com desconto
```

Saída típica — nomes genéricos, regra hardcoded sem nome, sem tipos:

```python
def calc(x, y):
    if x > 100:
        return x * 0.9  # desconto mágico de 10%
    return x - y
```

```
# Prompt estruturado
Contexto: módulo de preços de um sistema de e-commerce. Todos os
identificadores devem estar em português brasileiro.

Implemente `calcular_preco_final(item: ItemPedido) -> float` que:
1. Aplica desconto por volume: DESCONTO_VOLUME_PCT (0.10) para
   quantidades >= QUANTIDADE_MINIMA_VOLUME (5 unidades).
2. Aplica desconto por categoria: DESCONTO_PREMIUM_PCT (0.15) se
   item.categoria == "premium".
3. Descontos não se acumulam — aplica apenas o maior.
4. Lança ValueError com mensagem descritiva se preco_unitario <= 0.

Restrições: sem bibliotecas externas, cada regra em sua própria função.
Formato: retorna float (preço final arredondado para 2 casas decimais).

Exemplo do padrão de código esperado:
    @dataclass
    class ItemPedido:
        descricao: str
        preco_unitario: float
        quantidade: int
        categoria: str
```

Saída típica — nomes descritivos, constantes nomeadas, responsabilidade única:

```python
DESCONTO_VOLUME_PCT = 0.10
QUANTIDADE_MINIMA_VOLUME = 5
DESCONTO_PREMIUM_PCT = 0.15

def calcular_preco_final(item: ItemPedido) -> float:
    desconto = _selecionar_maior_desconto(item)
    preco_com_desconto = item.preco_unitario * (1 - desconto) * item.quantidade
    return round(preco_com_desconto, 2)
```

A diferença não é o tamanho do prompt — é a presença dos cinco elementos. Cada um elimina uma categoria de ambiguidade que a IA resolveria com um default genérico.

### Iterar o prompt, não aceitar a primeira resposta

Um prompt forte é um ponto de partida, não uma garantia. A IA pode ignorar parte das restrições, especialmente as de idioma. O ciclo correto é:

1. Envie o prompt estruturado.
2. Leia o código gerado com o checklist do Tutorial 08.
3. Identifique as restrições que a IA ignorou.
4. Adicione essas restrições explicitamente ao prompt e reenvie.
5. Repita até o ponto de partida ser aceitável — depois revise o código.

Iterar o prompt é mais eficiente do que corrigir o código manualmente: você está ajustando a especificação, não o resultado de uma especificação ruim.

---

## 3. Exercício

O exercício está em `exercicios/` e tem duas partes:

**Parte estática** (`exercicio.py` / `exercicio.ts`): módulo de cupom de desconto progressivo gerado a partir de um prompt fraco. Sua tarefa:
1. Reescreva o prompt para ser mais forte.
2. Refatore o código aplicando os princípios de Clean Code.
3. Liste os problemas que você encontrou.

```bash
# Veja o código a ser refatorado:
python3 sessao-5/tutorial-09-engenharia-de-prompt/exercicios/exercicio.py

# Compare com a solução de referência:
python3 sessao-5/tutorial-09-engenharia-de-prompt/exercicios/gabarito.py
```

**Parte hands-on** (`roteiro-ia.md`): monte um template de prompt reutilizável e aplique-o para gerar a função de cupom, comparando com a saída do prompt fraco.

> Arquivo: [`exercicios/exercicio.py`](exercicios/exercicio.py) · [`exercicios/exercicio.ts`](exercicios/exercicio.ts)  
> Gabarito: [`exercicios/gabarito.py`](exercicios/gabarito.py) · [`exercicios/gabarito.ts`](exercicios/gabarito.ts)  
> Revisão comentada: [`exercicios/gabarito_revisao.md`](exercicios/gabarito_revisao.md)  
> Roteiro hands-on: [`exercicios/roteiro-ia.md`](exercicios/roteiro-ia.md)

---

## 4. Checklist — Avaliando seu Prompt Antes de Enviar

Use estas perguntas antes de enviar qualquer prompt de geração de código:

1. **Dei contexto do projeto?** — A IA sabe o domínio de negócio, o idioma dos identificadores e o que o módulo faz no sistema?
2. **Listei as restrições explicitamente?** — Especifiquei o que a IA *não* deve fazer (sem libs externas, sem mistura de idioma, responsabilidade única)?
3. **Dei um exemplo do padrão desejado?** — Mostrei um trecho do código existente ou do estilo esperado (few-shot)?
4. **Defini o formato de saída?** — O contrato de retorno, os tipos esperados e o tratamento de erro estão especificados?
5. **Iterei em vez de aceitar a primeira resposta?** — Identifiquei as restrições ignoradas e refinei o prompt antes de editar o código manualmente?
6. **Incluí a linguagem de domínio?** — Usei os termos que o negócio usa, não sinônimos genéricos?

---

## 5. Referências

- **Clean Code**, Robert C. Martin — Capítulo 2: *Meaningful Names* (p. 17–30)
- **Clean Code**, Robert C. Martin — Capítulo 3: *Functions* (p. 31–52)
- Arquivos de exemplo: [`exemplos/prompt.md`](exemplos/prompt.md) · [`exemplos/preco_gerado.py`](exemplos/preco_gerado.py) · [`exemplos/preco_revisado.py`](exemplos/preco_revisado.py)

---

> **Tutorial anterior:** [Tutorial 08 — Clean Code com IA](../tutorial-08-clean-code-com-ia/README.md)
