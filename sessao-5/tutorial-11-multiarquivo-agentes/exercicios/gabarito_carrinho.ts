/**
 * Gabarito — Módulo de Carrinho de Compras com Frete (consistente)
 * Referência: Tutorial 11 — Geração multi-arquivo com agentes
 * Execute: npx ts-node gabarito_carrinho.ts
 *
 * Correção em relação a exercicio_carrinho.ts:
 *   - fecharPedido agora chama calcularTotalPedido(pedido.itens, pedido.regiao).
 *   - O frete da região é calculado e incluído no total retornado.
 *   - O dict de retorno expõe subtotal, frete e total separadamente.
 *
 * Diferença cross-file resolvida:
 *   ANTES: total = _calcularTotalLocal(pedido.itens)                    <- sem frete
 *   DEPOIS: resultado = calcularTotalPedido(itens, pedido.regiao)       <- com frete
 */

// ─── Constantes de frete (replicadas para auto-contenção) ─────────────────────

const FRETE_POR_REGIAO: Record<string, number> = {
  sudeste:    15.90,
  sul:        18.90,
  nordeste:   29.90,
  norte:      39.90,
  centroeste: 24.90,
};

const FRETE_GRATIS_ACIMA = 299.00;

// ─── Interfaces ───────────────────────────────────────────────────────────────

interface ItemPedido {
  produtoId:     string;
  descricao:     string;
  precoUnitario: number;
  quantidade:    number;
}

interface Pedido {
  id:     string;
  itens:  ItemPedido[];
  regiao: string;
}

interface ResumoPedido {
  pedidoId:  string;
  qtdItens:  number;
  regiao:    string;
  subtotal:  number;
  frete:     number;
  total:     number;
}

// ─── Lógica de precificação (alinhada com gabarito_precificacao.ts) ───────────

function _subtotalItem(item: ItemPedido): number {
  return Math.round(item.precoUnitario * item.quantidade * 100) / 100;
}

function _calcularFrete(subtotal: number, regiao: string): number {
  const regiaonorm = regiao.toLowerCase().trim();
  if (!(regiaonorm in FRETE_POR_REGIAO)) {
    const regioes = Object.keys(FRETE_POR_REGIAO).sort().join(", ");
    throw new Error(`Região desconhecida: '${regiao}'. Regiões válidas: ${regioes}`);
  }
  if (subtotal >= FRETE_GRATIS_ACIMA) return 0;
  return FRETE_POR_REGIAO[regiaonorm];
}

function calcularTotalPedido(itens: ItemPedido[], regiao: string): ResumoPedido {
  if (itens.length === 0) throw new Error("A lista de itens não pode ser vazia");
  const subtotal = itens.reduce((acc, i) => acc + _subtotalItem(i), 0);
  const frete = _calcularFrete(subtotal, regiao);
  return {
    pedidoId:  "",   // preenchido em fecharPedido
    qtdItens:  0,    // preenchido em fecharPedido
    regiao,
    subtotal:  Math.round(subtotal * 100) / 100,
    frete,
    total:     Math.round((subtotal + frete) * 100) / 100,
  };
}

// ─── Operações de pedido ──────────────────────────────────────────────────────

function criarPedido(id: string): Pedido {
  return { id, itens: [], regiao: "" };
}

function adicionarItem(pedido: Pedido, item: ItemPedido): void {
  const existente = pedido.itens.find(i => i.produtoId === item.produtoId);
  if (existente) {
    existente.quantidade += item.quantidade;
  } else {
    pedido.itens.push({ ...item });
  }
}

function definirRegiao(pedido: Pedido, regiao: string): void {
  pedido.regiao = regiao.toLowerCase().trim();
}

function fecharPedido(pedido: Pedido): ResumoPedido {
  /**
   * CORREÇÃO: chama calcularTotalPedido(pedido.itens, pedido.regiao) —
   * agora passa a região corretamente; o frete é incluído no total.
   */
  const resultado = calcularTotalPedido(pedido.itens, pedido.regiao);  // ← correto: passa regiao

  return {
    ...resultado,
    pedidoId: pedido.id,
    qtdItens: pedido.itens.reduce((acc, i) => acc + i.quantidade, 0),
  };
}

function formatarPedido(pedido: Pedido): string {
  const linhas: string[] = [`Pedido ${pedido.id}:`];
  for (const item of pedido.itens) {
    linhas.push(
      `  [${item.produtoId}] ${item.descricao}: ` +
      `R$ ${item.precoUnitario.toFixed(2)} x ${item.quantidade} = ` +
      `R$ ${_subtotalItem(item).toFixed(2)}`
    );
  }
  const subtotal = pedido.itens.reduce((acc, i) => acc + _subtotalItem(i), 0);
  linhas.push(`  Subtotal: R$ ${subtotal.toFixed(2)}`);
  if (pedido.regiao) {
    linhas.push(`  Região:   ${pedido.regiao}`);
  }
  return linhas.join("\n");
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

const pedido = criarPedido("P-2026-042");

adicionarItem(pedido, { produtoId: "P001", descricao: "Teclado mecânico", precoUnitario:  89.90, quantidade: 1 });
adicionarItem(pedido, { produtoId: "P002", descricao: "Mouse sem fio",    precoUnitario:  49.90, quantidade: 2 });

definirRegiao(pedido, "nordeste");

console.log("=== Carrinho de Compras com Frete (gabarito — total com frete correto) ===\n");
console.log(formatarPedido(pedido));
console.log();

const resumo = fecharPedido(pedido);
console.log("Resumo do pedido:");
console.log(`  Pedido:   ${resumo.pedidoId}`);
console.log(`  Itens:    ${resumo.qtdItens}`);
console.log(`  Região:   ${resumo.regiao}`);
console.log(`  Subtotal: R$ ${resumo.subtotal.toFixed(2)}`);
console.log(`  Frete:    R$ ${resumo.frete.toFixed(2)}  (nordeste)`);
console.log(`  Total:    R$ ${resumo.total.toFixed(2)}  <- CORRETO: frete incluído`);

console.log();

// Pedido com frete grátis
const pedido2 = criarPedido("P-2026-043");
adicionarItem(pedido2, { produtoId: "P010", descricao: 'Monitor 4K 27"', precoUnitario: 1_299.00, quantidade: 1 });
definirRegiao(pedido2, "sul");

const resumo2 = fecharPedido(pedido2);
console.log(`Pedido ${pedido2.id} — Sul, subtotal R$ ${resumo2.subtotal.toFixed(2)}:`);
console.log(`  Frete:    R$ ${resumo2.frete.toFixed(2)}  (grátis — acima de R$ ${FRETE_GRATIS_ACIMA.toFixed(2)})`);
console.log(`  Total:    R$ ${resumo2.total.toFixed(2)}`);

console.log();
console.log("Consistência: calcularTotalPedido(pedido.itens, pedido.regiao) — assinatura alinhada.");
