<?php
/**
 * EQUIVALENTE PHP — Nomes Significativos
 * Referência: Clean Code, Cap. 2
 */

// ❌ Ruim
$d = 0;
$lst = [];
function get($l, $s) { return array_filter($l, fn($i) => $i[0] === $s); }

// ✅ Bom
$diasDesdemCriacao = 0;
$pedidos = [];
function filtrarPedidosPorStatus(array $pedidos, string $status): array {
    return array_filter($pedidos, fn($pedido) => $pedido['status'] === $status);
}

// ❌ Notação húngara (comum em código legado PHP)
$strNome  = "João";
$intIdade = 30;
$arrItens = [];

// ✅ Sem prefixos de tipo
$nome  = "João";
$idade = 30;
$itens = [];

// ❌ Classe com nome obscuro
class UsrMgr {
    public $lst = [];
    public function add($u) { $this->lst[] = $u; }
}

// ✅ Nome expressivo
class GerenciadorDeUsuarios {
    private array $usuarios = [];
    public function adicionarUsuario(array $usuario): void {
        $this->usuarios[] = $usuario;
    }
}
