/**
 * codigo_para_revisar.ts — Módulo de cobrança. Revise em busca de padrões a melhorar.
 * Execute: npx ts-node codigo_para_revisar.ts
 */

interface Cliente {
    id:               string;
    nome:             string;
    cpf:              string;
    email:            string;
    nivelFidelidade:  string;    // "O", "P", "B"
    pontos:           number;
    historicoCompras: number;
}

class Cobranca {
    status:     string = "pendente";
    vencimento: string = "";

    constructor(
        public readonly id:        string,
        public readonly clienteId: string,
        public readonly valor:     number,
        public readonly tipo:      string,  // "B", "P", "C"
    ) {}

    calcularDescontoFidelidade(cliente: Cliente): number {
        if (cliente.nivelFidelidade === "O") {
            const base  = cliente.historicoCompras * 0.03;
            const bonus = cliente.pontos * 0.002;
            return Math.min(base + bonus, 150.0);
        } else if (cliente.nivelFidelidade === "P") {
            return Math.min(cliente.pontos * 0.001, 50.0);
        }
        return 0.0;
    }
}

class SmtpEmailSender {
    send(to: string, subject: string, body: string): void {
        console.log(`  [SMTP] → ${to}: ${subject}`);
    }
}

class BancoDadosPostgres {
    execute(sql: string, params: unknown[]): void {
        console.log(`  [PG] ${sql.slice(0, 40)}...`);
    }
}

class BoletoSimples {
    constructor(
        public readonly numero:     string,
        public readonly valor:      number,
        public readonly vencimento: string,
    ) {}

    validarVencimento(): boolean {
        const partes = this.vencimento.split("-");
        if (partes.length !== 3) return false;
        const dataVenc = new Date(
            parseInt(partes[0]), parseInt(partes[1]) - 1, parseInt(partes[2])
        );
        return dataVenc >= new Date(new Date().toDateString());
    }
}

class BoletoParcelado {
    constructor(
        public readonly numero:      string,
        public readonly valorTotal:  number,
        public readonly numParcelas: number,
        public readonly vencimento:  string,
    ) {}

    validarVencimento(): boolean {
        const partes = this.vencimento.split("-");
        if (partes.length !== 3) return false;
        const dataVenc = new Date(
            parseInt(partes[0]), parseInt(partes[1]) - 1, parseInt(partes[2])
        );
        return dataVenc >= new Date(new Date().toDateString());
    }

    valorParcela(): number {
        return Math.round((this.valorTotal / this.numParcelas) * 100) / 100;
    }
}

class GestorCobranca {
    private notificador: SmtpEmailSender;
    private banco:       BancoDadosPostgres;

    constructor() {
        this.notificador = new SmtpEmailSender();
        this.banco       = new BancoDadosPostgres();
    }

    validarCpf(cpf: string): boolean {
        return cpf.replace(/[.\-]/g, "").length === 11;
    }

    buscarCliente(clienteId: string): Cliente {
        console.log(`  buscando cliente ${clienteId}`);
        return {
            id: clienteId, nome: "Empresa Exemplo", cpf: "000.000.000-00",
            email: "empresa@exemplo.com", nivelFidelidade: "O",
            pontos: 500, historicoCompras: 8000.0,
        };
    }

    criarCobranca(clienteId: string, valor: number, tipo: string): Cobranca {
        const cob = new Cobranca(`COB-${clienteId}-001`, clienteId, valor, tipo);
        this.banco.execute("INSERT INTO cobrancas VALUES (%s,%s,%s)",
                           [cob.id, cob.clienteId, cob.valor]);
        return cob;
    }

    calcularDesconto(cobranca: Cobranca, cliente: Cliente): number {
        return cobranca.calcularDescontoFidelidade(cliente);
    }

    processarPagamento(cobranca: Cobranca): Record<string, unknown> {
        if (cobranca.tipo === "B") {
            const boleto = new BoletoSimples(`BOL-${cobranca.id}`, cobranca.valor, "2026-07-31");
            if (!boleto.validarVencimento()) {
                throw new Error("Boleto vencido");
            }
            return { metodo: "boleto", codigo: boleto.numero };
        } else if (cobranca.tipo === "P") {
            return { metodo: "pix", chave: `chave-${cobranca.clienteId}` };
        } else if (cobranca.tipo === "C") {
            return { metodo: "cartao", parcelas: 1 };
        } else {
            throw new Error(`Tipo desconhecido: ${cobranca.tipo}`);
        }
    }

    enviarEmail(cliente: Cliente, cobranca: Cobranca): void {
        this.notificador.send(
            cliente.email,
            `Cobrança ${cobranca.id}`,
            `Valor: R$${cobranca.valor.toFixed(2)}`
        );
    }

    gerarBoleto(cobranca: Cobranca): string {
        return `BOL-${cobranca.id}-${cobranca.valor.toFixed(2)}`;
    }

    arquivar(cobranca: Cobranca): void {
        this.banco.execute("UPDATE cobrancas SET status='arquivado' WHERE id=%s",
                           [cobranca.id]);
    }

    gerarRelatorio(clienteId: string): string {
        return `Relatório de cobranças: cliente ${clienteId}`;
    }

    exportarCsv(clienteId: string): string {
        return `id,valor,status\nCOB-${clienteId}-001,100.00,pendente`;
    }

    atualizarStatus(cobrancaId: string, novoStatus: string): void {
        this.banco.execute("UPDATE cobrancas SET status=%s WHERE id=%s",
                           [novoStatus, cobrancaId]);
    }

    reprocessarFalha(cobrancaId: string): boolean {
        console.log(`  reprocessando ${cobrancaId}`);
        return true;
    }

    consultarHistorico(clienteId: string): Record<string, unknown>[] {
        return [{ id: `COB-${clienteId}-001`, valor: 100.0, status: "pago" }];
    }
}

// --- Demo ---
console.log("=== Módulo de Cobrança — revise em busca de padrões a melhorar ===\n");

const gestor   = new GestorCobranca();
const cliente  = gestor.buscarCliente("CLI-100");
const cobranca = gestor.criarCobranca("CLI-100", 500.0, "B");
const desconto = gestor.calcularDesconto(cobranca, cliente);
console.log(`Desconto fidelidade: R$${desconto.toFixed(2)}`);
const resultado = gestor.processarPagamento(cobranca);
console.log(`Pagamento: ${JSON.stringify(resultado)}`);
gestor.enviarEmail(cliente, cobranca);
console.log(`Relatório: ${gestor.gerarRelatorio("CLI-100")}`);
