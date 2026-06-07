/**
 * equivalente.ts — Strategy e Template Method em TypeScript
 * Execute: npx ts-node equivalente.ts
 */

// ─── Ruim: if/elif de imposto ─────────────────────────────────────────────────
function calcularImpostoRuim(regime: string, valor: number): number {
    if (regime === 'simples')   return Math.round(valor * 0.06   * 100) / 100;
    if (regime === 'presumido') return Math.round(valor * 0.132  * 100) / 100;
    if (regime === 'real')      return Math.round(valor * 0.34   * 100) / 100;
    throw new Error(`Regime desconhecido: ${regime}`);
}

// ─── Bom: Strategy ────────────────────────────────────────────────────────────
interface EstrategiaImposto {
    calcular(valor: number): number;
    nome(): string;
}

class SimplesNacional implements EstrategiaImposto {
    calcular(valor: number): number { return Math.round(valor * 0.06  * 100) / 100; }
    nome(): string { return 'Simples Nacional'; }
}

class LucroPresumido implements EstrategiaImposto {
    calcular(valor: number): number { return Math.round(valor * 0.132 * 100) / 100; }
    nome(): string { return 'Lucro Presumido'; }
}

class LucroReal implements EstrategiaImposto {
    calcular(valor: number): number { return Math.round(valor * 0.34  * 100) / 100; }
    nome(): string { return 'Lucro Real'; }
}

class MEI implements EstrategiaImposto {  // adicionado sem alterar as demais
    calcular(valor: number): number { return Math.round(valor * 0.05  * 100) / 100; }
    nome(): string { return 'MEI'; }
}

class CalculadorImposto {
    constructor(private estrategia: EstrategiaImposto) {}

    calcular(valor: number): number { return this.estrategia.calcular(valor); }

    trocarEstrategia(estrategia: EstrategiaImposto): void {
        this.estrategia = estrategia;
    }
}

// ─── Bom: Template Method ─────────────────────────────────────────────────────
interface DadosVenda { produto: string; valor: number; quantidade: number; }

abstract class RelatorioBase {
    gerar(dados: DadosVenda[]): string {
        const filtrados = dados.filter(d => d.valor > 0);
        const linhas    = this.formatarLinhas(filtrados);
        const total     = filtrados.reduce((s, d) => s + d.valor * d.quantidade, 0);
        return this.montarSaida(linhas, total);
    }
    protected abstract formatarLinhas(dados: DadosVenda[]): string[];
    protected abstract montarSaida(linhas: string[], total: number): string;
}

class RelatorioVendas extends RelatorioBase {
    protected formatarLinhas(dados: DadosVenda[]): string[] {
        return dados.map(d => `  ${d.produto}: ${d.quantidade} × R$${d.valor.toFixed(2)}`);
    }
    protected montarSaida(linhas: string[], total: number): string {
        return `=== Relatório de Vendas ===\n${linhas.join('\n')}\nTotal: R$${total.toFixed(2)}`;
    }
}

class RelatorioFinanceiro extends RelatorioBase {
    protected formatarLinhas(dados: DadosVenda[]): string[] {
        return dados.map(d => `  R$${(d.valor * d.quantidade).toFixed(2)} (${d.produto})`);
    }
    protected montarSaida(linhas: string[], total: number): string {
        return `=== Relatório Financeiro ===\n${linhas.join('\n')}\nReceita: R$${total.toFixed(2)}`;
    }
}

// ─── Demo ─────────────────────────────────────────────────────────────────────
console.log("=== Strategy + Template Method TypeScript ===\n");

const calc = new CalculadorImposto(new SimplesNacional());
console.assert(calc.calcular(10000) === 600);
console.log("OK: Strategy — SimplesNacional R$600,00");

calc.trocarEstrategia(new MEI());
console.assert(calc.calcular(10000) === 500);
console.log("OK: Strategy — MEI adicionado sem alterar CalculadorImposto");

const dados: DadosVenda[] = [
    { produto: 'Webcam HD', valor: 299.90, quantidade: 2 },
    { produto: 'Teclado',   valor: 189.90, quantidade: 1 },
];

const rv = new RelatorioVendas().gerar(dados);
console.assert(rv.includes('Relatório de Vendas'));
console.log("OK: Template Method — RelatorioVendas gerado");

const rf = new RelatorioFinanceiro().gerar(dados);
console.assert(rf.includes('Relatório Financeiro'));
console.log("OK: Template Method — RelatorioFinanceiro gerado");
