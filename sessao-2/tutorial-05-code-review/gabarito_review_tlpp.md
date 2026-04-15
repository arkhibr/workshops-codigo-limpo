# Gabarito — Code Review: `codigo_para_revisar.tlpp`

> Simulação de comentários de code review esperados.
> Cada comentário segue o formato: **Linha · Problema · Sugestão**.

---

## Categoria: Nomes

---

**Linhas 7-9 — Constantes sem nome expressivo**

`DC`, `DC2` e `LM` não comunicam o que representam. Em ADVPL/TLPP, constantes devem ter nomes que descrevam o domínio, não abreviações.

Sugestão: `#define PERC_DESCONTO_PROMO10  0.10`, `#define PERC_DESCONTO_PROMO15  0.15` e `#define LIMITE_MAXIMO_PEDIDO  500.0`.

---

**Linhas 13-17 — Data Members sem prefixo de tipo e com nomes de 1-2 caracteres**

`n`, `lm`, `p`, `pd` e `x` violam duas convenções ADVPL ao mesmo tempo: não usam prefixo de tipo (`c`, `n`, `a`, `d`, `l`, `o`) e não revelam nenhuma intenção de negócio.

Sugestão: `cNomeLoja`, `nLimiteMaximo`, `aItensPedido`, `aHistoricoPedidos`, `nContadorAdicoes`. O prefixo `a` indica array, `c` indica caractere, `n` indica numérico.

---

**Linha 27 — Parâmetros sem prefixo de tipo em `Add`**

`pid`, `nm`, `pr`, `qt` não seguem as convenções de prefixo e são abreviações obscuras. Quem mantém o código não sabe se `pr` é "prefixo", "prioridade" ou "preço".

Sugestão: `cProdutoId`, `cNome`, `nPreco`, `nQuantidade` — o prefixo já comunica o tipo, o nome comunica a intenção.

---

**Linha 46 — Parâmetro `cpd` em `Calc`**

`cpd` é uma abreviação de cupom de desconto, mas não é óbvia. Combinada com a variável local `t`, torna o método difícil de ler.

Sugestão: `cCupom` para o parâmetro e `nTotal` para a variável de acúmulo.

---

**Linha 62 — Parâmetro `end` em `Fechar`**

`end` é ambíguo: em ADVPL, a palavra `End` encerra estruturas de controle (`EndIf`, `EndClass`). Usar `end` como nome de variável cria confusão visual.

Sugestão: `cEnderecoEntrega`.

---

**Linhas 90, 95 — Métodos `Itens` e `Hist` são nomes incompletos**

`Hist` não deixa claro que retorna o histórico de pedidos fechados.

Sugestão: `ListarItensDoPedido()` e `ObterHistoricoDePedidos()`.

---

## Categoria: Funções

---

**Linha 46 — `Calc` faz cálculo E aplica lógica de cupom na mesma função**

A função calcula o subtotal, verifica o tipo de cupom e aplica o desconto correspondente. São duas responsabilidades: calcular e descontar.

Sugestão: extraia `_AplicarCupom( nSubtotal, cCupom )` como método privado (convenção TLPP: prefixo `_` para métodos internos).

---

**Linha 62 — `Fechar` tem mais de uma responsabilidade**

O método valida, calcula, gera número, monta resultado, limpa estado e registra no histórico. São pelo menos 5 responsabilidades em um único método.

Sugestão: extraia `_ValidarPedido()`, `_GerarNumeroPedido()` e `_RegistrarNoHistorico( aResultado )`.

---

**Linha 53 — Magic number `0.9` dentro de `Calc`**

O valor `0.9` aparece diretamente no código, desconectado da constante `DC`. Se `DC` mudar, este trecho não muda junto.

Sugestão: use `1 - DC` (ou `1 - PERC_DESCONTO_PROMO10` após o renome) no lugar de `0.9`.

---

## Categoria: Comentários

---

**Linha 30 — Comentário `// adiciona item` é redundante**

Mesmo com o nome ruim `Add`, o comentário não agrega nenhuma informação que já não esteja implícita. Com um nome expressivo, o comentário se torna ainda mais desnecessário.

Sugestão: remova o comentário. Deixe o nome do método comunicar a intenção.

---

**Linha 58 — TODO sem rastreabilidade**

`// TODO: implementar desconto fidelidade` não tem ticket, responsável ou prazo. Em projetos Protheus, TODOs sem rastreabilidade costumam ficar no código por anos.

Sugestão: `// TODO [LANCH-42]: implementar desconto fidelidade. Responsavel: @dev-protheus | Sprint 18`.

---

**Linhas 77-79 — Código comentado sem explicação**

Três linhas de código morto (`DbSave`, `NotificarCozinha`, `EnviarSms`) sem nenhum contexto. O leitor não sabe se foram removidas por um bug ou se estão planejadas para retornar.

Sugestão: remova o código morto. Se for algo planejado, crie um TODO rastreável.

---

**Linhas 100-102 — Diário de bordo em comentário**

O histórico de alterações do método `_Log` pertence ao controle de versão, não ao código. Em ambientes Protheus com TFS ou Git, esse padrão é especialmente prejudicial porque o histórico real fica em dois lugares diferentes.

Sugestão: remova as três linhas de comentário de data/autor. Use o histórico do controle de versão.

---

## Categoria: Formatação

---

**Linhas 13-17 — Ausência de tipo explícito nas declarações `Data`**

Em TLPP moderno, `Data` aceita declaração de tipo: `Data cNomeLoja As Character`. Sem isso, o compilador não pode verificar atribuições incorretas de tipo.

Sugestão:
```tlpp
Data cNomeLoja          As Character
Data nLimiteMaximo      As Numeric
Data aItensPedido       As Array
Data aHistoricoPedidos  As Array
Data nContadorAdicoes   As Numeric
```

---

**Linha 83 — Linha de montagem do resultado com mais de 100 caracteres**

A linha `r := { "ok" => .T., "num" => num, "t" => t, ... }` ultrapassa 100 caracteres e é difícil de ler em qualquer editor.

Sugestão: quebre a inicialização do array em múltiplas linhas, uma chave por linha.

---

> **Total: 14 comentários de review**
> Distribuição: 6 Nomes · 3 Funções · 4 Comentários · 2 Formatação
