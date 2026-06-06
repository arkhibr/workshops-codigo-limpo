/**
 * MÓDULO DE DASHBOARD DE VENDAS — versão consolidada após revisão de deriva
 * Referência: Clean Code, Cap. 1 e 17; Regra do Escoteiro
 *
 * Sinais de deriva eliminados em relação ao exercício:
 *   - Duplicação removida: getTotal() e calcular_soma_vendas() eliminadas;
 *     calcularTotalPeriodo() é a única função de cálculo de total.
 *   - Estilo unificado: todos os nomes em camelCase português com tipagem explícita.
 *   - Dependência desnecessária removida: UtilPercentual substituído por
 *     toFixed nativo (runtime resolve sem dependência externa).
 *   - Formatação unificada: espaçamento e assinaturas consistentes.
 *
 * Execute: npx ts-node sessao-6/tutorial-15-manutenibilidade-agentes/exercicios/gabarito.ts
 */

const META_MENSAL: number = 10_000.0;

interface Venda {
  descricao: string;
  valor: number;
}

// ── Funções de cálculo ────────────────────────────────────────────────────────

function calcularTotalPeriodo(vendas: Venda[]): number {
  /** Retorna a soma dos valores das vendas no período. */
  return vendas.reduce((soma, v) => soma + v.valor, 0);
}

function calcularPercentualMeta(total: number): number {
  /** Retorna o percentual atingido em relação à meta mensal. */
  if (META_MENSAL === 0) return 0;
  return total / META_MENSAL;
}

// ── Formatação ────────────────────────────────────────────────────────────────

const _formatadorReais = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

function formatarReais(valor: number): string {
  /** Formata um número como moeda brasileira usando Intl.NumberFormat nativo. */
  return _formatadorReais.format(valor);
}

function formatarPercentual(valor: number): string {
  /** Formata um número fracionário como percentual com uma casa decimal. */
  return `${(valor * 100).toFixed(1)}%`;
}

// ── Dashboard ─────────────────────────────────────────────────────────────────

function exibirDashboard(vendas: Venda[], periodo: string = "Período Atual"): void {
  /** Imprime o dashboard de vendas com total, percentual de meta e status. */
  const total = calcularTotalPeriodo(vendas);
  const percentual = calcularPercentualMeta(total);

  console.log(`=== Dashboard: ${periodo} ===`);
  console.log(`Vendas registradas: ${vendas.length}`);
  console.log(`Total: ${formatarReais(total)}`);
  console.log(`Meta atingida: ${formatarPercentual(percentual)}`);

  if (total >= META_MENSAL) {
    console.log("STATUS: META ATINGIDA");
  } else {
    const faltam = META_MENSAL - total;
    console.log(`STATUS: faltam ${formatarReais(faltam)}`);
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
