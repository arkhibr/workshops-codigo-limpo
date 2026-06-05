/**
 * SAÍDA TÍPICA DE IA — cálculo de preço com descontos (a partir de prompt fraco)
 * Referência: Clean Code, Cap. 2–3; engenharia de contexto em prompts de código
 *
 * ⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
 *     Representa o tipo de código que uma IA gera a partir de um prompt vago.
 *     Analise os problemas antes de ver a versão revisada.
 *
 * Execute: npx ts-node sessao-5/tutorial-09-engenharia-de-prompt/exemplos/preco_gerado.ts
 */

// Prompt usado: "calcula o preço com desconto"


function calc(x: number, y: string, q: number): number {  // o que é x? y? q?
  // aplica desconto
  if (q >= 5) {
    x = x * 0.9;  // número mágico — por que 0.9? o que representa?
  }
  if (y === "premium") {
    x = x * 0.85;  // outro número mágico — acumula com o anterior?
  }
  const total = x * q;
  return Math.round(total * 100) / 100;
}


function getPreco(items: any[]): number {  // nome em inglês; "items" — lista de quê?
  let result = 0;
  for (const i of items) {
    // i[0] = preco, i[1] = categoria, i[2] = quantidade
    result += calc(i[0], i[1], i[2]);  // acessa por índice — frágil
  }
  return result;
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

// item simples: preço 50.0, categoria "padrao", quantidade 3
const p1 = calc(50.0, "padrao", 3);
console.log("Preço item 1 (sem desconto):", p1);

// item com desconto por volume: quantidade 6
const p2 = calc(50.0, "padrao", 6);
console.log("Preço item 2 (desconto volume):", p2);

// item premium com volume: qual desconto prevalece?
const p3 = calc(50.0, "premium", 6);
console.log("Preço item 3 (premium + volume, acumulados):", p3);

// pedido com múltiplos itens
const pedido = [
  [50.0, "padrao", 3],
  [80.0, "premium", 2],
  [30.0, "padrao", 5],
];
const total = getPreco(pedido);
console.log("\nTotal do pedido:", total);
