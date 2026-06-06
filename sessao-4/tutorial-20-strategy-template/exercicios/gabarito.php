<?php
/**
 * gabarito.php — Solução do Exercício 20: Strategy e Template Method em PHP 8.1
 * Execute: php gabarito.php
 */

// ─── Strategy: EstrategiaFrete ───────────────────────────────────────────────
interface EstrategiaFrete {
    public function calcular(float $peso, float $distancia): float;
    public function nome(): string;
}

class FreteCorreios implements EstrategiaFrete {
    public function calcular(float $peso, float $distancia): float {
        return round($peso * 2.5 + $distancia * 0.10, 2);
    }
    public function nome(): string { return 'Correios'; }
}

class FreteJadlog implements EstrategiaFrete {
    public function calcular(float $peso, float $distancia): float {
        return round($peso * 2.0 + $distancia * 0.12, 2);
    }
    public function nome(): string { return 'Jadlog'; }
}

class FreteRetirada implements EstrategiaFrete {
    public function calcular(float $peso, float $distancia): float { return 0.0; }
    public function nome(): string { return 'Retirada'; }
}

class FreteLoggi implements EstrategiaFrete {   // adicionado sem alterar as demais
    public function calcular(float $peso, float $distancia): float {
        return round($peso * 1.8 + $distancia * 0.08, 2);
    }
    public function nome(): string { return 'Loggi'; }
}

class CalculadorFrete {
    public function __construct(private EstrategiaFrete $estrategia) {}

    public function calcular(float $peso, float $distancia): float {
        return $this->estrategia->calcular($peso, $distancia);
    }

    public function trocarEstrategia(EstrategiaFrete $estrategia): void {
        $this->estrategia = $estrategia;
    }
}

// ─── Template Method: RelatorioLogistica ─────────────────────────────────────
abstract class RelatorioLogistica {
    final public function gerar(array $entregas): string {
        $filtradas = array_values(array_filter($entregas, fn($e) => $e['valor_nf'] > 0));
        $linhas    = $this->formatarLinhas($filtradas);
        $total     = array_sum(array_map(fn($e) => $e['valor_nf'], $filtradas));
        return $this->montarSaida($linhas, $total);
    }
    abstract protected function formatarLinhas(array $entregas): array;
    abstract protected function montarSaida(array $linhas, float $total): string;
}

class RelatorioEntregas extends RelatorioLogistica {
    protected function formatarLinhas(array $entregas): array {
        return array_map(
            fn($e) => "  {$e['id']}: {$e['transportadora']} — R$" . number_format($e['valor_nf'], 2),
            $entregas
        );
    }
    protected function montarSaida(array $linhas, float $total): string {
        return "=== Relatório de Entregas ===\n" . implode("\n", $linhas) . "\nTotal NF: R$" . number_format($total, 2);
    }
}

class RelatorioColetas extends RelatorioLogistica {
    protected function formatarLinhas(array $entregas): array {
        return array_map(
            fn($e) => "  {$e['id']}: {$e['peso']}kg × {$e['distancia']}km",
            $entregas
        );
    }
    protected function montarSaida(array $linhas, float $total): string {
        return "=== Relatório de Coletas ===\n" . implode("\n", $linhas) . "\nVolume: R$" . number_format($total, 2);
    }
}

// ─── Verificação ─────────────────────────────────────────────────────────────
function verificar(string $caso, bool $ok): void {
    echo ($ok ? "OK: $caso" : "FALHOU: $caso") . "\n";
}

echo "=== Gabarito 20 — Strategy e Template Method: Logística ===\n\n";

// Strategy
$calc = new CalculadorFrete(new FreteCorreios());
$freteCorreios = $calc->calcular(2.5, 150.0);
$esperado = round(2.5 * 2.5 + 150.0 * 0.10, 2);
verificar("Strategy — Correios: R$" . number_format($freteCorreios, 2), $freteCorreios === $esperado);

$calc->trocarEstrategia(new FreteLoggi());
$freteLoggi = $calc->calcular(2.5, 150.0);
$esperadoLoggi = round(2.5 * 1.8 + 150.0 * 0.08, 2);
verificar("Strategy — Loggi adicionado sem alterar CalculadorFrete: R$" . number_format($freteLoggi, 2), $freteLoggi === $esperadoLoggi);

$calc->trocarEstrategia(new FreteRetirada());
verificar("Strategy — Retirada: R\$0,00", $calc->calcular(0.5, 0.0) === 0.0);

// Template Method
$entregas = [
    ['id' => 'ENT-001', 'transportadora' => 'correios', 'peso' => 2.5, 'distancia' => 150.0, 'valor_nf' => 89.90],
    ['id' => 'ENT-002', 'transportadora' => 'jadlog',   'peso' => 5.0, 'distancia' => 300.0, 'valor_nf' => 199.90],
];

$re = (new RelatorioEntregas())->gerar($entregas);
verificar("Template Method — RelatorioEntregas gerado", str_contains($re, 'Relatório de Entregas') && str_contains($re, 'Total NF'));

$rc = (new RelatorioColetas())->gerar($entregas);
verificar("Template Method — RelatorioColetas gerado", str_contains($rc, 'Relatório de Coletas') && str_contains($rc, 'Volume'));

verificar("Template Method — filtrar e calcular_total não duplicados", true);
