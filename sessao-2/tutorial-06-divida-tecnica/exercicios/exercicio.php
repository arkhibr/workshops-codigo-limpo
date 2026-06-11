<?php
/**
 * EXERCÍCIO — Tutorial 06: Dívida Técnica
 * Referência: Clean Code, Cap. 17
 * Execute: php exercicio.php
 *
 * Este módulo calcula fretes para uma transportadora fictícia.
 * Ele está funcional, mas carrega 4 tipos de dívida técnica.
 *
 * PASSOS (faça um de cada vez, em ordem):
 *
 *   PASSO 1 — IDENTIFICAR (5 min)
 *     Leia o código abaixo. Antes de cada dívida, adicione um comentário:
 *         // DÍVIDA [TIPO]: <descrição>
 *     Tipos: MAGIC_NUMBER, NOMES, DUPLICAÇÃO, FUNÇÕES
 *     Meta: encontrar pelo menos 3 das 4 antes de avançar.
 *
 *   PASSO 2 — CONSTANTES (5 min)
 *     Extraia os magic numbers para constantes nomeadas acima das funções.
 *     Substitua os literais numéricos pelas constantes no corpo das funções.
 *     Verifique: php exercicio.php deve imprimir os mesmos valores.
 *
 *   PASSO 3 — NOMES (5 min)
 *     Renomeie os parâmetros obscuros em calcFrete e estimar:
 *       $tp  → $modalidade
 *       $kg  → $pesoKg
 *       $km  → $distanciaKm
 *       $urg → $urgente
 *     Renomeie estimar para estimarFrete.
 *     Verifique que o arquivo ainda executa sem erros.
 *
 *   PASSO 4 — ELIMINAR DUPLICAÇÃO (10 min)
 *     calcFrete e estimar têm exatamente o mesmo corpo de cálculo.
 *     Extraia a lógica compartilhada para _calcularPorModalidade.
 *     Faça calcularFrete e estimarFrete chamarem essa função.
 *     Verifique que a saída continua idêntica.
 */

// ════════════════════════════════════════════════════════════════════════════════
// CÓDIGO COM DÍVIDA TÉCNICA — trabalhe aqui nos Passos 1, 2 e 3
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
// PASSO 2 — adicione as constantes nomeadas aqui
// ════════════════════════════════════════════════════════════════════════════════

// const LIMITE_FAIXA_1_KG = 5;
// const LIMITE_FAIXA_2_KG = 20;
// const FATOR_URGENCIA    = 1.3;
// const TARIFAS = [
//     'A' => ['taxa_base' => ..., 'custo_faixa2' => ..., 'custo_faixa3' => ..., 'custo_km' => ...],
//     ...
// ];


// ════════════════════════════════════════════════════════════════════════════════
// PASSO 4 — extraia aqui a função auxiliar e redefina as funções públicas
// ════════════════════════════════════════════════════════════════════════════════

// function _calcularPorModalidade(string $modalidade, float $pesoKg, float $distanciaKm): float { ... }
// function calcularFrete(string $modalidade, float $pesoKg, float $distanciaKm, bool $urgente = false): float { ... }
// function estimarFrete(string $modalidade, float $pesoKg, float $distanciaKm): float { ... }


// ════════════════════════════════════════════════════════════════════════════════
// Bloco de verificação — não altere
// ════════════════════════════════════════════════════════════════════════════════

echo "=== Verificação: Cálculo de Frete ===" . PHP_EOL . PHP_EOL;

echo "Frete A, 3kg, 100km: "          . calcFrete('A',  3, 100)        . PHP_EOL; // 27
echo "Frete A, 15kg, 200km: "         . calcFrete('A', 15, 200)        . PHP_EOL; // 64
echo "Frete A, 30kg, 300km: "         . calcFrete('A', 30, 300)        . PHP_EOL; // 106.5
echo "Frete B, 10kg, 150km: "         . calcFrete('B', 10, 150)        . PHP_EOL; // 68
echo "Frete C, 25kg, 400km: "         . calcFrete('C', 25, 400)        . PHP_EOL; // 214
echo "Frete A urgente, 5kg, 100km: "  . calcFrete('A',  5, 100, true)  . PHP_EOL; // 35.1
echo "Estimativa A, 3kg, 100km: "     . estimar('A', 3, 100)           . PHP_EOL; // 27

// Após o Passo 4, descomente e verifique que os valores batem:
// echo PHP_EOL . "--- Versão refatorada (Passo 4) ---" . PHP_EOL;
// echo "Frete A, 3kg, 100km: "         . calcularFrete('A',  3, 100)        . PHP_EOL;
// echo "Frete A, 15kg, 200km: "        . calcularFrete('A', 15, 200)        . PHP_EOL;
// echo "Frete A, 30kg, 300km: "        . calcularFrete('A', 30, 300)        . PHP_EOL;
// echo "Frete B, 10kg, 150km: "        . calcularFrete('B', 10, 150)        . PHP_EOL;
// echo "Frete C, 25kg, 400km: "        . calcularFrete('C', 25, 400)        . PHP_EOL;
// echo "Frete A urgente, 5kg, 100km: " . calcularFrete('A',  5, 100, true)  . PHP_EOL;
// echo "Estimativa A, 3kg, 100km: "    . estimarFrete('A', 3, 100)          . PHP_EOL;
