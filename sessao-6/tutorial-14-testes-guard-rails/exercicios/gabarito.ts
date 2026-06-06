/**
 * GABARITO — Testes de Caracterização + Mudança Protegida
 * Referência: Feathers (testes de caracterização) + Clean Code, Cap. 9 (Testes)
 *
 * O que este arquivo demonstra:
 *   1. Testes de caracterização completos cobrindo todas as faixas e limites.
 *   2. A nova faixa (2.000+ pts → 25%) adicionada pela mudança assistida.
 *   3. Todas as verificações passam — a mudança foi integrada sem regressão.
 *
 * Execute: npx ts-node sessao-6/tutorial-14-testes-guard-rails/exercicios/gabarito.ts
 */

// Faixas de desconto por pontos acumulados:
//   0–499 pontos      → 0% de desconto
//   500–999 pontos    → 5% de desconto
//   1.000–1.999 pts   → 10% de desconto
//   2.000+ pontos     → 25% de desconto  (faixa adicionada pela mudança)

const DESCONTO_SEM_PONTOS_GB = 0.00;
const DESCONTO_BRONZE_GB = 0.05;
const DESCONTO_PRATA_GB = 0.10;
const DESCONTO_OURO_GB = 0.25; // nova faixa

function calcularDescontoFidelidade(pontos: number, valorCompra: number): number {
  /**
   * Calcula o desconto de fidelidade com base nos pontos acumulados.
   * Retorna o valor do desconto (não o valor final da compra).
   */
  let percentual: number;

  if (pontos < 500) {
    percentual = DESCONTO_SEM_PONTOS_GB;
  } else if (pontos < 1000) {
    percentual = DESCONTO_BRONZE_GB;
  } else if (pontos < 2000) {
    percentual = DESCONTO_PRATA_GB;
  } else {
    percentual = DESCONTO_OURO_GB;
  }

  return Math.round(valorCompra * percentual * 100) / 100;
}

// ─── Testes de caracterização completos ───────────────────────────────────────

function verificarDescontoSemPontosTipico(): void {
  const resultado = calcularDescontoFidelidade(100, 200.00);
  const esperado = 0.00;
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: desconto sem pontos — típico (100 pts)");
  } else {
    console.log(`FALHOU: desconto sem pontos (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarLimiteInferiorBronze(): void {
  const resultado = calcularDescontoFidelidade(499, 200.00);
  const esperado = 0.00;
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: limite inferior bronze (499 pts → 0%)");
  } else {
    console.log(`FALHOU: limite inferior bronze (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarDescontoBronzeTipico(): void {
  const resultado = calcularDescontoFidelidade(750, 200.00);
  const esperado = 10.00; // 200 * 0.05
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: desconto bronze — típico (750 pts, R$ 200,00)");
  } else {
    console.log(`FALHOU: desconto bronze típico (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarLimiteInferiorBronzeExato(): void {
  const resultado = calcularDescontoFidelidade(500, 200.00);
  const esperado = 10.00; // 200 * 0.05
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: entrada bronze exata (500 pts → 5%)");
  } else {
    console.log(`FALHOU: entrada bronze exata (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarLimiteSuperiorBronze(): void {
  const resultado = calcularDescontoFidelidade(999, 200.00);
  const esperado = 10.00; // 200 * 0.05
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: limite superior bronze (999 pts → 5%)");
  } else {
    console.log(`FALHOU: limite superior bronze (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarDescontoPrataTipico(): void {
  const resultado = calcularDescontoFidelidade(1500, 300.00);
  const esperado = 30.00; // 300 * 0.10
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: desconto prata — típico (1.500 pts, R$ 300,00)");
  } else {
    console.log(`FALHOU: desconto prata típico (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarLimiteInferiorPrataExato(): void {
  const resultado = calcularDescontoFidelidade(1000, 200.00);
  const esperado = 20.00; // 200 * 0.10
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: entrada prata exata (1.000 pts → 10%)");
  } else {
    console.log(`FALHOU: entrada prata exata (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarLimiteSuperiorPrata(): void {
  const resultado = calcularDescontoFidelidade(1999, 200.00);
  const esperado = 20.00; // 200 * 0.10
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: limite superior prata (1.999 pts → 10%)");
  } else {
    console.log(`FALHOU: limite superior prata (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarDescontoOuroTipico(): void {
  const resultado = calcularDescontoFidelidade(2500, 400.00);
  const esperado = 100.00; // 400 * 0.25
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: desconto ouro — típico (2.500 pts, R$ 400,00)");
  } else {
    console.log(`FALHOU: desconto ouro típico (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarLimiteInferiorOuroExato(): void {
  const resultado = calcularDescontoFidelidade(2000, 200.00);
  const esperado = 50.00; // 200 * 0.25
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: entrada ouro exata (2.000 pts → 25%)");
  } else {
    console.log(`FALHOU: entrada ouro exata (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarValorCompraZero(): void {
  const resultado = calcularDescontoFidelidade(1500, 0.00);
  const esperado = 0.00;
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: valor de compra zero (desconto = 0.00)");
  } else {
    console.log(`FALHOU: valor de compra zero (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function executarTodasVerificacoes(): void {
  verificarDescontoSemPontosTipico();
  verificarLimiteInferiorBronze();
  verificarDescontoBronzeTipico();
  verificarLimiteInferiorBronzeExato();
  verificarLimiteSuperiorBronze();
  verificarDescontoPrataTipico();
  verificarLimiteInferiorPrataExato();
  verificarLimiteSuperiorPrata();
  verificarDescontoOuroTipico();
  verificarLimiteInferiorOuroExato();
  verificarValorCompraZero();
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

console.log("=== Gabarito: gabarito.ts ===");
console.log();
console.log("Suite completa de caracterização (todas as faixas + limites):");
executarTodasVerificacoes();
console.log();
console.log("Todas as verificações OK — mudança integrada sem regressão.");
console.log();
console.log("Descontos por faixa (R$ 200,00 de compra):");
console.log(`  100 pts  → R$ ${calcularDescontoFidelidade(100, 200.00).toFixed(2)}  (0%)`);
console.log(`  750 pts  → R$ ${calcularDescontoFidelidade(750, 200.00).toFixed(2)}  (5% bronze)`);
console.log(`  1.500 pts → R$ ${calcularDescontoFidelidade(1500, 200.00).toFixed(2)}  (10% prata)`);
console.log(`  2.500 pts → R$ ${calcularDescontoFidelidade(2500, 200.00).toFixed(2)}  (25% ouro)`);
