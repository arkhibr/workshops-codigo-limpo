<?php
/**
 * GABARITO 02 — Funções
 * Abra este arquivo apenas após tentar o exercício por conta própria.
 */

// ─── Solução 1: Quebrar função grande em responsabilidades únicas ─────────────

const ALIQUOTA_INSS = 0.275;

function calcularSalarioLiquido(float $salarioBruto): float {
    return $salarioBruto * (1 - ALIQUOTA_INSS);
}

function calcularBonus(float $salarioBruto): float {
    if ($salarioBruto > 5000) {
        return $salarioBruto * 0.10;
    }
    return $salarioBruto * 0.05;
}

function calcularRemuneracaoTotal(float $salarioBruto): array {
    $liquido = calcularSalarioLiquido($salarioBruto);
    $bonus   = calcularBonus($salarioBruto);
    return [$liquido, $bonus, $liquido + $bonus];
}

function formatarLinhaResumida(array $funcionario, float $total): string {
    return "{$funcionario['nome']}: R$" . number_format($total, 2, ',', '.');
}

function formatarLinhaDetalhada(array $funcionario, float $salarioLiquido, float $bonus, float $total): string {
    return "Nome: {$funcionario['nome']}" .
           " | Salário bruto: R$" . number_format($funcionario['salario'], 2, ',', '.') .
           " | Líquido: R$"       . number_format($salarioLiquido, 2, ',', '.') .
           " | Bônus: R$"         . number_format($bonus, 2, ',', '.') .
           " | Total: R$"         . number_format($total, 2, ',', '.');
}

function formatarLinhaFuncionario(array $funcionario, string $formato): string {
    [$liquido, $bonus, $total] = calcularRemuneracaoTotal($funcionario['salario']);
    if ($formato === 'resumido') {
        return formatarLinhaResumida($funcionario, $total);
    }
    return formatarLinhaDetalhada($funcionario, $liquido, $bonus, $total);
}

function filtrarFuncionarios(array $funcionarios, bool $incluirInativos): array {
    if ($incluirInativos) {
        return $funcionarios;
    }
    return array_values(array_filter($funcionarios, fn($f) => $f['ativo']));
}

function gerarRelatorio(array $funcionarios, bool $incluirInativos, string $formato): array {
    $selecionados = filtrarFuncionarios($funcionarios, $incluirInativos);
    return array_map(fn($f) => formatarLinhaFuncionario($f, $formato), $selecionados);
}

// ─── Solução 2: Duas funções em vez de flag booleana ─────────────────────────

function enviarNotificacaoNormal(array $usuario, string $mensagem): void {
    echo "Para: {$usuario['email']} | {$mensagem}\n";
}

function enviarNotificacaoUrgente(array $usuario, string $mensagem): void {
    echo "[URGENTE] Para: {$usuario['email']} | {$mensagem}\n";
}

// ─── Solução 3: Efeito colateral explícito no retorno ────────────────────────

function adicionarProdutoAoCarrinho(array $carrinho, string $nome, float $preco, int $quantidade): array {
    $subtotal    = $preco * $quantidade;
    $novosItens  = $carrinho['itens'];
    $novosItens[] = ['nome' => $nome, 'preco' => $preco, 'quantidade' => $quantidade];
    return [
        'itens' => $novosItens,
        'total' => $carrinho['total'] + $subtotal,
    ];
}

// ─── Verificação ──────────────────────────────────────────────────────────────

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
enviarNotificacaoNormal($usuario, 'Reunião amanhã às 9h');
enviarNotificacaoUrgente($usuario, 'Servidor fora do ar!');

echo "\n=== Carrinho (sem estado global) ===\n";
$carrinho = ['itens' => [], 'total' => 0.0];
$carrinho = adicionarProdutoAoCarrinho($carrinho, 'Teclado', 250.0, 1);
$carrinho = adicionarProdutoAoCarrinho($carrinho, 'Mouse', 80.0, 2);
echo "Total no carrinho: R$ " . number_format($carrinho['total'], 2, ',', '.') . "\n";
