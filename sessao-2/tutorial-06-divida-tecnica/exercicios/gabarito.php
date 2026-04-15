<?php
/**
 * GABARITO — Tutorial 06: Dívida Técnica
 * Referência: Clean Code, Cap. 17
 * Execute: php gabarito.php
 *
 * Dívidas identificadas e pagas:
 *   1. MAGIC_NUMBER — 15.0, 25.0, 40.0, 2.5, 3.2, 4.0, 1.8, 2.1, 2.8, 0.12, 0.18, 0.25, 1.3
 *   2. DUPLICAÇÃO   — lógica de cálculo por faixa de peso copiada em calcFrete e estimar
 *   3. FUNÇÕES      — calcFrete faz validação de modalidade, cálculo por faixa, soma de km e taxa de urgência
 *   4. NOMES        — $tp, $kg, $km, $t, $urg não revelam intenção; estimar é ambíguo
 */

// ── Constantes ──────────────────────────────────────────────────────────────────
// Dívida 1 paga: todos os magic numbers têm nome e estão agrupados por modalidade

// Estrutura de tarifas: [taxa_base, custo_por_kg_faixa2, custo_por_kg_faixa3, custo_por_km]
// Faixa 1: 0-5 kg (cobrada pela taxa base)
// Faixa 2: 5-20 kg (custo adicional por kg)
// Faixa 3: acima de 20 kg (custo adicional por kg, mais barato por volume)

const MODALIDADE_ECONOMICA = 'A';
const MODALIDADE_PADRAO    = 'B';
const MODALIDADE_EXPRESSA  = 'C';

const LIMITE_FAIXA_1_KG = 5;
const LIMITE_FAIXA_2_KG = 20;

const TARIFAS_POR_MODALIDADE = [
    MODALIDADE_ECONOMICA => [
        'taxa_base'           => 15.0,
        'custo_faixa2_por_kg' => 2.5,
        'custo_faixa3_por_kg' => 1.8,
        'custo_por_km'        => 0.12,
    ],
    MODALIDADE_PADRAO => [
        'taxa_base'           => 25.0,
        'custo_faixa2_por_kg' => 3.2,
        'custo_faixa3_por_kg' => 2.1,
        'custo_por_km'        => 0.18,
    ],
    MODALIDADE_EXPRESSA => [
        'taxa_base'           => 40.0,
        'custo_faixa2_por_kg' => 4.0,
        'custo_faixa3_por_kg' => 2.8,
        'custo_por_km'        => 0.25,
    ],
];

const FATOR_URGENCIA = 1.3; // acréscimo de 30% para entregas urgentes


// ── Funções auxiliares ──────────────────────────────────────────────────────────
// Dívida 3 paga: cada função faz uma única coisa

function _calcularCustoPeloPeso(float $pesoKg, array $tarifas): float
{
    if ($pesoKg <= LIMITE_FAIXA_1_KG) {
        return $tarifas['taxa_base'];
    }

    if ($pesoKg <= LIMITE_FAIXA_2_KG) {
        $excedenteFaixa2 = $pesoKg - LIMITE_FAIXA_1_KG;
        return $tarifas['taxa_base'] + $excedenteFaixa2 * $tarifas['custo_faixa2_por_kg'];
    }

    // Faixa 3: acima de 20 kg
    $custoFaixa2Completa = (LIMITE_FAIXA_2_KG - LIMITE_FAIXA_1_KG) * $tarifas['custo_faixa2_por_kg'];
    $excedenteFaixa3     = $pesoKg - LIMITE_FAIXA_2_KG;
    return $tarifas['taxa_base'] + $custoFaixa2Completa + $excedenteFaixa3 * $tarifas['custo_faixa3_por_kg'];
}

function _calcularCustoPelaDistancia(float $distanciaKm, array $tarifas): float
{
    return $distanciaKm * $tarifas['custo_por_km'];
}


// ── Funções públicas ────────────────────────────────────────────────────────────
// Dívida 2 paga: lógica centralizada em uma única função; calcularFrete e estimarFrete
//               chamam a mesma lógica de cálculo por modalidade

function _calcularFretePorModalidade(
    string $modalidade,
    float $pesoKg,
    float $distanciaKm
): float {
    if (!isset(TARIFAS_POR_MODALIDADE[$modalidade])) {
        throw new InvalidArgumentException("Modalidade inválida: {$modalidade}. Use A, B ou C.");
    }

    $tarifas       = TARIFAS_POR_MODALIDADE[$modalidade];
    $custoPeso     = _calcularCustoPeloPeso($pesoKg, $tarifas);
    $custoDistancia = _calcularCustoPelaDistancia($distanciaKm, $tarifas);
    return $custoPeso + $custoDistancia;
}


function calcularFrete(
    string $modalidade,
    float $pesoKg,
    float $distanciaKm,
    bool $urgente = false
): float {
    // Dívida 4 paga: parâmetros com nomes descritivos
    $valorBase = _calcularFretePorModalidade($modalidade, $pesoKg, $distanciaKm);

    if ($urgente) {
        // Taxa de urgência: 30% de acréscimo — definido em contrato comercial
        $valorBase *= FATOR_URGENCIA;
    }

    return round($valorBase, 2);
}


function estimarFrete(string $modalidade, float $pesoKg, float $distanciaKm): float
{
    // Estimativa sem urgência — alias para calcularFrete sem flag de urgência
    return calcularFrete($modalidade, $pesoKg, $distanciaKm, false);
}


// ── Execução de demonstração ────────────────────────────────────────────────────

echo "=== Gabarito: Cálculo de Frete Refatorado ===" . PHP_EOL . PHP_EOL;

echo "Frete A, 3kg, 100km: " . calcularFrete('A', 3, 100) . PHP_EOL;
echo "Frete A, 15kg, 200km: " . calcularFrete('A', 15, 200) . PHP_EOL;
echo "Frete A, 30kg, 300km: " . calcularFrete('A', 30, 300) . PHP_EOL;
echo "Frete B, 10kg, 150km: " . calcularFrete('B', 10, 150) . PHP_EOL;
echo "Frete C, 25kg, 400km: " . calcularFrete('C', 25, 400) . PHP_EOL;
echo "Frete A urgente, 5kg, 100km: " . calcularFrete('A', 5, 100, true) . PHP_EOL;
echo "Estimativa A, 3kg, 100km: " . estimarFrete('A', 3, 100) . PHP_EOL;

echo PHP_EOL . "=== Comparação com versão original (valores devem ser iguais) ===" . PHP_EOL . PHP_EOL;
require_once __DIR__ . '/exercicio.php';

$casos = [
    ['A',  3, 100, false],
    ['A', 15, 200, false],
    ['A', 30, 300, false],
    ['B', 10, 150, false],
    ['C', 25, 400, false],
    ['A',  5, 100, true],
];

$todosIguais = true;
foreach ($casos as [$modalidade, $peso, $distancia, $urgente]) {
    $original   = calcFrete($modalidade, $peso, $distancia, $urgente);
    $refatorado = calcularFrete($modalidade, $peso, $distancia, $urgente);
    $status     = ($original === $refatorado) ? 'OK' : 'DIVERGÊNCIA';
    if ($status === 'DIVERGÊNCIA') {
        $todosIguais = false;
    }
    $label = $urgente ? 'urgente' : '       ';
    echo "  {$modalidade} {$peso}kg {$distancia}km {$label}: original={$original} refatorado={$refatorado} [{$status}]" . PHP_EOL;
}

echo PHP_EOL . "Todos os valores batem: " . ($todosIguais ? 'SIM' : 'NÃO — verifique a refatoração') . PHP_EOL;
