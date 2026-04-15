# Gabarito — Code Review: `codigo_para_revisar.ts`

> Simulação de comentários de code review esperados.
> Cada comentário segue o formato: **Linha · Problema · Sugestão**.

---

## Categoria: Nomes

---

**Linhas 7-9 — Constantes sem nome expressivo**

`DC`, `DC2` e `LM` não comunicam o que representam. Quem lê o código não tem como saber que `DC` é um desconto de 10%, `DC2` é de 15% e `LM` é o limite máximo do pedido.

Sugestão: renomeie para `PERCENTUAL_DESCONTO_PROMO10 = 0.10`, `PERCENTUAL_DESCONTO_PROMO15 = 0.15` e `LIMITE_MAXIMO_PEDIDO = 500.0`.

---

**Linhas 12-16 — Propriedades com nomes de 1-2 caracteres**

`n`, `lm`, `p`, `pd` e `x` não revelam nenhuma intenção. A leitura dos métodos exige rastrear cada propriedade até o construtor para entender o que ela guarda.

Sugestão: `nomeLoja`, `limiteMaximo`, `itensPedidoAtual`, `historicoDePedidos`, `contadorDeAdicoes`.

---

**Linha 22 — Método `add` não descreve o que adiciona**

`add` é genérico demais. O domínio é claro: estamos adicionando um item a um pedido de lanchonete.

Sugestão: `adicionarItem(produtoId: string, nome: string, preco: number, quantidade: number = 1): void`.

---

**Linha 36 — Método `calc` é abreviação desnecessária**

`calc` pode ser calcular qualquer coisa. Os parâmetros `cpd` (cupom de desconto?) e `t` (total?) agravam o problema.

Sugestão: `calcularTotal(cupom: string | null = null): number` com variável local `total` no lugar de `t`.

---

**Linha 55 — Método `fechar` tem parâmetro `end`**

`end` é uma palavra com conotação de fim/término em inglês, além de ser confusa para leitores familiarizados com outras linguagens onde é reservada. Para um campo de endereço de entrega, o nome não comunica o domínio.

Sugestão: `enderecoEntrega` ou `endereco`.

---

**Linhas 75, 80 — Métodos `itens` e `hist` são nomes incompletos**

Em especial `hist` não deixa claro que retorna o histórico de pedidos fechados.

Sugestão: `listarItensDoPedidoAtual()` e `obterHistoricoDePedidos()`.

---

## Categoria: Funções

---

**Linha 36 — `calc` faz cálculo E aplica lógica de cupom na mesma função**

A função calcula o subtotal, verifica o tipo de cupom e aplica o desconto correspondente. São duas responsabilidades: calcular e descontar.

Sugestão: extraia `private _aplicarCupom(subtotal: number, cupom: string): number`. `calcularTotal` chama `_aplicarCupom` para o resultado final.

---

**Linha 55 — `fechar` tem mais de uma responsabilidade**

O método valida o pedido, calcula o total, gera o número do pedido, monta o objeto de resultado, limpa o estado atual e adiciona ao histórico. São pelo menos 5 responsabilidades.

Sugestão: extraia `private _validarPedidoAtual()`, `private _gerarNumeroDePedido()` e `private _registrarPedidoNoHistorico(pedido: object)` como métodos privados.

---

**Linha 44 — Magic number `0.9` dentro de `calc`**

O valor `0.9` aparece diretamente no código, desconectado da constante `DC`. Se `DC` mudar, este trecho não muda junto — e ninguém vai notar.

Sugestão: use `1 - DC` (ou `1 - PERCENTUAL_DESCONTO_PROMO10` após o renome) no lugar de `0.9`.

---

**Linha 13 — Tipo `any[]` em `pd`**

`pd: any[]` desabilita a verificação de tipos justamente na propriedade que armazena o histórico de pedidos — exatamente onde a consistência importa.

Sugestão: defina uma interface `Pedido` e use `pd: Pedido[]`.

---

## Categoria: Comentários

---

**Linha 24 — Comentário `// adiciona item` é redundante**

Mesmo com o nome ruim `add`, o comentário não agrega nenhuma informação que já não esteja implícita. Com um nome expressivo (`adicionarItem`), o comentário se torna ainda mais desnecessário.

Sugestão: remova o comentário. Deixe o nome do método comunicar a intenção.

---

**Linha 50 — TODO sem rastreabilidade: `// TODO: implementar desconto fidelidade`**

Não há ticket, responsável ou prazo. Esse TODO vai ficar aqui indefinidamente.

Sugestão: `// TODO [LANCH-42]: implementar lógica de desconto para clientes fidelidade. Responsável: @dev-backend | Prazo: Sprint 18`.

---

**Linhas 63-65 — Código comentado sem explicação**

Três linhas de código morto (`db.save`, `notificarCozinha`, `enviarSms`) sem nenhum contexto. O leitor não sabe se foi removido por um bug, se está planejado para voltar ou se já foi movido para outro lugar.

Sugestão: remova o código morto. Se for algo planejado, crie um TODO rastreável.

---

**Linhas 86-88 — Diário de bordo em comentário**

O histórico de alterações do método `_log` pertence ao controle de versão, não ao código.

Sugestão: remova as três linhas de comentário. Use `git log -p -- codigo_para_revisar.ts` para ver o histórico real.

---

## Categoria: Formatação

---

**Linha 15 — Tipo de `p` usa `Record` com tipo de valor inline complexo**

`Record<string, { id: string; n: string; p: number; qt: number }>` declara o tipo inline e ainda usa nomes de campo ruins (`n`, `p`). Isso compromete tanto a legibilidade quanto a reutilização do tipo.

Sugestão:
```typescript
interface ItemPedido {
    id: string;
    nome: string;
    preco: number;
    quantidade: number;
}
```
E use `itensPedidoAtual: Record<string, ItemPedido>`.

---

**Linha 67 — Construção do `num` com regex complexo inline**

`new Date().toISOString().replace(/[-T:.Z]/g, '').slice(0, 14)` é difícil de ler e de testar. A intenção é gerar um timestamp compacto.

Sugestão: extraia `private _gerarNumeroDePedido(): string` para isolar e nomear essa lógica.

---

> **Total: 15 comentários de review**
> Distribuição: 6 Nomes · 4 Funções · 4 Comentários · 2 Formatação
