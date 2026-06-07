/**
 * Refatoração de IA — Cálculo de Comissão de Vendas com Faixas
 * Referência: Tutorial 13 — Refatoração assistida avançada
 * Execute: npx ts-node comissao_gerado.ts
 *
 * Contexto: o código ORIGINAL usava um if/else em escada para calcular a comissão
 * por faixas de valor. A IA refatorou para uma tabela de faixas (array de objetos),
 * tornando o código mais legível e extensível.
 *
 * O código refatorado é idiomático e polido. A verificação de equivalência incluída
 * cobre apenas casos no meio de cada faixa — e passa. Um caso de fronteira exata
 * (valor == limite de faixa) silenciosamente mudou de comportamento.
 */

// ─── Domínio ──────────────────────────────────────────────────────────────────

interface Venda {
  vendedorId: string;
  valor:      number;
}

// ─── Versão ORIGINAL (if/else em escada) ─────────────────────────────────────

function calcularComissaoOriginal(venda: Venda): number {
  const { valor } = venda;
  if (valor >= 50_000) return valor * 0.10;
  if (valor >= 20_000) return valor * 0.08;
  if (valor >= 10_000) return valor * 0.06;
  if (valor >= 5_000)  return valor * 0.04;
  return valor * 0.02;
}

// ─── Versão REFATORADA pela IA (tabela de faixas) ────────────────────────────

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
  for (const faixa of TABELA_COMISSAO) {
    if (venda.valor > faixa.limiteInferior) {
      return venda.valor * faixa.percentual;
    }
  }
  return venda.valor * TABELA_COMISSAO[TABELA_COMISSAO.length - 1].percentual;
}

// ─── Verificação FRACA (só casos no meio das faixas) ─────────────────────────

function verificarEquivalencia(): void {
  /**
   * Compara a versão refatorada contra a original.
   * Cobre casos representativos de cada faixa — não inclui os limites exatos.
   */
  const casos: Venda[] = [
    { vendedorId: "V01", valor:  1_000 },  // faixa 0–4999
    { vendedorId: "V02", valor:  7_500 },  // faixa 5000–9999
    { vendedorId: "V03", valor: 15_000 },  // faixa 10000–19999
    { vendedorId: "V04", valor: 35_000 },  // faixa 20000–49999
    { vendedorId: "V05", valor: 80_000 },  // faixa 50000+
  ];

  console.log("=== Verificação de equivalência (fraca — só meio das faixas) ===\n");
  let todosOk = true;
  for (const venda of casos) {
    const esperado = calcularComissaoOriginal(venda);
    const obtido   = calcularComissaoRefatorada(venda);
    if (Math.abs(obtido - esperado) < 0.001) {
      console.log(`  OK: valor=${String(venda.valor).padStart(8)}  comissão=${obtido.toFixed(2).padStart(9)}`);
    } else {
      console.log(`  FALHOU: valor=${String(venda.valor).padStart(8)}  esperado=${esperado.toFixed(2)}  obtido=${obtido.toFixed(2)}`);
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

console.log("=== Comissão de Vendas — refatoração de IA (tabela de faixas) ===\n");

const demonstracao: Venda[] = [
  { vendedorId: "V01", valor:  1_000 },
  { vendedorId: "V02", valor:  7_500 },
  { vendedorId: "V03", valor: 15_000 },
  { vendedorId: "V04", valor: 35_000 },
  { vendedorId: "V05", valor: 80_000 },
];

console.log(`  ${"Vendedor".padEnd(10)} ${"Valor".padStart(12)}  ${"Original".padStart(10)}  ${"Refatorada".padStart(10)}`);
console.log("  " + "-".repeat(48));
for (const venda of demonstracao) {
  const orig  = calcularComissaoOriginal(venda);
  const refat = calcularComissaoRefatorada(venda);
  console.log(
    `  ${venda.vendedorId.padEnd(10)} R$${String(venda.valor.toLocaleString("pt-BR")).padStart(9)}` +
    `  R$${orig.toFixed(2).padStart(9)}  R$${refat.toFixed(2).padStart(9)}`
  );
}

console.log();
verificarEquivalencia();
