<?php
/**
 * EXERCÍCIO 02 — Funções
 * Tempo estimado: 15 minutos
 * Referência: Clean Code, Cap. 3
 *
 * INSTRUÇÕES:
 *   Refatore as funções abaixo aplicando os princípios do Clean Code:
 *   - Cada função deve fazer UMA coisa
 *   - Extraia funções auxiliares com nomes descritivos
 *   - Elimine flags booleanas (crie funções separadas)
 *   - Elimine efeitos colaterais ocultos
 *
 *   Não mude o comportamento externo — apenas a organização interna.
 *
 * Execute: php exercicio.php
 */

// ─── Problema 1 ───────────────────────────────────────────────────────────────
// Esta função faz pelo menos 4 coisas diferentes. Quebre-a.

function gerarRelatorio(array $funcionarios, bool $incluirInativos, string $formato): array {
    $resultado = [];
    foreach ($funcionarios as $f) {
        if (!$incluirInativos && !$f['ativo']) {
            continue;
        }
        $salarioLiquido = $f['salario'] - ($f['salario'] * 0.275);
        if ($f['salario'] > 5000) {
            $bonus = $f['salario'] * 0.10;
        } else {
            $bonus = $f['salario'] * 0.05;
        }
        $total = $salarioLiquido + $bonus;
        if ($formato === 'resumido') {
            $linha = "{$f['nome']}: R$" . number_format($total, 2, ',', '.');
        } else {
            $linha = "Nome: {$f['nome']} | Salário bruto: R$" . number_format($f['salario'], 2, ',', '.') .
                     " | Líquido: R$" . number_format($salarioLiquido, 2, ',', '.') .
                     " | Bônus: R$" . number_format($bonus, 2, ',', '.') .
                     " | Total: R$" . number_format($total, 2, ',', '.');
        }
        $resultado[] = $linha;
    }
    return $resultado;
}

// ─── Problema 2 ───────────────────────────────────────────────────────────────
// Flag booleana — crie duas funções distintas.

function enviarNotificacao(array $usuario, string $mensagem, bool $urgente): void {
    if ($urgente) {
        echo "[URGENTE] Para: {$usuario['email']} | {$mensagem}\n";
    } else {
        echo "Para: {$usuario['email']} | {$mensagem}\n";
    }
}

// ─── Problema 3 ───────────────────────────────────────────────────────────────
// Efeito colateral oculto — torne o efeito explícito no retorno.

$carrinhoGlobal = ['itens' => [], 'total' => 0.0];

function adicionarProduto(string $nome, float $preco, int $quantidade): float {
    global $carrinhoGlobal;
    $subtotal = $preco * $quantidade;
    $carrinhoGlobal['itens'][] = [
        'nome'       => $nome,
        'preco'      => $preco,
        'quantidade' => $quantidade,
    ];
    $carrinhoGlobal['total'] += $subtotal;   // efeito colateral oculto!
    return $subtotal;
}

// ─── Verificação (não altere este bloco) ──────────────────────────────────────

$funcionarios = [
    ['nome' => 'Ana',   'salario' => 6000.0, 'ativo' => true],
    ['nome' => 'Bruno', 'salario' => 4000.0, 'ativo' => false],
    ['nome' => 'Carla', 'salario' => 3500.0, 'ativo' => true],
];

echo "=== Relatório resumido (todos) ===\n";
foreach (gerarRelatorio($funcionarios, true, 'resumido') as $linha) {
    echo $linha . "\n";
}

echo "\n=== Relatório detalhado (apenas ativos) ===\n";
foreach (gerarRelatorio($funcionarios, false, 'detalhado') as $linha) {
    echo $linha . "\n";
}

echo "\n=== Notificações ===\n";
$usuario = ['email' => 'ana@empresa.com'];
enviarNotificacao($usuario, 'Reunião amanhã às 9h', false);
enviarNotificacao($usuario, 'Servidor fora do ar!', true);

echo "\n=== Carrinho ===\n";
adicionarProduto('Teclado', 250.0, 1);
adicionarProduto('Mouse', 80.0, 2);
echo "Total no carrinho: R$ " . number_format($carrinhoGlobal['total'], 2, ',', '.') . "\n";
