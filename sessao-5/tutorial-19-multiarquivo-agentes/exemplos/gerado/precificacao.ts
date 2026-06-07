/**
 * Saída do agente de IA — Módulo de Precificação (carrinho de compras)
 * Referência: Tutorial 11 — Geração multi-arquivo com agentes
 * Execute: npx ts-node precificacao.ts
 *
 * ATENÇÃO: saída de agente após mudança multi-arquivo — inconsistência cross-file presente.
 * O agente recebeu a tarefa "adicionar suporte a cupom de desconto ao carrinho".
 * Ele atualizou ESTE arquivo corretamente: calcularTotal agora exige um segundo
 * argumento 'cupom: Cupom | null' (sem valor padrão / sem "?").
 *
 * INCONSISTÊNCIA CROSS-FILE: carrinho.ts ainda chama calcularTotal(itens) —
 * sem o argumento 'cupom'. O TypeScript acusaria erro de compilação em um
 * build integrado. Cada arquivo roda sua própria demo sem erro; a inconsistência
 * só aparece ao revisar o diff de ambos os arquivos juntos.
 * Veja exemplos/diff-comentado.md.
 */

// ─── Interfaces ───────────────────────────────────────────────────────────────

interface ItemCarrinho {
  produtoId:     string;
  descricao:     string;
  precoUnitario: number;
  quantidade:    number;
}

interface Cupom {
  codigo:              string;
  percentualDesconto:  number;  // 0.0 a 1.0
}

// ─── Constantes ───────────────────────────────────────────────────────────────

const CUPONS_VALIDOS: Record<string, Cupom> = {
  BEMVINDO10:    { codigo: "BEMVINDO10",    percentualDesconto: 0.10 },
  BLACKFRIDAY20: { codigo: "BLACKFRIDAY20", percentualDesconto: 0.20 },
};

// ─── Operações de precificação ────────────────────────────────────────────────

function subtotalItem(item: ItemCarrinho): number {
  return Math.round(item.precoUnitario * item.quantidade * 100) / 100;
}

function resolverCupom(codigo: string): Cupom | null {
  return CUPONS_VALIDOS[codigo.toUpperCase()] ?? null;
}

/**
 * Calcula o valor total aplicando desconto do cupom.
 *
 * MUDANÇA: 'cupom' agora é obrigatório (sem '?', sem valor padrão).
 * Chamadores que omitirem este argumento terão erro de compilação TypeScript.
 * carrinho.ts ainda chama calcularTotal(itens) → TS2554: Expected 2 arguments.
 */
function calcularTotal(
  itens: ItemCarrinho[],
  cupom: Cupom | null,   // ← ASSINATURA NOVA — agente adicionou; obrigatório
): number {
  if (itens.length === 0) {
    throw new Error("A lista de itens não pode ser vazia");
  }

  const bruto = itens.reduce((acc, i) => acc + subtotalItem(i), 0);

  if (cupom === null) {
    return Math.round(bruto * 100) / 100;
  }

  const desconto = Math.round(bruto * cupom.percentualDesconto * 100) / 100;
  return Math.round((bruto - desconto) * 100) / 100;
}

function formatarResumo(itens: ItemCarrinho[], cupom: Cupom | null): string {
  const bruto = itens.reduce((acc, i) => acc + subtotalItem(i), 0);
  const total = calcularTotal(itens, cupom);
  if (cupom !== null) {
    const desconto = Math.round((bruto - total) * 100) / 100;
    return (
      `Subtotal: R$ ${bruto.toFixed(2)} | ` +
      `Desconto ${cupom.codigo} (-${(cupom.percentualDesconto * 100).toFixed(0)}%): ` +
      `-R$ ${desconto.toFixed(2)} | ` +
      `Total: R$ ${total.toFixed(2)}`
    );
  }
  return `Subtotal: R$ ${bruto.toFixed(2)} | Total: R$ ${total.toFixed(2)}`;
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

const itensDemo: ItemCarrinho[] = [
  { produtoId: "P001", descricao: "Teclado mecânico",  precoUnitario: 349.90, quantidade: 1 },
  { produtoId: "P002", descricao: "Mouse sem fio",      precoUnitario:  89.90, quantidade: 2 },
  { produtoId: "P003", descricao: "Mousepad XL",        precoUnitario:  49.90, quantidade: 1 },
];

console.log("=== Precificação (saída do agente — assinatura nova com cupom) ===\n");

console.log("Itens do carrinho:");
itensDemo.forEach(item => {
  console.log(
    `  ${item.descricao}: R$ ${item.precoUnitario.toFixed(2)} x ${item.quantidade}` +
    ` = R$ ${subtotalItem(item).toFixed(2)}`
  );
});
console.log();

// Sem cupom
console.log(formatarResumo(itensDemo, null));

// Com cupom BEMVINDO10 (10%)
const cupomBv = resolverCupom("BEMVINDO10");
console.log(formatarResumo(itensDemo, cupomBv));

// Com cupom BLACKFRIDAY20 (20%)
const cupomBf = resolverCupom("BLACKFRIDAY20");
console.log(formatarResumo(itensDemo, cupomBf));

// Cupom inválido → null → sem desconto
const cupomInv = resolverCupom("INVALIDO");
console.log(`Cupom 'INVALIDO' → ${cupomInv} → sem desconto`);
console.log(formatarResumo(itensDemo, cupomInv));

console.log();
console.log("Assinatura NOVA (este arquivo): calcularTotal(itens, cupom)");
console.log("Assinatura ANTIGA (carrinho.ts): calcularTotal(itens)  <- inconsistência cross-file");
console.log("Ver exemplos/diff-comentado.md para o diff anotado.");
