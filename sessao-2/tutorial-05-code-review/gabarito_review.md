# Gabarito — Code Review: `sistema_pedidos.py`

> Simulação de comentários de code review esperados.
> Cada comentário segue o formato: **Linha · Problema · Sugestão**.

---

## Categoria: Nomes

---

**Linha 8 — Constantes sem nome expressivo**

`DC`, `DC2` e `LM` não comunicam o que representam. Quem lê o código não tem como saber que `DC` é um desconto de 10%, `DC2` é de 15% e `LM` é o limite máximo do pedido.

Sugestão: renomeie para `PERCENTUAL_DESCONTO_PROMO10 = 0.10`, `PERCENTUAL_DESCONTO_PROMO15 = 0.15` e `LIMITE_MAXIMO_PEDIDO = 500.0`.

---

**Linha 11 — Atributos de instância com nomes de 1-2 caracteres**

`self.n`, `self.lm`, `self.p`, `self.pd` e `self.x` não revelam nenhuma intenção. A leitura dos métodos exige rastrear cada atributo até a `__init__` para entender o que é.

Sugestão: `self.nome_loja`, `self.limite_maximo`, `self._itens_do_pedido_atual`, `self._historico_de_pedidos`, `self._contador_de_adicoes`.

---

**Linha 19 — Método `add` não descreve o que adiciona**

`add` é genérico demais. O domínio é claro: estamos adicionando um item a um pedido de lanchonete.

Sugestão: `adicionar_item(self, produto_id, nome, preco, quantidade=1)`.

---

**Linha 26 — Método `calc` é abreviação desnecessária**

`calc` pode ser calcular qualquer coisa. Os parâmetros `cpd` (cupom de desconto?) e `t` (total?) agravam o problema.

Sugestão: `calcular_total(self, cupom=None)` com variável local `total` no lugar de `t`.

---

**Linha 44 — Método `fechar` tem parâmetro `end`**

`end` é uma palavra reservada de `print()` em Python e também uma abreviação de "endereço". Ambos causam confusão.

Sugestão: `endereco_entrega` ou simplesmente `endereco`.

---

**Linhas 55, 58 — Métodos `itens` e `hist` são abreviações**

Em especial `hist` não deixa claro que retorna o histórico de pedidos fechados.

Sugestão: `listar_itens_do_pedido_atual` e `obter_historico_de_pedidos`.

---

## Categoria: Funções

---

**Linha 26 — `calc` faz cálculo E aplica lógica de cupom na mesma função**

A função calcula o subtotal, verifica o tipo de cupom e aplica o desconto correspondente. São duas responsabilidades: calcular e descontar.

Sugestão: extraia `_aplicar_cupom(self, subtotal, cupom)` como método privado. `calcular_total` chama `_aplicar_cupom` para o resultado final.

---

**Linha 44 — `fechar` tem mais de uma responsabilidade**

O método valida o pedido, calcula o total, gera o número do pedido, monta o dicionário de resultado, limpa o estado atual e adiciona ao histórico. São pelo menos 5 responsabilidades.

Sugestão: extraia `_validar_pedido_atual()`, `_gerar_numero_pedido()` e `_registrar_pedido_no_historico(pedido)` como métodos privados.

---

**Linha 33 — Magic number `0.9` dentro de `calc`**

O valor `0.9` aparece diretamente no código, desconectado da constante `DC`. Se `DC` mudar, este trecho não muda junto — e ninguém vai notar.

Sugestão: use `1 - PERCENTUAL_DESCONTO_PROMO10` no lugar de `0.9` para que os dois permaneçam sincronizados.

---

## Categoria: Comentários

---

**Linha 27 — Comentário `# adiciona item` é redundante**

O nome do método `add` já comunica essa intenção (mesmo que mal). O comentário não agrega nada.

Sugestão: remova o comentário. Se o método tiver nome expressivo (`adicionar_item`), dispensa qualquer explicação.

---

**Linha 38 — TODO sem rastreabilidade: `# TODO: implementar desconto fidelidade`**

Não há ticket, responsável ou prazo. Esse TODO vai ficar aqui para sempre.

Sugestão: `# TODO [LANCH-42]: implementar lógica de desconto para clientes fidelidade. Responsável: @dev-backend | Prazo: Sprint 18`.

---

**Linhas 47-49 — Código comentado sem explicação**

Três linhas de código morto (`db.save`, `notificar_cozinha`, `enviar_sms`) sem nenhum contexto. O leitor não sabe se isso foi removido por um bug, se está planejado para voltar ou se já foi movido para outro lugar.

Sugestão: remova o código morto. Se for algo planejado, crie um TODO rastreável.

---

**Linhas 61-63 — Diário de bordo em comentário**

O histórico de alterações do método `_log` pertence ao controle de versão, não ao código.

Sugestão: remova as três linhas de comentário. Use `git log -p -- sistema_pedidos.py` para ver o histórico real.

---

## Categoria: Formatação

---

**Linha 2 — Imports em uma única linha separados por vírgula**

`import json,os,sys` viola PEP 8: cada módulo importado deve ter sua própria linha.

Sugestão:
```python
import json
import os
import sys
```

---

**Linhas em geral — Sem espaços ao redor de operadores e após vírgulas**

Exemplos: `l=Lanchonete(...)`, `l.add("X001","X-Burguer",18.50,2)`, `t=t+(v["p"]*v["qt"])`.

Sugestão: aplique `black sistema_pedidos.py` para corrigir automaticamente toda a formatação horizontal.

---

**Linha 44 — Linha de retorno do dicionário com 120+ caracteres**

A linha que monta `r = {"ok": True, "num": num, ...}` ultrapassa 100 caracteres, dificultando a leitura em qualquer editor.

Sugestão: quebre o dicionário com uma chave por linha, no padrão black (máx. 88 chars).

---

> **Total: 15 comentários de review**
> Distribuição: 6 Nomes · 3 Funções · 4 Comentários · 2 Formatação
