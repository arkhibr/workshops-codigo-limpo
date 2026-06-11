<?php
/**
 * GABARITO 19 — Anti-patterns Clássicos (PHP 8.1)
 * Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3
 * Execute: php gabarito.php
 */

declare(strict_types=1);

// ─── Passo 1: Magic Strings/Numbers → const nomeadas ─────────────────────────

const CATEGORIA_CLT        = 'C';
const CATEGORIA_PJ         = 'P';
const CATEGORIA_ESTAGIARIO = 'E';

const SALARIO_MINIMO_2026      = 1412.0;
const LIMITE_FAIXA_INSS_2      = 2666.68;
const ALIQUOTA_INSS_FAIXA_1    = 0.075;
const ALIQUOTA_INSS_FAIXA_2    = 0.09;
const ALIQUOTA_INSS_FAIXA_3    = 0.12;
const ALIQUOTA_INSS_ESTAGIARIO = 0.03;
const ALIQUOTA_FGTS            = 0.08;

// ─── Modelo de domínio ────────────────────────────────────────────────────────

class Funcionario
{
    public function __construct(
        public string $id,
        public string $nome,
        public string $email,
        public string $categoria,  // usa as constantes CATEGORIA_* acima
        public float  $salario,
    ) {}

    // Passo 2: Feature Envy → calcularInss() pertence ao dono dos dados
    public function calcularInss(): float
    {
        if ($this->categoria === CATEGORIA_CLT) {
            if ($this->salario <= SALARIO_MINIMO_2026) {
                return round($this->salario * ALIQUOTA_INSS_FAIXA_1, 2);
            }
            if ($this->salario <= LIMITE_FAIXA_INSS_2) {
                return round($this->salario * ALIQUOTA_INSS_FAIXA_2, 2);
            }
            return round($this->salario * ALIQUOTA_INSS_FAIXA_3, 2);
        }
        if ($this->categoria === CATEGORIA_PJ) {
            return 0.0;
        }
        return round($this->salario * ALIQUOTA_INSS_ESTAGIARIO, 2);
    }
}

// ─── Passo 3: Copy-Paste → função livre compartilhada ────────────────────────

function calcularBase(Funcionario $func): float
{
    if ($func->categoria === CATEGORIA_CLT) {
        return max($func->salario, SALARIO_MINIMO_2026);
    }
    return $func->salario;
}

class CalculoNormal
{
    public function calcularBase(Funcionario $func): float
    {
        return calcularBase($func);
    }

    public function calcularLiquido(Funcionario $func): float
    {
        return round($this->calcularBase($func) * 0.85, 2);
    }
}

class CalculoTerceirizado
{
    public function calcularBase(Funcionario $func): float
    {
        return calcularBase($func);
    }

    public function calcularLiquido(Funcionario $func): float
    {
        return round($this->calcularBase($func) * 0.80, 2);
    }
}

// ─── Passo 4: God Object → 3 classes com responsabilidade única ──────────────

class RepositorioFuncionario
{
    public function buscarFuncionario(string $funcId): Funcionario
    {
        echo "  [BD] buscar funcionário {$funcId}\n";
        return new Funcionario($funcId, 'João Silva', 'joao@empresa.com',
                               CATEGORIA_CLT, 3500.0);
    }

    public function salvarFuncionario(Funcionario $func): void
    {
        echo "  [BD] salvar {$func->id}\n";
    }

    public function calcularFgts(Funcionario $func): float
    {
        if ($func->categoria === CATEGORIA_CLT) {
            return round($func->salario * ALIQUOTA_FGTS, 2);
        }
        return 0.0;
    }
}

class ServicoNotificacao
{
    public function enviarContracheque(string $email, float $valor): void
    {
        echo "  [Email] → {$email}: contracheque R$" . number_format($valor, 2, '.', '') . "\n";
    }

    public function notificarRh(string $msg): void
    {
        echo "  [RH] {$msg}\n";
    }
}

class GeradorRelatorioRH
{
    public function gerarRelatorio(int $ano): string
    {
        return "Relatório folha {$ano}";
    }

    public function exportarCsv(array $dados): string
    {
        return "funcionario,salario\n" . implode("\n", array_map('strval', $dados));
    }

    public function arquivarFolha(int $mes, int $ano): void
    {
        echo "  [BD] arquivando folha {$mes}/{$ano}\n";
    }
}

// ─── Verificação ──────────────────────────────────────────────────────────────

echo "=== Gabarito 19 — Anti-patterns RH (PHP) ===\n\n";

// Passo 1
assert(CATEGORIA_CLT        === 'C');
assert(CATEGORIA_PJ         === 'P');
assert(CATEGORIA_ESTAGIARIO === 'E');
assert(SALARIO_MINIMO_2026  === 1412.0);
echo "PASSO 1 OK: constantes CATEGORIA_* e SALARIO_MINIMO_2026 definidas\n";

// Passo 2
$fClt   = new Funcionario('F1', 'João', 'j@e.com', CATEGORIA_CLT,        3500.0);
$fPj    = new Funcionario('F2', 'Ana',  'a@e.com', CATEGORIA_PJ,         8000.0);
$fEstag = new Funcionario('F3', 'Leo',  'l@e.com', CATEGORIA_ESTAGIARIO,  900.0);
assert(abs($fClt->calcularInss()   - round(3500.0 * ALIQUOTA_INSS_FAIXA_3,    2)) < 0.01);
assert($fPj->calcularInss()    === 0.0);
assert(abs($fEstag->calcularInss() - round(900.0  * ALIQUOTA_INSS_ESTAGIARIO, 2)) < 0.01);
echo "PASSO 2 OK: calcularInss() em Funcionario "
   . "(CLT=R$" . number_format($fClt->calcularInss(), 2, '.', '')
   . ", PJ=R$" . number_format($fPj->calcularInss(),  2, '.', '') . ")\n";

// Passo 3
$n = new CalculoNormal();
$t = new CalculoTerceirizado();
assert(abs($n->calcularLiquido($fClt) - round(3500.0 * 0.85, 2)) < 0.01);
assert(abs($t->calcularLiquido($fClt) - round(3500.0 * 0.80, 2)) < 0.01);
echo "PASSO 3 OK: calcularBase() sem duplicação "
   . "(CLT=R$" . number_format($n->calcularLiquido($fClt), 2, '.', '')
   . ", Terc=R$" . number_format($t->calcularLiquido($fClt), 2, '.', '') . ")\n";

// Passo 4
foreach ([RepositorioFuncionario::class, ServicoNotificacao::class, GeradorRelatorioRH::class] as $cls) {
    $obj  = new $cls();
    $qtd  = count(array_filter(get_class_methods($obj), fn($m) => !str_starts_with($m, '_')));
    assert($qtd <= 5, "{$cls} ainda tem responsabilidades demais");
}
echo "PASSO 4 OK: RepositorioFuncionario / ServicoNotificacao / GeradorRelatorioRH\n";

echo "\n--- Demo completo ---\n";
$repo  = new RepositorioFuncionario();
$notif = new ServicoNotificacao();
$func  = $repo->buscarFuncionario('FUNC-001');
$inss  = $func->calcularInss();
$fgts  = $repo->calcularFgts($func);
echo "INSS: R$" . number_format($inss, 2, '.', '') . ", FGTS: R$" . number_format($fgts, 2, '.', '') . "\n";
$notif->enviarContracheque($func->email, $func->salario - $inss);
