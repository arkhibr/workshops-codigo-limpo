/**
 * Gabarito — Cupom Progressivo (regra de negócio correta)
 * Referência: Tutorial 09 — Engenharia de contexto e prompt para gerar código
 * Execute: npx ts-node gabarito.ts
 *
 * Correção aplicada em relação a exercicio.ts:
 *   - determinarFaixa usava `>` (exclusivo) nos limiares de faixa —
 *     valores exatos de fronteira (R$ 200,00 e R$ 500,00) caíam na faixa abaixo.
 *   - Correto: `>=` (inclusivo), pois as faixas são definidas como "a partir de".
 */

// ─── Constantes de domínio ────────────────────────────────────────────────────

const FAIXA_BRONZE_MIN  =   0.01;  // R$ 0,01–199,99 → 5 %
const FAIXA_PRATA_MIN   = 200.00;  // R$ 200,00–499,99 → 10 %
const FAIXA_OURO_MIN    = 500.00;  // R$ 500,00+ → 20 %

const DESCONTO_BRONZE   = 0.05;
const DESCONTO_PRATA    = 0.10;
const DESCONTO_OURO     = 0.20;

// ─── Entidade ─────────────────────────────────────────────────────────────────

interface ResultadoCupom {
  valorOriginal:  number;
  percentual:     number;
  valorDesconto:  number;
  valorFinal:     number;
  faixa:          string;
}

// ─── Lógica de cupom progressivo ─────────────────────────────────────────────

function determinarFaixa(valor: number): [string, number] {
  /**
   * Determina a faixa e o percentual de desconto pelo valor da compra.
   *
   * Faixas:
   *   Bronze: R$ 0,01–R$ 199,99 → 5 %
   *   Prata:  R$ 200,00–R$ 499,99 → 10 %
   *   Ouro:   R$ 500,00+ → 20 %
   */
  if (valor >= FAIXA_OURO_MIN)   return ["ouro",      DESCONTO_OURO];    // >= garante que R$500,00 entre em "ouro"
  if (valor >= FAIXA_PRATA_MIN)  return ["prata",     DESCONTO_PRATA];   // >= garante que R$200,00 entre em "prata"
  if (valor >= FAIXA_BRONZE_MIN) return ["bronze",    DESCONTO_BRONZE];
  return ["sem_faixa", 0.0];
}

function calcularCupomProgressivo(valorCompra: number): ResultadoCupom {
  /**
   * Calcula o desconto do cupom progressivo para o valor informado.
   * Lança Error se o valor for negativo.
   */
  if (valorCompra < 0) {
    throw new Error("Valor da compra não pode ser negativo");
  }

  const [faixa, percentual] = determinarFaixa(valorCompra);
  const valorDesconto = valorCompra * percentual;
  const valorFinal    = valorCompra - valorDesconto;

  return { valorOriginal: valorCompra, percentual, valorDesconto, valorFinal, faixa };
}

function formatarCupom(r: ResultadoCupom): string {
  return (
    `  faixa=${r.faixa.padEnd(10)}  ` +
    `original=R$${r.valorOriginal.toFixed(2).padStart(8)}  ` +
    `desconto=${(r.percentual * 100).toFixed(0)}%  ` +
    `final=R$${r.valorFinal.toFixed(2).padStart(8)}`
  );
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

console.log("=== Cupom Progressivo (gabarito — regra de negócio correta) ===\n");

const casos = [50.00, 199.99, 200.00, 350.00, 499.99, 500.00, 750.00];

for (const valor of casos) {
  const resultado = calcularCupomProgressivo(valor);
  console.log(formatarCupom(resultado));
}

console.log();
console.log("Casos de fronteira (confirmam a correção):");
for (const valor of [200.00, 500.00]) {
  const resultado = calcularCupomProgressivo(valor);
  console.log(`  R$${valor.toFixed(2)} → faixa=${resultado.faixa}, desconto=${(resultado.percentual * 100).toFixed(0)}%`);
}
