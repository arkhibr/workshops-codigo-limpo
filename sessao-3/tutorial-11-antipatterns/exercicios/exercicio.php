<?php
/**
 * EXERCÍCIO 19 — Anti-patterns Clássicos (PHP 8.1)
 * Tempo estimado: 34 minutos (4 micro-passos)
 * Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3
 *
 * INSTRUÇÕES GERAIS:
 *   O código abaixo demonstra 4 anti-patterns.
 *   Siga os 4 passos em ordem — cada passo é independente e verificável.
 *   Execute: php exercicio.php (deve rodar sem erro antes e depois de cada passo)
 *
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 * PASSO 1 — MAGIC STRINGS/NUMBERS  (8 min)
 *   Extraia as strings e números mágicos para constantes nomeadas:
 *     const SALARIO_MINIMO_2026 = 1412.0;
 *     const CATEGORIA_CLT = "C"; / CATEGORIA_PJ = "P"; / CATEGORIA_ESTAGIARIO = "E";
 *   Substitua todas as ocorrências nos lugares onde estão usados.
 *   Verifique que o demo ainda roda.
 *
 * PASSO 2 — FEATURE ENVY  (8 min)
 *   Mova calcularInss() de GestorFolhaPagamento para a classe Funcionario.
 *   Funcionario::calcularInss(): float — sem parâmetros extras, usa $this->salario/$this->categoria.
 *   Atualize os chamadores.
 *   Verifique que o demo ainda roda.
 *
 * PASSO 3 — COPY-PASTE  (8 min)
 *   Extraia calcularBase() como função de módulo (função livre):
 *     function calcularBase(Funcionario $func): float { ... }
 *   Faça CalculoNormal::calcularBase() e CalculoTerceirizado::calcularBase()
 *   chamarem calcularBase().
 *   Verifique que o demo ainda roda.
 *
 * PASSO 4 — GOD OBJECT  (10 min)
 *   Separe GestorFolhaPagamento em 3 classes com responsabilidade única:
 *     RepositorioFuncionario  — buscarFuncionario, salvarFuncionario
 *     ServicoNotificacao      — enviarContracheque, notificarRh
 *     GeradorRelatorioRH      — gerarRelatorio, exportarCsv, arquivarFolha
 *   Deixe calcularFgts() em RepositorioFuncionario ou crie CalculadorFolha separado.
 *   Verifique que o demo ainda roda.
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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

// ─── Anti-pattern 3 — Feature Envy (calcularInss vive fora de Funcionario) ───

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

    // Feature Envy: sabe mais sobre Funcionario do que sobre si mesmo
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

// ─── Anti-pattern 4 — Copy-Paste ─────────────────────────────────────────────

class CalculoNormal
{
    public function calcularBase(Funcionario $func): float
    {
        $salarioBase = 1412;           // magic number — copiado em CalculoTerceirizado
        if ($func->categoria === 'C') {
            return max($func->salario, $salarioBase);
        }
        return $func->salario;
    }

    public function calcularLiquido(Funcionario $func): float
    {
        return round($this->calcularBase($func) * 0.85, 2);
    }
}

class CalculoTerceirizado
{
    public function calcularBase(Funcionario $func): float   // idêntico a CalculoNormal
    {
        $salarioBase = 1412;           // magic number — copiado de CalculoNormal
        if ($func->categoria === 'C') {
            return max($func->salario, $salarioBase);
        }
        return $func->salario;
    }

    public function calcularLiquido(Funcionario $func): float
    {
        return round($this->calcularBase($func) * 0.80, 2);
    }
}

// ─── Demo ─────────────────────────────────────────────────────────────────────

$gestor = new GestorFolhaPagamento();
$func   = $gestor->buscarFuncionario('FUNC-001');
$inss   = $gestor->calcularInss($func->salario, $func->categoria);
$fgts   = $gestor->calcularFgts($func->salario, $func->categoria);
echo "INSS: R$" . number_format($inss, 2, '.', '') . ", FGTS: R$" . number_format($fgts, 2, '.', '') . "\n";
$gestor->enviarContracheque($func->email, $func->salario - $inss);
$metodos = array_filter(get_class_methods($gestor), fn($m) => !str_starts_with($m, '_'));
echo "GestorFolhaPagamento tem " . count($metodos) . " métodos\n";

$normal       = new CalculoNormal();
$terceirizado = new CalculoTerceirizado();
echo "Líquido CLT: R$"  . number_format($normal->calcularLiquido($func),       2, '.', '') . "\n";
echo "Líquido Terc: R$" . number_format($terceirizado->calcularLiquido($func), 2, '.', '') . "\n";

// ── Stubs de verificação — descomente após cada passo ─────────────────────────

// PASSO 1 — descomente para verificar:
// assert(CATEGORIA_CLT        === 'C');
// assert(CATEGORIA_PJ         === 'P');
// assert(CATEGORIA_ESTAGIARIO === 'E');
// assert(SALARIO_MINIMO_2026  === 1412.0);
// echo "PASSO 1 OK: constantes definidas e usadas\n";

// PASSO 2 — descomente para verificar (requer Passo 1 feito):
// $fClt = new Funcionario('F1', 'João', 'j@e.com', CATEGORIA_CLT, 3500.0);
// assert(abs($fClt->calcularInss() - round(3500.0 * 0.12, 2)) < 0.01);
// $fPj = new Funcionario('F2', 'Ana', 'a@e.com', CATEGORIA_PJ, 8000.0);
// assert($fPj->calcularInss() === 0.0);
// echo "PASSO 2 OK: calcularInss() pertence a Funcionario\n";

// PASSO 3 — descomente para verificar (requer Passo 1 feito):
// $fTeste = new Funcionario('F3', 'Leo', 'l@e.com', CATEGORIA_CLT, 3500.0);
// $n = new CalculoNormal();
// $t = new CalculoTerceirizado();
// assert(abs($n->calcularLiquido($fTeste) - round(3500.0 * 0.85, 2)) < 0.01);
// assert(abs($t->calcularLiquido($fTeste) - round(3500.0 * 0.80, 2)) < 0.01);
// echo "PASSO 3 OK: calcularBase() sem duplicação\n";

// PASSO 4 — descomente para verificar:
// foreach ([RepositorioFuncionario::class, ServicoNotificacao::class, GeradorRelatorioRH::class] as $cls) {
//     $obj = new $cls();
//     $qtd = count(array_filter(get_class_methods($obj), fn($m) => !str_starts_with($m, '_')));
//     assert($qtd <= 5, "{$cls} ainda tem responsabilidades demais");
// }
// echo "PASSO 4 OK: God Object separado em 3 classes\n";
