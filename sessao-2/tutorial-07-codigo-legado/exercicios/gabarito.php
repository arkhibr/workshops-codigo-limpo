<?php
/**
 * GABARITO — Tutorial 07: Gestão de Código Legado
 *
 * Para rodar: php gabarito.php
 */

// ============================================================================
// ETAPA 1: Testes de Caracterização (executados sobre o código original)
//
// Preservamos a classe original apenas para validar os testes.
// Executados ANTES de qualquer refatoração — documentam o comportamento atual.
// ============================================================================

$vendedores_raw = [
    'V001' => ['nome' => 'Ana Paula',   'tipo' => 'SR', 'regiao' => 'SP'],
    'V002' => ['nome' => 'Carlos Lima', 'tipo' => 'JR', 'regiao' => 'RJ'],
    'V003' => ['nome' => 'Maria Costa', 'tipo' => 'SR', 'regiao' => 'MG'],
];

class CommissionCalcOriginal
{
    private array $cache = [];
    private array $vendedores;

    public function __construct(array $vendedores)
    {
        $this->vendedores = $vendedores;
    }

    public function calcComm($s, $r, $t, $m)
    {
        if (isset($this->cache[$s])) {
            return $this->cache[$s];
        }

        $v = $this->vendedores[$s] ?? null;
        if (!$v) {
            return 0;
        }

        if ($v['tipo'] === 'SR') {
            if ($r >= $m) {
                $c = $r * 0.08;
                if ($r > $m * 1.2) {
                    $c = $c + ($r - $m * 1.2) * 0.03;
                }
            } else {
                if ($r >= $m * 0.8) {
                    $c = $r * 0.05;
                } else {
                    $c = $r * 0.03;
                }
            }
            if ($t === 'AGR') {
                $c = $c * 1.1;
            }
            if ($r < 5000) {
                $c = 0;
            }
        } else {
            if ($r >= $m) {
                $c = $r * 0.05;
                if ($r > $m * 1.2) {
                    $c = $c + ($r - $m * 1.2) * 0.02;
                }
            } else {
                if ($r >= $m * 0.8) {
                    $c = $r * 0.03;
                } else {
                    $c = $r * 0.03;
                }
            }
            if ($t === 'AGR') {
                $c = $c * 1.1;
            }
            if ($r < 5000) {
                $c = 0;
            }
        }

        $this->cache[$s] = round($c, 2);
        return $this->cache[$s];
    }
}

function executarTestesDeCaracterizacao(array $vendedores): void
{
    // SR, receita acima de 120% da meta → base 8% + bônus 3% do excedente
    // 10000 * 0.08 = 800 + (10000 - 9600) * 0.03 = 800 + 12 = 812
    $o1 = new CommissionCalcOriginal($vendedores);
    assert($o1->calcComm('V001', 10000, 'STD', 8000) === 812.0,
        'SR, receita=10000, meta=8000, tipo=STD');

    // SR, receita abaixo do mínimo → comissão zerada
    $o2 = new CommissionCalcOriginal($vendedores);
    assert($o2->calcComm('V001', 4000, 'STD', 8000) === 0.0,
        'SR, receita < 5000 deve zerar comissão');

    // SR, receita entre 80% e 100% da meta → alíquota 5%: 7000 * 0.05 = 350
    $o3 = new CommissionCalcOriginal($vendedores);
    assert($o3->calcComm('V003', 7000, 'STD', 8000) === 350.0,
        'SR, receita entre 80% e 100% da meta');

    // JR, receita acima da meta → alíquota 5%: 6000 * 0.05 = 300
    $o4 = new CommissionCalcOriginal($vendedores);
    assert($o4->calcComm('V002', 6000, 'STD', 5000) === 300.0,
        'JR, receita=6000, meta=5000, tipo=STD');

    // JR com meta AGR → acréscimo de 10%: 300 * 1.1 = 330
    $o5 = new CommissionCalcOriginal($vendedores);
    assert($o5->calcComm('V002', 6000, 'AGR', 5000) === 330.0,
        'JR, tipo=AGR deve acrescentar 10%');

    // JR, receita abaixo do mínimo → comissão zerada
    $o6 = new CommissionCalcOriginal($vendedores);
    assert($o6->calcComm('V002', 4000, 'STD', 5000) === 0.0,
        'JR, receita < 5000 deve zerar comissão');

    // Vendedor inexistente → retorna 0
    $o7 = new CommissionCalcOriginal($vendedores);
    assert($o7->calcComm('V999', 10000, 'STD', 8000) === 0,
        'Vendedor inexistente deve retornar 0');

    echo '[OK] Todos os testes de caracterização passaram.' . PHP_EOL;
}


// ============================================================================
// ETAPA 2: Smells identificados
//
// SMELL: variável global $cache modificada dentro do método
//   → viola isolamento; duas chamadas para o mesmo vendedor
//     retornam o valor da primeira, ignorando novos parâmetros.
//
// SMELL: parâmetros obscuros $s, $r, $t, $m
//   → impossível entender a assinatura sem ler todo o corpo.
//
// SMELL: magic numbers 0.08, 0.05, 0.03, 0.02, 1.1, 5000, 1.2
//   → sem contexto; qualquer mudança exige reentender a regra de negócio.
//
// SMELL: lógica duplicada entre calcComm e batchCalc
//   → qualquer mudança na regra precisa ser replicada em dois lugares.
//
// SMELL: comentário desatualizado ("atualizado em jan/2020")
//   → a lógica foi alterada em 2022 sem atualizar o comentário.
//
// SMELL: dois else com alíquotas idênticas para JR
//   → `if ($r >= $m*0.8) $c = $r*0.03; else $c = $r*0.03;`
//      as duas ramificações fazem o mesmo — bug ou intenção?
// ============================================================================


// ============================================================================
// ETAPA 3: Versão Refatorada
// ============================================================================

// Constantes nomeadas — cada número tem contexto e pode ser alterado com segurança
const ALIQUOTA_SR_META_ATINGIDA   = 0.08;
const ALIQUOTA_SR_BONUS_EXCEDENTE = 0.03;
const ALIQUOTA_SR_PARCIAL         = 0.05;
const ALIQUOTA_SR_ABAIXO          = 0.03;

const ALIQUOTA_JR_META_ATINGIDA   = 0.05;
const ALIQUOTA_JR_BONUS_EXCEDENTE = 0.02;
const ALIQUOTA_JR_ABAIXO          = 0.03;

const MULTIPLICADOR_META_BONUS    = 1.2;   // Acima de 120% da meta — bônus de excedente
const MULTIPLICADOR_META_PARCIAL  = 0.8;   // Acima de 80% da meta — alíquota intermediária
const MULTIPLICADOR_META_AGRICOLA = 1.1;   // Acréscimo para metas AGR
const RECEITA_MINIMA_COMISSAO     = 5000.0;


final class Vendedor
{
    public function __construct(
        public readonly string $id,
        public readonly string $nome,
        public readonly string $tipo,
        public readonly string $regiao,
    ) {}
}

final class EntradaComissao
{
    public function __construct(
        public readonly string $vendedorId,
        public readonly float  $receita,
        public readonly string $tipoMeta,
        public readonly float  $meta,
    ) {}
}


class RepositorioDeVendedores
{
    private array $vendedores = [];

    public function __construct(array $dados)
    {
        foreach ($dados as $id => $d) {
            $this->vendedores[$id] = new Vendedor($id, $d['nome'], $d['tipo'], $d['regiao']);
        }
    }

    public function buscar(string $id): ?Vendedor
    {
        return $this->vendedores[$id] ?? null;
    }
}


class CalculadorDeComissao
{
    /** Calcula comissão a partir de dados de receita e meta. Sem estado interno. */
    public function calcular(EntradaComissao $entrada, Vendedor $vendedor): float
    {
        if ($entrada->receita < RECEITA_MINIMA_COMISSAO) {
            return 0.0;
        }

        $comissao = $vendedor->tipo === 'SR'
            ? $this->comissaoSenior($entrada->receita, $entrada->meta)
            : $this->comissaoJunior($entrada->receita, $entrada->meta);

        if ($entrada->tipoMeta === 'AGR') {
            $comissao *= MULTIPLICADOR_META_AGRICOLA;
        }

        return round($comissao, 2);
    }

    private function comissaoSenior(float $receita, float $meta): float
    {
        if ($receita >= $meta) {
            $comissao = $receita * ALIQUOTA_SR_META_ATINGIDA;
            if ($receita > $meta * MULTIPLICADOR_META_BONUS) {
                $comissao += ($receita - $meta * MULTIPLICADOR_META_BONUS) * ALIQUOTA_SR_BONUS_EXCEDENTE;
            }
        } elseif ($receita >= $meta * MULTIPLICADOR_META_PARCIAL) {
            $comissao = $receita * ALIQUOTA_SR_PARCIAL;
        } else {
            $comissao = $receita * ALIQUOTA_SR_ABAIXO;
        }
        return $comissao;
    }

    private function comissaoJunior(float $receita, float $meta): float
    {
        if ($receita >= $meta) {
            $comissao = $receita * ALIQUOTA_JR_META_ATINGIDA;
            if ($receita > $meta * MULTIPLICADOR_META_BONUS) {
                $comissao += ($receita - $meta * MULTIPLICADOR_META_BONUS) * ALIQUOTA_JR_BONUS_EXCEDENTE;
            }
        } else {
            // Nota: no original, parcial e abaixo usavam a mesma alíquota para JR.
            // Comportamento preservado.
            $comissao = $receita * ALIQUOTA_JR_ABAIXO;
        }
        return $comissao;
    }
}


class ProcessadorDeComissoes
{
    public function __construct(
        private readonly RepositorioDeVendedores $repositorio,
        private readonly CalculadorDeComissao    $calculador,
    ) {}

    public function calcularIndividual(EntradaComissao $entrada): float
    {
        $vendedor = $this->repositorio->buscar($entrada->vendedorId);
        if ($vendedor === null) {
            return 0.0;
        }
        return $this->calculador->calcular($entrada, $vendedor);
    }

    /** @param EntradaComissao[] $entradas */
    public function calcularLote(array $entradas): array
    {
        $resultados = [];
        foreach ($entradas as $entrada) {
            $resultados[$entrada->vendedorId] = $this->calcularIndividual($entrada);
        }
        return $resultados;
    }
}


// ============================================================================
// ETAPA 4: Verificação — os testes de caracterização devem passar na versão nova
// ============================================================================

function executarTestesNaVersaoRefatorada(array $vendedores): void
{
    $repositorio = new RepositorioDeVendedores($vendedores);
    $processador = new ProcessadorDeComissoes($repositorio, new CalculadorDeComissao());

    $calcular = fn($vid, $r, $t, $m) =>
        $processador->calcularIndividual(new EntradaComissao($vid, $r, $t, $m));

    assert($calcular('V001', 10000, 'STD', 8000) === 812.0);
    assert($calcular('V001', 4000,  'STD', 8000) === 0.0);
    assert($calcular('V003', 7000,  'STD', 8000) === 350.0);
    assert($calcular('V002', 6000,  'STD', 5000) === 300.0);
    assert($calcular('V002', 6000,  'AGR', 5000) === 330.0);
    assert($calcular('V002', 4000,  'STD', 5000) === 0.0);
    assert($calcular('V999', 10000, 'STD', 8000) === 0.0);

    echo '[OK] Todos os testes de caracterização passaram na versão refatorada.' . PHP_EOL;
}


// ── Execução principal ──────────────────────────────────────────────────────

assert_options(ASSERT_ACTIVE, 1);
assert_options(ASSERT_EXCEPTION, 1);

echo '=== Etapa 1: Testes de Caracterização (versão original) ===' . PHP_EOL;
executarTestesDeCaracterizacao($vendedores_raw);
echo PHP_EOL;

echo '=== Etapa 4: Verificação (versão refatorada) ===' . PHP_EOL;
executarTestesNaVersaoRefatorada($vendedores_raw);
echo PHP_EOL;

echo '=== Demonstração da versão refatorada ===' . PHP_EOL;
$repositorio = new RepositorioDeVendedores($vendedores_raw);
$processador = new ProcessadorDeComissoes($repositorio, new CalculadorDeComissao());

$e1 = new EntradaComissao('V001', 10000, 'STD', 8000);
echo 'Ana Paula (SR): R$ ' . number_format($processador->calcularIndividual($e1), 2, ',', '.') . PHP_EOL;

$e2 = new EntradaComissao('V002', 6000, 'AGR', 5000);
echo 'Carlos Lima (JR, AGR): R$ ' . number_format($processador->calcularIndividual($e2), 2, ',', '.') . PHP_EOL;

echo PHP_EOL . '=== Cálculo em lote ===' . PHP_EOL;
$lote = [
    new EntradaComissao('V001', 10000, 'STD', 8000),
    new EntradaComissao('V002', 6000,  'AGR', 5000),
    new EntradaComissao('V003', 7000,  'STD', 8000),
];
foreach ($processador->calcularLote($lote) as $id => $comissao) {
    $v = $repositorio->buscar($id);
    echo "  {$v->nome}: R$ " . number_format($comissao, 2, ',', '.') . PHP_EOL;
}
