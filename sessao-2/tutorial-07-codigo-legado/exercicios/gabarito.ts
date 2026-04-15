/**
 * GABARITO — Tutorial 07: Gestão de Código Legado
 *
 * Para rodar: npx ts-node gabarito.ts
 */

// ============================================================================
// ETAPA 1: Testes de Caracterização (executados sobre o código original)
// ============================================================================

const vendedoresRaw: Record<string, { nome: string; tipo: string; regiao: string }> = {
    'V001': { nome: 'Ana Paula',   tipo: 'SR', regiao: 'SP' },
    'V002': { nome: 'Carlos Lima', tipo: 'JR', regiao: 'RJ' },
    'V003': { nome: 'Maria Costa', tipo: 'SR', regiao: 'MG' },
};

class CommissionCalcOriginal {
    private cache: Record<string, number> = {};

    calcComm(s: string, r: number, t: string, m: number): number {
        if (s in this.cache) return this.cache[s];

        const v = vendedoresRaw[s];
        if (!v) return 0;

        let c = 0;
        if (v.tipo === 'SR') {
            if (r >= m) {
                c = r * 0.08;
                if (r > m * 1.2) c = c + (r - m * 1.2) * 0.03;
            } else {
                c = r >= m * 0.8 ? r * 0.05 : r * 0.03;
            }
            if (t === 'AGR') c *= 1.1;
            if (r < 5000)    c = 0;
        } else {
            if (r >= m) {
                c = r * 0.05;
                if (r > m * 1.2) c = c + (r - m * 1.2) * 0.02;
            } else {
                c = r * 0.03; // parcial e abaixo idênticos para JR
            }
            if (t === 'AGR') c *= 1.1;
            if (r < 5000)    c = 0;
        }

        this.cache[s] = Math.round(c * 100) / 100;
        return this.cache[s];
    }
}

function executarTestesDeCaracterizacao(): void {
    // SR, receita acima de 120% da meta → 10000*0.08 + (10000-9600)*0.03 = 812
    const o1 = new CommissionCalcOriginal();
    console.assert(o1.calcComm('V001', 10000, 'STD', 8000) === 812, 'SR 10000/8000 STD');

    // SR, receita abaixo do mínimo → zerada
    const o2 = new CommissionCalcOriginal();
    console.assert(o2.calcComm('V001', 4000, 'STD', 8000) === 0, 'SR receita < 5000');

    // SR, receita entre 80%-100% da meta → 7000*0.05 = 350
    const o3 = new CommissionCalcOriginal();
    console.assert(o3.calcComm('V003', 7000, 'STD', 8000) === 350, 'SR parcial 7000/8000');

    // JR, receita acima da meta → 6000*0.05 = 300
    const o4 = new CommissionCalcOriginal();
    console.assert(o4.calcComm('V002', 6000, 'STD', 5000) === 300, 'JR 6000/5000 STD');

    // JR com meta AGR → 300 * 1.1 = 330
    const o5 = new CommissionCalcOriginal();
    console.assert(o5.calcComm('V002', 6000, 'AGR', 5000) === 330, 'JR 6000/5000 AGR');

    // JR, receita abaixo do mínimo → zerada
    const o6 = new CommissionCalcOriginal();
    console.assert(o6.calcComm('V002', 4000, 'STD', 5000) === 0, 'JR receita < 5000');

    // Vendedor inexistente → 0
    const o7 = new CommissionCalcOriginal();
    console.assert(o7.calcComm('V999', 10000, 'STD', 8000) === 0, 'Vendedor inexistente');

    console.log('[OK] Todos os testes de caracterização passaram.');
}


// ============================================================================
// ETAPA 2: Smells identificados
//
// SMELL: cache global mutável compartilhado entre instâncias
// SMELL: parâmetros de uma letra (s, r, t, m)
// SMELL: magic numbers 0.08, 0.05, 0.03, 0.02, 1.1, 5000, 1.2
// SMELL: lógica duplicada entre calcComm e batchCalc
// SMELL: comentário desatualizado ("jan/2020")
// SMELL: dois ramos else com alíquotas idênticas para JR (bug ou intenção?)
// ============================================================================


// ============================================================================
// ETAPA 3: Versão Refatorada
// ============================================================================

const ALIQUOTA_SR_META_ATINGIDA   = 0.08;
const ALIQUOTA_SR_BONUS_EXCEDENTE = 0.03;
const ALIQUOTA_SR_PARCIAL         = 0.05;
const ALIQUOTA_SR_ABAIXO          = 0.03;

const ALIQUOTA_JR_META_ATINGIDA   = 0.05;
const ALIQUOTA_JR_BONUS_EXCEDENTE = 0.02;
const ALIQUOTA_JR_ABAIXO          = 0.03;

const MULTIPLICADOR_META_BONUS    = 1.2;
const MULTIPLICADOR_META_PARCIAL  = 0.8;
const MULTIPLICADOR_META_AGRICOLA = 1.1;
const RECEITA_MINIMA_COMISSAO     = 5000;


interface DadosVendedor {
    nome: string;
    tipo: string;
    regiao: string;
}

class Vendedor {
    constructor(
        public readonly id: string,
        public readonly nome: string,
        public readonly tipo: string,
        public readonly regiao: string,
    ) {}
}

class EntradaComissao {
    constructor(
        public readonly vendedorId: string,
        public readonly receita: number,
        public readonly tipoMeta: string,
        public readonly meta: number,
    ) {}
}


class RepositorioDeVendedores {
    private vendedores: Map<string, Vendedor>;

    constructor(dados: Record<string, DadosVendedor>) {
        this.vendedores = new Map(
            Object.entries(dados).map(([id, d]) =>
                [id, new Vendedor(id, d.nome, d.tipo, d.regiao)]
            )
        );
    }

    buscar(id: string): Vendedor | undefined {
        return this.vendedores.get(id);
    }
}


class CalculadorDeComissao {
    calcular(entrada: EntradaComissao, vendedor: Vendedor): number {
        if (entrada.receita < RECEITA_MINIMA_COMISSAO) return 0;

        const comissao = vendedor.tipo === 'SR'
            ? this.comissaoSenior(entrada.receita, entrada.meta)
            : this.comissaoJunior(entrada.receita, entrada.meta);

        const fator = entrada.tipoMeta === 'AGR' ? MULTIPLICADOR_META_AGRICOLA : 1;
        return Math.round(comissao * fator * 100) / 100;
    }

    private comissaoSenior(receita: number, meta: number): number {
        if (receita >= meta) {
            let c = receita * ALIQUOTA_SR_META_ATINGIDA;
            if (receita > meta * MULTIPLICADOR_META_BONUS) {
                c += (receita - meta * MULTIPLICADOR_META_BONUS) * ALIQUOTA_SR_BONUS_EXCEDENTE;
            }
            return c;
        }
        return receita >= meta * MULTIPLICADOR_META_PARCIAL
            ? receita * ALIQUOTA_SR_PARCIAL
            : receita * ALIQUOTA_SR_ABAIXO;
    }

    private comissaoJunior(receita: number, meta: number): number {
        if (receita >= meta) {
            let c = receita * ALIQUOTA_JR_META_ATINGIDA;
            if (receita > meta * MULTIPLICADOR_META_BONUS) {
                c += (receita - meta * MULTIPLICADOR_META_BONUS) * ALIQUOTA_JR_BONUS_EXCEDENTE;
            }
            return c;
        }
        // Nota: no original, parcial e abaixo usavam a mesma alíquota para JR.
        // Comportamento preservado.
        return receita * ALIQUOTA_JR_ABAIXO;
    }
}


class ProcessadorDeComissoes {
    constructor(
        private readonly repositorio: RepositorioDeVendedores,
        private readonly calculador: CalculadorDeComissao,
    ) {}

    calcularIndividual(entrada: EntradaComissao): number {
        const vendedor = this.repositorio.buscar(entrada.vendedorId);
        if (!vendedor) return 0;
        return this.calculador.calcular(entrada, vendedor);
    }

    calcularLote(entradas: EntradaComissao[]): Record<string, number> {
        return Object.fromEntries(
            entradas.map(e => [e.vendedorId, this.calcularIndividual(e)])
        );
    }
}


// ============================================================================
// ETAPA 4: Verificação — os testes de caracterização devem passar na versão nova
// ============================================================================

function executarTestesNaVersaoRefatorada(): void {
    const repositorio = new RepositorioDeVendedores(vendedoresRaw);
    const processador = new ProcessadorDeComissoes(repositorio, new CalculadorDeComissao());

    const calcular = (vid: string, r: number, t: string, m: number) =>
        processador.calcularIndividual(new EntradaComissao(vid, r, t, m));

    console.assert(calcular('V001', 10000, 'STD', 8000) === 812);
    console.assert(calcular('V001', 4000,  'STD', 8000) === 0);
    console.assert(calcular('V003', 7000,  'STD', 8000) === 350);
    console.assert(calcular('V002', 6000,  'STD', 5000) === 300);
    console.assert(calcular('V002', 6000,  'AGR', 5000) === 330);
    console.assert(calcular('V002', 4000,  'STD', 5000) === 0);
    console.assert(calcular('V999', 10000, 'STD', 8000) === 0);

    console.log('[OK] Todos os testes de caracterização passaram na versão refatorada.');
}


// ── Execução principal ──────────────────────────────────────────────────────

console.log('=== Etapa 1: Testes de Caracterização (versão original) ===');
executarTestesDeCaracterizacao();
console.log();

console.log('=== Etapa 4: Verificação (versão refatorada) ===');
executarTestesNaVersaoRefatorada();
console.log();

console.log('=== Demonstração da versão refatorada ===');
const repositorio = new RepositorioDeVendedores(vendedoresRaw);
const processador = new ProcessadorDeComissoes(repositorio, new CalculadorDeComissao());

const e1 = new EntradaComissao('V001', 10000, 'STD', 8000);
console.log(`Ana Paula (SR): R$ ${processador.calcularIndividual(e1).toFixed(2)}`);

const e2 = new EntradaComissao('V002', 6000, 'AGR', 5000);
console.log(`Carlos Lima (JR, AGR): R$ ${processador.calcularIndividual(e2).toFixed(2)}`);

console.log('\n=== Cálculo em lote ===');
const lote = [
    new EntradaComissao('V001', 10000, 'STD', 8000),
    new EntradaComissao('V002', 6000,  'AGR', 5000),
    new EntradaComissao('V003', 7000,  'STD', 8000),
];
const resultados = processador.calcularLote(lote);
for (const [id, comissao] of Object.entries(resultados)) {
    const v = repositorio.buscar(id)!;
    console.log(`  ${v.nome}: R$ ${comissao.toFixed(2)}`);
}
