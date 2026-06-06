/**
 * Revisão corrigida — Cálculo de Preço com Descontos
 * Referência: Tutorial 09 — Engenharia de contexto e prompt para gerar código
 * Execute: npx ts-node preco_revisado.ts
 *
 * Correção aplicada em relação a preco_gerado.ts:
 *   - Regra de negócio restaurada: aplica apenas o MAIOR desconto disponível,
 *     não a composição multiplicativa dos dois.
 *   - Demo idêntico ao gerado — resultado agora correto.
 */

// ─── Constantes de domínio ────────────────────────────────────────────────────

const DESCONTO_VOLUME_MEDIO      = 0.05;  // 5 % para 10–49 unidades
const DESCONTO_VOLUME_ALTO       = 0.10;  // 10 % para 50+ unidades
const DESCONTO_CATEGORIA_PREMIUM = 0.15;  // 15 % para categoria "premium"

const LIMIAR_VOLUME_MEDIO = 10;
const LIMIAR_VOLUME_ALTO  = 50;

// ─── Entidade ─────────────────────────────────────────────────────────────────

interface ItemPedido {
  produtoId:  string;
  categoria:  string;
  precoUnit:  number;
  quantidade: number;
}

// ─── Cálculo de preço ─────────────────────────────────────────────────────────

function calcularDescontoVolume(quantidade: number): number {
  if (quantidade >= LIMIAR_VOLUME_ALTO)  return DESCONTO_VOLUME_ALTO;
  if (quantidade >= LIMIAR_VOLUME_MEDIO) return DESCONTO_VOLUME_MEDIO;
  return 0.0;
}

function calcularDescontoCategoria(categoria: string): number {
  if (categoria === "premium") return DESCONTO_CATEGORIA_PREMIUM;
  return 0.0;
}

function calcularPrecoFinal(item: ItemPedido): number {
  /**
   * Calcula o preço final do item aplicando os descontos disponíveis.
   *
   * Regra de negócio: vale o MAIOR desconto — apenas um é aplicado.
   * Se o item for premium (15%) e tiver volume alto (10%), aplica 15%.
   */
  const subtotal = item.precoUnit * item.quantidade;

  const descontoVolume    = calcularDescontoVolume(item.quantidade);
  const descontoCategoria = calcularDescontoCategoria(item.categoria);

  // Regra correta: seleciona o MAIOR desconto disponível.
  const melhorDesconto = Math.max(descontoVolume, descontoCategoria);
  return subtotal * (1.0 - melhorDesconto);
}

function formatarResultado(item: ItemPedido, precoFinal: number): string {
  const subtotal = item.precoUnit * item.quantidade;
  const economia = subtotal - precoFinal;
  return (
    `  ${item.produtoId} (${item.categoria}): ` +
    `subtotal=R$${subtotal.toFixed(2)}  final=R$${precoFinal.toFixed(2)}  ` +
    `economia=R$${economia.toFixed(2)}`
  );
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

const itens: ItemPedido[] = [
  { produtoId: "P001", categoria: "eletronicos", precoUnit: 100.00, quantidade:  5 },  // sem desconto
  { produtoId: "P002", categoria: "eletronicos", precoUnit: 100.00, quantidade: 20 },  // só volume médio (5%)
  { produtoId: "P003", categoria: "premium",     precoUnit: 200.00, quantidade:  3 },  // só categoria (15%)
  { produtoId: "P004", categoria: "premium",     precoUnit: 200.00, quantidade: 60 },  // maior = categoria (15%)
];

console.log("=== Cálculo de Preço (revisado — regra de negócio correta) ===\n");

for (const item of itens) {
  const preco = calcularPrecoFinal(item);
  console.log(formatarResultado(item, preco));
}

console.log();
console.log("Caso crítico — P004 (premium, 60 unidades):");
const itemCritico = itens[3];
const subtotalCritico = itemCritico.precoUnit * itemCritico.quantidade;
const precoCorreto = calcularPrecoFinal(itemCritico);
const precoEsperado = subtotalCritico * (1.0 - DESCONTO_CATEGORIA_PREMIUM);
console.log(`  subtotal             = R$${subtotalCritico.toFixed(2)}`);
console.log(`  desconto maior (15%) = R$${(subtotalCritico * DESCONTO_CATEGORIA_PREMIUM).toFixed(2)}`);
console.log(`  preço esperado       = R$${precoEsperado.toFixed(2)}`);
console.log(`  preço calculado      = R$${precoCorreto.toFixed(2)}  <- CORRETO`);
