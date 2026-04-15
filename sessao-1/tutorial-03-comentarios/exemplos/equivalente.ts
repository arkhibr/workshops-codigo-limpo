/**
 * EQUIVALENTE TypeScript — Comentários
 * Referência: Clean Code, Cap. 4
 *
 * Foco: JSDoc mal usado vs bem usado, comentários redundantes em código tipado.
 */

// ════════════════════════════════════════════════════════════════
// PROBLEMA 1: JSDoc redundante em código TypeScript tipado
// ════════════════════════════════════════════════════════════════

// ❌ Ruim: TypeScript JÁ documenta os tipos — o JSDoc não adiciona nada
/**
 * Calcula o total.
 * @param preco - O preço do produto.
 * @param quantidade - A quantidade de produtos.
 * @returns O total calculado.
 */
function calcularTotal(preco: number, quantidade: number): number {
  return preco * quantidade;
}

// ✅ Bom: JSDoc só quando agrega contexto que o tipo não consegue expressar
/**
 * Aplica arredondamento bancário (half-even) ao valor.
 *
 * Diferente do arredondamento convencional, 2.5 arredonda para 2 e 3.5 para 4.
 * Isso neutraliza o viés acumulado em grandes volumes de transações financeiras.
 */
function aplicarArredondamentoBancario(valor: number): number {
  return Math.round(valor * 100) / 100;
}


// ════════════════════════════════════════════════════════════════
// PROBLEMA 2: Comentários redundantes em código bem tipado
// ════════════════════════════════════════════════════════════════

interface Pedido {
  id: string;
  status: "pendente" | "entregue" | "cancelado";
  total: number;
  criadoEm: Date;
}

// ❌ Ruim: o tipo já diz tudo — o comentário é ruído
function filtrarPedidos_ruim(
  pedidos: Pedido[],     // array de pedidos
  status: string,        // status a filtrar
): Pedido[] {            // retorna pedidos filtrados
  // filtra os pedidos pelo status
  return pedidos.filter((pedido) => pedido.status === status);
}

// ✅ Bom: sem comentários redundantes — o código é autodocumentado
function filtrarPedidosPorStatus(
  pedidos: Pedido[],
  status: Pedido["status"],
): Pedido[] {
  return pedidos.filter((pedido) => pedido.status === status);
}


// ════════════════════════════════════════════════════════════════
// PROBLEMA 3: Comentário enganoso vs. comentário de intenção
// ════════════════════════════════════════════════════════════════

const PRAZO_CANCELAMENTO_HORAS = 2;

// ❌ Ruim: comentário que mente sobre o comportamento
function podeSerCancelado_ruim(pedido: Pedido): boolean {
  // retorna false se o pedido puder ser cancelado
  const horasDecorridas =
    (Date.now() - pedido.criadoEm.getTime()) / (1000 * 3600);
  return horasDecorridas <= PRAZO_CANCELAMENTO_HORAS; // na verdade retorna true
}

// ✅ Bom: comentário explica a regra de negócio, não o código
function podeSerCancelado(pedido: Pedido): boolean {
  // Política comercial: cancelamento gratuito nas primeiras 2 horas após o pedido.
  // Após esse prazo, o pedido entra na fila de separação e não pode ser revertido.
  const horasDecorridas =
    (Date.now() - pedido.criadoEm.getTime()) / (1000 * 3600);
  return horasDecorridas <= PRAZO_CANCELAMENTO_HORAS;
}


// ════════════════════════════════════════════════════════════════
// PROBLEMA 4: TODO rastreável vs TODO sem contexto
// ════════════════════════════════════════════════════════════════

// ❌ Ruim
async function buscarUsuario_ruim(id: string) {
  // TODO: adicionar cache
  // TODO: melhorar isso
  return { id, nome: "Mock" };
}

// ✅ Bom
async function buscarUsuario(id: string) {
  // TODO [PLAT-1847]: substituir mock por chamada real ao serviço de usuários.
  // Responsável: @ana.souza  |  Prazo: Sprint 42
  return { id, nome: "Mock" };
}
