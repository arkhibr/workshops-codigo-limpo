/**
 * Saída do agente de IA — Módulo de Carrinho de Compras
 * Referência: Tutorial 11 — Geração multi-arquivo com agentes
 * Execute: npx ts-node carrinho.ts
 *
 * ATENÇÃO: saída de agente após mudança multi-arquivo — inconsistência cross-file presente.
 * O agente recebeu a tarefa "adicionar suporte a cupom de desconto ao carrinho".
 * Ele atualizou precificacao.ts corretamente (nova assinatura com 'cupom'),
 * mas NÃO atualizou os chamadores neste arquivo.
 *
 * INCONSISTÊNCIA CROSS-FILE: finalizarCarrinho chama internamente calcularTotal(itens)
 * sem o argumento 'cupom'. Em um build integrado, o TypeScript acusaria:
 *   TS2554: Expected 2 arguments, but got 1.
 * O cupom está no Carrinho mas o desconto nunca chega ao total calculado.
 * Cada arquivo roda sua própria demo sem erro — a inconsistência só aparece
 * ao revisar o diff de ambos juntos. Veja exemplos/diff-comentado.md.
 */

// ─── Interfaces (replicadas para auto-contenção deste arquivo) ────────────────

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
  carrinhoId: string;
  qtdItens:   number;
  total:      number;
  cupom:      string | null;
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

function _subtotalItem(item: ItemCarrinho): number {
  return Math.round(item.precoUnitario * item.quantidade * 100) / 100;
}

// ── Função auxiliar local (NÃO atualizada pelo agente) ─────────────────────
// Esta versão foi copiada da lógica ANTERIOR (antes da mudança do agente).
// Em produção o código chamaria calcularTotal de precificacao.ts assim:
//
//   import { calcularTotal } from "./precificacao";
//   const total = calcularTotal(carrinho.itens);   // ← CHAMADA ANTIGA — falta cupom
//
// A nova assinatura exige: calcularTotal(itens, cupom)
// ⚠️  INCONSISTÊNCIA CROSS-FILE: este módulo não foi atualizado pelo agente.

function _calcularTotalLocal(itens: ItemCarrinho[]): number {
  if (itens.length === 0) throw new Error("A lista de itens não pode ser vazia");
  const bruto = itens.reduce((acc, i) => acc + _subtotalItem(i), 0);
  return Math.round(bruto * 100) / 100;
}

function finalizarCarrinho(carrinho: Carrinho): ResumoCarrinho {
  /**
   * BUG LATENTE: em produção isto chamaria calcularTotal de precificacao.ts.
   * Como o agente atualizou a assinatura mas não atualizou este chamador,
   * a chamada seria:
   *
   *   const total = calcularTotal(carrinho.itens);  // TS2554: Expected 2 args, got 1
   *
   * O resultado: carrinho.cupom é ignorado — o desconto nunca é aplicado.
   */
  const total = _calcularTotalLocal(carrinho.itens);  // ← usa versão antiga (sem cupom)

  return {
    carrinhoId: carrinho.id,
    qtdItens:   carrinho.itens.reduce((acc, i) => acc + i.quantidade, 0),
    total,
    cupom:      carrinho.cupom?.codigo ?? null,
    // ⚠️  total não reflete o desconto do cupom — inconsistência cross-file
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
    linhas.push(`  Cupom: ${carrinho.cupom.codigo} (não aplicado — inconsistência)`);
  }
  return linhas.join("\n");
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

const carrinho = criarCarrinho("C-2026-001");

adicionarItem(carrinho, { produtoId: "P001", descricao: "Teclado mecânico",  precoUnitario: 349.90, quantidade: 1 });
adicionarItem(carrinho, { produtoId: "P002", descricao: "Mouse sem fio",      precoUnitario:  89.90, quantidade: 2 });
adicionarItem(carrinho, { produtoId: "P003", descricao: "Mousepad XL",        precoUnitario:  49.90, quantidade: 1 });

console.log("=== Carrinho de Compras (saída do agente — chamador não atualizado) ===\n");
console.log(formatarCarrinho(carrinho));
console.log();

const cupomBv: Cupom = { codigo: "BEMVINDO10", percentualDesconto: 0.10 };
aplicarCupom(carrinho, cupomBv);
console.log(`Cupom aplicado: ${carrinho.cupom!.codigo} (-10%)`);

const resumo = finalizarCarrinho(carrinho);
console.log("\nResumo final:");
console.log(`  Carrinho: ${resumo.carrinhoId}`);
console.log(`  Itens:    ${resumo.qtdItens}`);
console.log(`  Cupom:    ${resumo.cupom}`);

const bruto = carrinho.itens.reduce((acc, i) => acc + _subtotalItem(i), 0);
const esperado = Math.round(bruto * 0.90 * 100) / 100;
console.log(`  Total:    R$ ${resumo.total.toFixed(2)}  <- ERRADO: desconto de 10% não foi aplicado`);
console.log(`  Esperado: R$ ${esperado.toFixed(2)}  (com 10% de desconto BEMVINDO10)`);

console.log();
console.log("A inconsistência cross-file: calcularTotal em precificacao.ts exige 'cupom'");
console.log("mas finalizarCarrinho chama a versão antiga sem esse argumento.");
console.log("O cupom está no carrinho mas o desconto nunca chega ao total.");
