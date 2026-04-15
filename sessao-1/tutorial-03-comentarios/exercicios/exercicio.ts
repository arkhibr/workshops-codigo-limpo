/**
 * EXERCÍCIO — Tutorial 03: Comentários
 * Referência: Clean Code, Cap. 4
 * Execute: npx ts-node exercicio.ts
 *
 * Este exercício tem dois problemas independentes.
 *
 * PROBLEMA 1 — REMOVER / REESCREVER
 *     O código abaixo tem comentários ruins: redundantes, enganosos e código comentado.
 *     Sua tarefa:
 *       a) Remova os comentários que não agregam nada.
 *       b) Reescreva os enganosos como comentário de intenção (se houver algo a dizer).
 *       c) Remova o código comentado.
 *       d) Quando necessário, renomeie funções/variáveis para tornar o código autodocumentado.
 *
 * PROBLEMA 2 — ADICIONAR O COMENTÁRIO CORRETO
 *     O código abaixo tem uma lógica não óbvia sem nenhum comentário.
 *     Sua tarefa: adicione APENAS o comentário necessário para explicar o "porquê".
 *     Não reescreva o código — apenas comente.
 */

// ════════════════════════════════════════════════════════════════════════════════
// PROBLEMA 1: Código com comentários ruins — remova/reescreva/renomeie
// ════════════════════════════════════════════════════════════════════════════════

// verifica se o usuário está ativo
function chk(u: { st: number; nome: string }): boolean {
    // retorna true se o campo "st" for igual a 1
    return u.st === 1;
}

// calcula o preço com desconto
function calc(p: number, d: number): number {
    // subtrai o desconto do preço
    const r = p - d;
    // retorna o resultado
    return r;
}

function registrarAcesso(usuarioId: string, timestamp: string): number {
    // TODO: melhorar isso
    // TODO: adicionar log
    // incrementa o contador
    let contador = 0;
    contador = contador + 1; // soma 1
    // insere no banco
    // db.insert("acessos", { usuario: usuarioId, ts: timestamp });
    // dbAntigo.log(usuarioId);
    // enviarEmailBoasVindas(usuarioId); // não era necessário
    console.log(`[LOG] Acesso registrado: ${usuarioId} em ${timestamp}`);
    return contador;
}

function calcularMulta(diasAtraso: number, valorOriginal: number): number {
    // 15/01/2024 - Pedro mudou a multa de 1% para 2%
    // 03/03/2024 - Ana reverteu para 1% a pedido do jurídico
    // 10/04/2024 - Carlos subiu para 2% novamente
    const taxaMulta = 0.02;
    return valorOriginal * taxaMulta * diasAtraso;
}

// ════════════════════════════════════════════════════════════════════════════════
// PROBLEMA 2: Lógica não óbvia sem comentário — adicione o comentário correto
// ════════════════════════════════════════════════════════════════════════════════

function calcularParcelaFinanciamento(
    valorPrincipal: number,
    taxaMensal: number,
    numeroParcelas: number
): number {
    if (taxaMensal === 0) {
        return valorPrincipal / numeroParcelas;
    }
    const fator   = Math.pow(1 + taxaMensal, numeroParcelas);
    const parcela = valorPrincipal * (taxaMensal * fator) / (fator - 1);
    return Math.round(parcela * 100) / 100;
}

// ════════════════════════════════════════════════════════════════════════════════
// Bloco de verificação — NÃO altere este bloco
// ════════════════════════════════════════════════════════════════════════════════

console.log("=== Verificação do Exercício ===\n");

// Problema 1
const usuarioAtivo   = { st: 1, nome: "Maria" };
const usuarioInativo = { st: 0, nome: "João" };
console.log("chk (ativo):",   chk(usuarioAtivo));   // esperado: true
console.log("chk (inativo):", chk(usuarioInativo)); // esperado: false

console.log("calc(100, 15):", calc(100, 15)); // esperado: 85

registrarAcesso("U001", "2026-04-14 10:00:00");

console.log("calcularMulta(5 dias, R$200):", calcularMulta(5, 200)); // esperado: 20

// Problema 2
console.log("\ncalcularParcelaFinanciamento:");
console.log("  R$10.000 / 12x / 1% a.m.:",       calcularParcelaFinanciamento(10000, 0.01, 12));
console.log("  R$5.000 / 24x / 0.8% a.m.:",       calcularParcelaFinanciamento(5000, 0.008, 24));
console.log("  R$3.000 / 10x / 0% (sem juros):",  calcularParcelaFinanciamento(3000, 0, 10));
