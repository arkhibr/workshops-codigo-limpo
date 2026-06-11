/**
 * EXERCÍCIO — Tutorial 06: Dívida Técnica
 * Referência: Clean Code, Cap. 17
 * Execute: npx ts-node exercicio.ts
 *
 * Este módulo calcula fretes para uma transportadora fictícia.
 * Ele está funcional, mas carrega 4 tipos de dívida técnica.
 *
 * PASSOS (faça um de cada vez, em ordem):
 *
 *   PASSO 1 — IDENTIFICAR (5 min)
 *     Leia o código abaixo. Antes de cada dívida, adicione um comentário:
 *         // DÍVIDA [TIPO]: <descrição>
 *     Tipos: MAGIC_NUMBER, NOMES, DUPLICAÇÃO, FUNÇÕES
 *     Meta: encontrar pelo menos 3 das 4 antes de avançar.
 *
 *   PASSO 2 — CONSTANTES (5 min)
 *     Extraia os magic numbers para constantes nomeadas acima das funções.
 *     Substitua os literais numéricos pelas constantes no corpo das funções.
 *     Verifique: npx ts-node exercicio.ts deve imprimir os mesmos valores.
 *
 *   PASSO 3 — NOMES (5 min)
 *     Renomeie os parâmetros obscuros em calcFrete e estimar:
 *       tp  → modalidade
 *       kg  → pesoKg
 *       km  → distanciaKm
 *       urg → urgente
 *     Renomeie estimar para estimarFrete.
 *     Verifique que o arquivo ainda executa sem erros.
 *
 *   PASSO 4 — ELIMINAR DUPLICAÇÃO (10 min)
 *     calcFrete e estimar têm exatamente o mesmo corpo de cálculo.
 *     Extraia a lógica compartilhada para _calcularPorModalidade.
 *     Faça calcularFrete e estimarFrete chamarem essa função.
 *     Verifique que a saída continua idêntica.
 */

// ════════════════════════════════════════════════════════════════════════════════
// CÓDIGO COM DÍVIDA TÉCNICA — trabalhe aqui nos Passos 1, 2 e 3
// ════════════════════════════════════════════════════════════════════════════════

function calcFrete(tp: string, kg: number, km: number, urg: boolean = false): number {
    let t = 0.0;
    if (tp === 'A') {
        if (kg <= 5) {
            t = 15.0;
        } else if (kg <= 20) {
            t = 15.0 + (kg - 5) * 2.5;
        } else {
            t = 15.0 + (20 - 5) * 2.5 + (kg - 20) * 1.8;
        }
        t += km * 0.12;
    } else if (tp === 'B') {
        if (kg <= 5) {
            t = 25.0;
        } else if (kg <= 20) {
            t = 25.0 + (kg - 5) * 3.2;
        } else {
            t = 25.0 + (20 - 5) * 3.2 + (kg - 20) * 2.1;
        }
        t += km * 0.18;
    } else if (tp === 'C') {
        if (kg <= 5) {
            t = 40.0;
        } else if (kg <= 20) {
            t = 40.0 + (kg - 5) * 4.0;
        } else {
            t = 40.0 + (20 - 5) * 4.0 + (kg - 20) * 2.8;
        }
        t += km * 0.25;
    }
    if (urg) {
        t = t * 1.3;
    }
    return Math.round(t * 100) / 100;
}


function estimar(tp: string, kg: number, km: number): number {
    let t = 0.0;
    if (tp === 'A') {
        if (kg <= 5) {
            t = 15.0;
        } else if (kg <= 20) {
            t = 15.0 + (kg - 5) * 2.5;
        } else {
            t = 15.0 + (20 - 5) * 2.5 + (kg - 20) * 1.8;
        }
        t += km * 0.12;
    } else if (tp === 'B') {
        if (kg <= 5) {
            t = 25.0;
        } else if (kg <= 20) {
            t = 25.0 + (kg - 5) * 3.2;
        } else {
            t = 25.0 + (20 - 5) * 3.2 + (kg - 20) * 2.1;
        }
        t += km * 0.18;
    } else if (tp === 'C') {
        if (kg <= 5) {
            t = 40.0;
        } else if (kg <= 20) {
            t = 40.0 + (kg - 5) * 4.0;
        } else {
            t = 40.0 + (20 - 5) * 4.0 + (kg - 20) * 2.8;
        }
        t += km * 0.25;
    }
    return Math.round(t * 100) / 100;
}


// ════════════════════════════════════════════════════════════════════════════════
// PASSO 2 — adicione as constantes nomeadas aqui
// ════════════════════════════════════════════════════════════════════════════════

// const LIMITE_FAIXA_1_KG = 5;
// const LIMITE_FAIXA_2_KG = 20;
// const FATOR_URGENCIA    = 1.3;
// const TARIFAS: Record<string, {taxaBase: number; custoFaixa2: number; custoFaixa3: number; custoKm: number}> = { ... };


// ════════════════════════════════════════════════════════════════════════════════
// PASSO 4 — extraia aqui a função auxiliar e redefina as funções públicas
// ════════════════════════════════════════════════════════════════════════════════

// function _calcularPorModalidade(modalidade: string, pesoKg: number, distanciaKm: number): number { ... }
// function calcularFrete(modalidade: string, pesoKg: number, distanciaKm: number, urgente: boolean = false): number { ... }
// function estimarFrete(modalidade: string, pesoKg: number, distanciaKm: number): number { ... }


// ════════════════════════════════════════════════════════════════════════════════
// Bloco de verificação — não altere
// ════════════════════════════════════════════════════════════════════════════════

console.log('=== Verificação: Cálculo de Frete ===\n');

console.log('Frete A, 3kg, 100km:',          calcFrete('A',  3, 100));        // 27
console.log('Frete A, 15kg, 200km:',         calcFrete('A', 15, 200));        // 64
console.log('Frete A, 30kg, 300km:',         calcFrete('A', 30, 300));        // 106.5
console.log('Frete B, 10kg, 150km:',         calcFrete('B', 10, 150));        // 68
console.log('Frete C, 25kg, 400km:',         calcFrete('C', 25, 400));        // 214
console.log('Frete A urgente, 5kg, 100km:',  calcFrete('A',  5, 100, true));  // 35.1
console.log('Estimativa A, 3kg, 100km:',     estimar('A', 3, 100));           // 27

// Após o Passo 4, descomente e verifique que os valores batem:
// console.log('\n--- Versão refatorada (Passo 4) ---');
// console.log('Frete A, 3kg, 100km:',         calcularFrete('A',  3, 100));
// console.log('Frete A, 15kg, 200km:',        calcularFrete('A', 15, 200));
// console.log('Frete A, 30kg, 300km:',        calcularFrete('A', 30, 300));
// console.log('Frete B, 10kg, 150km:',        calcularFrete('B', 10, 150));
// console.log('Frete C, 25kg, 400km:',        calcularFrete('C', 25, 400));
// console.log('Frete A urgente, 5kg, 100km:', calcularFrete('A',  5, 100, true));
// console.log('Estimativa A, 3kg, 100km:',    estimarFrete('A', 3, 100));
