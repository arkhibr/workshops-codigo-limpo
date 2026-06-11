<?php
/**
 * EXERCÍCIO — Tutorial 07: Código Legado
 *
 * Módulo de cálculo de comissões de vendedores.
 * Status: em produção desde 2020, nunca teve testes, nunca foi refatorado.
 *
 * PASSOS (faça um de cada vez, em ordem):
 *
 *   PASSO 1 — TESTES DE CARACTERIZAÇÃO (10 min)
 *     No bloco de execução ao final, escreva asserts para documentar
 *     o comportamento atual. Rode o arquivo para ver os valores, então
 *     substitua os ??? pelos valores observados.
 *     Meta: cobrir pelo menos 5 casos distintos antes de tocar no código.
 *     Importante: use instâncias novas de CommissionCalc por assert —
 *     o cache da instância mascara resultados de chamadas anteriores.
 *
 *   PASSO 2 — MAPEAR SMELLS (5 min)
 *     Leia CommissionCalc e adicione um comentário // SMELL: antes de
 *     cada problema encontrado.
 *     Exemplos: magic number, nome obscuro, estado global, duplicação,
 *     comentário desatualizado.
 *
 *   PASSO 3 — CONSTANTES + NOMES (8 min)
 *     a) Extraia os magic numbers para constantes nomeadas acima da classe:
 *        0.08, 0.05, 0.03, 0.02, 1.1, 1.2, 0.8, 5000
 *     b) Renomeie os parâmetros em calcComm:
 *        $s → $vendedorId   $r → $receita   $t → $tipoMeta   $m → $meta
 *     Verifique que seus testes do Passo 1 ainda passam.
 *
 *   PASSO 4 — ELIMINAR DUPLICAÇÃO (10 min)
 *     batchCalc duplica toda a lógica de calcComm em vez de chamá-lo.
 *     Altere batchCalc para chamar $this->calcComm em vez de repetir.
 *     Mova também o cache de variável de instância para o construtor,
 *     para que cada instância tenha seu próprio estado isolado.
 *     Verifique que seus testes continuam passando.
 *
 * Para rodar: php exercicio.php
 */

// Tabela de vendedores (simulando banco de dados)
$vendedores = [
    'V001' => ['nome' => 'Ana Paula',   'tipo' => 'SR', 'regiao' => 'SP'],
    'V002' => ['nome' => 'Carlos Lima', 'tipo' => 'JR', 'regiao' => 'RJ'],
    'V003' => ['nome' => 'Maria Costa', 'tipo' => 'SR', 'regiao' => 'MG'],
];


class CommissionCalc
{
    // Calcula comissao mensal — atualizado em jan/2020
    // (comentario desatualizado: a logica foi alterada em 2022 sem atualizar o comentario)

    private array $cache = [];

    public function calcComm($s, $r, $t, $m)
    {
        // s = vendedor id, r = receita total, t = tipo de meta, m = meta
        global $vendedores;

        if (isset($this->cache[$s])) {
            return $this->cache[$s];
        }

        $v = $vendedores[$s] ?? null;
        if (!$v) {
            return 0;
        }

        // calcula para senior
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

        // calcula para junior — copiado e modificado do bloco acima
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
                    $c = $r * 0.03; // igual ao else acima — bug ou intencional?
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

    public function batchCalc(array $vendas): array
    {
        global $vendedores;
        $resultados = [];

        foreach ($vendas as $venda) {
            $s = $venda['id'];
            $r = $venda['receita'];
            $t = $venda['tipo_meta'];
            $m = $venda['meta'];

            $v = $vendedores[$s] ?? null;
            if (!$v) {
                continue;
            }

            // duplica toda a logica de calcComm ao invés de chamar o método
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
                if ($t === 'AGR') { $c = $c * 1.1; }
                if ($r < 5000)    { $c = 0; }
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
                if ($t === 'AGR') { $c = $c * 1.1; }
                if ($r < 5000)    { $c = 0; }
            }

            $resultados[$s] = round($c, 2);
        }

        return $resultados;
    }
}

// ── Execução principal ──────────────────────────────────────────────────────────

// -----------------------------------------------------------------------
// PASSO 1: escreva seus testes de caracterização aqui.
// Rode o arquivo para ver os valores, depois substitua ??? pelo resultado.
// Use new CommissionCalc() por assert para evitar que o cache mascare.
// -----------------------------------------------------------------------

echo "=== Explorando o comportamento atual ===" . PHP_EOL;
echo "SR, receita=10000, meta=8000, tipo=STD: " . (new CommissionCalc())->calcComm('V001', 10000, 'STD', 8000) . PHP_EOL;
echo "SR, receita=4000,  meta=8000, tipo=STD: " . (new CommissionCalc())->calcComm('V003', 4000,  'STD', 8000) . PHP_EOL;
echo "SR, receita=7000,  meta=8000, tipo=STD: " . (new CommissionCalc())->calcComm('V003', 7000,  'STD', 8000) . PHP_EOL;
echo "JR, receita=6000,  meta=5000, tipo=STD: " . (new CommissionCalc())->calcComm('V002', 6000,  'STD', 5000) . PHP_EOL;
echo "JR, receita=6000,  meta=5000, tipo=AGR: " . (new CommissionCalc())->calcComm('V002', 6000,  'AGR', 5000) . PHP_EOL;
echo "JR, receita=4000,  meta=5000, tipo=STD: " . (new CommissionCalc())->calcComm('V002', 4000,  'STD', 5000) . PHP_EOL;
echo "Inexistente V999: "                        . (new CommissionCalc())->calcComm('V999', 10000, 'STD', 8000) . PHP_EOL;

echo PHP_EOL . "=== Batch ===" . PHP_EOL;
$vendas = [
    ['id' => 'V001', 'receita' => 10000, 'tipo_meta' => 'STD', 'meta' => 8000],
    ['id' => 'V002', 'receita' => 6000,  'tipo_meta' => 'AGR', 'meta' => 5000],
];
echo json_encode((new CommissionCalc())->batchCalc($vendas)) . PHP_EOL;

// -----------------------------------------------------------------------
// Substitua os ??? e descomente os asserts após anotar os valores acima:
// -----------------------------------------------------------------------
// assert((new CommissionCalc())->calcComm('V001', 10000, 'STD', 8000) === ???);
// assert((new CommissionCalc())->calcComm('V003', 4000,  'STD', 8000) === ???);
// assert((new CommissionCalc())->calcComm('V003', 7000,  'STD', 8000) === ???);
// assert((new CommissionCalc())->calcComm('V002', 6000,  'STD', 5000) === ???);
// assert((new CommissionCalc())->calcComm('V002', 6000,  'AGR', 5000) === ???);
// assert((new CommissionCalc())->calcComm('V002', 4000,  'STD', 5000) === ???);
// assert((new CommissionCalc())->calcComm('V999', 10000, 'STD', 8000) === ???);
// echo "[OK] testes de caracterização passando" . PHP_EOL;
