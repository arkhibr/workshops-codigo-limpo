/**
 * Exercício — Refatoração de IA com regressão de borda
 * Referência: Tutorial 13 — Refatoração assistida avançada
 * Execute: npx ts-node exercicio.ts
 *
 * Contexto: uma IA refatorou o cálculo de bônus por meta de vendas.
 * O código original usava if/else por faixas de atingimento (em percentual).
 * A versão refatorada usa uma tabela de faixas — idiomática e legível.
 *
 * Tarefas:
 *   (1) Escreva a função verificarEquivalencia incluindo os limites exatos
 *       de cada faixa de atingimento (ex.: exatamente 80%, 100%, 120%).
 *   (2) Rode a verificação contra a versão refatorada abaixo.
 *   (3) Identifique qual caso de borda regrediu e corrija a refatoração.
 *
 * Compare sua solução com gabarito.ts.
 */

// ─── Domínio ──────────────────────────────────────────────────────────────────

interface MetaVendedor {
  vendedorId:   string;
  salarioBase:  number;
  atingimento:  number;  // percentual: 0.0 a qualquer valor (ex.: 1.25 = 125%)
}

// ─── Versão ORIGINAL (if/else em escada) ─────────────────────────────────────

function calcularBonusOriginal(meta: MetaVendedor): number {
  if (meta.atingimento >= 1.20) return meta.salarioBase * 0.30;
  if (meta.atingimento >= 1.00) return meta.salarioBase * 0.20;
  if (meta.atingimento >= 0.80) return meta.salarioBase * 0.10;
  return 0.0;
}

// ─── Versão REFATORADA pela IA (tabela de faixas) ────────────────────────────

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
  for (const faixa of TABELA_BONUS) {
    if (meta.atingimento > faixa.atingimentoMinimo) {
      return meta.salarioBase * faixa.percentualBonus;
    }
  }
  return 0.0;
}

// ─── Verificação FRACA (só casos no interior das faixas) ─────────────────────

function verificarEquivalencia(): void {
  /**
   * TODO: implemente uma verificação completa que inclua os limites exatos.
   * Esta versão cobre apenas o interior de cada faixa — não os limites.
   */
  const salario = 5_000;
  const casos: MetaVendedor[] = [
    { vendedorId: "V01", salarioBase: salario, atingimento: 0.60 },  // abaixo → 0
    { vendedorId: "V02", salarioBase: salario, atingimento: 0.90 },  // interior 80–99%
    { vendedorId: "V03", salarioBase: salario, atingimento: 1.10 },  // interior 100–119%
    { vendedorId: "V04", salarioBase: salario, atingimento: 1.30 },  // acima 120%
  ];

  console.log("=== Verificação de equivalência (fraca — só interior das faixas) ===\n");
  let todosOk = true;
  for (const meta of casos) {
    const esperado = calcularBonusOriginal(meta);
    const obtido   = calcularBonusRefatorado(meta);
    if (Math.abs(obtido - esperado) < 0.001) {
      console.log(`  OK: atingimento=${(meta.atingimento * 100).toFixed(0).padStart(4)}%  bônus=${obtido.toFixed(2).padStart(9)}`);
    } else {
      console.log(`  FALHOU: atingimento=${(meta.atingimento * 100).toFixed(0).padStart(4)}%  esperado=${esperado.toFixed(2)}  obtido=${obtido.toFixed(2)}`);
      todosOk = false;
    }
  }

  console.log();
  if (todosOk) {
    console.log("Resultado: todos os casos passaram.");
  } else {
    console.log("Resultado: há divergências.");
  }
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

const salarioBase = 5_000;

const demonstracao: MetaVendedor[] = [
  { vendedorId: "V01", salarioBase, atingimento: 0.60 },
  { vendedorId: "V02", salarioBase, atingimento: 0.90 },
  { vendedorId: "V03", salarioBase, atingimento: 1.10 },
  { vendedorId: "V04", salarioBase, atingimento: 1.30 },
];

console.log("=== Bônus por Meta — refatoração de IA (tabela de faixas) ===\n");
console.log(`  ${"Vendedor".padEnd(10)} ${"Atingimento".padStart(12)}  ${"Original".padStart(10)}  ${"Refatorada".padStart(10)}`);
console.log("  " + "-".repeat(48));
for (const meta of demonstracao) {
  const orig  = calcularBonusOriginal(meta);
  const refat = calcularBonusRefatorado(meta);
  console.log(
    `  ${meta.vendedorId.padEnd(10)} ${((meta.atingimento * 100).toFixed(0) + "%").padStart(12)}` +
    `  R$${orig.toFixed(2).padStart(9)}  R$${refat.toFixed(2).padStart(9)}`
  );
}

console.log();
verificarEquivalencia();
