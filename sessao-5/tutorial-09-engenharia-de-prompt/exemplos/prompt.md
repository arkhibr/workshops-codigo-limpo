# Prompt Fraco vs. Prompt Estruturado — Cálculo de Preço com Descontos

> O prompt é uma especificação informal. Cada lacuna que você não preenche, a IA preenche com um default genérico.

---

## Prompt Fraco

```
calcula o preço com desconto
```

**O que a IA não sabe** e vai inventar: o domínio (e-commerce? clínica? academia?), quais regras de desconto aplicar, se descontos se acumulam, qual é o tipo de retorno, como tratar erros, os nomes dos campos da estrutura de dados, e em que idioma nomear os identificadores.

**Resultado típico:** parâmetros de uma letra (`x`, `y`), nome de função genérico (`calc`), regra de desconto hardcoded sem nome (`* 0.9`), dois descontos percentuais que se acumulam sem regra explícita de qual prevalece, sem tipo de retorno declarado.

> Arquivo de exemplo: `preco_gerado.py` / `preco_gerado.ts`

---

## Prompt Estruturado

```
Contexto: módulo de preços de um sistema de e-commerce. Todos os
identificadores devem estar em português brasileiro — sem mistura
de idiomas.

Implemente `calcular_preco_final(item: ItemPedido) -> float` que:
1. Aplica desconto por volume: DESCONTO_VOLUME_PCT para quantidades
   >= QUANTIDADE_MINIMA_VOLUME (defina ambos como constantes nomeadas).
2. Aplica desconto por categoria: DESCONTO_PREMIUM_PCT se
   item.categoria == "premium" (constante nomeada).
3. Descontos não se acumulam — aplica apenas o maior entre os elegíveis.
4. Lança ValueError com mensagem descritiva se preco_unitario <= 0.

Restrições:
- Sem bibliotecas externas.
- Cada regra de desconto em sua própria função privada.
- Responsabilidade única por função.
- Sem números mágicos — todos os valores em constantes nomeadas.

Exemplo do padrão de código esperado no projeto:
    @dataclass
    class ItemPedido:
        descricao: str
        preco_unitario: float
        quantidade: int
        categoria: str = "padrao"

Formato de saída: retorna float (preço final arredondado para 2 casas
decimais). Estrutura de dados: use o @dataclass ItemPedido acima como
base, sem adicionar dependências externas.

Linguagem: Python 3.10+. Sem frameworks externos.
```

**O que muda:** o domínio está definido, os nomes dos identificadores são especificados, as regras de negócio estão enumeradas, a restrição de não acumulação está explícita, o tratamento de erro é especificado, e o padrão de código (few-shot) é mostrado.

**Resultado típico:** `@dataclass ItemPedido`, constantes `DESCONTO_VOLUME_PCT` e `QUANTIDADE_MINIMA_VOLUME`, funções `_desconto_por_volume` e `_desconto_por_categoria` extraídas, função principal `calcular_preco_final` coesa.

> Arquivo de exemplo: `preco_revisado.py` / `preco_revisado.ts`

---

## O que muda na prática

| Dimensão              | Prompt fraco                        | Prompt estruturado                          |
|-----------------------|-------------------------------------|---------------------------------------------|
| Nomes                 | `calc`, `x`, `y`                    | `calcular_preco_final`, `item`, `desconto`  |
| Idioma                | Misturado ou inglês                 | Consistente (PT)                            |
| Regras de negócio     | Hardcoded sem nome (`* 0.9`)        | Constantes: `DESCONTO_VOLUME_PCT = 0.10`    |
| Coesão                | Tudo numa função                    | Cada regra em função própria               |
| Estrutura de dados    | Parâmetros soltos ou dict           | `@dataclass ItemPedido` tipado              |
| Tratamento de erro    | Retorna `0` ou silencia             | `raise ValueError("...")`                  |

**Conclusão:** mesmo um prompt estruturado não elimina a revisão — ele eleva o ponto de partida. O desenvolvedor ainda precisa ler o código gerado e aplicar o checklist de Clean Code. A versão revisada deste tutorial mostra exatamente o que precisou ser ajustado mesmo a partir de um bom prompt.
