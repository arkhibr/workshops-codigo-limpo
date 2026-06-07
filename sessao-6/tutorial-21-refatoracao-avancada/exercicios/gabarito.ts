/**
 * Gabarito — Refatoração de IA com regressão de borda
 * Referência: Tutorial 13 — Refatoração assistida avançada
 * Execute: npx ts-node gabarito.ts
 *
 * Correções aplicadas em relação a exercicio.ts:
 *   (1) verificarEquivalencia completa: inclui os limites exatos de atingimento
 *       (80%, 100%, 120%) onde a regressão de borda se manifesta.
 *   (2) calcularBonusRefatorado corrigido: operador '>' substituído por '>='
 *       para preservar o comportamento do if/else original nos limites.
 */

// ─── Domínio ──────────────────────────────────────────────────────────────────

interface MetaVendedor {
  vendedorId:   string;
  salarioBase:  number;
  atingimento:  number;  // percentual: 0.0 a qualquer valor (ex.: 1.25 = 125%)
}

// ─── Versão ORIGINAL (if/else em escada) — comportamento de referência ────────

function calcularBonusOriginal(meta: MetaVendedor): number {
  if (meta.atingimento >= 1.20) return meta.salarioBase * 0.30;
  if (meta.atingimento >= 1.00) return meta.salarioBase * 0.20;
  if (meta.atingimento >= 0.80) return meta.salarioBase * 0.10;
  return 0.0;
}

// ─── Versão REFATORADA correta (tabela de faixas com operador correto) ────────

interface FaixaBonus {
  atingimentoMinimo: number;
  percentualBonus:   number;
}

const TABELA_BONUS: FaixaBonus[] = [
  { atingimentoMinimo: 1.20, percentualBonus: 0.30 },
  { atingimentoMinimo: 1.00, percentualBonus: 0.20 },
  { atingimentoMinimo: 0.80, percentualBonus: 0.10 },
];

function calcularBonusRefatorado(meta: MetaVendedor): number {
  /**
   * Usa '>=' para preservar o comportamento exato do original:
   * atingimento == atingimentoMinimo entra na faixa desse limite (não abaixo).
   */
  for (const faixa of TABELA_BONUS) {
    if (meta.atingimento >= faixa.atingimentoMinimo) {
      return meta.salarioBase * faixa.percentualBonus;
    }
  }
  return 0.0;
}

// ─── Verificação COMPLETA (inclui limites exatos de cada faixa) ──────────────

function verificarEquivalencia(): void {
  /**
   * Compara a versão refatorada contra a original para todos os casos relevantes:
   * - Casos no interior de cada faixa
   * - Casos nos limites exatos (80%, 100%, 120%) onde a regressão se manifesta
   * - Casos logo abaixo dos limites
   */
  const salario = 5_000;
  const casos: MetaVendedor[] = [
    // Interior das faixas
    { vendedorId: "interior-sem-bonus", salarioBase: salario, atingimento: 0.60 },
    { vendedorId: "interior-faixa1",    salarioBase: salario, atingimento: 0.90 },
    { vendedorId: "interior-faixa2",    salarioBase: salario, atingimento: 1.10 },
    { vendedorId: "interior-faixa3",    salarioBase: salario, atingimento: 1.30 },
    // Limites exatos — onde a regressão de borda se manifesta
    { vendedorId: "limite-faixa1",      salarioBase: salario, atingimento: 0.80 },  // >= 80% → 10% (não 0)
    { vendedorId: "limite-faixa2",      salarioBase: salario, atingimento: 1.00 },  // >= 100% → 20% (não 10%)
    { vendedorId: "limite-faixa3",      salarioBase: salario, atingimento: 1.20 },  // >= 120% → 30% (não 20%)
    // Logo abaixo dos limites
    { vendedorId: "abaixo-faixa1",      salarioBase: salario, atingimento: 0.799 },
    { vendedorId: "abaixo-faixa2",      salarioBase: salario, atingimento: 0.999 },
    { vendedorId: "abaixo-faixa3",      salarioBase: salario, atingimento: 1.199 },
  ];

  console.log("=== Verificação de equivalência (completa — inclui bordas) ===\n");
  let todosOk = true;
  for (const meta of casos) {
    const esperado = calcularBonusOriginal(meta);
    const obtido   = calcularBonusRefatorado(meta);
    const pct      = (meta.atingimento * 100).toFixed(1) + "%";
    if (Math.abs(obtido - esperado) < 0.001) {
      console.log(
        `  OK: ${meta.vendedorId.padEnd(22)}  atingimento=${pct.padStart(6)}` +
        `  bônus=${obtido.toFixed(2).padStart(9)}`
      );
    } else {
      console.log(
        `  FALHOU: ${meta.vendedorId.padEnd(22)}  atingimento=${pct.padStart(6)}` +
        `  esperado=${esperado.toFixed(2)}  obtido=${obtido.toFixed(2)}`
      );
      todosOk = false;
    }
  }

  console.log();
  if (todosOk) {
    console.log("Resultado: todos os casos passaram — refatoração preserva o comportamento.");
  } else {
    console.log("Resultado: há divergências — refatoração altera o comportamento.");
  }
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

const salarioBase = 5_000;

const demonstracao: MetaVendedor[] = [
  { vendedorId: "V01", salarioBase, atingimento: 0.60 },
  { vendedorId: "V02", salarioBase, atingimento: 0.80 },  // limite exato — deve ser 10%, não 0
  { vendedorId: "V03", salarioBase, atingimento: 1.00 },  // limite exato — deve ser 20%, não 10%
  { vendedorId: "V04", salarioBase, atingimento: 1.20 },  // limite exato — deve ser 30%, não 20%
  { vendedorId: "V05", salarioBase, atingimento: 1.30 },
];

console.log("=== Bônus por Meta — gabarito (operador correto) ===\n");
console.log(`  ${"Vendedor".padEnd(10)} ${"Atingimento".padStart(12)}  ${"Original".padStart(10)}  ${"Refatorada".padStart(10)}  ${"Status".padStart(8)}`);
console.log("  " + "-".repeat(60));
for (const meta of demonstracao) {
  const orig   = calcularBonusOriginal(meta);
  const refat  = calcularBonusRefatorado(meta);
  const status = Math.abs(orig - refat) < 0.001 ? "OK" : "DIFERENTE";
  console.log(
    `  ${meta.vendedorId.padEnd(10)} ${((meta.atingimento * 100).toFixed(0) + "%").padStart(12)}` +
    `  R$${orig.toFixed(2).padStart(9)}  R$${refat.toFixed(2).padStart(9)}  ${status.padStart(8)}`
  );
}

console.log();
verificarEquivalencia();
