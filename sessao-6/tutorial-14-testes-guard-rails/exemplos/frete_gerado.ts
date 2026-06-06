/**
 * SAÍDA TÍPICA DE IA — cálculo de frete com faixas de peso (mudança assistida sem proteção)
 * Referência: Feathers (testes de caracterização) + Clean Code, Cap. 9 (Testes)
 *
 * ⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
 *     A mudança assistida adicionou a faixa acima de 15 kg, mas deslocou
 *     o limite entre a faixa 2 e a faixa 3: pedidos de 10,01–15 kg que
 *     antes custavam R$ 1,80/kg + R$ 3,00 agora caem na faixa mais barata.
 *     A regressão é silenciosa porque a suite só cobre casos "felizes"
 *     (um por faixa) e NENHUM deles está na zona afetada.
 *     Todas as verificações imprimem OK — mas o valor está errado para
 *     pedidos entre 10 kg e 15 kg.
 *
 * Execute: npx ts-node sessao-6/tutorial-14-testes-guard-rails/exemplos/frete_gerado.ts
 */

// Faixas originais (antes da mudança assistida):
//   até 5 kg       → R$ 2,00/kg
//   5,01–10 kg     → R$ 1,80/kg + R$ 3,00 fixo
//   acima de 10 kg → R$ 1,50/kg + R$ 5,00 fixo
//
// Prompt usado para a mudança:
//   "Adiciona faixa acima de 15 kg com R$ 1,20/kg + R$ 8,00 fixo."
//
// A IA adicionou a nova faixa mas usou "> 15" onde deveria ser "> 10"
// para a faixa intermediária — deslocando o limite silenciosamente.

const DISTANCIA_BASE_KM = 100.0;

function calcularFrete(peso: number, distancia: number): number {
  /**
   * Calcula o frete com base no peso (kg) e na distância (km).
   * O resultado é proporcional à distância em relação à base de 100 km.
   *
   * ⚠️ REGRESSÃO INTRODUZIDA PELA MUDANÇA ASSISTIDA:
   * O limite entre faixa 2 e faixa 3 foi deslocado de 10 kg para 15 kg.
   * Pedidos de 10,01–15 kg recebem valor incorreto (mais barato do que deveriam).
   */
  const fatorDistancia = distancia / DISTANCIA_BASE_KM;
  let valorBase: number;

  if (peso <= 5.0) {
    // Faixa 1 — intacta
    valorBase = peso * 2.00;
  } else if (peso <= 15.0) {
    // Faixa 2 — REGRESSÃO: deveria ser "peso <= 10.0"
    // Pedidos 10,01–15 kg caem aqui em vez de na faixa 3
    valorBase = peso * 1.80 + 3.00;
  } else if (peso <= 30.0) {
    // Faixa 3 — deslocada pela mudança (era "acima de 10 kg")
    valorBase = peso * 1.50 + 5.00;
  } else {
    // Faixa 4 — nova faixa adicionada pela mudança assistida
    valorBase = peso * 1.20 + 8.00;
  }

  return Math.round(valorBase * fatorDistancia * 100) / 100;
}

// ─── Suite fraca: apenas caminhos felizes ─────────────────────────────────────
// Cobre apenas um caso por faixa — nenhum está na zona 10–15 kg afetada.

function verificarFreteFaixa1(): void {
  // Faixa 1: peso de 3 kg, distância de 100 km.
  const resultado = calcularFrete(3.0, 100.0);
  const esperado = 6.00; // 3 * 2.00 * (100/100)
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: frete faixa 1 (3 kg, 100 km)");
  } else {
    console.log(`FALHOU: frete faixa 1 (esperado ${esperado}, obtido ${resultado})`);
  }
}

function verificarFreteFaixa2(): void {
  // Faixa 2: peso de 8 kg, distância de 100 km.
  const resultado = calcularFrete(8.0, 100.0);
  const esperado = 17.40; // 8 * 1.80 + 3.00 = 17.40
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: frete faixa 2 (8 kg, 100 km)");
  } else {
    console.log(`FALHOU: frete faixa 2 (esperado ${esperado}, obtido ${resultado})`);
  }
}

function verificarFreteFaixa3(): void {
  // Faixa 3: peso de 20 kg, distância de 100 km — caso feliz, não afetado.
  const resultado = calcularFrete(20.0, 100.0);
  const esperado = 35.00; // 20 * 1.50 + 5.00 = 35.00
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: frete faixa 3 (20 kg, 100 km)");
  } else {
    console.log(`FALHOU: frete faixa 3 (esperado ${esperado}, obtido ${resultado})`);
  }
}

function verificarFreteFaixa4(): void {
  // Faixa 4 (nova): peso de 40 kg, distância de 100 km.
  const resultado = calcularFrete(40.0, 100.0);
  const esperado = 56.00; // 40 * 1.20 + 8.00 = 56.00
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: frete faixa 4 (40 kg, 100 km)");
  } else {
    console.log(`FALHOU: frete faixa 4 (esperado ${esperado}, obtido ${resultado})`);
  }
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

console.log("=== Demonstração: frete_gerado.ts ===");
console.log();
console.log("Cálculos (caminho feliz):");
console.log(`  3 kg, 100 km  → R$ ${calcularFrete(3.0, 100.0).toFixed(2)}`);
console.log(`  8 kg, 100 km  → R$ ${calcularFrete(8.0, 100.0).toFixed(2)}`);
console.log(`  20 kg, 100 km → R$ ${calcularFrete(20.0, 100.0).toFixed(2)}`);
console.log(`  40 kg, 100 km → R$ ${calcularFrete(40.0, 100.0).toFixed(2)}`);
console.log();
console.log("Verificações (suite fraca — apenas caminho feliz):");
verificarFreteFaixa1();
verificarFreteFaixa2();
verificarFreteFaixa3();
verificarFreteFaixa4();
console.log();
console.log("Todas as verificações passaram — mas a regressão está presente.");
console.log("Tente: calcularFrete(12.0, 100.0)");
console.log(`  Obtido:  R$ ${calcularFrete(12.0, 100.0).toFixed(2)}  (faixa 2 com limite deslocado)`);
console.log(`  Correto: R$ ${(Math.round((12.0 * 1.50 + 5.00) * 100) / 100).toFixed(2)}  (deveria ser faixa 3)`);
console.log();
console.log("⚠ A suite fraca não cobriu o intervalo 10–15 kg — regressão invisível.");
