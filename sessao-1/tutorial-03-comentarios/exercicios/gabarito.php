<?php
/**
 * GABARITO — Tutorial 03: Comentários
 * Referência: Clean Code, Cap. 4
 * Execute: php gabarito.php
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

function usuarioEstaAtivo(array $usuario): bool
{
    return $usuario['status'] === 1;
}

function calcularPrecoComDesconto(float $preco, float $desconto): float
{
    return $preco - $desconto;
}

function registrarAcesso(string $usuarioId, string $timestamp): int
{
    // TODO [OPS-304]: persistir no banco de acessos.
    // Responsável: @carlos.lima  |  Prazo: Sprint 43
    $contador = 1;
    echo "[LOG] Acesso registrado: {$usuarioId} em {$timestamp}\n";
    return $contador;
}

// 2% ao dia — definido em contrato (cláusula 9.1, rev. 2024)
const TAXA_MULTA_DIARIA = 0.02;

function calcularMulta(int $diasAtraso, float $valorOriginal): float
{
    return $valorOriginal * TAXA_MULTA_DIARIA * $diasAtraso;
}

// ════════════════════════════════════════════════════════════════════════════════
// PROBLEMA 2 — RESOLVIDO
// ════════════════════════════════════════════════════════════════════════════════
//
// O comentário adicionado explica o "porquê" (fórmula de Price / amortização
// constante) — algo que nunca ficaria óbvio só lendo o código.

function calcularParcelaFinanciamento(
    float $valorPrincipal,
    float $taxaMensal,
    int $numeroParcelas
): float {
    if ($taxaMensal === 0.0) {
        return $valorPrincipal / $numeroParcelas;
    }

    // Fórmula de Price (Sistema Francês de Amortização):
    //   PMT = PV * (i * (1+i)^n) / ((1+i)^n - 1)
    // onde PV = valor principal, i = taxa mensal, n = número de parcelas.
    // Usamos Price porque o contrato prevê parcelas fixas — ao contrário do
    // SAC, onde as parcelas decrescem ao longo do tempo.
    $fator   = pow(1 + $taxaMensal, $numeroParcelas);
    $parcela = $valorPrincipal * ($taxaMensal * $fator) / ($fator - 1);
    return round($parcela, 2);
}

// ════════════════════════════════════════════════════════════════════════════════
// Bloco de verificação — saída idêntica ao exercicio.php
// ════════════════════════════════════════════════════════════════════════════════

echo "=== Verificação do Gabarito ===\n\n";

// As funções foram renomeadas no Problema 1 — ajustamos as chamadas:
$usuarioAtivo   = ['status' => 1, 'nome' => 'Maria'];
$usuarioInativo = ['status' => 0, 'nome' => 'João'];
echo "usuarioEstaAtivo (ativo): "   . (usuarioEstaAtivo($usuarioAtivo)   ? 'true' : 'false') . "\n"; // true
echo "usuarioEstaAtivo (inativo): " . (usuarioEstaAtivo($usuarioInativo) ? 'true' : 'false') . "\n"; // false

echo "calcularPrecoComDesconto(100, 15): " . calcularPrecoComDesconto(100.0, 15.0) . "\n"; // 85

registrarAcesso('U001', '2026-04-14 10:00:00');

echo "calcularMulta(5 dias, R\$200): " . calcularMulta(5, 200.0) . "\n"; // 20

echo "\ncalcularParcelaFinanciamento:\n";
echo "  R\$10.000 / 12x / 1% a.m.: "        . calcularParcelaFinanciamento(10000.0, 0.01, 12) . "\n";
echo "  R\$5.000 / 24x / 0.8% a.m.: "       . calcularParcelaFinanciamento(5000.0, 0.008, 24) . "\n";
echo "  R\$3.000 / 10x / 0% (sem juros): "  . calcularParcelaFinanciamento(3000.0, 0.0, 10)   . "\n";
