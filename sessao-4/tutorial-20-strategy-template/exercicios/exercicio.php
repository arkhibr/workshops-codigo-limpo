<?php
/**
 * EXERCÍCIO 20 — Strategy e Template Method em PHP 8.1
 * Tempo estimado: 20 minutos
 * Execute: php exercicio.php
 *
 * INSTRUÇÕES:
 *   O código abaixo tem dois problemas:
 *   1. calcularFrete() usa if/elseif — adicionar transportadora exige alterar a função.
 *   2. RelatorioEntregas e RelatorioColetas duplicam o esqueleto de 4 etapas.
 *
 *   1. Refatore calcularFrete() para Strategy: crie a interface EstrategiaFrete
 *      com calcular(float $peso, float $distancia) e classes concretas.
 *   2. Refatore os relatórios para Template Method: extraia a classe base abstrata
 *      RelatorioLogistica com formatarLinhas() e montarSaida() abstratos.
 *   3. Execute: php exercicio.php (deve rodar antes e depois)
 */

// ─── Sem Strategy: if/elseif de transportadora ────────────────────────────────
function calcularFrete(string $transportadora, float $peso, float $distancia): float {
    /** Adicionar 'loggi' exige alterar esta função. */
    if ($transportadora === 'correios') {
        return round($peso * 2.5 + $distancia * 0.10, 2);
    } elseif ($transportadora === 'jadlog') {
        return round($peso * 2.0 + $distancia * 0.12, 2);
    } elseif ($transportadora === 'retirada') {
        return 0.0;
    } else {
        throw new \InvalidArgumentException("Transportadora desconhecida: $transportadora");
    }
}

// ─── Sem Template Method: esqueleto duplicado em duas classes ─────────────────
class RelatorioEntregas {
    public function gerar(array $entregas): string {
        // Etapa 1: filtrar apenas entregas com valor
        $filtradas = array_values(array_filter($entregas, fn($e) => $e['valor_nf'] > 0));
        // Etapa 2: formatar linhas (DUPLICADO em RelatorioColetas)
        $linhas = array_map(
            fn($e) => "  {$e['id']}: {$e['transportadora']} — R$" . number_format($e['valor_nf'], 2),
            $filtradas
        );
        // Etapa 3: calcular total (DUPLICADO)
        $total = array_sum(array_map(fn($e) => $e['valor_nf'], $filtradas));
        // Etapa 4: montar saída (DUPLICADO)
        return "=== Relatório de Entregas ===\n" . implode("\n", $linhas) . "\nTotal NF: R$" . number_format($total, 2);
    }
}

class RelatorioColetas {
    public function gerar(array $entregas): string {
        // Etapa 1: filtrar (DUPLICADO)
        $filtradas = array_values(array_filter($entregas, fn($e) => $e['valor_nf'] > 0));
        // Etapa 2: formatar linhas — diferença real está aqui
        $linhas = array_map(
            fn($e) => "  {$e['id']}: {$e['peso']}kg × {$e['distancia']}km",
            $filtradas
        );
        // Etapa 3: calcular total (DUPLICADO)
        $total = array_sum(array_map(fn($e) => $e['valor_nf'], $filtradas));
        // Etapa 4: montar saída (DUPLICADO)
        return "=== Relatório de Coletas ===\n" . implode("\n", $linhas) . "\nVolume: R$" . number_format($total, 2);
    }
}

// ─── Demo ─────────────────────────────────────────────────────────────────────
$entregas = [
    ['id' => 'ENT-001', 'transportadora' => 'correios',  'peso' => 2.5, 'distancia' => 150.0, 'valor_nf' => 89.90],
    ['id' => 'ENT-002', 'transportadora' => 'jadlog',    'peso' => 5.0, 'distancia' => 300.0, 'valor_nf' => 199.90],
    ['id' => 'ENT-003', 'transportadora' => 'retirada',  'peso' => 0.5, 'distancia' => 0.0,   'valor_nf' => 49.90],
];

foreach ($entregas as $e) {
    $frete = calcularFrete($e['transportadora'], $e['peso'], $e['distancia']);
    echo "{$e['id']}: frete R$" . number_format($frete, 2) . "\n";
}

echo "\n" . (new RelatorioEntregas())->gerar($entregas) . "\n";
echo "\n" . (new RelatorioColetas())->gerar($entregas) . "\n";
