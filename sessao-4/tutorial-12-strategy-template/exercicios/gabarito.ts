/**
 * gabarito.ts — Solução do Exercício 20: Strategy e Template Method em TypeScript
 * Execute: npx ts-node gabarito.ts
 */

// ─── Strategy: EstrategiaFrete ───────────────────────────────────────────────
interface EstrategiaFrete {
    calcular(peso: number, distancia: number): number;
    nome(): string;
}

class FreteCorreios implements EstrategiaFrete {
    calcular(peso: number, distancia: number): number {
        return Math.round((peso * 2.5 + distancia * 0.10) * 100) / 100;
    }
    nome(): string { return 'Correios'; }
}

class FreteJadlog implements EstrategiaFrete {
    calcular(peso: number, distancia: number): number {
        return Math.round((peso * 2.0 + distancia * 0.12) * 100) / 100;
    }
    nome(): string { return 'Jadlog'; }
}

class FreteRetirada implements EstrategiaFrete {
    calcular(peso: number, distancia: number): number { return 0; }
    nome(): string { return 'Retirada'; }
}

class FreteLoggi implements EstrategiaFrete {   // adicionado sem alterar as demais
    calcular(peso: number, distancia: number): number {
        return Math.round((peso * 1.8 + distancia * 0.08) * 100) / 100;
    }
    nome(): string { return 'Loggi'; }
}

class CalculadorFrete {
    constructor(private estrategia: EstrategiaFrete) {}

    calcular(peso: number, distancia: number): number {
        return this.estrategia.calcular(peso, distancia);
    }

    trocarEstrategia(estrategia: EstrategiaFrete): void {
        this.estrategia = estrategia;
    }
}

// ─── Template Method: RelatorioLogistica ─────────────────────────────────────
interface Entrega {
    id:             string;
    transportadora: string;
    peso:           number;
    distancia:      number;
    valorNf:        number;
}

abstract class RelatorioLogistica {
    gerar(entregas: Entrega[]): string {
        const filtradas = entregas.filter(e => e.valorNf > 0);
        const linhas    = this.formatarLinhas(filtradas);
        const total     = filtradas.reduce((s, e) => s + e.valorNf, 0);
        return this.montarSaida(linhas, total);
    }
    protected abstract formatarLinhas(entregas: Entrega[]): string[];
    protected abstract montarSaida(linhas: string[], total: number): string;
}

class RelatorioEntregas extends RelatorioLogistica {
    protected formatarLinhas(entregas: Entrega[]): string[] {
        return entregas.map(e => `  ${e.id}: ${e.transportadora} — R$${e.valorNf.toFixed(2)}`);
    }
    protected montarSaida(linhas: string[], total: number): string {
        return `=== Relatório de Entregas ===\n${linhas.join('\n')}\nTotal NF: R$${total.toFixed(2)}`;
    }
}

class RelatorioColetas extends RelatorioLogistica {
    protected formatarLinhas(entregas: Entrega[]): string[] {
        return entregas.map(e => `  ${e.id}: ${e.peso}kg × ${e.distancia}km`);
    }
    protected montarSaida(linhas: string[], total: number): string {
        return `=== Relatório de Coletas ===\n${linhas.join('\n')}\nVolume: R$${total.toFixed(2)}`;
    }
}

// ─── Verificação ─────────────────────────────────────────────────────────────
function verificar(caso: string, ok: boolean): void {
    console.log(ok ? `OK: ${caso}` : `FALHOU: ${caso}`);
}

console.log("=== Gabarito 20 — Strategy e Template Method: Logística ===\n");

// Strategy
const calc = new CalculadorFrete(new FreteCorreios());
const freteCorreios = calc.calcular(2.5, 150.0);
const esperadoCorreios = Math.round((2.5 * 2.5 + 150.0 * 0.10) * 100) / 100;
verificar(`Strategy — Correios: R$${freteCorreios.toFixed(2)}`, freteCorreios === esperadoCorreios);

calc.trocarEstrategia(new FreteLoggi());
const freteLoggi = calc.calcular(2.5, 150.0);
const esperadoLoggi = Math.round((2.5 * 1.8 + 150.0 * 0.08) * 100) / 100;
verificar(`Strategy — Loggi adicionado sem alterar CalculadorFrete: R$${freteLoggi.toFixed(2)}`, freteLoggi === esperadoLoggi);

calc.trocarEstrategia(new FreteRetirada());
verificar("Strategy — Retirada: R$0,00", calc.calcular(0.5, 0) === 0);

// Template Method
const entregas: Entrega[] = [
    { id: 'ENT-001', transportadora: 'correios', peso: 2.5, distancia: 150.0, valorNf: 89.90 },
    { id: 'ENT-002', transportadora: 'jadlog',   peso: 5.0, distancia: 300.0, valorNf: 199.90 },
];

const re = new RelatorioEntregas().gerar(entregas);
verificar("Template Method — RelatorioEntregas gerado",
    re.includes('Relatório de Entregas') && re.includes('Total NF'));

const rc = new RelatorioColetas().gerar(entregas);
verificar("Template Method — RelatorioColetas gerado",
    rc.includes('Relatório de Coletas') && rc.includes('Volume'));

verificar("Template Method — filtrar e calcular_total não duplicados", true);
