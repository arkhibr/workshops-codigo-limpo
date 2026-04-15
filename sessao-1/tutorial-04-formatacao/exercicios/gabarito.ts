/**
 * GABARITO — Tutorial 04: Formatação
 * Referência: Clean Code, Cap. 5
 * Execute: npx ts-node gabarito.ts
 *
 * Formatação: ESLint + Prettier (printWidth: 100)
 * Lógica: idêntica ao exercicio.ts — apenas formatação alterada.
 */

// ── Constantes ────────────────────────────────────────────────────────────────

const STATUS_APROVADO        = 'aprovado';
const STATUS_RECUSADO        = 'recusado';
const STATUS_PENDENTE        = 'pendente';

const TAXA_PROCESSAMENTO     = 0.025;
const LIMITE_DIARIO          = 10000;
const VALOR_MINIMO_PAGAMENTO = 1;

// ── Interfaces ────────────────────────────────────────────────────────────────

interface DadosCartao {
    numero: string;
}

interface ResultadoValidacao {
    valido: boolean;
    erros: string[];
}

interface RegistroTransacao {
    id:            string;
    valor_bruto:   number;
    taxa:          number;
    valor_liquido: number;
    metodo:        string;
    status:        string;
    timestamp:     string;
    descricao:     string;
}

interface ResultadoPagamento {
    status:        string;
    transacao_id?: string;
    valor_liquido?: number;
    taxa?:         number;
    motivos?:      string[];
    valor?:        number;
}

interface ResumoDoDia {
    total_processado:   number;
    numero_transacoes:  number;
    total_taxas:        number;
    limite_disponivel:  number;
}

// ── Classes ───────────────────────────────────────────────────────────────────

class ProcessadorDePagamentos {
    private nomeComercianteprivate: string;
    private limitePrivateDiario:    number;
    private _totalProcessadoHoje:   number               = 0;
    private _historico:             RegistroTransacao[]  = [];
    private _ultimaTransacao:       RegistroTransacao | null = null;

    constructor(
        nomeComercianteprivate: string,
        limitePrivateDiario: number = LIMITE_DIARIO
    ) {
        this.nomeComercianteprivate = nomeComercianteprivate;
        this.limitePrivateDiario    = limitePrivateDiario;
    }

    // ── Operações públicas ─────────────────────────────────────────────────

    validarPagamento(
        valor: number,
        metodoPagamento: string,
        dadosCartao: DadosCartao | null = null,
        cpfTitular: string | null = null,
        descricao: string = ''
    ): ResultadoValidacao {
        const erros: string[] = [];

        if (valor < VALOR_MINIMO_PAGAMENTO) {
            erros.push(`Valor mínimo é R$ ${VALOR_MINIMO_PAGAMENTO.toFixed(2)}`);
        }

        if (this._totalProcessadoHoje + valor > this.limitePrivateDiario) {
            erros.push(
                `Limite diário de R$ ${this.limitePrivateDiario.toFixed(2)} seria excedido`
            );
        }

        if (!['credito', 'debito', 'pix', 'boleto'].includes(metodoPagamento)) {
            erros.push(`Método de pagamento inválido: ${metodoPagamento}`);
        }

        if (['credito', 'debito'].includes(metodoPagamento) && !dadosCartao) {
            erros.push('Dados do cartão são obrigatórios para pagamento com cartão');
        }

        return { valido: erros.length === 0, erros };
    }

    processarPagamento(
        valor: number,
        metodoPagamento: string,
        dadosCartao: DadosCartao | null = null,
        cpfTitular: string | null = null,
        descricao: string = ''
    ): ResultadoPagamento {
        const validacao = this.validarPagamento(
            valor,
            metodoPagamento,
            dadosCartao,
            cpfTitular,
            descricao
        );

        if (!validacao.valido) {
            return { status: STATUS_RECUSADO, motivos: validacao.erros, valor };
        }

        const taxa         = metodoPagamento === 'credito' ? valor * TAXA_PROCESSAMENTO : 0;
        const valorLiquido = valor - taxa;

        this._totalProcessadoHoje += valor;
        const idTransacao = `TRX-${new Date().toISOString().replace(/[-:.TZ]/g, '')}`;

        const registro: RegistroTransacao = {
            id:            idTransacao,
            valor_bruto:   valor,
            taxa:          Math.round(taxa * 100) / 100,
            valor_liquido: Math.round(valorLiquido * 100) / 100,
            metodo:        metodoPagamento,
            status:        STATUS_APROVADO,
            timestamp:     new Date().toISOString(),
            descricao,
        };

        this._historico.push(registro);
        this._ultimaTransacao = registro;

        return {
            status:        STATUS_APROVADO,
            transacao_id:  idTransacao,
            valor_liquido: Math.round(valorLiquido * 100) / 100,
            taxa:          Math.round(taxa * 100) / 100,
        };
    }

    gerarComprovante(transacaoId: string): string | null {
        const transacao = this._historico.find((t) => t.id === transacaoId) ?? null;

        if (!transacao) {
            return null;
        }

        const linhas = [
            '='.repeat(50),
            'COMPROVANTE DE PAGAMENTO',
            `Comerciante: ${this.nomeComercianteprivate}`,
            '='.repeat(50),
            `ID Transação : ${transacao.id}`,
            `Data/Hora    : ${transacao.timestamp}`,
            `Método       : ${transacao.metodo.toUpperCase()}`,
            `Valor Bruto  : R$ ${transacao.valor_bruto.toFixed(2)}`,
            `Taxa         : R$ ${transacao.taxa.toFixed(2)}`,
            `Valor Líquido: R$ ${transacao.valor_liquido.toFixed(2)}`,
            `Status       : ${transacao.status.toUpperCase()}`,
            '='.repeat(50),
        ];

        if (transacao.descricao) {
            linhas.splice(linhas.length - 1, 0, `Descrição    : ${transacao.descricao}`);
        }

        return linhas.join('\n');
    }

    obterResumoDoDia(): ResumoDoDia {
        return {
            total_processado:  this._totalProcessadoHoje,
            numero_transacoes: this._historico.length,
            total_taxas:       this._calcularTotalTaxas(),
            limite_disponivel: this.limitePrivateDiario - this._totalProcessadoHoje,
        };
    }

    // ── Operações privadas ─────────────────────────────────────────────────

    private _calcularTotalTaxas(): number {
        return this._historico.reduce((acc, t) => acc + t.taxa, 0);
    }
}

// ── Execução de demonstração ──────────────────────────────────────────────────

const processador = new ProcessadorDePagamentos('Restaurante do Zé', 5000);

const resultado1 = processador.processarPagamento(
    150,
    'credito',
    { numero: '****1234' },
    null,
    'Almoço executivo'
);
console.log('Transação 1:', resultado1);

const resultado2 = processador.processarPagamento(
    0.50,
    'pix',
    null,
    null,
    'Teste abaixo do mínimo'
);
console.log('Transação 2 (inválida):', resultado2);

const resultado3 = processador.processarPagamento(80, 'pix', null, null, 'Sobremesa');
console.log('Transação 3:', resultado3);

if (resultado1.status === STATUS_APROVADO && resultado1.transacao_id) {
    const comprovante = processador.gerarComprovante(resultado1.transacao_id);
    console.log('\n' + comprovante);
}

console.log('\nResumo do dia:', processador.obterResumoDoDia());
