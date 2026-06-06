/**
 * Exercício — Módulo de Carrinho de Compras com Frete (chamador não atualizado)
 * Referência: Tutorial 11 — Geração multi-arquivo com agentes
 * Execute: npx ts-node exercicio_carrinho.ts
 *
 * INSTRUÇÕES:
 *   (1) Execute este arquivo e exercicio_precificacao.ts separadamente — ambos rodam sem erro.
 *   (2) Revise o diff entre os dois arquivos como se estivesse revisando uma mudança
 *       de agente em altitude: olhe os dois juntos, não isoladamente.
 *   (3) Ache a inconsistência cross-file: onde a assinatura mudou mas o chamador não acompanhou?
 *   (4) Corrija a mudança e compare com gabarito_carrinho.ts e gabarito_precificacao.ts.
 *
 * CONTEXTO: o agente recebeu a tarefa "adicionar cálculo de frete ao pedido".
 * Ele adicionou o campo 'regiao' ao Pedido e atualizou precificacao.ts corretamente.
 * Mas NÃO atualizou todos os chamadores neste arquivo.
 *
 * A inconsistência está em fecharPedido — revise o diff dos dois arquivos juntos.
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
  regiao: string;   // ← campo adicionado pelo agente
}

interface ResumoPedido {
  pedidoId: string;
  qtdItens: number;
  regiao:   string;
  total:    number;
}

// ─── Lógica de precificação (versão local — NÃO atualizada pelo agente) ────────
// Em produção o código chamaria calcularTotalPedido de precificacao.ts assim:
//
//   import { calcularTotalPedido } from "./precificacao";
//   const resultado = calcularTotalPedido(pedido.itens);  // <- CHAMADA ANTIGA — falta regiao
//
// A nova assinatura exige: calcularTotalPedido(itens, regiao)
// ⚠️  INCONSISTÊNCIA CROSS-FILE: fecharPedido não foi atualizado pelo agente.

function _subtotalItem(item: ItemPedido): number {
  return Math.round(item.precoUnitario * item.quantidade * 100) / 100;
}

function _calcularTotalLocal(itens: ItemPedido[]): number {
  if (itens.length === 0) throw new Error("A lista de itens não pode ser vazia");
  const bruto = itens.reduce((acc, i) => acc + _subtotalItem(i), 0);
  return Math.round(bruto * 100) / 100;
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
   * BUG LATENTE: em produção isto chamaria calcularTotalPedido de precificacao.ts.
   * Como o agente atualizou a assinatura mas não atualizou este chamador,
   * a chamada seria:
   *
   *   const resultado = calcularTotalPedido(pedido.itens);  // TS2554: Expected 2 args, got 1
   *
   * O resultado: pedido.regiao é ignorado — o frete nunca é calculado.
   * O total não inclui frete, mesmo que a região esteja definida.
   */
  const total = _calcularTotalLocal(pedido.itens);  // ← versão antiga (sem frete)

  return {
    pedidoId: pedido.id,
    qtdItens: pedido.itens.reduce((acc, i) => acc + i.quantidade, 0),
    regiao:   pedido.regiao,
    total,
    // ⚠️  frete não incluído — inconsistência cross-file
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
    linhas.push(`  Região:   ${pedido.regiao} (frete não calculado — inconsistência)`);
  }
  return linhas.join("\n");
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

const pedido = criarPedido("P-2026-042");

adicionarItem(pedido, { produtoId: "P001", descricao: "Teclado mecânico", precoUnitario:  89.90, quantidade: 1 });
adicionarItem(pedido, { produtoId: "P002", descricao: "Mouse sem fio",    precoUnitario:  49.90, quantidade: 2 });

definirRegiao(pedido, "nordeste");

console.log("=== Carrinho de Compras com Frete (exercício — chamador não atualizado) ===\n");
console.log(formatarPedido(pedido));
console.log();

const resumo = fecharPedido(pedido);
const subtotal = pedido.itens.reduce((acc, i) => acc + _subtotalItem(i), 0);
const freteNordeste = FRETE_POR_REGIAO["nordeste"];
const esperado = Math.round((subtotal + freteNordeste) * 100) / 100;

console.log("Resumo do pedido:");
console.log(`  Pedido:   ${resumo.pedidoId}`);
console.log(`  Itens:    ${resumo.qtdItens}`);
console.log(`  Região:   ${resumo.regiao}`);
console.log(`  Total:    R$ ${resumo.total.toFixed(2)}  <- ERRADO: frete nordeste (R$ ${freteNordeste.toFixed(2)}) não incluído`);
console.log(`  Esperado: R$ ${esperado.toFixed(2)}  (subtotal R$ ${subtotal.toFixed(2)} + frete R$ ${freteNordeste.toFixed(2)})`);

console.log();
console.log("DICA: revise o diff de exercicio_precificacao.ts e exercicio_carrinho.ts juntos.");
console.log("A inconsistência está em fecharPedido — qual argumento está faltando?");
