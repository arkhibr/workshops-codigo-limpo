<?php
/**
 * gabarito.php — Solução do Exercício 22: Idiom Patterns em PHP 8.1
 * Execute: php gabarito.php
 */

// ─── Idiom 1: enum Departamento ───────────────────────────────────────────────
enum Departamento: string {
    case TI         = 'TI';
    case RH         = 'RH';
    case Financeiro = 'Financeiro';

    public function descricao(): string {
        return match($this) {
            self::TI         => 'Tecnologia da Informação',
            self::RH         => 'Recursos Humanos',
            self::Financeiro => 'Financeiro e Controladoria',
        };
    }
}

// ─── Idiom 2: readonly class com constructor property promotion + validação ────
class Funcionario {
    public function __construct(
        public readonly string      $id,
        public readonly string      $nome,
        public readonly Departamento $departamento,
        public readonly float       $salario
    ) {
        if ($salario <= 0) {
            throw new \InvalidArgumentException("salario deve ser positivo: $salario");
        }
        if (trim($nome) === '') {
            throw new \InvalidArgumentException("nome não pode ser vazio");
        }
    }
}

// ─── Idiom 3: wrapper de medição de tempo ────────────────────────────────────
function medirTempo(string $nome, callable $fn): mixed {
    $inicio    = hrtime(true);
    $resultado = $fn();
    $elapsed   = (hrtime(true) - $inicio) / 1_000_000;
    echo "  $nome: " . round($elapsed, 2) . "ms\n";
    return $resultado;
}

// ─── Idiom 4: named arguments ────────────────────────────────────────────────
function criarFuncionario(string $id, string $nome, Departamento $depto, float $salario): Funcionario {
    return new Funcionario(
        id:           $id,
        nome:         $nome,
        departamento: $depto,
        salario:      $salario
    );
}

// ─── Lógica de negócio ────────────────────────────────────────────────────────
function filtrarPorDepartamento(array $funcionarios, Departamento $depto): array {
    return array_values(array_filter($funcionarios, fn($f) => $f->departamento === $depto));
}

function calcularTotalFolha(array $funcionarios): float {
    return medirTempo('calcularTotalFolha', fn() =>
        array_sum(array_map(fn($f) => $f->salario, $funcionarios))
    );
}

function calcularMediaSalario(array $funcionarios): float {
    return medirTempo('calcularMediaSalario', function() use ($funcionarios) {
        $total = array_sum(array_map(fn($f) => $f->salario, $funcionarios));
        return count($funcionarios) > 0 ? $total / count($funcionarios) : 0.0;
    });
}

// ─── Verificação ──────────────────────────────────────────────────────────────
echo "=== Gabarito 22 PHP — Idiom Patterns: Folha de Pagamento ===\n\n";

// readonly class + named arguments
$func = criarFuncionario(
    id:     "F001",
    nome:   "Ana Silva",
    depto:  Departamento::TI,
    salario: 5000.0
);
assert($func->salario === 5000.0);
echo "OK: readonly class — Funcionario criado com named arguments\n";

// validação
try {
    new Funcionario("F999", "Inválido", Departamento::RH, -100.0);
    echo "FALHOU: deveria rejeitar salario negativo\n";
} catch (\InvalidArgumentException $e) {
    echo "OK: readonly class — rejeita salario negativo\n";
}

// enum com método
$depto = Departamento::TI;
assert($depto->descricao() === 'Tecnologia da Informação');
echo "OK: enum — Departamento::TI->descricao() = '" . $depto->descricao() . "'\n";

// filtro e cálculos
$funcionarios = [
    criarFuncionario("F001", "Ana Silva",  Departamento::TI,         5000.0),
    criarFuncionario("F002", "João Costa", Departamento::RH,         3500.0),
    criarFuncionario("F003", "Maria Lima", Departamento::TI,         6000.0),
    criarFuncionario("F004", "Pedro Alves",Departamento::Financeiro, 4200.0),
];

$ti = filtrarPorDepartamento($funcionarios, Departamento::TI);
assert(count($ti) === 2);
echo "OK: enum como parâmetro — filtrarPorDepartamento('TI') retornou " . count($ti) . " funcionário(s)\n";

$total = calcularTotalFolha($funcionarios);
assert($total === 18700.0);
echo "OK: medirTempo — calcularTotalFolha sem duplicar código (total=R$" . number_format($total, 2) . ")\n";

$media = calcularMediaSalario($funcionarios);
assert(abs($media - 18700.0 / 4) < 0.01);
echo "OK: medirTempo — calcularMediaSalario sem duplicar código (média=R$" . number_format($media, 2) . ")\n";
