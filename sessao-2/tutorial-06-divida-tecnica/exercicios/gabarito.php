<?php
/**
 * GABARITO — Tutorial 06: Dívida Técnica
 * Execute: php gabarito.php
 *
 * Quatro passos aplicados em sequência sobre o código original:
 *   Passo 1 — Dívidas identificadas:
 *     MAGIC_NUMBER  15.0/25.0/40.0 (taxa_base), 2.5/3.2/4.0 (faixa 2),
 *                   1.8/2.1/2.8 (faixa 3), 0.12/0.18/0.25 (km), 1.3 (urgência), 5 e 20
 *     NOMES         $tp, $kg, $km, $t, $urg obscuros; estimar é ambíguo
 *     DUPLICAÇÃO    corpo idêntico em calcFrete e estimar
 *     FUNÇÕES       calcFrete faz: validar + calcular por faixa + km + urgência
 *   Passo 2 — constantes extraídas
 *   Passo 3 — parâmetros renomeados
 *   Passo 4 — _calcularPorModalidade extraída; estimarFrete chama calcularFrete
 */

// ── Passo 2: constantes nomeadas ─────────────────────────────────────────────

const LIMITE_FAIXA_1_KG = 5;
const LIMITE_FAIXA_2_KG = 20;
const FATOR_URGENCIA    = 1.3;

const TARIFAS = [
    'A' => ['taxa_base' => 15.0, 'custo_faixa2' => 2.5, 'custo_faixa3' => 1.8, 'custo_km' => 0.12],
    'B' => ['taxa_base' => 25.0, 'custo_faixa2' => 3.2, 'custo_faixa3' => 2.1, 'custo_km' => 0.18],
    'C' => ['taxa_base' => 40.0, 'custo_faixa2' => 4.0, 'custo_faixa3' => 2.8, 'custo_km' => 0.25],
];


// ── Passo 4: lógica extraída — zero duplicação ────────────────────────────────

function _calcularPorModalidade(string $modalidade, float $pesoKg, float $distanciaKm): float
{
    if (!isset(TARIFAS[$modalidade])) {
        throw new InvalidArgumentException("Modalidade inválida: {$modalidade}. Use A, B ou C.");
    }
    $t = TARIFAS[$modalidade];
    if ($pesoKg <= LIMITE_FAIXA_1_KG) {
        $custo = $t['taxa_base'];
    } elseif ($pesoKg <= LIMITE_FAIXA_2_KG) {
        $custo = $t['taxa_base'] + ($pesoKg - LIMITE_FAIXA_1_KG) * $t['custo_faixa2'];
    } else {
        $custo = $t['taxa_base']
               + (LIMITE_FAIXA_2_KG - LIMITE_FAIXA_1_KG) * $t['custo_faixa2']
               + ($pesoKg - LIMITE_FAIXA_2_KG) * $t['custo_faixa3'];
    }
    $custo += $distanciaKm * $t['custo_km'];
    return $custo;
}


// ── Passos 3+4: funções públicas com nomes descritivos ───────────────────────

function calcularFrete(string $modalidade, float $pesoKg, float $distanciaKm, bool $urgente = false): float
{
    $valor = _calcularPorModalidade($modalidade, $pesoKg, $distanciaKm);
    if ($urgente) {
        $valor *= FATOR_URGENCIA;
    }
    return round($valor, 2);
}


function estimarFrete(string $modalidade, float $pesoKg, float $distanciaKm): float
{
    return calcularFrete($modalidade, $pesoKg, $distanciaKm, false);
}


// ── Verificação ──────────────────────────────────────────────────────────────

$casos = [
    ['A',  3, 100, false,  27.0],
    ['A', 15, 200, false,  64.0],
    ['A', 30, 300, false, 106.5],
    ['B', 10, 150, false,  68.0],
    ['C', 25, 400, false, 214.0],
    ['A',  5, 100, true,   35.1],
];

echo "=== Gabarito T06 — valores esperados ===" . PHP_EOL . PHP_EOL;

$ok = true;
foreach ($casos as [$modalidade, $peso, $dist, $urgente, $esperado]) {
    $resultado = calcularFrete($modalidade, $peso, $dist, $urgente);
    $status    = ($resultado == $esperado) ? 'OK' : "ERRO — esperado {$esperado}";
    if ($resultado != $esperado) { $ok = false; }
    $label = $urgente ? 'urgente' : '       ';
    echo "  {$modalidade} {$peso}kg {$dist}km {$label}: {$resultado} [{$status}]" . PHP_EOL;
}

echo PHP_EOL . "Estimativa A, 3kg, 100km: " . estimarFrete('A', 3, 100) . PHP_EOL;
echo PHP_EOL . "Todos corretos: " . ($ok ? 'SIM' : 'NÃO') . PHP_EOL;
