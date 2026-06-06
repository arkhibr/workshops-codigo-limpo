/**
 * MÓDULO DE DASHBOARD DE VENDAS — acumulou deriva por contribuições de IA
 * Referência: Clean Code, Cap. 1 e 17; Regra do Escoteiro
 *
 * ⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
 *     Representa um módulo que cresceu com contribuições de IA sem contexto.
 *
 * Sua tarefa:
 *   (1) Identifique os sinais de deriva (duplicação, estilo divergente,
 *       dependência supérflua, formatação inconsistente).
 *   (2) Consolide o módulo mantendo o comportamento observável.
 *   (3) Liste o que foi unificado.
 *
 * Execute: npx ts-node sessao-6/tutorial-15-manutenibilidade-agentes/exercicios/exercicio.ts
 */

// Dependência desnecessária — reimplementada localmente para rodar sem instalação.
// Em um projeto real, a IA teria feito: import { UtilPercentual } from "util-percentual"
const UtilPercentual = {
  formatar(valor: number): string {
    return `${(valor * 100).toFixed(1)}%`;
  },
};

const META_MENSAL: number = 10_000.0;

interface Venda {
  descricao: string;
  valor: number;
}

// ── Contribuição 1 — estilo original ─────────────────────────────────────────

function calcularTotalPeriodo(vendas: Venda[]): number {
  /** Retorna a soma dos valores das vendas no período. */
  return vendas.reduce((soma, v) => soma + v.valor, 0);
}

function calcularPercentualMeta(total: number): number {
  /** Retorna o percentual atingido em relação à meta mensal. */
  if (META_MENSAL === 0) return 0;
  return total / META_MENSAL;
}

// ── Contribuição 2 — IA duplicou sem saber que a função já existia ────────────

function getTotal(sales: any[]): number {  // inglês; any; duplica calcularTotalPeriodo
  let t = 0;
  for (const s of sales) {
    t += s.valor;
  }
  return t;
}

function calcular_soma_vendas(lista: any[]): number {  // snake_case misturado; terceiro nome
  let soma = 0.0;
  lista.forEach(item => { soma = soma + item.valor; });
  return soma;
}

// ── Contribuição 3 — IA usou UtilPercentual em vez de toFixed nativo ──────────

function formatarPercentualDashboard(valor: number): string {
  // Usa UtilPercentual em vez de template literal nativo
  return UtilPercentual.formatar(valor);
}

// ── Contribuição 4 — estilo e formatação divergentes ─────────────────────────
function exibirDashboard(vendas: any[],periodo = "Período Atual") { // sem tipagem no retorno
  const total=getTotal(vendas);  // usa duplicata em vez da função original
  const pct=calcularPercentualMeta(total);
  const fmt = (v: number) => new Intl.NumberFormat("pt-BR",{minimumFractionDigits:2}).format(v);
  console.log(`=== Dashboard: ${periodo} ===`);
  console.log(`Vendas registradas: ${vendas.length}`);
  console.log(`Total: R$ ${fmt(total)}`);
  console.log("Meta atingida: "+formatarPercentualDashboard(pct));
  if (total>=META_MENSAL) {
    console.log("STATUS: META ATINGIDA");
  } else {
    const faltam=META_MENSAL-total;
    console.log(`STATUS: faltam R$ ${fmt(faltam)}`);
  }
}

// ── Execução de demonstração ──────────────────────────────────────────────────

const vendasFevereiro: Venda[] = [
  { descricao: "Produto A", valor: 3200.00 },
  { descricao: "Produto B", valor: 1750.00 },
  { descricao: "Produto C", valor: 4100.00 },
];

exibirDashboard(vendasFevereiro, "Fevereiro/2026");
console.log();
console.log("calcularTotalPeriodo:", calcularTotalPeriodo(vendasFevereiro));
console.log("getTotal (duplicata):", getTotal(vendasFevereiro));
console.log("calcular_soma_vendas (duplicata):", calcular_soma_vendas(vendasFevereiro));
