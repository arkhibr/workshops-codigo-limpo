/**
 * EQUIVALENTE TypeScript — Padrões de Criação
 * Referência: Design Patterns (GoF), Cap. 3 — Creational Patterns
 * Execute: npx ts-node equivalente.ts
 */

// ─────────────────────────────────────────────────────────────────────────────
// ❌ Ruim — interface com 10 campos + função factory com if/else
// ─────────────────────────────────────────────────────────────────────────────

interface DocumentoCobrancaRuim {
    tipo:          string;
    valor:         number;
    vencimento:    string;
    beneficiario:  string;
    codigoBarras?: string;   // só boleto
    chavePix?:     string;   // só pix
    numeroNf?:     string;   // só nota fiscal
    cfop?:         string;   // só nota fiscal
    descricao?:    string;
    observacoes?:  string;
}

function criarDocumentoRuim(tipo: string, dados: Record<string, unknown>): DocumentoCobrancaRuim {
    // Adicionar 'TED' exige alterar esta função
    if (tipo === "boleto") {
        return {
            tipo:         "boleto",
            valor:        dados["valor"] as number,
            vencimento:   dados["vencimento"] as string,
            beneficiario: dados["beneficiario"] as string,
            codigoBarras: (dados["codigoBarras"] as string) ?? "9999.99999 99999.999999",
        };
    } else if (tipo === "pix") {
        return {
            tipo:         "pix",
            valor:        dados["valor"] as number,
            vencimento:   dados["vencimento"] as string,
            beneficiario: dados["beneficiario"] as string,
            chavePix:     (dados["chavePix"] as string) ?? "chave@exemplo.com.br",
        };
    } else if (tipo === "nota_fiscal") {
        return {
            tipo:         "nota_fiscal",
            valor:        dados["valor"] as number,
            vencimento:   dados["vencimento"] as string,
            beneficiario: dados["beneficiario"] as string,
            numeroNf:     (dados["numeroNf"] as string) ?? "NF-000001",
            cfop:         (dados["cfop"] as string) ?? "5102",
        };
    } else {
        throw new Error(`Tipo desconhecido: ${tipo}`);
    }
}


// ─────────────────────────────────────────────────────────────────────────────
// ✅ Bom — Factory Method + Builder
// ─────────────────────────────────────────────────────────────────────────────

interface DocumentoCobranca {
    readonly tipo:        string;
    readonly valor:       number;
    readonly vencimento:  string;
    readonly beneficiario: string;
    descricao(): string;
}

class Boleto implements DocumentoCobranca {
    readonly tipo = "boleto";

    constructor(
        readonly valor:        number,
        readonly vencimento:   string,
        readonly beneficiario: string,
        readonly codigoBarras: string,
    ) {
        if (valor <= 0) throw new Error(`Valor deve ser positivo, recebido: ${valor}`);
    }

    descricao(): string {
        return `Boleto R$${this.valor.toFixed(2)} venc ${this.vencimento} | ${this.codigoBarras}`;
    }
}

class Pix implements DocumentoCobranca {
    readonly tipo = "pix";

    constructor(
        readonly valor:        number,
        readonly vencimento:   string,
        readonly beneficiario: string,
        readonly chavePix:     string,
    ) {
        if (valor <= 0) throw new Error(`Valor deve ser positivo, recebido: ${valor}`);
    }

    descricao(): string {
        return `Pix R$${this.valor.toFixed(2)} → ${this.chavePix}`;
    }
}

class NotaFiscal implements DocumentoCobranca {
    readonly tipo = "nota_fiscal";

    constructor(
        readonly valor:        number,
        readonly vencimento:   string,
        readonly beneficiario: string,
        readonly numeroNf:     string,
        readonly cfop:         string,
    ) {
        if (valor <= 0) throw new Error(`Valor deve ser positivo, recebido: ${valor}`);
    }

    descricao(): string {
        return `NF ${this.numeroNf} CFOP ${this.cfop} R$${this.valor.toFixed(2)}`;
    }
}

type FabricaFn = (dados: Record<string, unknown>) => DocumentoCobranca;

class FabricaDocumento {
    private static registro: Map<string, FabricaFn> = new Map();

    static registrar(tipo: string, fabrica: FabricaFn): void {
        FabricaDocumento.registro.set(tipo, fabrica);
    }

    static criar(tipo: string, dados: Record<string, unknown>): DocumentoCobranca {
        const fabrica = FabricaDocumento.registro.get(tipo);
        if (!fabrica) {
            const disponiveis = [...FabricaDocumento.registro.keys()].sort().join(", ");
            throw new Error(`Tipo '${tipo}' não registrado. Disponíveis: ${disponiveis}`);
        }
        return fabrica(dados);
    }
}

FabricaDocumento.registrar("boleto", (d) => new Boleto(
    d["valor"] as number, d["vencimento"] as string, d["beneficiario"] as string,
    (d["codigoBarras"] as string) ?? "0000.00000 00000.000000"
));
FabricaDocumento.registrar("pix", (d) => new Pix(
    d["valor"] as number, d["vencimento"] as string, d["beneficiario"] as string,
    (d["chavePix"] as string) ?? "chave@exemplo.com.br"
));
FabricaDocumento.registrar("nota_fiscal", (d) => new NotaFiscal(
    d["valor"] as number, d["vencimento"] as string, d["beneficiario"] as string,
    (d["numeroNf"] as string) ?? "NF-000001", (d["cfop"] as string) ?? "5102"
));


class ConstruirBoleto {
    private _valor?:        number;
    private _vencimento?:   string;
    private _beneficiario?: string;
    private _codigoBarras   = "0000.00000 00000.000000";

    comValor(valor: number): this {
        this._valor = valor;
        return this;
    }

    comVencimento(vencimento: string): this {
        this._vencimento = vencimento;
        return this;
    }

    comBeneficiario(beneficiario: string): this {
        this._beneficiario = beneficiario;
        return this;
    }

    comCodigoBarras(codigo: string): this {
        this._codigoBarras = codigo;
        return this;
    }

    construir(): Boleto {
        if (this._valor === undefined) throw new Error("valor é obrigatório");
        if (!this._vencimento)         throw new Error("vencimento é obrigatório");
        if (!this._beneficiario)       throw new Error("beneficiario é obrigatório");
        return new Boleto(this._valor, this._vencimento, this._beneficiario, this._codigoBarras);
    }
}


// ─── Demo ─────────────────────────────────────────────────────────────────────

console.log("=== Equivalente TypeScript — Padrões de Criação ===\n");

console.log("--- ❌ Ruim ---");
const boletoRuim = criarDocumentoRuim("boleto", {
    valor: 1500.0, vencimento: "2026-07-15", beneficiario: "CLI-100"
});
console.log(`Boleto: R$${boletoRuim.valor}, venc ${boletoRuim.vencimento}`);
console.log(`  campos não usados: chavePix=${boletoRuim.chavePix}, numeroNf=${boletoRuim.numeroNf}`);

console.log("\n--- ✅ Bom — Factory ---");
const boleto = FabricaDocumento.criar("boleto", {
    valor: 1500.0, vencimento: "2026-07-15",
    beneficiario: "CLI-100", codigoBarras: "1234.56789 00000.000000"
});
console.log(boleto.descricao());

const pix = FabricaDocumento.criar("pix", {
    valor: 250.0, vencimento: "2026-07-10",
    beneficiario: "CLI-200", chavePix: "empresa@exemplo.com.br"
});
console.log(pix.descricao());

const nf = FabricaDocumento.criar("nota_fiscal", {
    valor: 890.0, vencimento: "2026-07-30",
    beneficiario: "CLI-300", numeroNf: "NF-000042", cfop: "5102"
});
console.log(nf.descricao());

console.log("\n--- ✅ Bom — Builder ---");
const boletoBuilder = new ConstruirBoleto()
    .comValor(750.0)
    .comVencimento("2026-08-01")
    .comBeneficiario("CLI-300")
    .comCodigoBarras("9876.54321 00000.000000")
    .construir();
console.log(boletoBuilder.descricao());

try {
    new ConstruirBoleto().comValor(100.0).construir();
    console.log("FALHOU: deveria rejeitar boleto sem vencimento");
} catch (e) {
    console.log(`OK: Builder rejeita boleto incompleto — ${(e as Error).message}`);
}
