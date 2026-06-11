/**
 * EXERCÍCIO 17 TypeScript — Padrões de Criação
 * Referência: Design Patterns (GoF), Cap. 3
 *
 * PASSOS (31 min no total):
 *
 *   PASSO 1 — IDENTIFICAR (5 min)
 *     Leia o código abaixo e adicione comentários marcando os dois problemas:
 *       // PROBLEMA: interface com 9 campos, maioria opcional — fácil criar objeto inválido
 *       // PROBLEMA: if/else rígido — adicionar tipo exige alterar criarContrato()
 *     Meta: encontrar os 2 problemas e anotar onde estão antes de alterar código.
 *
 *   PASSO 2 — FACTORY COM MAP (8 min)
 *     Substitua o if/else de criarContrato() por um Map:
 *       const fabrica = new Map<string, (dados: Record<string, unknown>) => Contrato>()
 *       fabrica.set("servico", (d) => ...)
 *     criarContrato() consulta o Map e chama a entrada correspondente.
 *     Verifique que o demo ainda roda.
 *
 *   PASSO 3 — FACTORY REGISTRÁVEL (8 min)
 *     Transforme o Map em FabricaContrato com:
 *       FabricaContrato.registrar(tipo: string, fabrica: (dados: any) => Contrato): void
 *       FabricaContrato.criar(tipo: string, dados: Record<string, unknown>): Contrato
 *     Use Map<string, (dados: any) => Contrato> internamente.
 *     Registre os 3 tipos existentes externamente.
 *     Verifique que o demo ainda roda e que um novo tipo pode ser registrado
 *     sem alterar FabricaContrato.
 *
 *   PASSO 4 — BUILDER (10 min)
 *     Crie ConstruirContratoServico com métodos fluentes:
 *       comValorMensal(valor: number): this
 *       comVigencia(meses: number): this
 *       comContratante(contratante: string): this
 *       construir(): Contrato  (lança Error se campos obrigatórios faltarem)
 *     Verifique que o demo roda com a nova sintaxe fluente.
 *
 * Execute: npx ts-node exercicio.ts (deve rodar antes e depois de cada passo)
 */

interface Contrato {
    tipo:           string;
    valorMensal:    number;
    vigenciaMeses:  number;
    contratante:    string;
    objeto?:        string;       // serviço ou bem locado
    endereco?:      string;       // para locação
    fornecedorId?:  string;       // para fornecimento
    prazoEntrega?:  number;       // dias, para fornecimento
    observacoes?:   string;
}

function criarContrato(tipo: string, dados: Record<string, unknown>): Contrato {
    // Adicionar ContratoObrasCivil exige alterar esta função
    if (tipo === "servico") {
        return {
            tipo:          "servico",
            valorMensal:   dados["valorMensal"] as number,
            vigenciaMeses: dados["vigenciaMeses"] as number,
            contratante:   dados["contratante"] as string,
            objeto:        (dados["objeto"] as string) ?? "Serviços gerais",
        };
    } else if (tipo === "locacao") {
        return {
            tipo:          "locacao",
            valorMensal:   dados["valorMensal"] as number,
            vigenciaMeses: dados["vigenciaMeses"] as number,
            contratante:   dados["contratante"] as string,
            objeto:        dados["objeto"] as string | undefined,
            endereco:      dados["endereco"] as string | undefined,
        };
    } else if (tipo === "fornecimento") {
        return {
            tipo:          "fornecimento",
            valorMensal:   dados["valorMensal"] as number,
            vigenciaMeses: dados["vigenciaMeses"] as number,
            contratante:   dados["contratante"] as string,
            fornecedorId:  dados["fornecedorId"] as string | undefined,
            prazoEntrega:  dados["prazoEntrega"] as number | undefined,
        };
    } else {
        throw new Error(`Tipo desconhecido: ${tipo}`);
    }
}

// Demo
const c1 = criarContrato("servico", {
    valorMensal: 5000.0, vigenciaMeses: 12, contratante: "EMP-001"
});
console.log(`Contrato: ${c1.tipo} R$${c1.valorMensal.toFixed(2)}/mês × ${c1.vigenciaMeses} meses`);
console.log(`  campos não usados: endereco=${c1.endereco}, fornecedorId=${c1.fornecedorId}`);

// --- Stub Passo 3: registrar novo tipo sem alterar FabricaContrato ---
// Após implementar FabricaContrato, descomente e verifique:
// FabricaContrato.registrar("obras_civil", (d) => ({
//     tipo:          "obras_civil",
//     valorMensal:   d["valorMensal"] as number,
//     vigenciaMeses: d["vigenciaMeses"] as number,
//     contratante:   d["contratante"] as string,
// }));
// const obras = FabricaContrato.criar("obras_civil", {
//     valorMensal: 25000.0, vigenciaMeses: 8, contratante: "EMP-004"
// });
// console.log(`Novo tipo: ${obras.tipo} R$${obras.valorMensal.toFixed(2)}/mês`);

// --- Stub Passo 4: sintaxe fluente do Builder ---
// Após implementar ConstruirContratoServico, descomente e verifique:
// const c2 = new ConstruirContratoServico()
//     .comValorMensal(5000.0)
//     .comVigencia(12)
//     .comContratante("EMP-001")
//     .construir();
// console.log(`Builder: ${c2.tipo} R$${c2.valorMensal.toFixed(2)}/mês × ${c2.vigenciaMeses} meses`);
