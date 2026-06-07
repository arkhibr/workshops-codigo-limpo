/**
 * Gabarito — Módulo de Precificação com Frete (consistente)
 * Referência: Tutorial 11 — Geração multi-arquivo com agentes
 * Execute: npx ts-node gabarito_precificacao.ts
 *
 * Este arquivo é idêntico a exercicio_precificacao.ts — a assinatura de
 * calcularTotalPedido já estava correta no exercício. A correção necessária
 * estava em exercicio_carrinho.ts (fecharPedido), que precisava passar 'regiao'.
 */

// ─── Constantes de frete ──────────────────────────────────────────────────────

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

interface ResultadoPedido {
  subtotal: number;
  frete:    number;
  total:    number;
  regiao:   string;
}

// ─── Operações de precificação ────────────────────────────────────────────────

function subtotalItem(item: ItemPedido): number {
  return Math.round(item.precoUnitario * item.quantidade * 100) / 100;
}

function calcularFrete(subtotal: number, regiao: string): number {
  const regiaonorm = regiao.toLowerCase().trim();
  if (!(regiaonorm in FRETE_POR_REGIAO)) {
    const regioes = Object.keys(FRETE_POR_REGIAO).sort().join(", ");
    throw new Error(`Região desconhecida: '${regiao}'. Regiões válidas: ${regioes}`);
  }
  if (subtotal >= FRETE_GRATIS_ACIMA) return 0;
  return FRETE_POR_REGIAO[regiaonorm];
}

function calcularTotalPedido(
  itens: ItemPedido[],
  regiao: string,
): ResultadoPedido {
  if (itens.length === 0) throw new Error("A lista de itens não pode ser vazia");

  const subtotal = itens.reduce((acc, i) => acc + subtotalItem(i), 0);
  const frete = calcularFrete(subtotal, regiao);
  const total = Math.round((subtotal + frete) * 100) / 100;

  return { subtotal: Math.round(subtotal * 100) / 100, frete, total, regiao };
}

function formatarResultado(resultado: ResultadoPedido): string {
  const linhas = [
    `  Região:   ${resultado.regiao}`,
    `  Subtotal: R$ ${resultado.subtotal.toFixed(2)}`,
  ];
  if (resultado.frete === 0) {
    linhas.push(`  Frete:    grátis (acima de R$ ${FRETE_GRATIS_ACIMA.toFixed(2)})`);
  } else {
    linhas.push(`  Frete:    R$ ${resultado.frete.toFixed(2)}`);
  }
  linhas.push(`  Total:    R$ ${resultado.total.toFixed(2)}`);
  return linhas.join("\n");
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

const itens: ItemPedido[] = [
  { produtoId: "P001", descricao: "Teclado mecânico", precoUnitario:  89.90, quantidade: 1 },
  { produtoId: "P002", descricao: "Mouse sem fio",    precoUnitario:  49.90, quantidade: 2 },
];

console.log("=== Precificação com Frete (gabarito — consistente com gabarito_carrinho.ts) ===\n");

console.log("Itens do pedido:");
itens.forEach(item => {
  console.log(
    `  ${item.descricao}: R$ ${item.precoUnitario.toFixed(2)} x ${item.quantidade}` +
    ` = R$ ${subtotalItem(item).toFixed(2)}`
  );
});
console.log();

// Nordeste (subtotal < 299 → frete cobrado)
const resultadoNe = calcularTotalPedido(itens, "nordeste");
console.log("Pedido — Nordeste:");
console.log(formatarResultado(resultadoNe));

console.log();

// Sudeste (subtotal < 299 → frete cobrado)
const resultadoSe = calcularTotalPedido(itens, "sudeste");
console.log("Pedido — Sudeste:")
console.log(formatarResultado(resultadoSe));

console.log();

// Região inválida
try {
  calcularTotalPedido(itens, "marte");
} catch (erro) {
  console.log(`Região inválida -> Error: ${(erro as Error).message}`);
}

console.log();
console.log("Consistência: gabarito_carrinho.ts chama calcularTotalPedido(itens, pedido.regiao).");
