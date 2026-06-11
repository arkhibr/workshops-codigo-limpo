/**
 * GABARITO — Tutorial 07: Código Legado
 * Execute: npx ts-node gabarito.ts
 *
 * Quatro passos aplicados em sequência sobre o código original:
 *   Passo 1: testes de caracterização escritos e validados
 *   Passo 2: smells anotados no código
 *   Passo 3: magic numbers → constantes; s/r/t/m → nomes descritivos
 *   Passo 4: cache para instância; batchCalc chama calcComm
 */

// ── Passo 3: constantes nomeadas ─────────────────────────────────────────────

const ALIQUOTA_SR_META_ATINGIDA  = 0.08;
const ALIQUOTA_SR_BONUS          = 0.03;
const ALIQUOTA_SR_PARCIAL        = 0.05;
const ALIQUOTA_SR_ABAIXO         = 0.03;

const ALIQUOTA_JR_META_ATINGIDA  = 0.05;
const ALIQUOTA_JR_BONUS          = 0.02;
const ALIQUOTA_JR_ABAIXO         = 0.03;

const MULTIPLICADOR_AGR          = 1.1;
const MULTIPLICADOR_BONUS_META   = 1.2;
const MULTIPLICADOR_PARCIAL_META = 0.8;
const RECEITA_MINIMA             = 5000.0;

// Tabela de vendedores (simulando banco de dados)
const vendedores: Record<string, { nome: string; tipo: string; regiao: string }> = {
    'V001': { nome: 'Ana Paula',   tipo: 'SR', regiao: 'SP' },
    'V002': { nome: 'Carlos Lima', tipo: 'JR', regiao: 'RJ' },
    'V003': { nome: 'Maria Costa', tipo: 'SR', regiao: 'MG' },
};


class CommissionCalc {
    // Passo 2 — smells identificados:
    // SMELL: parâmetros s, r, t, m obscuros → renomeados no Passo 3
    // SMELL: magic numbers → constantes no Passo 3
    // SMELL: cache em módulo global → movido para instância no Passo 4
    // SMELL: lógica idêntica duplicada em batchCalc → eliminada no Passo 4
    // SMELL: comentário "atualizado em jan/2020" desatualizado

    // Passo 4: cache na instância em vez de no módulo
    private cache: Record<string, number> = {};

    calcComm(vendedorId: string, receita: number, tipoMeta: string, meta: number): number {
        // Passo 3: s, r, t, m → vendedorId, receita, tipoMeta, meta
        if (vendedorId in this.cache) {
            return this.cache[vendedorId];
        }

        const v = vendedores[vendedorId];
        if (!v) return 0;

        let comissao = 0;

        if (v.tipo === 'SR') {
            if (receita >= meta) {
                comissao = receita * ALIQUOTA_SR_META_ATINGIDA;
                if (receita > meta * MULTIPLICADOR_BONUS_META) {
                    comissao += (receita - meta * MULTIPLICADOR_BONUS_META) * ALIQUOTA_SR_BONUS;
                }
            } else if (receita >= meta * MULTIPLICADOR_PARCIAL_META) {
                comissao = receita * ALIQUOTA_SR_PARCIAL;
            } else {
                comissao = receita * ALIQUOTA_SR_ABAIXO;
            }
            if (tipoMeta === 'AGR') { comissao *= MULTIPLICADOR_AGR; }
            if (receita < RECEITA_MINIMA) { comissao = 0; }
        } else {
            if (receita >= meta) {
                comissao = receita * ALIQUOTA_JR_META_ATINGIDA;
                if (receita > meta * MULTIPLICADOR_BONUS_META) {
                    comissao += (receita - meta * MULTIPLICADOR_BONUS_META) * ALIQUOTA_JR_BONUS;
                }
            } else {
                // Nota: no original as duas ramificações usam a mesma alíquota para JR.
                // Comportamento preservado intencionalmente.
                comissao = receita * ALIQUOTA_JR_ABAIXO;
            }
            if (tipoMeta === 'AGR') { comissao *= MULTIPLICADOR_AGR; }
            if (receita < RECEITA_MINIMA) { comissao = 0; }
        }

        this.cache[vendedorId] = Math.round(comissao * 100) / 100;
        return this.cache[vendedorId];
    }

    batchCalc(vendas: Array<{ id: string; receita: number; tipo_meta: string; meta: number }>): Record<string, number> {
        // Passo 4: chama calcComm em vez de duplicar a lógica
        const resultados: Record<string, number> = {};
        for (const venda of vendas) {
            resultados[venda.id] = this.calcComm(venda.id, venda.receita, venda.tipo_meta, venda.meta);
        }
        return resultados;
    }
}


// ── Passo 1: testes de caracterização (com valores preenchidos) ──────────────

console.log('=== Passo 1: testes de caracterização ===');

// SR, receita > 120% da meta → bônus: 10000*0.08 + (10000-9600)*0.03 = 812
console.assert(new CommissionCalc().calcComm('V001', 10000, 'STD', 8000) === 812.0, 'SR >120% da meta');
// SR, receita < 5000 → comissão zerada
console.assert(new CommissionCalc().calcComm('V003', 4000, 'STD', 8000) === 0.0, 'SR abaixo do mínimo');
// SR, entre 80%-100% da meta → 7000*0.05 = 350
console.assert(new CommissionCalc().calcComm('V003', 7000, 'STD', 8000) === 350.0, 'SR 80%-100% da meta');
// JR, meta atingida → 6000*0.05 = 300
console.assert(new CommissionCalc().calcComm('V002', 6000, 'STD', 5000) === 300.0, 'JR meta atingida');
// JR, tipo AGR → 300 * 1.1 = 330
console.assert(new CommissionCalc().calcComm('V002', 6000, 'AGR', 5000) === 330.0, 'JR com AGR');
// JR, receita < 5000 → comissão zerada
console.assert(new CommissionCalc().calcComm('V002', 4000, 'STD', 5000) === 0.0, 'JR abaixo do mínimo');
// Vendedor inexistente → 0
console.assert(new CommissionCalc().calcComm('V999', 10000, 'STD', 8000) === 0, 'Inexistente');

console.log('[OK] todos os testes de caracterização passaram');
console.log();

// ── Passo 4: verificação — batchCalc usa calcComm ────────────────────────────

console.log('=== Passo 4: batchCalc sem duplicação ===');
const calc = new CommissionCalc();
const resultado = calc.batchCalc([
    { id: 'V001', receita: 10000, tipo_meta: 'STD', meta: 8000 },
    { id: 'V002', receita: 6000,  tipo_meta: 'AGR', meta: 5000 },
    { id: 'V003', receita: 7000,  tipo_meta: 'STD', meta: 8000 },
]);
console.assert(JSON.stringify(resultado) === JSON.stringify({ V001: 812.0, V002: 330.0, V003: 350.0 }));
console.log('  Resultado:', resultado);
console.log('[OK] batchCalc chama calcComm, sem lógica duplicada');
