# Gabarito — Code Review: `codigo_para_revisar.php`

> Simulação de comentários de code review esperados.
> Cada comentário segue o formato: **Linha · Problema · Sugestão**.

---

## Categoria: Nomes

---

**Linhas 7-9 — Constantes sem nome expressivo**

`DC`, `DC2` e `LM` não comunicam o que representam. Quem lê o código não tem como saber que `DC` é um desconto de 10%, `DC2` é de 15% e `LM` é o limite máximo do pedido.

Sugestão: renomeie para `PERCENTUAL_DESCONTO_PROMO10 = 0.10`, `PERCENTUAL_DESCONTO_PROMO15 = 0.15` e `LIMITE_MAXIMO_PEDIDO = 500.0`.

---

**Linhas 13-17 — Propriedades com nomes de 1-2 caracteres**

`$n`, `$lm`, `$p`, `$pd` e `$x` não revelam nenhuma intenção. A leitura dos métodos exige rastrear cada propriedade até o construtor para entender o que ela guarda.

Sugestão: `$nomeLoja`, `$limiteMaximo`, `$itensPedidoAtual`, `$historicoDePedidos`, `$contadorDeAdicoes`.

---

**Linha 27 — Método `add` não descreve o que adiciona**

`add` é genérico demais. O domínio é claro: estamos adicionando um item a um pedido de lanchonete.

Sugestão: `adicionarItem(string $produtoId, string $nome, float $preco, int $quantidade = 1)`.

---

**Linha 45 — Método `calc` é abreviação desnecessária**

`calc` pode ser calcular qualquer coisa. Os parâmetros `$cpd` (cupom de desconto?) e `$t` (total?) agravam o problema.

Sugestão: `calcularTotal(?string $cupom = null)` com variável local `$total` no lugar de `$t`.

---

**Linha 62 — Método `fechar` tem parâmetro `$end`**

`$end` é uma abreviação de "endereço" que não é intuitiva, especialmente para quem vem de outras linguagens onde `end` é palavra reservada.

Sugestão: `$enderecoEntrega` ou simplesmente `$endereco`.

---

**Linhas 83, 88 — Métodos `itens` e `hist` são nomes incompletos**

Em especial `hist` não deixa claro que retorna o histórico de pedidos fechados.

Sugestão: `listarItensDoPedidoAtual()` e `obterHistoricoDePedidos()`.

---

## Categoria: Funções

---

**Linha 45 — `calc` faz cálculo E aplica lógica de cupom na mesma função**

A função calcula o subtotal, verifica o tipo de cupom e aplica o desconto correspondente. São duas responsabilidades: calcular e descontar.

Sugestão: extraia `_aplicarCupom(float $subtotal, string $cupom): float` como método privado. `calcularTotal` chama `_aplicarCupom` para o resultado final.

---

**Linha 62 — `fechar` tem mais de uma responsabilidade**

O método valida o pedido, calcula o total, gera o número do pedido, monta o array de resultado, limpa o estado atual e adiciona ao histórico. São pelo menos 5 responsabilidades.

Sugestão: extraia `_validarPedidoAtual()`, `_gerarNumeroDePedido()` e `_registrarPedidoNoHistorico(array $pedido)` como métodos privados.

---

**Linha 52 — Magic number `0.9` dentro de `calc`**

O valor `0.9` aparece diretamente no código, desconectado da constante `DC`. Se `DC` mudar, este trecho não muda junto — e ninguém vai notar.

Sugestão: use `1 - DC` (ou `1 - PERCENTUAL_DESCONTO_PROMO10` após o renome) no lugar de `0.9`.

---

**Linha 16 — Visibilidade `public` nas propriedades**

Todas as propriedades são `public`, quebrando o encapsulamento. Código externo pode modificar `$p` ou `$pd` diretamente sem passar pelos métodos.

Sugestão: declare as propriedades como `private` e exponha apenas os dados necessários através de métodos.

---

## Categoria: Comentários

---

**Linha 30 — Comentário `// adiciona item` é redundante**

Mesmo com o nome ruim `add`, o comentário não agrega nenhuma informação que já não esteja implícita. Com um nome expressivo (`adicionarItem`), o comentário se torna ainda mais desnecessário.

Sugestão: remova o comentário. Deixe o nome do método comunicar a intenção.

---

**Linha 57 — TODO sem rastreabilidade: `// TODO: implementar desconto fidelidade`**

Não há ticket, responsável ou prazo. Esse TODO vai ficar aqui indefinidamente.

Sugestão: `// TODO [LANCH-42]: implementar lógica de desconto para clientes fidelidade. Responsável: @dev-backend | Prazo: Sprint 18`.

---

**Linhas 70-72 — Código comentado sem explicação**

Três linhas de código morto (`$db->save`, `notificarCozinha`, `enviarSms`) sem nenhum contexto. O leitor não sabe se foi removido por um bug, se está planejado para voltar ou se já foi movido para outro lugar.

Sugestão: remova o código morto. Se for algo planejado, crie um TODO rastreável.

---

**Linhas 101-103 — Diário de bordo em comentário**

O histórico de alterações do método `_log` pertence ao controle de versão, não ao código.

Sugestão: remova as três linhas de comentário. Use `git log -p -- codigo_para_revisar.php` para ver o histórico real.

---

## Categoria: Formatação

---

**Linhas 13-17 — Ausência de tipos nas propriedades**

Em PHP 7.4+ as propriedades podem ter tipo declarado. Sem tipagem, o IDE e o analisador estático não conseguem detectar uso incorreto.

Sugestão:
```php
private string $nomeLoja;
private float  $limiteMaximo;
private array  $itensPedidoAtual;
private array  $historicoDePedidos;
private int    $contadorDeAdicoes;
```

---

**Linha 76 — Array de resultado com mais de 100 caracteres na mesma linha**

A linha que monta `$r = ['ok' => true, 'num' => $num, ...]` ultrapassa 100 caracteres, dificultando a leitura.

Sugestão: quebre o array com uma chave por linha, no padrão PSR-12.

---

> **Total: 15 comentários de review**
> Distribuição: 6 Nomes · 4 Funções · 4 Comentários · 2 Formatação
