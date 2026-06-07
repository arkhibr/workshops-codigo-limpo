<?php
/**
 * EXERCÍCIO 22 — Idiom Patterns em PHP 8.1
 * Tempo estimado: 20 minutos
 *
 * INSTRUÇÕES:
 *   O código abaixo é funcional mas não usa os idioms do PHP 8.1.
 *   1. Funcionario usa __construct manual sem constructor property promotion
 *      — converta para readonly class com promoção de propriedades e validação.
 *   2. Departamento é uma string solta ("TI", "RH", "Financeiro")
 *      — crie um enum Departamento: string com os casos.
 *   3. calcularTotalFolha() e calcularMediaSalario() duplicam o timing manual
 *      — extraia uma função wrapper de medição de tempo.
 *   4. criarFuncionario() usa argumentos posicionais
 *      — use named arguments na chamada.
 *   Execute: php exercicio.php (deve rodar antes e depois)
 */

// ─── Sem constructor promotion, sem validação ─────────────────────────────────
class Funcionario {
    public string $id;
    public string $nome;
    public string $departamento;
    public float  $salario;

    public function __construct(string $id, string $nome, string $departamento, float $salario) {
        // sem validação: salario=-500 passa silenciosamente
        $this->id           = $id;
        $this->nome         = $nome;
        $this->departamento = $departamento;
        $this->salario      = $salario;
    }
}

// ─── Strings de departamento soltas (sem enum) ────────────────────────────────
function filtrarPorDepartamento(array $funcionarios, string $depto): array {
    return array_filter($funcionarios, fn($f) => $f->departamento === $depto);
}

// ─── Timing copiado em duas funções ──────────────────────────────────────────
function calcularTotalFolha(array $funcionarios): float {
    $inicio = microtime(true);
    $total  = array_sum(array_map(fn($f) => $f->salario, $funcionarios));
    $fim    = microtime(true);
    echo "  calcularTotalFolha: " . round(($fim - $inicio) * 1000, 2) . "ms\n";
    return $total;
}

function calcularMediaSalario(array $funcionarios): float {
    $inicio = microtime(true);                   // copiado
    $total  = array_sum(array_map(fn($f) => $f->salario, $funcionarios));
    $media  = count($funcionarios) > 0 ? $total / count($funcionarios) : 0.0;
    $fim    = microtime(true);                   // copiado
    echo "  calcularMediaSalario: " . round(($fim - $inicio) * 1000, 2) . "ms\n";
    return $media;
}

// ─── Demo ─────────────────────────────────────────────────────────────────────
echo "=== Exercício 22 PHP — antes dos idioms ===\n\n";

$funcionarios = [
    new Funcionario("F001", "Ana Silva",  "TI",        5000.0),
    new Funcionario("F002", "João Costa", "RH",        3500.0),
    new Funcionario("F003", "Maria Lima", "TI",        6000.0),
    new Funcionario("F004", "Pedro Alves","Financeiro",4200.0),
];

$ti = array_values(filtrarPorDepartamento($funcionarios, "TI"));
echo "TI: " . count($ti) . " funcionário(s)\n";

$total = calcularTotalFolha($funcionarios);
echo "Total folha: R$" . number_format($total, 2) . "\n";

$media = calcularMediaSalario($funcionarios);
echo "Média salarial: R$" . number_format($media, 2) . "\n";
