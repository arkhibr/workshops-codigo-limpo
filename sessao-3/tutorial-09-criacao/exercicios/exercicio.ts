/**
 * EXERCÍCIO 17 TypeScript — Padrões de Criação
 * Tempo estimado: 15 minutos
 * Referência: Design Patterns (GoF), Cap. 3
 *
 * INSTRUÇÕES:
 *   O código abaixo tem dois problemas:
 *   1. Interface com 9 campos, maioria opcional — fácil criar objeto inválido.
 *   2. Função criarContrato() com if/else — adicionar novo tipo exige alterá-la.
 *
 *   Aplique:
 *   1. Factory Method: crie uma FabricaContrato com Map de registros.
 *   2. Builder: crie ConstruirContratoServico com métodos fluentes.
 *
 *   Execute: npx ts-node exercicio.ts
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
