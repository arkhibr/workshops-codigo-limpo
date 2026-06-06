<?php
/**
 * GABARITO 19 — Anti-patterns Clássicos (PHP 8.1)
 * Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3
 * Execute: php gabarito.php
 */

declare(strict_types=1);

// ─── Correção: Magic Strings → enum + constantes ──────────────────────────────

enum CategoriaCargo: string
{
    case CLT        = 'clt';
    case PJ         = 'pj';
    case Estagiario = 'estagiario';
}

const SALARIO_MINIMO_2026      = 1412.0;
const LIMITE_FAIXA_INSS_1      = 2666.68;
const ALIQUOTA_INSS_FAIXA_1    = 0.075;
const ALIQUOTA_INSS_FAIXA_2    = 0.09;
const ALIQUOTA_INSS_FAIXA_3    = 0.12;
const ALIQUOTA_INSS_ESTAGIARIO = 0.03;
const ALIQUOTA_FGTS            = 0.08;

// ─── Modelo de domínio ────────────────────────────────────────────────────────

class Funcionario
{
    public function __construct(
        public string        $id,
        public string        $nome,
        public string        $email,
        public CategoriaCargo $categoria,
        public float          $salario,
    ) {}
}

// ─── Correção: God Object → classes com responsabilidade única ────────────────

class RepositorioFuncionario
{
    public function buscar(string $funcId): Funcionario
    {
        echo "  [BD] buscar funcionário {$funcId}\n";
        return new Funcionario($funcId, 'João Silva', 'joao@empresa.com',
                               CategoriaCargo::CLT, 3500.0);
    }

    public function salvar(Funcionario $func): void
    {
        echo "  [BD] salvar {$func->id}\n";
    }
}

class CalculadorInss
{
    public function calcular(float $salario, CategoriaCargo $categoria): float
    {
        if ($categoria === CategoriaCargo::CLT) {
            if ($salario <= SALARIO_MINIMO_2026) {
                return round($salario * ALIQUOTA_INSS_FAIXA_1, 2);
            }
            if ($salario <= LIMITE_FAIXA_INSS_1) {
                return round($salario * ALIQUOTA_INSS_FAIXA_2, 2);
            }
            return round($salario * ALIQUOTA_INSS_FAIXA_3, 2);
        }
        if ($categoria === CategoriaCargo::PJ) {
            return 0.0;
        }
        return round($salario * ALIQUOTA_INSS_ESTAGIARIO, 2);
    }
}

class CalculadorFgts
{
    public function calcular(float $salario, CategoriaCargo $categoria): float
    {
        if ($categoria === CategoriaCargo::CLT) {
            return round($salario * ALIQUOTA_FGTS, 2);
        }
        return 0.0;
    }
}

class ServicoNotificacaoRH
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
    public function gerar(int $ano): string
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

// ─── Demo ─────────────────────────────────────────────────────────────────────

echo "=== Gabarito 19 — Anti-patterns RH (PHP) ===\n\n";

$repo        = new RepositorioFuncionario();
$calcInss    = new CalculadorInss();
$calcFgts    = new CalculadorFgts();
$notificacao = new ServicoNotificacaoRH();

$func = $repo->buscar('FUNC-001');
$inss = $calcInss->calcular($func->salario, $func->categoria);
$fgts = $calcFgts->calcular($func->salario, $func->categoria);

echo "INSS: R$" . number_format($inss, 2, '.', '') . ", FGTS: R$" . number_format($fgts, 2, '.', '') . "\n";
$notificacao->enviarContracheque($func->email, $func->salario - $inss);

echo "\nVerificações:\n";
$aprovados = 0;
foreach ([RepositorioFuncionario::class, CalculadorInss::class, CalculadorFgts::class,
          ServicoNotificacaoRH::class, GeradorRelatorioRH::class] as $classe) {
    $obj     = new $classe();
    $metodos = array_filter(get_class_methods($obj), fn($m) => !str_starts_with($m, '_'));
    $qtd     = count($metodos);
    if ($qtd <= 5) {
        echo "OK: {$classe} tem {$qtd} método(s) — responsabilidade única\n";
        $aprovados++;
    } else {
        echo "FALHOU: {$classe} tem {$qtd} métodos — ainda muito grande\n";
    }
}

$inssClT        = round(3500 * ALIQUOTA_INSS_FAIXA_3, 2);
$inssCalculado  = $calcInss->calcular(3500.0, CategoriaCargo::CLT);
if (abs($inssCalculado - $inssClT) < 0.01) {
    echo "OK: CalculadorInss — alíquota CLT correta para R\$3500\n";
} else {
    echo "FALHOU: CalculadorInss — esperado R\${$inssClT}, obtido R\${$inssCalculado}\n";
}

$inssPJ = $calcInss->calcular(5000.0, CategoriaCargo::PJ);
if ($inssPJ === 0.0) {
    echo "OK: CalculadorInss — PJ retorna zero\n";
} else {
    echo "FALHOU: CalculadorInss — PJ esperado 0, obtido {$inssPJ}\n";
}

echo "OK: CategoriaCargo enum — CLT='" . CategoriaCargo::CLT->value . "', PJ='" . CategoriaCargo::PJ->value . "'\n";
echo "OK: SALARIO_MINIMO_2026 = " . SALARIO_MINIMO_2026 . "\n";
