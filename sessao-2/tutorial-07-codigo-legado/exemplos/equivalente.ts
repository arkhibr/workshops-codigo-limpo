/**
 * TUTORIAL 07 — Código Legado em TypeScript
 * Conceito: Strangler Fig Pattern
 *
 * O padrão Strangler Fig (Martin Fowler) permite substituir código
 * legado gradualmente: a nova implementação coexiste com a antiga
 * via uma interface compartilhada. O cliente não sabe qual versão está
 * usando — a migração acontece sem big bang, sem reescrita total.
 *
 * Nome: vem da figueira-estranguladora, que cresce sobre uma árvore
 * existente até substituí-la completamente, sem derrubar a original.
 */

// ==========================================================================
// Contrato compartilhado — a interface que tanto legado quanto nova
// implementação precisam honrar
// ==========================================================================

interface Pedido {
  id: string;
  clienteId: string;
  valor: number;
  itens: string[];
}

interface ResultadoPedido {
  pedidoId: string;
  total: number;
  status: string;
}

interface ProcessadorDePedidos {
  processar(pedido: Pedido): ResultadoPedido;
}


// ==========================================================================
// ANTES — chamada direta ao código legado (sem interface, sem substituição)
// O problema: ClienteCheckout está acoplado diretamente à implementação
// legada. Não há como migrar sem alterar ClienteCheckout.
// ==========================================================================

class ProcessadorLegado {
  processar(pedido: Pedido): ResultadoPedido {
    // Lógica antiga: tudo em um lugar, regras enterradas
    const imposto = pedido.valor * 0.12;
    const total = pedido.valor + imposto;
    console.log(`[LEGADO] Pedido ${pedido.id} processado. Total: R$ ${total.toFixed(2)}`);
    return { pedidoId: pedido.id, total, status: "PROCESSADO_LEGADO" };
  }
}

// Acoplamento direto — ClienteCheckoutLegado não pode ser migrado sem edição
class ClienteCheckoutLegado {
  private processador = new ProcessadorLegado(); // instanciação direta

  finalizar(pedido: Pedido): void {
    const resultado = this.processador.processar(pedido);
    console.log(`Checkout finalizado: ${resultado.status}`);
  }
}


// ==========================================================================
// DEPOIS — Strangler Fig via interface compartilhada
// Passo 1: extrair interface do legado
// Passo 2: nova implementação satisfaz a mesma interface
// Passo 3: roteador decide qual usar (feature flag, percentual, etc.)
// Passo 4: quando nova implementação estiver estável, remover o legado
// ==========================================================================

// Legado agora implementa a interface (sem alterar sua lógica interna)
class ProcessadorLegadoV2 implements ProcessadorDePedidos {
  processar(pedido: Pedido): ResultadoPedido {
    const imposto = pedido.valor * 0.12;
    const total = pedido.valor + imposto;
    console.log(`[LEGADO] Pedido ${pedido.id} processado. Total: R$ ${total.toFixed(2)}`);
    return { pedidoId: pedido.id, total, status: "PROCESSADO_LEGADO" };
  }
}

// Nova implementação: mesma interface, lógica melhorada
class ProcessadorNovo implements ProcessadorDePedidos {
  processar(pedido: Pedido): ResultadoPedido {
    // Nova lógica: impostos por faixa, desconto para muitos itens
    const aliquota = pedido.valor > 5000 ? 0.10 : 0.12;
    const imposto = pedido.valor * aliquota;
    const desconto = pedido.itens.length > 5 ? pedido.valor * 0.02 : 0;
    const total = pedido.valor + imposto - desconto;
    console.log(`[NOVO] Pedido ${pedido.id} processado. Total: R$ ${total.toFixed(2)}`);
    return { pedidoId: pedido.id, total, status: "PROCESSADO_NOVO" };
  }
}

// Roteador — o "estrangulador": decide qual implementação usar
// Permite migração gradual sem alterar o código cliente
class RoteadorDePedidos implements ProcessadorDePedidos {
  constructor(
    private legado: ProcessadorDePedidos,
    private novo: ProcessadorDePedidos,
    private usarNovo: (pedido: Pedido) => boolean
  ) {}

  processar(pedido: Pedido): ResultadoPedido {
    if (this.usarNovo(pedido)) {
      return this.novo.processar(pedido);
    }
    return this.legado.processar(pedido);
  }
}

// O cliente só enxerga a interface — não sabe que existe um roteador
class ClienteCheckout {
  constructor(private processador: ProcessadorDePedidos) {}

  finalizar(pedido: Pedido): void {
    const resultado = this.processador.processar(pedido);
    console.log(`Checkout finalizado: ${resultado.status}`);
  }
}


// ==========================================================================
// Demonstração
// ==========================================================================

const pedidoPequeno: Pedido = { id: "P001", clienteId: "C001", valor: 1000, itens: ["A", "B"] };
const pedidoGrande: Pedido = { id: "P002", clienteId: "C002", valor: 8000, itens: ["A", "B", "C", "D", "E", "F"] };

console.log("=== ANTES: acoplamento direto ao legado ===");
const checkoutLegado = new ClienteCheckoutLegado();
checkoutLegado.finalizar(pedidoPequeno);

console.log("\n=== DEPOIS: Strangler Fig com migração gradual ===");

// Estratégia: pedidos acima de R$ 5.000 vão para nova implementação
const roteador = new RoteadorDePedidos(
  new ProcessadorLegadoV2(),
  new ProcessadorNovo(),
  (pedido) => pedido.valor > 5000
);

const checkout = new ClienteCheckout(roteador);

console.log("-- Pedido pequeno (vai para legado) --");
checkout.finalizar(pedidoPequeno);

console.log("-- Pedido grande (vai para novo) --");
checkout.finalizar(pedidoGrande);

console.log("\n=== Migração completa: 100% no novo ===");
const checkoutNovo = new ClienteCheckout(new ProcessadorNovo());
checkoutNovo.finalizar(pedidoPequeno);
checkoutNovo.finalizar(pedidoGrande);
