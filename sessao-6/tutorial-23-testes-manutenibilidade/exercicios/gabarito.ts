/**
 * gabarito.ts — Desconto de fidelidade com suite completa e nova faixa (> 36 meses).
 *
 * Demonstra:
 *   (1) Suite de caracterização completa — mid-band E bordas exatas de cada faixa.
 *   (2) Nova faixa adicionada corretamente (> 36 meses: 20%) sem regressão.
 *   (3) Todos os casos da suite passam com o código corrigido.
 *
 * Execute: npx ts-node gabarito.ts
 */

// ---------------------------------------------------------------------------
// Constantes de domínio
// ---------------------------------------------------------------------------

const DESCONTO_NOVATO    = 0.00;   // clientes com menos de 6 meses — sem desconto
const DESCONTO_INICIANTE = 0.05;   // clientes de 6 a 11 meses — 5%
const DESCONTO_REGULAR   = 0.10;   // clientes de 12 a 23 meses — 10%
const DESCONTO_FIEL      = 0.15;   // clientes de 24 a 36 meses — 15%
const DESCONTO_VETERANO  = 0.20;   // clientes com mais de 36 meses — 20% (nova faixa)

// ---------------------------------------------------------------------------
// Lógica de desconto (nova faixa adicionada corretamente)
// ---------------------------------------------------------------------------

/**
 * Calcula o desconto de fidelidade com base no tempo como cliente.
 *
 * Faixas de fidelidade:
 *   - até 5 meses: sem desconto (0%)
 *   - 6 a 11 meses: desconto de 5%
 *   - 12 a 23 meses: desconto de 10%
 *   - 24 a 36 meses: desconto de 15%
 *   - acima de 36 meses: desconto de 20% (nova faixa)
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
  } else if (mesesCliente <= 36) {
    percentual = DESCONTO_FIEL;
  } else {
    percentual = DESCONTO_VETERANO;
  }

  const desconto = valorCompra * percentual;
  return Math.round(desconto * 100) / 100;
}

function descricaoFidelidade(mesesCliente: number): string {
  if (mesesCliente < 0)   return "inválido";
  if (mesesCliente < 6)   return "novato (até 5 meses)";
  if (mesesCliente < 12)  return "iniciante (6 a 11 meses)";
  if (mesesCliente < 24)  return "regular (12 a 23 meses)";
  if (mesesCliente <= 36) return "fiel (24 a 36 meses)";
  return "veterano (acima de 36 meses)";
}

// ---------------------------------------------------------------------------
// Suite COMPLETA de caracterização (inclui bordas exatas)
// ---------------------------------------------------------------------------

function verificarFaixaNovato(): void {
  const casos: Array<[number, number, number, string]> = [
    [0,  200.00,  0.00, "0 meses — borda inferior (início absoluto)"],
    [3,  200.00,  0.00, "3 meses — faixa novato mid-band"],
    [5,  200.00,  0.00, "5 meses — borda superior faixa novato"],
  ];
  for (const [meses, valor, esperado, descricao] of casos) {
    const obtido = calcularDescontoFidelidade(meses, valor);
    if (Math.abs(obtido - esperado) < 0.001) {
      console.log(`OK: ${descricao}`);
    } else {
      console.log(`FALHOU: ${descricao} (esperado ${esperado.toFixed(2)}, obtido ${obtido.toFixed(2)})`);
    }
  }
}

function verificarFaixaIniciante(): void {
  const casos: Array<[number, number, number, string]> = [
    [6,  200.00, 10.00, "6 meses — borda inferior faixa iniciante"],
    [9,  200.00, 10.00, "9 meses — faixa iniciante mid-band"],
    [11, 200.00, 10.00, "11 meses — borda superior faixa iniciante"],
  ];
  for (const [meses, valor, esperado, descricao] of casos) {
    const obtido = calcularDescontoFidelidade(meses, valor);
    if (Math.abs(obtido - esperado) < 0.001) {
      console.log(`OK: ${descricao}`);
    } else {
      console.log(`FALHOU: ${descricao} (esperado ${esperado.toFixed(2)}, obtido ${obtido.toFixed(2)})`);
    }
  }
}

function verificarFaixaRegular(): void {
  const casos: Array<[number, number, number, string]> = [
    [12, 200.00, 20.00, "12 meses — borda inferior faixa regular"],
    [18, 200.00, 20.00, "18 meses — faixa regular mid-band"],
    [23, 200.00, 20.00, "23 meses — borda superior faixa regular"],
  ];
  for (const [meses, valor, esperado, descricao] of casos) {
    const obtido = calcularDescontoFidelidade(meses, valor);
    if (Math.abs(obtido - esperado) < 0.001) {
      console.log(`OK: ${descricao}`);
    } else {
      console.log(`FALHOU: ${descricao} (esperado ${esperado.toFixed(2)}, obtido ${obtido.toFixed(2)})`);
    }
  }
}

function verificarFaixaFiel(): void {
  const casos: Array<[number, number, number, string]> = [
    [24, 200.00, 30.00, "24 meses — borda inferior faixa fiel"],
    [30, 200.00, 30.00, "30 meses — faixa fiel mid-band"],
    [36, 200.00, 30.00, "36 meses — borda superior faixa fiel"],
  ];
  for (const [meses, valor, esperado, descricao] of casos) {
    const obtido = calcularDescontoFidelidade(meses, valor);
    if (Math.abs(obtido - esperado) < 0.001) {
      console.log(`OK: ${descricao}`);
    } else {
      console.log(`FALHOU: ${descricao} (esperado ${esperado.toFixed(2)}, obtido ${obtido.toFixed(2)})`);
    }
  }
}

function verificarFaixaVeterano(): void {
  const casos: Array<[number, number, number, string]> = [
    [37, 200.00, 40.00, "37 meses — borda inferior faixa veterano"],
    [48, 200.00, 40.00, "48 meses — faixa veterano mid-band"],
    [60, 200.00, 40.00, "60 meses — faixa veterano extremo"],
  ];
  for (const [meses, valor, esperado, descricao] of casos) {
    const obtido = calcularDescontoFidelidade(meses, valor);
    if (Math.abs(obtido - esperado) < 0.001) {
      console.log(`OK: ${descricao}`);
    } else {
      console.log(`FALHOU: ${descricao} (esperado ${esperado.toFixed(2)}, obtido ${obtido.toFixed(2)})`);
    }
  }
}

function verificarEntradasInvalidas(): void {
  const casosInvalidos: Array<[number, number, string]> = [
    [-1,   200.00, "meses negativos"],
    [12,     0.00, "valor de compra zero"],
    [12,   -50.00, "valor de compra negativo"],
  ];
  for (const [meses, valor, descricao] of casosInvalidos) {
    try {
      calcularDescontoFidelidade(meses, valor);
      console.log(`FALHOU: ${descricao} — deveria lançar Error, mas não lançou`);
    } catch (_e) {
      console.log(`OK: ${descricao} — Error lançado corretamente`);
    }
  }
}

// ---------------------------------------------------------------------------
// Demo
// ---------------------------------------------------------------------------

function demonstrarDescontos(): void {
  const clientes: Array<[number, number]> = [
    [3,  500.00],
    [9,  500.00],
    [18, 500.00],
    [30, 500.00],
    [48, 500.00],
  ];

  console.log("Descontos por fidelidade (valor de compra: R$ 500,00):");
  console.log("  " + "Meses".padStart(6) + "  " + "Categoria".padEnd(32) + "  " +
              "Desconto".padStart(10) + "  " + "Valor final".padStart(12));
  console.log("  " + "-".repeat(68));
  for (const [meses, valor] of clientes) {
    const desconto = calcularDescontoFidelidade(meses, valor);
    const categoria = descricaoFidelidade(meses);
    const final = valor - desconto;
    console.log("  " + String(meses).padStart(6) + "  " + categoria.padEnd(32) +
                "  " + `R$${desconto.toFixed(2)}`.padStart(10) +
                "  " + `R$${final.toFixed(2)}`.padStart(12));
  }
  console.log();
}

// ─── Execução ────────────────────────────────────────────────────────────────

console.log("=== Desconto de Fidelidade — gabarito com suite completa ===\n");

demonstrarDescontos();

console.log("--- Verificações completas (incluindo bordas e nova faixa) ---");
verificarFaixaNovato();
verificarFaixaIniciante();
verificarFaixaRegular();
verificarFaixaFiel();
verificarFaixaVeterano();
verificarEntradasInvalidas();
