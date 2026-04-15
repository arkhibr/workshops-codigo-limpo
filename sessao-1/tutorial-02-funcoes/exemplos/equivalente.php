<?php
/**
 * EQUIVALENTE PHP — Funções
 * Referência: Clean Code, Cap. 3
 */

// ─── ❌ Função que faz tudo ────────────────────────────────────────────────────

function processarPedido(string $pedidoId, string $usuarioId, array $itens, ?string $cupom, array $endereco): array {
    if (!$usuarioId) return ['erro' => 'usuário inválido'];
    $total = array_sum(array_map(fn($i) => $i['preco'] * $i['quantidade'], $itens));
    if ($cupom === 'DESCONTO10') $total *= 0.9;
    $endFormatado = "{$endereco['rua']}, {$endereco['numero']} - {$endereco['cidade']}";
    return ['pedido_id' => $pedidoId, 'total' => $total, 'endereco' => $endFormatado];
}

// ─── ✅ Uma responsabilidade por função ────────────────────────────────────────

const CUPONS = ['DESCONTO10' => 0.90, 'DESCONTO20' => 0.80];

function calcularTotalItens(array $itens): float {
    return array_sum(array_map(fn($i) => $i['preco'] * $i['quantidade'], $itens));
}

function aplicarCupom(float $total, ?string $cupom): float {
    return $total * (CUPONS[$cupom] ?? 1.0);
}

function formatarEndereco(array $endereco): string {
    return "{$endereco['rua']}, {$endereco['numero']} - {$endereco['cidade']}";
}

// ─── ❌ Flag booleana ──────────────────────────────────────────────────────────

function formatarNome(string $nome, bool $formal): string {
    return $formal ? "Sr(a). $nome" : $nome;
}

// ─── ✅ Duas funções explícitas ────────────────────────────────────────────────

function formatarNomeInformal(string $nome): string { return $nome; }
function formatarNomeFormal(string $nome): string   { return "Sr(a). $nome"; }
