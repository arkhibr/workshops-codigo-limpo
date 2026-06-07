/**
 * GABARITO 17 TypeScript — Padrões de Criação
 * Referência: Design Patterns (GoF), Cap. 3
 *
 * SOLUÇÃO:
 *   1. Factory Method: FabricaContrato com Map de registros.
 *   2. Builder: ConstruirContratoServico com interface fluente.
 *
 * Execute: npx ts-node gabarito.ts
 */

// ─── Factory Method ───────────────────────────────────────────────────────────

interface Contrato {
    readonly tipo:          string;
    readonly valorMensal:   number;
    readonly vigenciaMeses: number;
    readonly contratante:   string;
    descricao(): string;
    valorTotal(): number;
}

abstract class ContratoBase implements Contrato {
    abstract readonly tipo: string;

    constructor(
        readonly valorMensal:   number,
        readonly vigenciaMeses: number,
        readonly contratante:   string,
    ) {
        if (valorMensal <= 0)   throw new Error(`Valor mensal deve ser positivo, recebido: ${valorMensal}`);
        if (vigenciaMeses <= 0) throw new Error(`Vigência deve ser positiva, recebida: ${vigenciaMeses}`);
    }

    abstract descricao(): string;

    valorTotal(): number {
        return this.valorMensal * this.vigenciaMeses;
    }
}

class ContratoServico extends ContratoBase {
    readonly tipo = "servico";

    constructor(
        valorMensal:   number,
        vigenciaMeses: number,
        contratante:   string,
        readonly objeto: string,
    ) {
        super(valorMensal, vigenciaMeses, contratante);
    }

    descricao(): string {
        return `Serviço: ${this.objeto} | ${this.contratante} | R$${this.valorMensal.toFixed(2)}/mês × ${this.vigenciaMeses} meses`;
    }
}

class ContratoLocacao extends ContratoBase {
    readonly tipo = "locacao";

    constructor(
        valorMensal:   number,
        vigenciaMeses: number,
        contratante:   string,
        readonly objeto:    string,
        readonly endereco:  string,
    ) {
        super(valorMensal, vigenciaMeses, contratante);
    }

    descricao(): string {
        return `Locação: ${this.objeto} | ${this.endereco} | ${this.contratante} | R$${this.valorMensal.toFixed(2)}/mês × ${this.vigenciaMeses} meses`;
    }
}

class ContratoFornecimento extends ContratoBase {
    readonly tipo = "fornecimento";

    constructor(
        valorMensal:   number,
        vigenciaMeses: number,
        contratante:   string,
        readonly fornecedorId:  string,
        readonly prazoEntrega:  number,
    ) {
        super(valorMensal, vigenciaMeses, contratante);
    }

    descricao(): string {
        return `Fornecimento: ${this.fornecedorId} | prazo ${this.prazoEntrega}d | R$${this.valorMensal.toFixed(2)}/mês × ${this.vigenciaMeses} meses`;
    }
}

type FabricaFn = (dados: Record<string, unknown>) => Contrato;

class FabricaContrato {
    private static registro: Map<string, FabricaFn> = new Map();

    static registrar(tipo: string, fabrica: FabricaFn): void {
        FabricaContrato.registro.set(tipo, fabrica);
    }

    static criar(tipo: string, dados: Record<string, unknown>): Contrato {
        const fabrica = FabricaContrato.registro.get(tipo);
        if (!fabrica) {
            const disponiveis = [...FabricaContrato.registro.keys()].sort().join(", ");
            throw new Error(`Tipo '${tipo}' não registrado. Disponíveis: ${disponiveis}`);
        }
        return fabrica(dados);
    }
}

FabricaContrato.registrar("servico", (d) => new ContratoServico(
    d["valorMensal"] as number, d["vigenciaMeses"] as number, d["contratante"] as string,
    (d["objeto"] as string) ?? "Serviços gerais"
));
FabricaContrato.registrar("locacao", (d) => new ContratoLocacao(
    d["valorMensal"] as number, d["vigenciaMeses"] as number, d["contratante"] as string,
    (d["objeto"] as string) ?? "", (d["endereco"] as string) ?? ""
));
FabricaContrato.registrar("fornecimento", (d) => new ContratoFornecimento(
    d["valorMensal"] as number, d["vigenciaMeses"] as number, d["contratante"] as string,
    (d["fornecedorId"] as string) ?? "", (d["prazoEntrega"] as number) ?? 30
));


// ─── Builder ──────────────────────────────────────────────────────────────────

class ConstruirContratoServico {
    private _valorMensal?:   number;
    private _vigenciaMeses?: number;
    private _contratante?:   string;
    private _objeto          = "Serviços gerais";

    comValorMensal(valor: number): this {
        this._valorMensal = valor;
        return this;
    }

    comVigencia(meses: number): this {
        this._vigenciaMeses = meses;
        return this;
    }

    comContratante(contratante: string): this {
        this._contratante = contratante;
        return this;
    }

    comObjeto(objeto: string): this {
        this._objeto = objeto;
        return this;
    }

    construir(): ContratoServico {
        if (this._valorMensal === undefined) throw new Error("valor_mensal é obrigatório");
        if (!this._vigenciaMeses)            throw new Error("vigencia_meses é obrigatório");
        if (!this._contratante)              throw new Error("contratante é obrigatório");
        return new ContratoServico(this._valorMensal, this._vigenciaMeses, this._contratante, this._objeto);
    }
}


// ─── Verificação ──────────────────────────────────────────────────────────────

console.log("=== Gabarito 17 TypeScript — Factory Method + Builder ===\n");

// Factory
const servico = FabricaContrato.criar("servico", {
    valorMensal: 5000.0, vigenciaMeses: 12,
    contratante: "EMP-001", objeto: "Consultoria em TI"
});
console.assert(servico instanceof ContratoServico);
console.assert(servico.valorTotal() === 60000.0);
console.log("OK: Factory — ContratoServico criado via FabricaContrato");
console.log("  " + servico.descricao());

const locacao = FabricaContrato.criar("locacao", {
    valorMensal: 3500.0, vigenciaMeses: 24,
    contratante: "EMP-002", objeto: "Sala comercial 40m²",
    endereco: "Av. Paulista, 1000 — SP"
});
console.assert(locacao instanceof ContratoLocacao);
console.log("OK: Factory — ContratoLocacao criado via FabricaContrato");

try {
    FabricaContrato.criar("obras_civil", { valorMensal: 1000.0, vigenciaMeses: 6, contratante: "X" });
    console.log("FALHOU: Factory — deveria rejeitar tipo não registrado");
} catch (e) {
    console.log(`OK: Factory — tipo desconhecido rejeitado — ${(e as Error).message}`);
}

console.log();

// Builder
const contrato = new ConstruirContratoServico()
    .comValorMensal(5000.0)
    .comVigencia(12)
    .comContratante("EMP-001")
    .comObjeto("Desenvolvimento de software")
    .construir();
console.assert(contrato instanceof ContratoServico);
console.assert(contrato.valorTotal() === 60000.0);
console.log("OK: Builder — ContratoServico construído com encadeamento fluente");
console.log("  " + contrato.descricao());

try {
    new ConstruirContratoServico().comValorMensal(5000.0).construir();
    console.log("FALHOU: Builder — deveria rejeitar contrato sem vigencia_meses");
} catch (e) {
    console.log(`OK: Builder — rejeita contrato incompleto — ${(e as Error).message}`);
}

try {
    new ConstruirContratoServico().comVigencia(12).construir();
    console.log("FALHOU: Builder — deveria rejeitar contrato sem valor_mensal");
} catch (e) {
    console.log(`OK: Builder — rejeita contrato incompleto — ${(e as Error).message}`);
}
