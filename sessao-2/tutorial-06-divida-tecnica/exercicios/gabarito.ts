/**
 * GABARITO — Tutorial 06: Dívida Técnica
 * Execute: npx ts-node gabarito.ts
 *
 * Quatro passos aplicados em sequência:
 *   Passo 1 — Dívidas identificadas:
 *     MAGIC_NUMBER  15/25/40 (taxa_base), 2.5/3.2/4.0 (faixa 2),
 *                   1.8/2.1/2.8 (faixa 3), 0.12/0.18/0.25 (km), 1.3 (urgência), 5 e 20
 *     NOMES         tp, kg, km, t, urg obscuros; estimar é ambíguo
 *     DUPLICAÇÃO    corpo idêntico em calcFrete e estimar
 *     FUNÇÕES       calcFrete faz: validar + calcular por faixa + km + urgência
 *   Passo 2 — constantes extraídas
 *   Passo 3 — parâmetros renomeados
 *   Passo 4 — _calcularPorModalidade extraída; estimarFrete chama calcularFrete
 */

// ── Passo 2: constantes nomeadas ─────────────────────────────────────────────

const LIMITE_FAIXA_1_KG = 5;
const LIMITE_FAIXA_2_KG = 20;
const FATOR_URGENCIA    = 1.3;

interface Tarifa { taxaBase: number; custoFaixa2: number; custoFaixa3: number; custoKm: number; }

const TARIFAS: Record<string, Tarifa> = {
    'A': { taxaBase: 15.0, custoFaixa2: 2.5, custoFaixa3: 1.8, custoKm: 0.12 },
    'B': { taxaBase: 25.0, custoFaixa2: 3.2, custoFaixa3: 2.1, custoKm: 0.18 },
    'C': { taxaBase: 40.0, custoFaixa2: 4.0, custoFaixa3: 2.8, custoKm: 0.25 },
};


// ── Passo 4: lógica extraída — zero duplicação ────────────────────────────────

function _calcularPorModalidade(modalidade: string, pesoKg: number, distanciaKm: number): number {
    const t = TARIFAS[modalidade];
    if (!t) throw new Error(`Modalidade inválida: ${modalidade}. Use A, B ou C.`);

    let custo: number;
    if (pesoKg <= LIMITE_FAIXA_1_KG) {
        custo = t.taxaBase;
    } else if (pesoKg <= LIMITE_FAIXA_2_KG) {
        custo = t.taxaBase + (pesoKg - LIMITE_FAIXA_1_KG) * t.custoFaixa2;
    } else {
        custo = t.taxaBase
              + (LIMITE_FAIXA_2_KG - LIMITE_FAIXA_1_KG) * t.custoFaixa2
              + (pesoKg - LIMITE_FAIXA_2_KG) * t.custoFaixa3;
    }
    custo += distanciaKm * t.custoKm;
    return custo;
}


// ── Passos 3+4: funções públicas com nomes descritivos ───────────────────────

function calcularFrete(modalidade: string, pesoKg: number, distanciaKm: number, urgente: boolean = false): number {
    let valor = _calcularPorModalidade(modalidade, pesoKg, distanciaKm);
    if (urgente) {
        valor *= FATOR_URGENCIA;
    }
    return Math.round(valor * 100) / 100;
}


function estimarFrete(modalidade: string, pesoKg: number, distanciaKm: number): number {
    return calcularFrete(modalidade, pesoKg, distanciaKm, false);
}


// ── Verificação ──────────────────────────────────────────────────────────────

const casos: Array<[string, number, number, boolean, number]> = [
    ['A',  3, 100, false,  27.0],
    ['A', 15, 200, false,  64.0],
    ['A', 30, 300, false, 106.5],
    ['B', 10, 150, false,  68.0],
    ['C', 25, 400, false, 214.0],
    ['A',  5, 100, true,   35.1],
];

console.log('=== Gabarito T06 — valores esperados ===\n');

let ok = true;
for (const [modalidade, peso, dist, urgente, esperado] of casos) {
    const resultado = calcularFrete(modalidade, peso, dist, urgente);
    const status    = resultado === esperado ? 'OK' : `ERRO — esperado ${esperado}`;
    if (resultado !== esperado) ok = false;
    const label = urgente ? 'urgente' : '       ';
    console.log(`  ${modalidade} ${String(peso).padStart(2)}kg ${String(dist).padStart(3)}km ${label}: ${resultado} [${status}]`);
}

console.log(`\nEstimativa A, 3kg, 100km: ${estimarFrete('A', 3, 100)}`);
console.log(`\nTodos corretos: ${ok ? 'SIM' : 'NÃO'}`);
