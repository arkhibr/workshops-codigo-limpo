<?php
/**
 * EXERCÍCIO — Tutorial 07: Gestão de Código Legado
 *
 * Módulo de cálculo de comissões de vendedores.
 * Status: em produção desde 2020, nunca teve testes, nunca foi refatorado.
 *
 * INSTRUÇÕES:
 *   1. Escreva "testes de caracterização" para o método calcComm abaixo:
 *      testes que documentam o comportamento ATUAL antes de qualquer mudança.
 *      Use asserts simples no bloco de execução ao final.
 *      Dica: passe valores conhecidos e verifique o retorno. Se o resultado
 *      parecer errado, documente-o assim mesmo — o objetivo é capturar o
 *      comportamento existente, não corrigi-lo ainda.
 *
 *   2. Identifique e anote com "// SMELL:" cada problema que você encontrar
 *      no código. Exemplos de smells: magic number, nome obscuro, estado
 *      global modificado, lógica duplicada, comentário que mente.
 *
 *   3. Refatore o código aplicando as técnicas do tutorial:
 *      - Constantes nomeadas para os magic numbers
 *      - Classes com responsabilidade única
 *      - Eliminar modificação de estado global dentro de método
 *      - Nomes descritivos para parâmetros e variáveis
 *      - Eliminar lógica duplicada
 *
 *   4. Execute seus testes de caracterização na versão refatorada.
 *      Se algum assert falhar, você mudou o comportamento — investigue.
 *
 * Para rodar: php exercicio.php
 */

// Estado global modificado por método — dificulta paralelismo e testes
$cache = [];

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

    public function calcComm($s, $r, $t, $m)
    {
        // s = vendedor id, r = receita total, t = tipo de meta, m = meta
        global $cache, $vendedores;

        if (isset($cache[$s])) {
            return $cache[$s];
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

        $cache[$s] = round($c, 2);
        return $cache[$s];
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

            $resultados[$s] = round($c, 2);
        }

        return $resultados;
    }
}

// ── Execução principal ──────────────────────────────────────────────────────────

$calc = new CommissionCalc();

// -----------------------------------------------------------------------
// ETAPA 1: Escreva aqui seus testes de caracterização
// Documente o comportamento atual ANTES de refatorar.
// Exemplo de estrutura (substitua pelos valores corretos):
//
//   $resultado = $calc->calcComm("V001", 10000, "STD", 8000);
//   assert($resultado === ???, "Esperado ???, obtido {$resultado}");
//
// Rode o arquivo, veja o que retorna, e use esse valor no assert.
// -----------------------------------------------------------------------

echo "=== Testes de caracterização ===" . PHP_EOL;
echo "(implemente seus asserts aqui antes de refatorar)" . PHP_EOL . PHP_EOL;

// Exemplos de chamadas para explorar o comportamento:
echo "SR, receita=10000, meta=8000, tipo=STD: " . $calc->calcComm('V001', 10000, 'STD', 8000) . PHP_EOL;
echo "SR, receita=4000,  meta=8000, tipo=STD: " . $calc->calcComm('V003', 4000,  'STD', 8000) . PHP_EOL;
echo "JR, receita=6000,  meta=5000, tipo=AGR: " . $calc->calcComm('V002', 6000,  'AGR', 5000) . PHP_EOL;
echo PHP_EOL;

echo "=== Batch ===" . PHP_EOL;
$vendas = [
    ['id' => 'V001', 'receita' => 10000, 'tipo_meta' => 'STD', 'meta' => 8000],
    ['id' => 'V002', 'receita' => 6000,  'tipo_meta' => 'AGR', 'meta' => 5000],
];
echo json_encode($calc->batchCalc($vendas)) . PHP_EOL;
