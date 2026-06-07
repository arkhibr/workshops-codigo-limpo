<?php
/**
 * equivalente.php — Strategy e Template Method em PHP 8.1
 * Execute: php equivalente.php
 */

// ─── Ruim: if/elif de imposto ────────────────────────────────────────────────
function calcularImpostoRuim(string $regime, float $valor): float {
    if ($regime === 'simples')   return round($valor * 0.06, 2);
    if ($regime === 'presumido') return round($valor * 0.132, 2);
    if ($regime === 'real')      return round($valor * 0.34, 2);
    throw new \InvalidArgumentException("Regime desconhecido: $regime");
}

// ─── Bom: Strategy ────────────────────────────────────────────────────────────
interface EstrategiaImposto {
    public function calcular(float $valor): float;
    public function nome(): string;
}

class SimplesNacional implements EstrategiaImposto {
    public function calcular(float $valor): float { return round($valor * 0.06, 2); }
    public function nome(): string { return 'Simples Nacional'; }
}

class LucroPresumido implements EstrategiaImposto {
    public function calcular(float $valor): float { return round($valor * 0.132, 2); }
    public function nome(): string { return 'Lucro Presumido'; }
}

class LucroReal implements EstrategiaImposto {
    public function calcular(float $valor): float { return round($valor * 0.34, 2); }
    public function nome(): string { return 'Lucro Real'; }
}

class MEI implements EstrategiaImposto {   // adicionado sem alterar as demais
    public function calcular(float $valor): float { return round($valor * 0.05, 2); }
    public function nome(): string { return 'MEI'; }
}

class CalculadorImposto {
    public function __construct(private EstrategiaImposto $estrategia) {}

    public function calcular(float $valor): float {
        return $this->estrategia->calcular($valor);
    }

    public function trocarEstrategia(EstrategiaImposto $estrategia): void {
        $this->estrategia = $estrategia;
    }
}

// ─── Ruim: Template Method duplicado ─────────────────────────────────────────
class RelatorioVendasRuim {
    public function gerar(array $dados): string {
        $filtrados = array_filter($dados, fn($d) => $d['valor'] > 0);
        $linhas = array_map(fn($d) => "  {$d['produto']}: {$d['qtd']} × R${$d['valor']}", $filtrados);
        $total  = array_sum(array_map(fn($d) => $d['valor'] * $d['qtd'], $filtrados));
        return "=== Relatório de Vendas ===\n" . implode("\n", $linhas) . "\nTotal: R$" . number_format($total, 2);
    }
}

class RelatorioFinanceiroRuim {
    public function gerar(array $dados): string {  // esqueleto copiado
        $filtrados = array_filter($dados, fn($d) => $d['valor'] > 0);
        $linhas = array_map(fn($d) => "  R$" . number_format($d['valor'] * $d['qtd'], 2) . " ({$d['produto']})", $filtrados);
        $total  = array_sum(array_map(fn($d) => $d['valor'] * $d['qtd'], $filtrados));
        return "=== Relatório Financeiro ===\n" . implode("\n", $linhas) . "\nReceita: R$" . number_format($total, 2);
    }
}

// ─── Bom: Template Method ────────────────────────────────────────────────────
abstract class RelatorioBase {
    final public function gerar(array $dados): string {
        $filtrados = array_filter($dados, fn($d) => $d['valor'] > 0);
        $linhas    = $this->formatarLinhas(array_values($filtrados));
        $total     = array_sum(array_map(fn($d) => $d['valor'] * $d['qtd'], $filtrados));
        return $this->montarSaida($linhas, $total);
    }
    abstract protected function formatarLinhas(array $dados): array;
    abstract protected function montarSaida(array $linhas, float $total): string;
}

class RelatorioVendas extends RelatorioBase {
    protected function formatarLinhas(array $dados): array {
        return array_map(fn($d) => "  {$d['produto']}: {$d['qtd']} × R${$d['valor']}", $dados);
    }
    protected function montarSaida(array $linhas, float $total): string {
        return "=== Relatório de Vendas ===\n" . implode("\n", $linhas) . "\nTotal: R$" . number_format($total, 2);
    }
}

class RelatorioFinanceiro extends RelatorioBase {
    protected function formatarLinhas(array $dados): array {
        return array_map(fn($d) => "  R$" . number_format($d['valor'] * $d['qtd'], 2) . " ({$d['produto']})", $dados);
    }
    protected function montarSaida(array $linhas, float $total): string {
        return "=== Relatório Financeiro ===\n" . implode("\n", $linhas) . "\nReceita: R$" . number_format($total, 2);
    }
}

// ─── Demo ─────────────────────────────────────────────────────────────────────
echo "=== Strategy + Template Method PHP 8.1 ===\n\n";

$calc = new CalculadorImposto(new SimplesNacional());
assert($calc->calcular(10000.0) === 600.0);
echo "OK: Strategy — SimplesNacional R\$600,00\n";

$calc->trocarEstrategia(new MEI());
assert($calc->calcular(10000.0) === 500.0);
echo "OK: Strategy — MEI adicionado sem alterar CalculadorImposto\n";

$dados = [
    ['produto' => 'Webcam HD', 'valor' => 299.90, 'qtd' => 2],
    ['produto' => 'Teclado',   'valor' => 189.90, 'qtd' => 1],
];
$rv = (new RelatorioVendas())->gerar($dados);
assert(str_contains($rv, 'Relatório de Vendas'));
echo "OK: Template Method — RelatorioVendas gerado\n";

$rf = (new RelatorioFinanceiro())->gerar($dados);
assert(str_contains($rf, 'Relatório Financeiro'));
echo "OK: Template Method — RelatorioFinanceiro gerado\n";
