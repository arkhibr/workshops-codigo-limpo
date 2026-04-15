<?php
/**
 * GABARITO 01 — Nomes Significativos
 * Abra este arquivo apenas após tentar o exercício por conta própria.
 */

// ─── Solução 1 ────────────────────────────────────────────────────────────────

const SEGUNDOS_POR_DIA    = 86400;
const DIAS_POR_SEMANA     = 7;
const SEGUNDOS_POR_SEMANA = SEGUNDOS_POR_DIA * DIAS_POR_SEMANA;

function calcularDesconto(float $preco, float $percentual): float {
    return $preco * $percentual / 100;
}

// ─── Solução 2 ────────────────────────────────────────────────────────────────

class CarrinhoDeCompras {
    private array $itens     = [];
    private int   $quantidade = 0;
    private float $total      = 0.0;

    public function adicionarItem(string $nomeProduto, float $preco): void {
        $this->itens[]   = ['produto' => $nomeProduto, 'preco' => $preco];
        $this->quantidade++;
        $this->total     += $preco;
    }

    public function removerItem(string $nomeProduto): void {
        $this->itens     = array_filter($this->itens, fn($i) => $i['produto'] !== $nomeProduto);
        $this->itens     = array_values($this->itens);
        $this->quantidade = count($this->itens);
        $this->total      = array_sum(array_column($this->itens, 'preco'));
    }

    public function listarItens(): array {
        return $this->itens;
    }

    public function obterTotal(): float {
        return $this->total;
    }
}

// ─── Solução 3 ────────────────────────────────────────────────────────────────

function usuarioTemAcessoAoRecurso(array $usuario, string $recurso, bool $ehAdministrador): bool {
    if ($ehAdministrador) return true;
    return in_array($recurso, $usuario['permissoes'] ?? []);
}

// ─── Verificação ──────────────────────────────────────────────────────────────

echo "=== Solução 1 ===\n";
echo "Segundos por semana: " . SEGUNDOS_POR_SEMANA . "\n";
echo "Desconto de 10% em R$200: R$ " . number_format(calcularDesconto(200, 10), 2, ',', '.') . "\n";

echo "\n=== Solução 2 ===\n";
$carrinho = new CarrinhoDeCompras();
$carrinho->adicionarItem("Camiseta", 89.90);
$carrinho->adicionarItem("Calça", 159.90);
echo "Itens: " . json_encode($carrinho->listarItens()) . "\n";
echo "Total: R$ " . number_format($carrinho->obterTotal(), 2, ',', '.') . "\n";
$carrinho->removerItem("Camiseta");
echo "Após remover Camiseta: R$ " . number_format($carrinho->obterTotal(), 2, ',', '.') . "\n";

echo "\n=== Solução 3 ===\n";
$usuario = ['nome' => 'João', 'permissoes' => ['leitura', 'escrita']];
echo "Acesso leitura: " . (usuarioTemAcessoAoRecurso($usuario, 'leitura', false) ? 'true' : 'false') . "\n";
echo "Acesso admin:   " . (usuarioTemAcessoAoRecurso($usuario, 'exclusao', true) ? 'true' : 'false') . "\n";
