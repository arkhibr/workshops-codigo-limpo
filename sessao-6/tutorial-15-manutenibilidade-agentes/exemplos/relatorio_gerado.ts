/**
 * MÓDULO DE RELATÓRIO DE VENDAS — acumulou deriva por contribuições de IA inconsistentes
 * Referência: Clean Code, Cap. 1 e 17; Regra do Escoteiro
 *
 * ⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
 *     Representa um módulo real que "cresceu" com várias sessões de IA sem contexto.
 *     Analise os quatro sinais de deriva antes de ver a versão revisada.
 *
 * Cenário: o módulo começou com calcularTotalVendas() (contribuição 1).
 *   Contribuição 2: IA adicionou calcTotal() sem saber que a função já existia.
 *   Contribuição 3: IA adicionou formatação de moeda via _formatadorExterno,
 *                   sem saber que Intl.NumberFormat resolve o problema.
 *   Contribuição 4: IA adicionou gerarResumo() com estilo e formatação divergentes.
 *
 * Execute: npx ts-node sessao-6/tutorial-15-manutenibilidade-agentes/exemplos/relatorio_gerado.ts
 */

// Dependência desnecessária — reimplementada localmente para o módulo rodar
// sem instalação. Em um projeto real, a IA teria feito: import formatadorExterno from "..."
const _formatadorExterno = {  // nome simula lib de terceiro
  formatarMoeda(valor: number): string {
    const inteiro = Math.floor(valor);
    const centavos = Math.round((valor - inteiro) * 100);
    const parteInteira = inteiro.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return `R$ ${parteInteira},${centavos.toString().padStart(2, "0")}`;
  },
};

interface Venda {
  descricao: string;
  valor: number;
}

// ── Contribuição 1 — estilo original do módulo ────────────────────────────────

function calcularTotalVendas(vendas: Venda[]): number {
  /** Retorna a soma dos valores de todas as vendas da lista. */
  return vendas.reduce((soma, v) => soma + v.valor, 0);
}

function calcularMediaVendas(vendas: Venda[]): number {
  /** Retorna o valor médio das vendas da lista. */
  if (vendas.length === 0) return 0;
  return calcularTotalVendas(vendas) / vendas.length;
}

// ── Contribuição 2 — IA não recebeu contexto; duplicou com estilo diferente ───

function calcTotal(vendas: any[]): number {  // any; duplica calcularTotalVendas
  let total = 0;
  for (const v of vendas) {
    total = total + v.valor;  // loop manual em vez de reduce
  }
  return total;
}

function calcular_total_geral(lista_de_vendas: any[]): number {  // snake_case misturado
  let soma = 0.0;
  lista_de_vendas.forEach(venda => { soma += venda.valor; });
  return soma;
}

// ── Contribuição 3 — IA puxou "dependência" para formatar moeda ───────────────

function formatarValorRelatorio(valor: number): string {
  // Usa _formatadorExterno em vez de Intl.NumberFormat nativo
  return _formatadorExterno.formatarMoeda(valor);
}

// ── Contribuição 4 — estilo e formatação divergentes ─────────────────────────
function gerarResumo(vendas: any[],titulo = "Resumo de Vendas") { // sem tipagem no retorno
  const total=calcTotal(vendas);  // usa a função duplicada em vez da original
  const media=calcularMediaVendas(vendas);
  console.log(titulo);
  console.log("-".repeat(40));
  vendas.forEach(v=>{
    console.log(v.descricao+" : "+formatarValorRelatorio(v.valor));
  });
  console.log("-".repeat(40));
  console.log("Total: "+formatarValorRelatorio(total));
  console.log("Média: "+formatarValorRelatorio(media));
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
console.log("calcTotal (duplicata):", calcTotal(vendasJaneiro));
console.log("calcular_total_geral (duplicata):", calcular_total_geral(vendasJaneiro));
