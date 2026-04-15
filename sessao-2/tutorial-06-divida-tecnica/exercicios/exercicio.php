<?php
/**
 * EXERCÍCIO — Tutorial 06: Dívida Técnica
 * Referência: Clean Code, Cap. 17
 * Execute: php exercicio.php
 *
 * Este módulo calcula fretes para uma transportadora fictícia.
 * Ele está funcional, mas tem pelo menos 4 tipos de dívida técnica.
 *
 * TAREFA:
 *   Parte 1 — IDENTIFICAR: leia o código abaixo e adicione um comentário
 *   antes de cada dívida encontrada no formato:
 *       // DÍVIDA [TIPO]: <descrição do problema>
 *   Onde TIPO pode ser: NOMES, FUNÇÕES, DUPLICAÇÃO, MAGIC_NUMBER
 *
 *   Parte 2 — REFATORAR: implemente a versão refatorada na seção
 *   marcada ao final deste arquivo. A saída do bloco de verificação
 *   deve ser idêntica antes e depois da refatoração.
 *
 * Tipos de dívida para encontrar (pelo menos 3 dos 4):
 *   - Magic numbers (valores sem constante nomeada)
 *   - Duplicação (lógica repetida em dois ou mais lugares)
 *   - Funções longas (função que faz mais de uma coisa)
 *   - Nomes obscuros (variáveis/funções que não revelam intenção)
 */

// ════════════════════════════════════════════════════════════════════════════════
// CÓDIGO COM DÍVIDA TÉCNICA — identifique e anote as dívidas
// ════════════════════════════════════════════════════════════════════════════════

function calcFrete(string $tp, float $kg, float $km, bool $urg = false): float
{
    $t = 0.0;
    if ($tp === 'A') {
        if ($kg <= 5) {
            $t = 15.0;
        } elseif ($kg <= 20) {
            $t = 15.0 + ($kg - 5) * 2.5;
        } else {
            $t = 15.0 + (20 - 5) * 2.5 + ($kg - 20) * 1.8;
        }
        $t += $km * 0.12;
    } elseif ($tp === 'B') {
        if ($kg <= 5) {
            $t = 25.0;
        } elseif ($kg <= 20) {
            $t = 25.0 + ($kg - 5) * 3.2;
        } else {
            $t = 25.0 + (20 - 5) * 3.2 + ($kg - 20) * 2.1;
        }
        $t += $km * 0.18;
    } elseif ($tp === 'C') {
        if ($kg <= 5) {
            $t = 40.0;
        } elseif ($kg <= 20) {
            $t = 40.0 + ($kg - 5) * 4.0;
        } else {
            $t = 40.0 + (20 - 5) * 4.0 + ($kg - 20) * 2.8;
        }
        $t += $km * 0.25;
    }
    if ($urg) {
        $t = $t * 1.3;
    }
    return round($t, 2);
}


function estimar(string $tp, float $kg, float $km): float
{
    $t = 0.0;
    if ($tp === 'A') {
        if ($kg <= 5) {
            $t = 15.0;
        } elseif ($kg <= 20) {
            $t = 15.0 + ($kg - 5) * 2.5;
        } else {
            $t = 15.0 + (20 - 5) * 2.5 + ($kg - 20) * 1.8;
        }
        $t += $km * 0.12;
    } elseif ($tp === 'B') {
        if ($kg <= 5) {
            $t = 25.0;
        } elseif ($kg <= 20) {
            $t = 25.0 + ($kg - 5) * 3.2;
        } else {
            $t = 25.0 + (20 - 5) * 3.2 + ($kg - 20) * 2.1;
        }
        $t += $km * 0.18;
    } elseif ($tp === 'C') {
        if ($kg <= 5) {
            $t = 40.0;
        } elseif ($kg <= 20) {
            $t = 40.0 + ($kg - 5) * 4.0;
        } else {
            $t = 40.0 + (20 - 5) * 4.0 + ($kg - 20) * 2.8;
        }
        $t += $km * 0.25;
    }
    return round($t, 2);
}


// ════════════════════════════════════════════════════════════════════════════════
// IMPLEMENTE AQUI A VERSÃO REFATORADA
// ════════════════════════════════════════════════════════════════════════════════

// Dica: comece pelas constantes, depois extraia funções pequenas.

// function calcularFretePorModalidade(...): float { ... }
// function calcularFrete(...): float { ... }
// function estimarFrete(...): float { ... }


// ════════════════════════════════════════════════════════════════════════════════
// Bloco de verificação — não altere
// ════════════════════════════════════════════════════════════════════════════════

echo "=== Verificação: Cálculo de Frete ===" . PHP_EOL . PHP_EOL;

// Usando funções originais (com dívida)
echo "Frete A, 3kg, 100km: " . calcFrete('A', 3, 100) . PHP_EOL;
echo "Frete A, 15kg, 200km: " . calcFrete('A', 15, 200) . PHP_EOL;
echo "Frete A, 30kg, 300km: " . calcFrete('A', 30, 300) . PHP_EOL;
echo "Frete B, 10kg, 150km: " . calcFrete('B', 10, 150) . PHP_EOL;
echo "Frete C, 25kg, 400km: " . calcFrete('C', 25, 400) . PHP_EOL;
echo "Frete A urgente, 5kg, 100km: " . calcFrete('A', 5, 100, true) . PHP_EOL;
echo "Estimativa A, 3kg, 100km: " . estimar('A', 3, 100) . PHP_EOL;

// Após implementar, descomente e verifique que os valores batem:
// echo PHP_EOL . "--- Versão Refatorada ---" . PHP_EOL;
// echo "Frete A, 3kg, 100km: " . calcularFrete('A', 3, 100) . PHP_EOL;
// echo "Frete A, 15kg, 200km: " . calcularFrete('A', 15, 200) . PHP_EOL;
// echo "Frete A, 30kg, 300km: " . calcularFrete('A', 30, 300) . PHP_EOL;
// echo "Frete B, 10kg, 150km: " . calcularFrete('B', 10, 150) . PHP_EOL;
// echo "Frete C, 25kg, 400km: " . calcularFrete('C', 25, 400) . PHP_EOL;
// echo "Frete A urgente, 5kg, 100km: " . calcularFrete('A', 5, 100, true) . PHP_EOL;
// echo "Estimativa A, 3kg, 100km: " . estimarFrete('A', 3, 100) . PHP_EOL;
