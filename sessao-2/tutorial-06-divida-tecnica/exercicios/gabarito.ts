/**
 * GABARITO — Tutorial 06: Dívida Técnica
 * Referência: Clean Code, Cap. 17
 * Execute: npx ts-node gabarito.ts
 *
 * Dívidas identificadas e pagas:
 *   1. MAGIC_NUMBER — 15.0, 25.0, 40.0, 2.5, 3.2, 4.0, 1.8, 2.1, 2.8, 0.12, 0.18, 0.25, 1.3
 *   2. DUPLICAÇÃO   — lógica de cálculo por faixa de peso copiada em calcFrete e estimar
 *   3. FUNÇÕES      — calcFrete faz validação de modalidade, cálculo por faixa, soma de km e taxa de urgência
 *   4. NOMES        — tp, kg, km, t, urg não revelam intenção; estimar é ambíguo
 */

// ── Constantes ──────────────────────────────────────────────────────────────────
// Dívida 1 paga: todos os magic numbers têm nome e estão agrupados por modalidade

// Faixa 1: 0-5 kg (cobrada pela taxa base)
// Faixa 2: 5-20 kg (custo adicional por kg)
// Faixa 3: acima de 20 kg (custo adicional por kg, mais barato por volume)

const MODALIDADE_ECONOMICA = 'A';
const MODALIDADE_PADRAO    = 'B';
const MODALIDADE_EXPRESSA  = 'C';

const LIMITE_FAIXA_1_KG = 5;
const LIMITE_FAIXA_2_KG = 20;

interface TarifaModalidade {
    taxaBase: number;
    custoFaixa2PorKg: number;
    custoFaixa3PorKg: number;
    custoPorKm: number;
}

const TARIFAS_POR_MODALIDADE: Record<string, TarifaModalidade> = {
    [MODALIDADE_ECONOMICA]: {
        taxaBase:          15.0,
        custoFaixa2PorKg:   2.5,
        custoFaixa3PorKg:   1.8,
        custoPorKm:         0.12,
    },
    [MODALIDADE_PADRAO]: {
        taxaBase:          25.0,
        custoFaixa2PorKg:   3.2,
        custoFaixa3PorKg:   2.1,
        custoPorKm:         0.18,
    },
    [MODALIDADE_EXPRESSA]: {
        taxaBase:          40.0,
        custoFaixa2PorKg:   4.0,
        custoFaixa3PorKg:   2.8,
        custoPorKm:         0.25,
    },
};

const FATOR_URGENCIA = 1.3; // acréscimo de 30% para entregas urgentes


// ── Funções auxiliares ──────────────────────────────────────────────────────────
// Dívida 3 paga: cada função faz uma única coisa

function _calcularCustoPeloPeso(pesoKg: number, tarifas: TarifaModalidade): number {
    if (pesoKg <= LIMITE_FAIXA_1_KG) {
        return tarifas.taxaBase;
    }

    if (pesoKg <= LIMITE_FAIXA_2_KG) {
        const excedenteFaixa2 = pesoKg - LIMITE_FAIXA_1_KG;
        return tarifas.taxaBase + excedenteFaixa2 * tarifas.custoFaixa2PorKg;
    }

    // Faixa 3: acima de 20 kg
    const custoFaixa2Completa = (LIMITE_FAIXA_2_KG - LIMITE_FAIXA_1_KG) * tarifas.custoFaixa2PorKg;
    const excedenteFaixa3     = pesoKg - LIMITE_FAIXA_2_KG;
    return tarifas.taxaBase + custoFaixa2Completa + excedenteFaixa3 * tarifas.custoFaixa3PorKg;
}

function _calcularCustoPelaDistancia(distanciaKm: number, tarifas: TarifaModalidade): number {
    return distanciaKm * tarifas.custoPorKm;
}


// ── Funções públicas ────────────────────────────────────────────────────────────
// Dívida 2 paga: lógica centralizada; calcularFrete e estimarFrete chamam a mesma base

function _calcularFretePorModalidade(
    modalidade: string,
    pesoKg: number,
    distanciaKm: number,
): number {
    const tarifas = TARIFAS_POR_MODALIDADE[modalidade];
    if (!tarifas) {
        throw new Error(`Modalidade inválida: ${modalidade}. Use A, B ou C.`);
    }

    const custoPeso      = _calcularCustoPeloPeso(pesoKg, tarifas);
    const custoDistancia = _calcularCustoPelaDistancia(distanciaKm, tarifas);
    return custoPeso + custoDistancia;
}


function calcularFrete(
    modalidade: string,
    pesoKg: number,
    distanciaKm: number,
    urgente: boolean = false,
): number {
    // Dívida 4 paga: parâmetros com nomes descritivos
    let valorBase = _calcularFretePorModalidade(modalidade, pesoKg, distanciaKm);

    if (urgente) {
        // Taxa de urgência: 30% de acréscimo — definido em contrato comercial
        valorBase *= FATOR_URGENCIA;
    }

    return Math.round(valorBase * 100) / 100;
}


function estimarFrete(modalidade: string, pesoKg: number, distanciaKm: number): number {
    // Estimativa sem urgência — alias para calcularFrete sem flag de urgência
    return calcularFrete(modalidade, pesoKg, distanciaKm, false);
}


// ── Execução de demonstração ────────────────────────────────────────────────────

console.log('=== Gabarito: Cálculo de Frete Refatorado ===\n');

console.log('Frete A, 3kg, 100km:', calcularFrete('A', 3, 100));
console.log('Frete A, 15kg, 200km:', calcularFrete('A', 15, 200));
console.log('Frete A, 30kg, 300km:', calcularFrete('A', 30, 300));
console.log('Frete B, 10kg, 150km:', calcularFrete('B', 10, 150));
console.log('Frete C, 25kg, 400km:', calcularFrete('C', 25, 400));
console.log('Frete A urgente, 5kg, 100km:', calcularFrete('A', 5, 100, true));
console.log('Estimativa A, 3kg, 100km:', estimarFrete('A', 3, 100));

// Verificação inline: reimplementação das funções originais para comparar
console.log('\n=== Comparação com versão original (valores devem ser iguais) ===\n');

function calcFreteOriginal(tp: string, kg: number, km: number, urg: boolean = false): number {
    let t = 0.0;
    if (tp === 'A') {
        if (kg <= 5) { t = 15.0; }
        else if (kg <= 20) { t = 15.0 + (kg - 5) * 2.5; }
        else { t = 15.0 + (20 - 5) * 2.5 + (kg - 20) * 1.8; }
        t += km * 0.12;
    } else if (tp === 'B') {
        if (kg <= 5) { t = 25.0; }
        else if (kg <= 20) { t = 25.0 + (kg - 5) * 3.2; }
        else { t = 25.0 + (20 - 5) * 3.2 + (kg - 20) * 2.1; }
        t += km * 0.18;
    } else if (tp === 'C') {
        if (kg <= 5) { t = 40.0; }
        else if (kg <= 20) { t = 40.0 + (kg - 5) * 4.0; }
        else { t = 40.0 + (20 - 5) * 4.0 + (kg - 20) * 2.8; }
        t += km * 0.25;
    }
    if (urg) { t = t * 1.3; }
    return Math.round(t * 100) / 100;
}

const casos: [string, number, number, boolean][] = [
    ['A',  3, 100, false],
    ['A', 15, 200, false],
    ['A', 30, 300, false],
    ['B', 10, 150, false],
    ['C', 25, 400, false],
    ['A',  5, 100, true],
];

let todosIguais = true;
for (const [modalidade, peso, distancia, urgente] of casos) {
    const original   = calcFreteOriginal(modalidade, peso, distancia, urgente);
    const refatorado = calcularFrete(modalidade, peso, distancia, urgente);
    const status     = original === refatorado ? 'OK' : 'DIVERGÊNCIA';
    if (status === 'DIVERGÊNCIA') { todosIguais = false; }
    const label = urgente ? 'urgente' : '       ';
    console.log(`  ${modalidade} ${peso}kg ${distancia}km ${label}: original=${original} refatorado=${refatorado} [${status}]`);
}

console.log(`\nTodos os valores batem: ${todosIguais ? 'SIM' : 'NÃO — verifique a refatoração'}`);
