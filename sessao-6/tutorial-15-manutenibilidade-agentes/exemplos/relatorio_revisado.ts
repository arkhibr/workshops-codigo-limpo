/**
 * MÓDULO DE RELATÓRIO DE VENDAS — versão consolidada após revisão de deriva
 * Referência: Clean Code, Cap. 1 e 17; Regra do Escoteiro
 *
 * Sinais de deriva eliminados em relação à versão gerada:
 *   - Duplicação removida: calcTotal() e calcular_total_geral() eliminadas;
 *     calcularTotalVendas() é a única função de cálculo de total.
 *   - Estilo unificado: todos os nomes em camelCase português com tipagem explícita.
 *   - Dependência desnecessária removida: _formatadorExterno substituído por
 *     Intl.NumberFormat nativo (runtime resolve sem dependência externa).
 *   - Formatação unificada: espaçamento e assinaturas consistentes em todas
 *     as funções.
 *
 * Execute: npx ts-node sessao-6/tutorial-15-manutenibilidade-agentes/exemplos/relatorio_revisado.ts
 */

interface Venda {
  descricao: string;
  valor: number;
}

// ── Funções de cálculo ────────────────────────────────────────────────────────

function calcularTotalVendas(vendas: Venda[]): number {
  /** Retorna a soma dos valores de todas as vendas da lista. */
  return vendas.reduce((soma, v) => soma + v.valor, 0);
}

function calcularMediaVendas(vendas: Venda[]): number {
  /** Retorna o valor médio das vendas da lista. */
  if (vendas.length === 0) return 0;
  return calcularTotalVendas(vendas) / vendas.length;
}

// ── Formatação ────────────────────────────────────────────────────────────────

const _formatadorReais = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

function formatarValorReais(valor: number): string {
  /** Formata um número como moeda brasileira usando Intl.NumberFormat nativo. */
  return _formatadorReais.format(valor);
}

// ── Relatório ─────────────────────────────────────────────────────────────────

function gerarResumo(vendas: Venda[], titulo: string = "Resumo de Vendas"): void {
  /** Imprime um resumo de vendas com total e média. */
  const total = calcularTotalVendas(vendas);
  const media = calcularMediaVendas(vendas);

  console.log(titulo);
  console.log("-".repeat(40));
  for (const v of vendas) {
    console.log(`${v.descricao}: ${formatarValorReais(v.valor)}`);
  }
  console.log("-".repeat(40));
  console.log(`Total: ${formatarValorReais(total)}`);
  console.log(`Média: ${formatarValorReais(media)}`);
}

// ── Execução de demonstração ──────────────────────────────────────────────────

const vendasJaneiro: Venda[] = [
  { descricao: "Produto A", valor: 1200.00 },
  { descricao: "Produto B", valor: 850.50 },
  { descricao: "Produto C", valor: 3400.00 },
];

gerarResumo(vendasJaneiro, "Relatório de Janeiro");
console.log();
console.log("calcularTotalVendas:", calcularTotalVendas(vendasJaneiro));
