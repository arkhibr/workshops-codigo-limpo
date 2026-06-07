/**
 * Versão revisada — Módulo de Carrinho de Compras (consistente)
 * Referência: Tutorial 11 — Geração multi-arquivo com agentes
 * Execute: npx ts-node carrinho.ts
 *
 * Correção em relação a gerado/carrinho.ts:
 *   - finalizarCarrinho agora passa o cupom do carrinho para calcularTotal.
 *   - A assinatura de calcularTotal (em precificacao.ts) exige 'cupom' como
 *     segundo argumento; esta versão fornece corretamente o argumento.
 *   - O desconto do cupom é refletido no total — inconsistência resolvida.
 *
 * Diferença cross-file resolvida:
 *   ANTES: const total = _calcularTotalLocal(carrinho.itens)        <- ignorava cupom
 *   DEPOIS: const total = calcularTotal(carrinho.itens, carrinho.cupom)  <- correto
 */

// ─── Interfaces ───────────────────────────────────────────────────────────────

interface ItemCarrinho {
  produtoId:     string;
  descricao:     string;
  precoUnitario: number;
  quantidade:    number;
}

interface Cupom {
  codigo:             string;
  percentualDesconto: number;
}

interface Carrinho {
  id:    string;
  itens: ItemCarrinho[];
  cupom: Cupom | null;
}

interface ResumoCarrinho {
  carrinhoId:    string;
  qtdItens:      number;
  subtotal:      number;
  descontoCupom: number;
  total:         number;
  cupom:         string | null;
}

// ─── Lógica de precificação (alinhada com precificacao.ts) ───────────────────

function _subtotalItem(item: ItemCarrinho): number {
  return Math.round(item.precoUnitario * item.quantidade * 100) / 100;
}

/**
 * Cálculo de total com suporte a cupom.
 * Alinhado com a assinatura de calcularTotal em precificacao.ts.
 */
function calcularTotal(itens: ItemCarrinho[], cupom: Cupom | null): number {
  if (itens.length === 0) throw new Error("A lista de itens não pode ser vazia");
  const bruto = itens.reduce((acc, i) => acc + _subtotalItem(i), 0);
  if (cupom === null) return Math.round(bruto * 100) / 100;
  const desconto = Math.round(bruto * cupom.percentualDesconto * 100) / 100;
  return Math.round((bruto - desconto) * 100) / 100;
}

// ─── Operações de carrinho ────────────────────────────────────────────────────

function criarCarrinho(id: string): Carrinho {
  return { id, itens: [], cupom: null };
}

function adicionarItem(carrinho: Carrinho, item: ItemCarrinho): void {
  const existente = carrinho.itens.find(i => i.produtoId === item.produtoId);
  if (existente) {
    existente.quantidade += item.quantidade;
  } else {
    carrinho.itens.push({ ...item });
  }
}

function removerItem(carrinho: Carrinho, produtoId: string): void {
  carrinho.itens = carrinho.itens.filter(i => i.produtoId !== produtoId);
}

function aplicarCupom(carrinho: Carrinho, cupom: Cupom): void {
  carrinho.cupom = cupom;
}

function finalizarCarrinho(carrinho: Carrinho): ResumoCarrinho {
  /**
   * CORREÇÃO: total calculado com calcularTotal(itens, carrinho.cupom) —
   * agora passa o cupom corretamente; o desconto é refletido no total.
   */
  const bruto = carrinho.itens.reduce((acc, i) => acc + _subtotalItem(i), 0);
  const total = calcularTotal(carrinho.itens, carrinho.cupom);  // ← correto: passa cupom
  const descontoCupom = Math.round((bruto - total) * 100) / 100;

  return {
    carrinhoId:    carrinho.id,
    qtdItens:      carrinho.itens.reduce((acc, i) => acc + i.quantidade, 0),
    subtotal:      Math.round(bruto * 100) / 100,
    descontoCupom,
    total,
    cupom:         carrinho.cupom?.codigo ?? null,
  };
}

function formatarCarrinho(carrinho: Carrinho): string {
  const linhas: string[] = [`Carrinho ${carrinho.id}:`];
  for (const item of carrinho.itens) {
    linhas.push(
      `  [${item.produtoId}] ${item.descricao}: ` +
      `R$ ${item.precoUnitario.toFixed(2)} x ${item.quantidade} = ` +
      `R$ ${_subtotalItem(item).toFixed(2)}`
    );
  }
  const bruto = carrinho.itens.reduce((acc, i) => acc + _subtotalItem(i), 0);
  linhas.push(`  Subtotal: R$ ${bruto.toFixed(2)}`);
  if (carrinho.cupom) {
    linhas.push(
      `  Cupom: ${carrinho.cupom.codigo} (-${(carrinho.cupom.percentualDesconto * 100).toFixed(0)}%)`
    );
  }
  return linhas.join("\n");
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

const carrinho = criarCarrinho("C-2026-001");

adicionarItem(carrinho, { produtoId: "P001", descricao: "Teclado mecânico",  precoUnitario: 349.90, quantidade: 1 });
adicionarItem(carrinho, { produtoId: "P002", descricao: "Mouse sem fio",      precoUnitario:  89.90, quantidade: 2 });
adicionarItem(carrinho, { produtoId: "P003", descricao: "Mousepad XL",        precoUnitario:  49.90, quantidade: 1 });

console.log("=== Carrinho de Compras (revisado — desconto de cupom correto) ===\n");
console.log(formatarCarrinho(carrinho));
console.log();

const cupomBv: Cupom = { codigo: "BEMVINDO10", percentualDesconto: 0.10 };
aplicarCupom(carrinho, cupomBv);
console.log(`Cupom aplicado: ${carrinho.cupom!.codigo} (-10%)`);

const resumo = finalizarCarrinho(carrinho);
console.log("\nResumo final:");
console.log(`  Carrinho:  ${resumo.carrinhoId}`);
console.log(`  Itens:     ${resumo.qtdItens}`);
console.log(`  Subtotal:  R$ ${resumo.subtotal.toFixed(2)}`);
console.log(`  Desconto:  -R$ ${resumo.descontoCupom.toFixed(2)} (cupom ${resumo.cupom})`);
console.log(`  Total:     R$ ${resumo.total.toFixed(2)}  <- CORRETO: desconto de 10% aplicado`);

console.log();
console.log("Consistência: calcularTotal(itens, carrinho.cupom) — assinatura alinhada com precificacao.ts.");
