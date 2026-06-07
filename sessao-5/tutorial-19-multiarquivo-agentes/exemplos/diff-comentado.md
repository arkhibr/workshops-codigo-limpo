# Diff comentado — mudança multi-arquivo com inconsistência cross-file

**Tarefa solicitada ao agente:** "Adicionar suporte a cupom de desconto ao carrinho.
Atualizar a precificação e todos os chamadores."

O agente aplicou a mudança em dois arquivos. O diff abaixo é o que você receberia
ao revisar em altitude — olhando os dois arquivos juntos, não isoladamente.

> **Nota:** este é um diff *representativo* da inconsistência. Para que cada arquivo
> do tutorial rode isoladamente (sem import entre arquivos do repo), `carrinho.py`
> usa uma cópia local `_calcular_total_local`; em um projeto real a chamada seria
> direta a `calcular_total`, como mostrado aqui.

---

## Diff: precificacao.py

```diff
# precificacao.py

  @dataclass
  class ItemCarrinho:
      produto_id:     str
      descricao:      str
      preco_unitario: float
      quantidade:     int

+ @dataclass
+ class Cupom:
+     codigo:              str
+     percentual_desconto: float  # 0.0 a 1.0
+
+     def __post_init__(self) -> None:
+         if not (0.0 <= self.percentual_desconto <= 1.0):
+             raise ValueError(...)
+
+ CUPONS_VALIDOS: dict[str, Cupom] = {
+     "BEMVINDO10":    Cupom(codigo="BEMVINDO10",    percentual_desconto=0.10),
+     "BLACKFRIDAY20": Cupom(codigo="BLACKFRIDAY20", percentual_desconto=0.20),
+ }

+ def resolver_cupom(codigo: str) -> Optional[Cupom]:
+     return CUPONS_VALIDOS.get(codigo.upper())

  def calcular_total(
      itens: list[ItemCarrinho],
+     cupom: Optional[Cupom],   # ← NOVO parâmetro — sem valor padrão
  ) -> float:
      ...
      bruto = sum(subtotal_item(i) for i in itens)
+     if cupom is None:
+         return round(bruto, 2)
+     valor_desconto = round(bruto * cupom.percentual_desconto, 2)
+     return round(bruto - valor_desconto, 2)
```

**Avaliação por arquivo:** a mudança em `precificacao.py` está correta. A nova
entidade `Cupom`, a constante `CUPONS_VALIDOS`, a função `resolver_cupom` e a
nova assinatura de `calcular_total` são consistentes entre si. O código é polido
e idiomático — não há nada suspeito olhando este arquivo isoladamente.

---

## Diff: carrinho.py

```diff
# carrinho.py

  @dataclass
  class Carrinho:
      id:    str
      itens: list[ItemCarrinho] = field(default_factory=list)
+     cupom: Optional[Cupom]   = None   # ← campo adicionado ao Carrinho

+ def aplicar_cupom(carrinho: Carrinho, cupom: Cupom) -> None:
+     carrinho.cupom = cupom

  def finalizar_carrinho(carrinho: Carrinho) -> dict:
-     total = calcular_total(carrinho.itens)
+     # ← o agente NÃO atualizou esta linha
+     total = calcular_total(carrinho.itens)   # ← CHAMADA ANTIGA — falta cupom
      return {
          "carrinho_id": carrinho.id,
          "total":       total,
+         "cupom":       carrinho.cupom.codigo if carrinho.cupom else None,
      }
```

**Avaliação por arquivo:** cada linha nova parece razoável isoladamente. O campo
`cupom` no `Carrinho` faz sentido. `aplicar_cupom` é simples e correto. O dict
de retorno inclui o código do cupom — parece que o cupom está sendo tratado.

---

## A inconsistência cross-file

Só aparece ao **ler o diff dos dois arquivos juntos**, em altitude:

```
precificacao.py:   def calcular_total(itens, cupom)       ← exige 2 argumentos
carrinho.py:           calcular_total(carrinho.itens)     ← passa 1 argumento
                                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                          INCONSISTÊNCIA: falta 'cupom'
```

**Consequência:** `finalizar_carrinho` levanta `TypeError: calcular_total()
missing 1 required positional argument: 'cupom'` na primeira vez que um cliente
tentar finalizar um pedido com cupom aplicado.

O defeito é sutil por três razões:

1. **Cada arquivo roda sua demo sem erro** — `precificacao.py` não chama
   `finalizar_carrinho`, e `carrinho.py` usa uma cópia local da lógica.

2. **O cupom aparece no dict de retorno** — `"cupom": carrinho.cupom.codigo`
   sugere visualmente que o cupom está sendo considerado; mas o `total`
   ao lado foi calculado sem ele.

3. **A linha não mudou** — `calcular_total(carrinho.itens)` existia antes
   da mudança. O agente adicionou linhas ao redor mas não tocou nesta.
   Em uma revisão rápida, linhas inalteradas não chamam atenção.

---

## O que uma revisão em altitude detecta

| O que revisar | Pergunta-chave | Resposta neste diff |
|---|---|---|
| Assinatura mudou? | Onde ela é declarada e onde é chamada? | Declarada em `precificacao.py`, chamada em `carrinho.py` |
| Todos os chamadores foram atualizados? | A chamada em `carrinho.py` passa os mesmos argumentos da nova assinatura? | **Não** — falta `cupom` |
| Campo novo → lógica nova? | `carrinho.cupom` aparece no dict mas chega ao cálculo? | Aparece no dict, não chega ao `calcular_total` |
| A mudança é coesa? | Todas as partes da feature (entidade, cálculo, chamador) foram atualizadas? | **Não** — chamador esquecido |

---

## Versão corrigida (revisado/carrinho.py)

```diff
  def finalizar_carrinho(carrinho: Carrinho) -> dict:
-     total = calcular_total(carrinho.itens)
+     total = calcular_total(carrinho.itens, carrinho.cupom)   # ← cupom propagado
      bruto = sum(_subtotal_item(i) for i in carrinho.itens)
+     desconto = round(bruto - total, 2) if total < bruto else 0.0
      return {
          "carrinho_id":    carrinho.id,
+         "subtotal":       bruto,
+         "desconto_cupom": desconto,
          "total":          total,
          "cupom":          carrinho.cupom.codigo if carrinho.cupom else None,
      }
```

A correção é uma linha: passar `carrinho.cupom` como segundo argumento.
O agente gerou tudo o que era necessário em `precificacao.py` — faltou
propagar o cupom até o ponto de cálculo em `carrinho.py`.
