/**
 * EXERCÍCIO — Tutorial 07: Código Legado
 *
 * Módulo de cálculo de comissões de vendedores.
 * Status: em produção desde 2020, nunca teve testes, nunca foi refatorado.
 *
 * PASSOS (faça um de cada vez, em ordem):
 *
 *   PASSO 1 — TESTES DE CARACTERIZAÇÃO (10 min)
 *     No bloco de execução ao final, escreva asserts para documentar
 *     o comportamento atual. Rode o arquivo para ver os valores, então
 *     substitua os ??? pelos valores observados.
 *     Meta: cobrir pelo menos 5 casos distintos antes de tocar no código.
 *     Importante: use new CommissionCalc() por assert — o cache compartilhado
 *     do módulo mascara resultados de chamadas anteriores.
 *
 *   PASSO 2 — MAPEAR SMELLS (5 min)
 *     Leia CommissionCalc e adicione um comentário // SMELL: antes de
 *     cada problema encontrado.
 *     Exemplos: magic number, nome obscuro, estado global, duplicação,
 *     comentário desatualizado.
 *
 *   PASSO 3 — CONSTANTES + NOMES (8 min)
 *     a) Extraia os magic numbers para constantes nomeadas acima da classe:
 *        0.08, 0.05, 0.03, 0.02, 1.1, 1.2, 0.8, 5000
 *     b) Renomeie os parâmetros em calcComm:
 *        s → vendedorId   r → receita   t → tipoMeta   m → meta
 *     Verifique que seus testes do Passo 1 ainda passam.
 *
 *   PASSO 4 — ELIMINAR DUPLICAÇÃO (10 min)
 *     batchCalc duplica toda a lógica de calcComm em vez de chamá-lo.
 *     Altere batchCalc para chamar this.calcComm em vez de repetir.
 *     Mova também o cache de variável de módulo para this.cache no construtor,
 *     para que cada instância tenha seu próprio estado isolado.
 *     Verifique que seus testes continuam passando.
 *
 * Para rodar: npx ts-node exercicio.ts
 */

// Estado global mutável modificado por método — dificulta paralelismo e testes
const cache: Record<string, number> = {};

// Tabela de vendedores (simulando banco de dados)
const vendedores: Record<string, { nome: string; tipo: string; regiao: string }> = {
    'V001': { nome: 'Ana Paula',   tipo: 'SR', regiao: 'SP' },
    'V002': { nome: 'Carlos Lima', tipo: 'JR', regiao: 'RJ' },
    'V003': { nome: 'Maria Costa', tipo: 'SR', regiao: 'MG' },
};


class CommissionCalc {
    // Calcula comissao mensal — atualizado em jan/2020
    // (comentario desatualizado: a logica foi alterada em 2022 sem atualizar o comentario)

    calcComm(s: string, r: number, t: string, m: number): number {
        // s = vendedor id, r = receita total, t = tipo de meta, m = meta

        if (s in cache) {
            return cache[s];
        }

        const v = vendedores[s];
        if (!v) {
            return 0;
        }

        let c = 0;

        // calcula para senior
        if (v.tipo === 'SR') {
            if (r >= m) {
                c = r * 0.08;
                if (r > m * 1.2) {
                    c = c + (r - m * 1.2) * 0.03;
                }
            } else {
                if (r >= m * 0.8) {
                    c = r * 0.05;
                } else {
                    c = r * 0.03;
                }
            }
            if (t === 'AGR') { c = c * 1.1; }
            if (r < 5000)    { c = 0; }

        // calcula para junior — copiado e modificado do bloco acima
        } else {
            if (r >= m) {
                c = r * 0.05;
                if (r > m * 1.2) {
                    c = c + (r - m * 1.2) * 0.02;
                }
            } else {
                if (r >= m * 0.8) {
                    c = r * 0.03;
                } else {
                    c = r * 0.03; // igual ao else acima — bug ou intencional?
                }
            }
            if (t === 'AGR') { c = c * 1.1; }
            if (r < 5000)    { c = 0; }
        }

        cache[s] = Math.round(c * 100) / 100;
        return cache[s];
    }

    batchCalc(vendas: Array<{ id: string; receita: number; tipo_meta: string; meta: number }>): Record<string, number> {
        const resultados: Record<string, number> = {};

        for (const venda of vendas) {
            const s = venda.id;
            const r = venda.receita;
            const t = venda.tipo_meta;
            const m = venda.meta;

            const v = vendedores[s];
            if (!v) continue;

            // duplica toda a logica de calcComm ao invés de chamar o método
            let c = 0;
            if (v.tipo === 'SR') {
                if (r >= m) {
                    c = r * 0.08;
                    if (r > m * 1.2) { c = c + (r - m * 1.2) * 0.03; }
                } else {
                    c = r >= m * 0.8 ? r * 0.05 : r * 0.03;
                }
                if (t === 'AGR') { c = c * 1.1; }
                if (r < 5000)    { c = 0; }
            } else {
                if (r >= m) {
                    c = r * 0.05;
                    if (r > m * 1.2) { c = c + (r - m * 1.2) * 0.02; }
                } else {
                    c = r * 0.03;
                }
                if (t === 'AGR') { c = c * 1.1; }
                if (r < 5000)    { c = 0; }
            }

            resultados[s] = Math.round(c * 100) / 100;
        }

        return resultados;
    }
}

// ── Execução principal ──────────────────────────────────────────────────────────

// -----------------------------------------------------------------------
// PASSO 1: escreva seus testes de caracterização aqui.
// Use new CommissionCalc() e delete cache[id] entre testes para evitar
// que o cache global mascare o comportamento.
// -----------------------------------------------------------------------

console.log('=== Explorando o comportamento atual ===');
const calcular = (vid: string, r: number, t: string, m: number) => {
    delete cache[vid];
    return new CommissionCalc().calcComm(vid, r, t, m);
};

console.log('SR, receita=10000, meta=8000, tipo=STD:', calcular('V001', 10000, 'STD', 8000));
console.log('SR, receita=4000,  meta=8000, tipo=STD:', calcular('V003', 4000,  'STD', 8000));
console.log('SR, receita=7000,  meta=8000, tipo=STD:', calcular('V003', 7000,  'STD', 8000));
console.log('JR, receita=6000,  meta=5000, tipo=STD:', calcular('V002', 6000,  'STD', 5000));
console.log('JR, receita=6000,  meta=5000, tipo=AGR:', calcular('V002', 6000,  'AGR', 5000));
console.log('JR, receita=4000,  meta=5000, tipo=STD:', calcular('V002', 4000,  'STD', 5000));
console.log('Inexistente V999:', calcular('V999', 10000, 'STD', 8000));

console.log('\n=== Batch ===');
Object.keys(cache).forEach(k => delete cache[k]);
console.log(new CommissionCalc().batchCalc([
    { id: 'V001', receita: 10000, tipo_meta: 'STD', meta: 8000 },
    { id: 'V002', receita: 6000,  tipo_meta: 'AGR', meta: 5000 },
]));

// -----------------------------------------------------------------------
// Substitua os ??? e descomente os asserts após anotar os valores acima:
// -----------------------------------------------------------------------
// console.assert(calcular('V001', 10000, 'STD', 8000) === ???, 'SR >120% da meta');
// console.assert(calcular('V003', 4000,  'STD', 8000) === ???, 'SR abaixo do mínimo');
// console.assert(calcular('V003', 7000,  'STD', 8000) === ???, 'SR 80%-100% da meta');
// console.assert(calcular('V002', 6000,  'STD', 5000) === ???, 'JR meta atingida');
// console.assert(calcular('V002', 6000,  'AGR', 5000) === ???, 'JR com AGR');
// console.assert(calcular('V002', 4000,  'STD', 5000) === ???, 'JR abaixo do mínimo');
// console.assert(calcular('V999', 10000, 'STD', 8000) === ???, 'Inexistente');
// console.log('[OK] testes de caracterização passando');
