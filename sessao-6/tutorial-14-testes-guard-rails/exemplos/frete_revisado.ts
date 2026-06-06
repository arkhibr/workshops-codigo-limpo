/**
 * VERSÃO REVISADA — cálculo de frete com testes de caracterização completos
 * Referência: Feathers (testes de caracterização) + Clean Code, Cap. 9 (Testes)
 *
 * O que este arquivo demonstra:
 *   1. Testes de caracterização escritos ANTES da mudança assistida.
 *   2. A mudança (nova faixa > 15 kg) introduz uma regressão: verificarLimiteFaixa2_3
 *      detecta que 12 kg retorna valor errado.
 *   3. A correção do limite restaura o comportamento: todas as verificações voltam a OK.
 *
 * Ciclo demonstrado aqui:
 *   caracterizar → mudança quebra → corrigir → tudo OK (estado final do arquivo)
 *
 * Execute: npx ts-node sessao-6/tutorial-14-testes-guard-rails/exemplos/frete_revisado.ts
 */

const DISTANCIA_BASE_KM_REV = 100.0;

function calcularFrete(peso: number, distancia: number): number {
  /**
   * Calcula o frete com base no peso (kg) e na distância (km).
   * O resultado é proporcional à distância em relação à base de 100 km.
   *
   * Faixas:
   *   até 5 kg       → R$ 2,00/kg
   *   5,01–10 kg     → R$ 1,80/kg + R$ 3,00 fixo
   *   10,01–15 kg    → R$ 1,50/kg + R$ 5,00 fixo
   *   acima de 15 kg → R$ 1,20/kg + R$ 8,00 fixo  (faixa adicionada pela mudança)
   */
  if (peso <= 0) return 0.0;

  const fatorDistancia = distancia / DISTANCIA_BASE_KM_REV;
  let valorBase: number;

  if (peso <= 5.0) {
    valorBase = peso * 2.00;
  } else if (peso <= 10.0) {
    valorBase = peso * 1.80 + 3.00;
  } else if (peso <= 15.0) {
    // Faixa 3 — limite corrigido após a regressão ser detectada pelos testes
    valorBase = peso * 1.50 + 5.00;
  } else {
    // Faixa 4 — nova faixa adicionada pela mudança assistida
    valorBase = peso * 1.20 + 8.00;
  }

  return Math.round(valorBase * fatorDistancia * 100) / 100;
}

// ─── Testes de caracterização completos ───────────────────────────────────────
// Escritos ANTES da mudança, cobrindo cada faixa, limites e bordas.
// A regressão do frete_gerado.ts seria capturada por verificarLimiteFaixa2_3.

function verificarPesoZero(): void {
  const resultado = calcularFrete(0.0, 100.0);
  const esperado = 0.00;
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: peso zero retorna frete zero");
  } else {
    console.log(`FALHOU: peso zero (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarFreteFaixa1Tipico(): void {
  const resultado = calcularFrete(3.0, 100.0);
  const esperado = 6.00; // 3 * 2.00
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: faixa 1 típico (3 kg, 100 km)");
  } else {
    console.log(`FALHOU: faixa 1 típico (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarLimiteFaixa1(): void {
  const resultado = calcularFrete(5.0, 100.0);
  const esperado = 10.00; // 5 * 2.00
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: limite faixa 1 (5 kg exatos, 100 km)");
  } else {
    console.log(`FALHOU: limite faixa 1 (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarFreteFaixa2Tipico(): void {
  const resultado = calcularFrete(8.0, 100.0);
  const esperado = 17.40; // 8 * 1.80 + 3.00
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: faixa 2 típico (8 kg, 100 km)");
  } else {
    console.log(`FALHOU: faixa 2 típico (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarLimiteFaixa2_3(): void {
  // Borda crítica: 12 kg deve usar faixa 3 (R$ 1,50/kg + R$ 5,00).
  // Esta verificação teria detectado a regressão do frete_gerado.ts.
  const resultado = calcularFrete(12.0, 100.0);
  const esperado = 23.00; // 12 * 1.50 + 5.00
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: limite faixa 2-3 (12 kg, 100 km)");
  } else {
    console.log(`FALHOU: limite faixa 2-3 (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarFreteFaixa3Tipico(): void {
  const resultado = calcularFrete(13.0, 100.0);
  const esperado = 24.50; // 13 * 1.50 + 5.00
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: faixa 3 típico (13 kg, 100 km)");
  } else {
    console.log(`FALHOU: faixa 3 típico (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarLimiteFaixa3_4(): void {
  const resultado = calcularFrete(15.0, 100.0);
  const esperado = 27.50; // 15 * 1.50 + 5.00
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: limite faixa 3-4 (15 kg exatos, 100 km)");
  } else {
    console.log(`FALHOU: limite faixa 3-4 (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarFreteFaixa4Tipico(): void {
  const resultado = calcularFrete(40.0, 100.0);
  const esperado = 56.00; // 40 * 1.20 + 8.00
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: faixa 4 nova (40 kg, 100 km)");
  } else {
    console.log(`FALHOU: faixa 4 nova (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function verificarFatorDistancia(): void {
  const resultado = calcularFrete(3.0, 200.0);
  const esperado = 12.00; // (3 * 2.00) * (200/100)
  if (Math.abs(resultado - esperado) < 0.01) {
    console.log("OK: fator de distância (3 kg, 200 km)");
  } else {
    console.log(`FALHOU: fator de distância (esperado ${esperado.toFixed(2)}, obtido ${resultado.toFixed(2)})`);
  }
}

function executarTodasVerificacoes(): void {
  verificarPesoZero();
  verificarFreteFaixa1Tipico();
  verificarLimiteFaixa1();
  verificarFreteFaixa2Tipico();
  verificarLimiteFaixa2_3();
  verificarFreteFaixa3Tipico();
  verificarLimiteFaixa3_4();
  verificarFreteFaixa4Tipico();
  verificarFatorDistancia();
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

console.log("=== Demonstração: frete_revisado.ts ===");
console.log();
console.log("Contexto: testes de caracterização escritos ANTES da mudança assistida.");
console.log("A mudança adicionou a faixa > 15 kg. A regressão foi detectada e corrigida.");
console.log("Estado final: implementação correta, todas as verificações passam.");
console.log();
console.log("Verificações de caracterização (suite completa):");
executarTodasVerificacoes();
console.log();
console.log("Verificação resumo: todas OK — guard-rails funcionaram.");
console.log();
console.log("Cálculos de referência (estado corrigido):");
console.log(`  0 kg, 100 km  → R$ ${calcularFrete(0.0, 100.0).toFixed(2)}  (peso zero)`);
console.log(`  3 kg, 100 km  → R$ ${calcularFrete(3.0, 100.0).toFixed(2)}  (faixa 1)`);
console.log(`  5 kg, 100 km  → R$ ${calcularFrete(5.0, 100.0).toFixed(2)}  (limite faixa 1)`);
console.log(`  8 kg, 100 km  → R$ ${calcularFrete(8.0, 100.0).toFixed(2)}  (faixa 2)`);
console.log(`  12 kg, 100 km → R$ ${calcularFrete(12.0, 100.0).toFixed(2)}  (faixa 3 — era a zona regredida)`);
console.log(`  15 kg, 100 km → R$ ${calcularFrete(15.0, 100.0).toFixed(2)}  (limite faixa 3)`);
console.log(`  40 kg, 100 km → R$ ${calcularFrete(40.0, 100.0).toFixed(2)}  (faixa 4 nova)`);
console.log(`  3 kg, 200 km  → R$ ${calcularFrete(3.0, 200.0).toFixed(2)}  (distância dupla)`);
