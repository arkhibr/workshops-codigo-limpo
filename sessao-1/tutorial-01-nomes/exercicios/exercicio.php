<?php
/**
 * EXERCÍCIO 01 — Nomes Significativos
 * Tempo estimado: 10 minutos
 * Referência: Clean Code, Cap. 2
 *
 * INSTRUÇÕES:
 *   Renomeie todas as variáveis, parâmetros, funções e classes abaixo
 *   para que os nomes revelem claramente a intenção do código.
 *   Não altere a lógica — apenas os nomes.
 *
 * Execute: php exercicio.php
 */

// ─── Problema 1 ───────────────────────────────────────────────────────────────
// O que este código calcula? Renomeie para tornar óbvio.

$x = 86400;
$y = 7;
$z = $x * $y;

function calc(float $a, float $b): float {
    return $a * $b / 100;
}

// ─── Problema 2 ───────────────────────────────────────────────────────────────
// Esta classe gerencia um carrinho de compras.
// Renomeie tudo para refletir isso.

class Mgr {
    private array $lst = [];
    private int $cnt = 0;
    private float $ttl = 0.0;

    public function add(string $itm, float $prc): void {
        $this->lst[] = ['itm' => $itm, 'prc' => $prc];
        $this->cnt++;
        $this->ttl += $prc;
    }

    public function rmv(string $itm): void {
        $this->lst = array_filter($this->lst, fn($i) => $i['itm'] !== $itm);
        $this->lst = array_values($this->lst);
        $this->cnt = count($this->lst);
        $this->ttl = array_sum(array_column($this->lst, 'prc'));
    }

    public function gtAll(): array {
        return $this->lst;
    }

    public function gtTtl(): float {
        return $this->ttl;
    }
}

// ─── Problema 3 ───────────────────────────────────────────────────────────────
// Esta função verifica se um usuário pode acessar um recurso.
// Renomeie os parâmetros e a função.

function proc(array $u, string $r, bool $adm): bool {
    if ($adm) return true;
    return in_array($r, $u['prms'] ?? []);
}

// ─── Verificação (não altere este bloco) ──────────────────────────────────────

echo "=== Problema 1 ===\n";
echo "x={$x}, y={$y}, z={$z}\n";
echo "calc(200, 10) = " . calc(200, 10) . "\n";

echo "\n=== Problema 2 ===\n";
$m = new Mgr();
$m->add("Camiseta", 89.90);
$m->add("Calça", 159.90);
echo "Itens: " . json_encode($m->gtAll()) . "\n";
echo "Total: R$ " . number_format($m->gtTtl(), 2, ',', '.') . "\n";
$m->rmv("Camiseta");
echo "Após remover Camiseta: R$ " . number_format($m->gtTtl(), 2, ',', '.') . "\n";

echo "\n=== Problema 3 ===\n";
$usuario = ['nome' => 'João', 'prms' => ['leitura', 'escrita']];
echo "Acesso leitura: " . (proc($usuario, 'leitura', false) ? 'true' : 'false') . "\n";
echo "Acesso admin:   " . (proc($usuario, 'exclusao', true) ? 'true' : 'false') . "\n";
