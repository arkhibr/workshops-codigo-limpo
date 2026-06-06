/**
 * EXERCÍCIO 20 — Strategy e Template Method em TypeScript
 * Tempo estimado: 20 minutos
 * Execute: npx ts-node exercicio.ts
 *
 * INSTRUÇÕES:
 *   O código abaixo tem dois problemas:
 *   1. calcularFrete() usa if/else — adicionar transportadora exige alterar a função.
 *   2. RelatorioEntregas e RelatorioColetas duplicam o esqueleto de 4 etapas.
 *
 *   1. Refatore calcularFrete() para Strategy: crie a interface EstrategiaFrete
 *      com calcular(peso: number, distancia: number) e classes concretas.
 *   2. Refatore os relatórios para Template Method: extraia a classe base abstrata
 *      RelatorioLogistica com formatarLinhas() e montarSaida() abstratos.
 *   3. Execute: npx ts-node exercicio.ts (deve rodar antes e depois)
 */

// ─── Sem Strategy: if/else de transportadora ─────────────────────────────────
interface Entrega {
    id:             string;
    transportadora: string;
    peso:           number;   // kg
    distancia:      number;   // km
    valorNf:        number;
}

function calcularFrete(transportadora: string, peso: number, distancia: number): number {
    /** Adicionar 'loggi' exige alterar esta função. */
    if (transportadora === 'correios') {
        return Math.round((peso * 2.5 + distancia * 0.10) * 100) / 100;
    } else if (transportadora === 'jadlog') {
        return Math.round((peso * 2.0 + distancia * 0.12) * 100) / 100;
    } else if (transportadora === 'retirada') {
        return 0;
    } else {
        throw new Error(`Transportadora desconhecida: ${transportadora}`);
    }
}

// ─── Sem Template Method: esqueleto duplicado em duas classes ─────────────────
class RelatorioEntregas {
    gerar(entregas: Entrega[]): string {
        // Etapa 1: filtrar apenas entregas com valor
        const filtradas = entregas.filter(e => e.valorNf > 0);
        // Etapa 2: formatar linhas (DUPLICADO em RelatorioColetas)
        const linhas = filtradas.map(e => `  ${e.id}: ${e.transportadora} — R$${e.valorNf.toFixed(2)}`);
        // Etapa 3: calcular total (DUPLICADO)
        const total = filtradas.reduce((s, e) => s + e.valorNf, 0);
        // Etapa 4: montar saída (DUPLICADO)
        return `=== Relatório de Entregas ===\n${linhas.join('\n')}\nTotal NF: R$${total.toFixed(2)}`;
    }
}

class RelatorioColetas {
    gerar(entregas: Entrega[]): string {
        // Etapa 1: filtrar (DUPLICADO)
        const filtradas = entregas.filter(e => e.valorNf > 0);
        // Etapa 2: formatar linhas — diferença real está aqui
        const linhas = filtradas.map(e => `  ${e.id}: ${e.peso}kg × ${e.distancia}km`);
        // Etapa 3: calcular total (DUPLICADO)
        const total = filtradas.reduce((s, e) => s + e.valorNf, 0);
        // Etapa 4: montar saída (DUPLICADO)
        return `=== Relatório de Coletas ===\n${linhas.join('\n')}\nVolume: R$${total.toFixed(2)}`;
    }
}

// ─── Demo ─────────────────────────────────────────────────────────────────────
const entregas: Entrega[] = [
    { id: 'ENT-001', transportadora: 'correios',  peso: 2.5, distancia: 150.0, valorNf: 89.90 },
    { id: 'ENT-002', transportadora: 'jadlog',    peso: 5.0, distancia: 300.0, valorNf: 199.90 },
    { id: 'ENT-003', transportadora: 'retirada',  peso: 0.5, distancia: 0.0,   valorNf: 49.90 },
];

for (const e of entregas) {
    const frete = calcularFrete(e.transportadora, e.peso, e.distancia);
    console.log(`${e.id}: frete R$${frete.toFixed(2)}`);
}

console.log('\n' + new RelatorioEntregas().gerar(entregas));
console.log('\n' + new RelatorioColetas().gerar(entregas));
