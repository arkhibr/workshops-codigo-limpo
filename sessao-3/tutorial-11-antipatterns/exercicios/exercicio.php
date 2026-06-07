<?php
/**
 * EXERCÍCIO 19 — Anti-patterns Clássicos (PHP 8.1)
 * Tempo estimado: 15 minutos
 * Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3
 *
 * INSTRUÇÕES:
 *   O código abaixo demonstra dois anti-patterns:
 *   1. God Object: GestorFolhaPagamento faz tudo — CRUD, cálculo, relatório, email.
 *   2. Magic Strings/Numbers: if ($categoria === "C"), $salarioBase = 1412.
 *
 *   1. Quebre o God Object em classes com responsabilidade única.
 *   2. Substitua as strings/números mágicos por enums e constantes.
 *   3. Execute: php exercicio.php (deve rodar antes e depois)
 */

declare(strict_types=1);

class Funcionario
{
    public function __construct(
        public string $id,
        public string $nome,
        public string $email,
        public string $categoria,  // "C" = CLT, "P" = PJ, "E" = Estagiário
        public float  $salario,
    ) {}
}

class GestorFolhaPagamento
{
    public function buscarFuncionario(string $funcId): Funcionario
    {
        echo "  [BD] buscar funcionário {$funcId}\n";
        return new Funcionario($funcId, 'João Silva', 'joao@empresa.com', 'C', 3500.0);
    }

    public function salvarFuncionario(Funcionario $func): void
    {
        echo "  [BD] salvar {$func->id}\n";
    }

    public function calcularInss(float $salario, string $categoria): float
    {
        if ($categoria === 'C') {         // magic string
            if ($salario <= 1412) {       // magic number — salário mínimo 2026
                return round($salario * 0.075, 2);
            } elseif ($salario <= 2666.68) {
                return round($salario * 0.09, 2);
            } else {
                return round($salario * 0.12, 2);
            }
        }
        if ($categoria === 'P') {         // magic string
            return 0.0;
        }
        return round($salario * 0.03, 2); // estagiário
    }

    public function calcularFgts(float $salario, string $categoria): float
    {
        if ($categoria === 'C') {
            return round($salario * 0.08, 2);
        }
        return 0.0;
    }

    public function enviarContracheque(string $email, float $valor): void
    {
        echo "  [Email] → {$email}: contracheque R$" . number_format($valor, 2, '.', '') . "\n";
    }

    public function arquivarFolha(int $mes, int $ano): void
    {
        echo "  [BD] arquivando folha {$mes}/{$ano}\n";
    }

    public function gerarRelatorio(int $ano): string
    {
        return "Relatório folha {$ano}";
    }

    public function exportarCsv(array $dados): string
    {
        return "funcionario,salario\n";
    }

    public function reprocessarFolha(int $mes): bool
    {
        echo "  reprocessando folha {$mes}\n";
        return true;
    }

    public function notificarRh(string $msg): void
    {
        echo "  [RH] {$msg}\n";
    }

    public function validarCpf(string $cpf): bool
    {
        return strlen(str_replace(['.', '-'], '', $cpf)) === 11;
    }

    public function calcularFerias(float $salario): float
    {
        return round($salario / 3, 2);
    }
}

// Demo
$gestor = new GestorFolhaPagamento();
$func   = $gestor->buscarFuncionario('FUNC-001');
$inss   = $gestor->calcularInss($func->salario, $func->categoria);
$fgts   = $gestor->calcularFgts($func->salario, $func->categoria);
echo "INSS: R$" . number_format($inss, 2, '.', '') . ", FGTS: R$" . number_format($fgts, 2, '.', '') . "\n";
$gestor->enviarContracheque($func->email, $func->salario - $inss);
$metodos = array_filter(get_class_methods($gestor), fn($m) => !str_starts_with($m, '_'));
echo "GestorFolhaPagamento tem " . count($metodos) . " métodos\n";
