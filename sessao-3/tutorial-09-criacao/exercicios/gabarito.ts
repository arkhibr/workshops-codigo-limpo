/**
 * GABARITO 17 TypeScript — Padrões de Criação
 * Referência: Design Patterns (GoF), Cap. 3
 *
 * Execute: npx ts-node gabarito.ts
 */

// ─── Interface (mesma do exercício) ───────────────────────────────────────────

interface Contrato {
    tipo:           string;
    valorMensal:    number;
    vigenciaMeses:  number;
    contratante:    string;
    objeto?:        string;
    endereco?:      string;
    fornecedorId?:  string;
    prazoEntrega?:  number;
    observacoes?:   string;
}


// ─── Passo 3: Factory registrável ────────────────────────────────────────────

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

FabricaContrato.registrar("servico", (d) => ({
    tipo:          "servico",
    valorMensal:   d["valorMensal"] as number,
    vigenciaMeses: d["vigenciaMeses"] as number,
    contratante:   d["contratante"] as string,
    objeto:        (d["objeto"] as string) ?? "Serviços gerais",
}));
FabricaContrato.registrar("locacao", (d) => ({
    tipo:          "locacao",
    valorMensal:   d["valorMensal"] as number,
    vigenciaMeses: d["vigenciaMeses"] as number,
    contratante:   d["contratante"] as string,
    objeto:        d["objeto"] as string | undefined,
    endereco:      d["endereco"] as string | undefined,
}));
FabricaContrato.registrar("fornecimento", (d) => ({
    tipo:          "fornecimento",
    valorMensal:   d["valorMensal"] as number,
    vigenciaMeses: d["vigenciaMeses"] as number,
    contratante:   d["contratante"] as string,
    fornecedorId:  d["fornecedorId"] as string | undefined,
    prazoEntrega:  d["prazoEntrega"] as number | undefined,
}));


// ─── Passo 4: Builder ─────────────────────────────────────────────────────────

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

    construir(): Contrato {
        if (this._valorMensal === undefined) throw new Error("valor_mensal é obrigatório");
        if (!this._vigenciaMeses)            throw new Error("vigencia_meses é obrigatório");
        if (!this._contratante)              throw new Error("contratante é obrigatório");
        return {
            tipo:          "servico",
            valorMensal:   this._valorMensal,
            vigenciaMeses: this._vigenciaMeses,
            contratante:   this._contratante,
            objeto:        this._objeto,
        };
    }
}


// ─── Verificação ──────────────────────────────────────────────────────────────

console.log("=== Gabarito 17 TypeScript — Factory Method + Builder ===\n");

// Passo 3: factory registrável
const servico = FabricaContrato.criar("servico", {
    valorMensal: 5000.0, vigenciaMeses: 12, contratante: "EMP-001"
});
console.assert(servico.tipo === "servico");
console.assert(servico.valorMensal * servico.vigenciaMeses === 60000.0);
console.log(`OK: Passo 3 — FabricaContrato.criar: ${servico.tipo} R$${servico.valorMensal.toFixed(2)}/mês`);

try {
    FabricaContrato.criar("desconhecido", { valorMensal: 1.0, vigenciaMeses: 1, contratante: "X" });
    console.log("FALHOU: deveria rejeitar tipo não registrado");
} catch (e) {
    console.log(`OK: Passo 3 — tipo desconhecido rejeitado — ${(e as Error).message}`);
}

// Passo 3: novo tipo sem alterar FabricaContrato
FabricaContrato.registrar("obras_civil", (d) => ({
    tipo:          "obras_civil",
    valorMensal:   d["valorMensal"] as number,
    vigenciaMeses: d["vigenciaMeses"] as number,
    contratante:   d["contratante"] as string,
    observacoes:   d["responsavelTecnico"] as string | undefined,
}));
const obras = FabricaContrato.criar("obras_civil", {
    valorMensal: 25000.0, vigenciaMeses: 8,
    contratante: "EMP-004", responsavelTecnico: "Eng. Silva CREA-12345"
});
console.assert(obras.tipo === "obras_civil");
console.log(`OK: Passo 3 — novo tipo registrado sem alterar FabricaContrato: ${obras.tipo}`);

console.log();

// Passo 4: builder
const c = new ConstruirContratoServico()
    .comValorMensal(5000.0)
    .comVigencia(12)
    .comContratante("EMP-001")
    .construir();
console.assert(c.tipo === "servico");
console.assert(c.valorMensal * c.vigenciaMeses === 60000.0);
console.log(`OK: Passo 4 — builder fluente: ${c.tipo} R$${c.valorMensal.toFixed(2)}/mês × ${c.vigenciaMeses} meses`);

try {
    new ConstruirContratoServico().comValorMensal(5000.0).construir();
    console.log("FALHOU: deveria rejeitar sem vigencia_meses");
} catch (e) {
    console.log(`OK: Passo 4 — rejeita construir() sem vigencia_meses`);
}

try {
    new ConstruirContratoServico().comVigencia(12).construir();
    console.log("FALHOU: deveria rejeitar sem valor_mensal");
} catch (e) {
    console.log(`OK: Passo 4 — rejeita construir() sem valor_mensal`);
}

try {
    new ConstruirContratoServico().comValorMensal(5000.0).comVigencia(12).construir();
    console.log("FALHOU: deveria rejeitar sem contratante");
} catch (e) {
    console.log(`OK: Passo 4 — rejeita construir() sem contratante`);
}
