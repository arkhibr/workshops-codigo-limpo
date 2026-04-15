/**
 * GABARITO — Tutorial 03: Comentários
 * Referência: Clean Code, Cap. 4
 * Execute: npx ts-node gabarito.ts
 */

// ════════════════════════════════════════════════════════════════════════════════
// PROBLEMA 1 — RESOLVIDO
// ════════════════════════════════════════════════════════════════════════════════
//
// O que foi feito:
//   - "chk" renomeado para "usuarioEstaAtivo"; parâmetro "u" → "usuario";
//     campo "st" → "status". Sem comentário: o nome já diz tudo.
//   - "calc" renomeado para "calcularPrecoComDesconto"; parâmetros "p","d"
//     → "preco","desconto". Todos os comentários redundantes removidos.
//   - "registrarAcesso": TODO reescrito com rastreabilidade; código comentado
//     removido (fica no histórico do git); diário de bordo removido de calcularMulta.

interface Usuario {
    status: number;
    nome: string;
}

function usuarioEstaAtivo(usuario: Usuario): boolean {
    return usuario.status === 1;
}

function calcularPrecoComDesconto(preco: number, desconto: number): number {
    return preco - desconto;
}

function registrarAcesso(usuarioId: string, timestamp: string): number {
    // TODO [OPS-304]: persistir no banco de acessos.
    // Responsável: @carlos.lima  |  Prazo: Sprint 43
    const contador = 1;
    console.log(`[LOG] Acesso registrado: ${usuarioId} em ${timestamp}`);
    return contador;
}

// 2% ao dia — definido em contrato (cláusula 9.1, rev. 2024)
const TAXA_MULTA_DIARIA = 0.02;

function calcularMulta(diasAtraso: number, valorOriginal: number): number {
    return valorOriginal * TAXA_MULTA_DIARIA * diasAtraso;
}

// ════════════════════════════════════════════════════════════════════════════════
// PROBLEMA 2 — RESOLVIDO
// ════════════════════════════════════════════════════════════════════════════════
//
// O comentário adicionado explica o "porquê" (fórmula de Price / amortização
// constante) — algo que nunca ficaria óbvio só lendo o código.

function calcularParcelaFinanciamento(
    valorPrincipal: number,
    taxaMensal: number,
    numeroParcelas: number
): number {
    if (taxaMensal === 0) {
        return valorPrincipal / numeroParcelas;
    }

    // Fórmula de Price (Sistema Francês de Amortização):
    //   PMT = PV * (i * (1+i)^n) / ((1+i)^n - 1)
    // onde PV = valor principal, i = taxa mensal, n = número de parcelas.
    // Usamos Price porque o contrato prevê parcelas fixas — ao contrário do
    // SAC, onde as parcelas decrescem ao longo do tempo.
    const fator   = Math.pow(1 + taxaMensal, numeroParcelas);
    const parcela = valorPrincipal * (taxaMensal * fator) / (fator - 1);
    return Math.round(parcela * 100) / 100;
}

// ════════════════════════════════════════════════════════════════════════════════
// Bloco de verificação — saída idêntica ao exercicio.ts
// ════════════════════════════════════════════════════════════════════════════════

console.log("=== Verificação do Gabarito ===\n");

// As funções foram renomeadas no Problema 1 — ajustamos as chamadas:
const usuarioAtivo:   Usuario = { status: 1, nome: "Maria" };
const usuarioInativo: Usuario = { status: 0, nome: "João" };
console.log("usuarioEstaAtivo (ativo):",   usuarioEstaAtivo(usuarioAtivo));   // true
console.log("usuarioEstaAtivo (inativo):", usuarioEstaAtivo(usuarioInativo)); // false

console.log("calcularPrecoComDesconto(100, 15):", calcularPrecoComDesconto(100, 15)); // 85

registrarAcesso("U001", "2026-04-14 10:00:00");

console.log("calcularMulta(5 dias, R$200):", calcularMulta(5, 200)); // 20

console.log("\ncalcularParcelaFinanciamento:");
console.log("  R$10.000 / 12x / 1% a.m.:",       calcularParcelaFinanciamento(10000, 0.01, 12));
console.log("  R$5.000 / 24x / 0.8% a.m.:",       calcularParcelaFinanciamento(5000, 0.008, 24));
console.log("  R$3.000 / 10x / 0% (sem juros):",  calcularParcelaFinanciamento(3000, 0, 10));
