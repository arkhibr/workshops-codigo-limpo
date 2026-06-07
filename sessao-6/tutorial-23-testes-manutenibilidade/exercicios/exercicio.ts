/**
 * exercicio.ts — Cálculo de desconto de fidelidade por faixas de tempo.
 *
 * Código funcional sem testes de caracterização.
 * Tarefa:
 *   (1) Escreva os testes de caracterização incluindo as bordas exatas de cada faixa.
 *   (2) Só então peça à IA que adicione uma nova faixa (clientes > 36 meses: 20%).
 *   (3) Rode a suite antes e depois — compare os resultados.
 *
 * Execute: npx ts-node exercicio.ts
 */

// ---------------------------------------------------------------------------
// Constantes de domínio
// ---------------------------------------------------------------------------

const DESCONTO_NOVATO    = 0.00;   // clientes com menos de 6 meses — sem desconto
const DESCONTO_INICIANTE = 0.05;   // clientes de 6 a 11 meses — 5%
const DESCONTO_REGULAR   = 0.10;   // clientes de 12 a 23 meses — 10%
const DESCONTO_FIEL      = 0.15;   // clientes com 24 meses ou mais — 15%

// ---------------------------------------------------------------------------
// Lógica de desconto
// ---------------------------------------------------------------------------

/**
 * Calcula o desconto de fidelidade com base no tempo como cliente.
 *
 * Faixas de fidelidade:
 *   - até 5 meses: sem desconto (0%)
 *   - 6 a 11 meses: desconto de 5%
 *   - 12 a 23 meses: desconto de 10%
 *   - 24 meses ou mais: desconto de 15%
 *
 * Retorna o valor do desconto em reais (não o valor final da compra).
 */
function calcularDescontoFidelidade(mesesCliente: number, valorCompra: number): number {
  if (mesesCliente < 0) {
    throw new Error(`mesesCliente inválido: ${mesesCliente}. Deve ser zero ou maior.`);
  }
  if (valorCompra <= 0) {
    throw new Error(`valorCompra inválido: ${valorCompra}. Deve ser maior que zero.`);
  }

  let percentual: number;
  if (mesesCliente < 6) {
    percentual = DESCONTO_NOVATO;
  } else if (mesesCliente < 12) {
    percentual = DESCONTO_INICIANTE;
  } else if (mesesCliente < 24) {
    percentual = DESCONTO_REGULAR;
  } else {
    percentual = DESCONTO_FIEL;
  }

  const desconto = valorCompra * percentual;
  return Math.round(desconto * 100) / 100;
}

function descricaoFidelidade(mesesCliente: number): string {
  if (mesesCliente < 0)  return "inválido";
  if (mesesCliente < 6)  return "novato (até 5 meses)";
  if (mesesCliente < 12) return "iniciante (6 a 11 meses)";
  if (mesesCliente < 24) return "regular (12 a 23 meses)";
  return "fiel (24 meses ou mais)";
}

// ---------------------------------------------------------------------------
// Demo — comportamento atual sem testes de caracterização
// ---------------------------------------------------------------------------

function demonstrarDescontos(): void {
  const clientes: Array<[number, number, string]> = [
    [3,  200.00, "cliente novo"],
    [9,  200.00, "cliente iniciante"],
    [18, 200.00, "cliente regular"],
    [30, 200.00, "cliente fiel"],
  ];

  console.log("Descontos por fidelidade (valor de compra: R$ 200,00):");
  console.log("  " + "Meses".padStart(6) + "  " + "Categoria".padEnd(28) + "  " +
              "Desconto".padStart(10) + "  " + "Valor final".padStart(12));
  console.log("  " + "-".repeat(64));
  for (const [meses, valor, _rotulo] of clientes) {
    const desconto = calcularDescontoFidelidade(meses, valor);
    const categoria = descricaoFidelidade(meses);
    const final = valor - desconto;
    console.log("  " + String(meses).padStart(6) + "  " + categoria.padEnd(28) +
                "  " + `R$${desconto.toFixed(2)}`.padStart(10) +
                "  " + `R$${final.toFixed(2)}`.padStart(12));
  }
  console.log();

  console.log("Dica para o exercício: quais valores de 'mesesCliente' são as fronteiras");
  console.log("exatas entre as faixas? Esses são os casos que a sua suite precisa cobrir.");
  console.log();
}

// ─── Execução ────────────────────────────────────────────────────────────────

console.log("=== Desconto de Fidelidade — exercício de caracterização ===\n");

demonstrarDescontos();

console.log("TODO: escreva as funções verificar*() cobrindo mid-band E bordas exatas.");
console.log("Fronteiras a cobrir: 5/6, 11/12 e 23/24 meses.");
console.log("Só depois de ter a suite passando, peça à IA que adicione a faixa > 36 meses.");
