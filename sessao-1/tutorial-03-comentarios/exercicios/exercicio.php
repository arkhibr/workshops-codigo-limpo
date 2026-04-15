<?php
/**
 * EXERCÍCIO — Tutorial 03: Comentários
 * Referência: Clean Code, Cap. 4
 * Execute: php exercicio.php
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
function chk(array $u): bool {
    // retorna true se o campo "st" for igual a 1
    return $u['st'] === 1;
}

// calcula o preço com desconto
function calc(float $p, float $d): float {
    // subtrai o desconto do preço
    $r = $p - $d;
    // retorna o resultado
    return $r;
}

function registrarAcesso(string $usuarioId, string $timestamp): int {
    // TODO: melhorar isso
    // TODO: adicionar log
    // incrementa o contador
    $contador = 0;
    $contador = $contador + 1; // soma 1
    // insere no banco
    // $db->insert("acessos", ["usuario" => $usuarioId, "ts" => $timestamp]);
    // $dbAntigo->log($usuarioId);
    // enviarEmailBoasVindas($usuarioId); // não era necessário
    echo "[LOG] Acesso registrado: {$usuarioId} em {$timestamp}\n";
    return $contador;
}

function calcularMulta(int $diasAtraso, float $valorOriginal): float {
    // 15/01/2024 - Pedro mudou a multa de 1% para 2%
    // 03/03/2024 - Ana reverteu para 1% a pedido do jurídico
    // 10/04/2024 - Carlos subiu para 2% novamente
    $taxaMulta = 0.02;
    return $valorOriginal * $taxaMulta * $diasAtraso;
}

// ════════════════════════════════════════════════════════════════════════════════
// PROBLEMA 2: Lógica não óbvia sem comentário — adicione o comentário correto
// ════════════════════════════════════════════════════════════════════════════════

function calcularParcelaFinanciamento(
    float $valorPrincipal,
    float $taxaMensal,
    int $numeroParcelas
): float {
    if ($taxaMensal === 0.0) {
        return $valorPrincipal / $numeroParcelas;
    }
    $fator = pow(1 + $taxaMensal, $numeroParcelas);
    $parcela = $valorPrincipal * ($taxaMensal * $fator) / ($fator - 1);
    return round($parcela, 2);
}

// ════════════════════════════════════════════════════════════════════════════════
// Bloco de verificação — NÃO altere este bloco
// ════════════════════════════════════════════════════════════════════════════════

echo "=== Verificação do Exercício ===\n\n";

// Problema 1
$usuarioAtivo   = ['st' => 1, 'nome' => 'Maria'];
$usuarioInativo = ['st' => 0, 'nome' => 'João'];
echo "chk (ativo): "   . (chk($usuarioAtivo)   ? 'true' : 'false') . "\n"; // esperado: true
echo "chk (inativo): " . (chk($usuarioInativo) ? 'true' : 'false') . "\n"; // esperado: false

echo "calc(100, 15): " . calc(100.0, 15.0) . "\n"; // esperado: 85

registrarAcesso('U001', '2026-04-14 10:00:00');

echo "calcularMulta(5 dias, R\$200): " . calcularMulta(5, 200.0) . "\n"; // esperado: 20

// Problema 2
echo "\ncalcularParcelaFinanciamento:\n";
echo "  R\$10.000 / 12x / 1% a.m.: "        . calcularParcelaFinanciamento(10000.0, 0.01, 12) . "\n";
echo "  R\$5.000 / 24x / 0.8% a.m.: "       . calcularParcelaFinanciamento(5000.0, 0.008, 24) . "\n";
echo "  R\$3.000 / 10x / 0% (sem juros): "  . calcularParcelaFinanciamento(3000.0, 0.0, 10)   . "\n";
