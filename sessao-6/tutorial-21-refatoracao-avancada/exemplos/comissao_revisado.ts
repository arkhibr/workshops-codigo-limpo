/**
 * Refatoração revisada — Cálculo de Comissão de Vendas com Faixas
 * Referência: Tutorial 13 — Refatoração assistida avançada
 * Execute: npx ts-node comissao_revisado.ts
 *
 * Correção aplicada em relação a comissao_gerado.ts:
 *   - O operador de comparação foi corrigido de '>' para '>=' nos limites de faixa.
 *   - A versão gerada usava 'valor > limiteInferior', o que fazia um valor exato
 *     no limite (ex.: 10.000) cair para a faixa anterior (6% → 4%).
 *   - A versão revisada usa 'valor >= limiteInferior', preservando o comportamento
 *     exato do if/else original onde '>= 10.000' entrava na faixa de 6%.
 *   - A verificação de equivalência é completa: inclui os limites exatos de cada faixa.
 */

// ─── Domínio ──────────────────────────────────────────────────────────────────

interface Venda {
  vendedorId: string;
  valor:      number;
}

// ─── Versão ORIGINAL (if/else em escada) — comportamento de referência ────────

function calcularComissaoOriginal(venda: Venda): number {
  const { valor } = venda;
  if (valor >= 50_000) return valor * 0.10;
  if (valor >= 20_000) return valor * 0.08;
  if (valor >= 10_000) return valor * 0.06;
  if (valor >= 5_000)  return valor * 0.04;
  return valor * 0.02;
}

// ─── Versão REFATORADA correta (tabela de faixas com operador correto) ────────

interface FaixaComissao {
  limiteInferior: number;
  percentual:     number;
}

const TABELA_COMISSAO: FaixaComissao[] = [
  { limiteInferior: 50_000, percentual: 0.10 },
  { limiteInferior: 20_000, percentual: 0.08 },
  { limiteInferior: 10_000, percentual: 0.06 },
  { limiteInferior:  5_000, percentual: 0.04 },
  { limiteInferior:      0, percentual: 0.02 },
];

function calcularComissaoRefatorada(venda: Venda): number {
  /**
   * Usa '>=' para preservar o comportamento exato do original:
   * valor == limiteInferior entra na faixa desse limite (não na faixa abaixo).
   */
  for (const faixa of TABELA_COMISSAO) {
    if (venda.valor >= faixa.limiteInferior) {
      return venda.valor * faixa.percentual;
    }
  }
  return venda.valor * TABELA_COMISSAO[TABELA_COMISSAO.length - 1].percentual;
}

// ─── Verificação COMPLETA (inclui limites exatos de cada faixa) ──────────────

function verificarEquivalencia(): void {
  /**
   * Compara a versão refatorada contra a original para todos os casos relevantes:
   * - Casos no interior de cada faixa
   * - Casos nos limites exatos de cada faixa (onde a regressão se manifesta)
   * - Caso abaixo do menor limite
   */
  const casos: Venda[] = [
    // Interior das faixas
    { vendedorId: "interior-baixo",    valor:  1_000 },
    { vendedorId: "interior-faixa2",   valor:  7_500 },
    { vendedorId: "interior-faixa3",   valor: 15_000 },
    { vendedorId: "interior-faixa4",   valor: 35_000 },
    { vendedorId: "interior-alto",     valor: 80_000 },
    // Limites exatos — onde a regressão de borda se manifesta
    { vendedorId: "limite-faixa2",     valor:  5_000 },  // >= 5000 → 4% (não 2%)
    { vendedorId: "limite-faixa3",     valor: 10_000 },  // >= 10000 → 6% (não 4%)
    { vendedorId: "limite-faixa4",     valor: 20_000 },  // >= 20000 → 8% (não 6%)
    { vendedorId: "limite-faixa5",     valor: 50_000 },  // >= 50000 → 10% (não 8%)
    // Um passo abaixo dos limites
    { vendedorId: "abaixo-faixa2",     valor:  4_999 },
    { vendedorId: "abaixo-faixa3",     valor:  9_999 },
    { vendedorId: "abaixo-faixa4",     valor: 19_999 },
    { vendedorId: "abaixo-faixa5",     valor: 49_999 },
  ];

  console.log("=== Verificação de equivalência (completa — inclui bordas) ===\n");
  let todosOk = true;
  for (const venda of casos) {
    const esperado = calcularComissaoOriginal(venda);
    const obtido   = calcularComissaoRefatorada(venda);
    if (Math.abs(obtido - esperado) < 0.001) {
      console.log(
        `  OK: ${venda.vendedorId.padEnd(22)}  valor=${String(venda.valor).padStart(8)}` +
        `  comissão=${obtido.toFixed(2).padStart(9)}`
      );
    } else {
      console.log(
        `  FALHOU: ${venda.vendedorId.padEnd(22)}  valor=${String(venda.valor).padStart(8)}` +
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

console.log("=== Comissão de Vendas — refatoração revisada (operador correto) ===\n");

const demonstracao: Venda[] = [
  { vendedorId: "V01", valor:  1_000 },
  { vendedorId: "V02", valor:  5_000 },  // limite exato — deve ser 4%, não 2%
  { vendedorId: "V03", valor: 10_000 },  // limite exato — deve ser 6%, não 4%
  { vendedorId: "V04", valor: 20_000 },  // limite exato — deve ser 8%, não 6%
  { vendedorId: "V05", valor: 50_000 },  // limite exato — deve ser 10%, não 8%
  { vendedorId: "V06", valor: 80_000 },
];

console.log(`  ${"Vendedor".padEnd(10)} ${"Valor".padStart(12)}  ${"Original".padStart(10)}  ${"Refatorada".padStart(10)}  ${"Status".padStart(8)}`);
console.log("  " + "-".repeat(60));
for (const venda of demonstracao) {
  const orig   = calcularComissaoOriginal(venda);
  const refat  = calcularComissaoRefatorada(venda);
  const status = Math.abs(orig - refat) < 0.001 ? "OK" : "DIFERENTE";
  console.log(
    `  ${venda.vendedorId.padEnd(10)} R$${String(venda.valor.toLocaleString("pt-BR")).padStart(9)}` +
    `  R$${orig.toFixed(2).padStart(9)}  R$${refat.toFixed(2).padStart(9)}  ${status.padStart(8)}`
  );
}

console.log();
verificarEquivalencia();
