<?php
/**
 * equivalente.php — Idiom Patterns em PHP 8.1
 * Execute: php equivalente.php
 */

// ─── Ruim: __construct manual sem validation, strings de status soltas ────────
class ItemVendaRuim {
    public string $produtoId;
    public string $descricao;
    public float  $precoUnitario;
    public int    $quantidade;
    public int    $mes;

    public function __construct(string $id, string $desc, float $preco, int $qtd, int $mes) {
        // sem validação
        $this->produtoId     = $id;
        $this->descricao     = $desc;
        $this->precoUnitario = $preco;
        $this->quantidade    = $qtd;
        $this->mes           = $mes;
    }
}

function calcularDescontoRuim(string $status, float $valor): float {
    if ($status === 'ativo')     return $valor * 0.10;
    if ($status === 'premium')   return $valor * 0.20;
    if ($status === 'inativo')   return 0.0;
    return 0.0;
}

// ─── Bom: readonly class + constructor property promotion ─────────────────────
class ItemVenda {
    public function __construct(
        public readonly string $produtoId,
        public readonly string $descricao,
        public readonly float  $precoUnitario,
        public readonly int    $quantidade,
        public readonly int    $mes
    ) {
        if ($precoUnitario <= 0) {
            throw new \InvalidArgumentException("precoUnitario deve ser positivo: $precoUnitario");
        }
    }
}

// ─── Bom: enum com método ─────────────────────────────────────────────────────
enum StatusVenda: string {
    case Ativo   = 'ativo';
    case Premium = 'premium';
    case Inativo = 'inativo';

    public function desconto(float $valor): float {
        return match($this) {
            self::Ativo   => $valor * 0.10,
            self::Premium => $valor * 0.20,
            self::Inativo => 0.0,
        };
    }
}

// ─── Bom: named arguments ────────────────────────────────────────────────────
// Sem named arguments: ItemVenda("P001", "Webcam", 299.90, 2, 6) — posição importa
// Com named arguments: mais legível e à prova de reordenação de parâmetros
function criarItemComNamed(): ItemVenda {
    return new ItemVenda(
        produtoId:      "P001",
        descricao:      "Webcam HD",
        precoUnitario:  299.90,
        quantidade:     2,
        mes:            6
    );
}

// ─── Demo ─────────────────────────────────────────────────────────────────────
echo "=== Idioms PHP 8.1 ===\n\n";

$item = criarItemComNamed();
assert($item->precoUnitario === 299.90);
echo "OK: readonly class — ItemVenda com named arguments\n";

try {
    new ItemVenda("P999", "Inválido", -1.0, 1, 6);
    echo "FALHOU: deveria rejeitar preco negativo\n";
} catch (\InvalidArgumentException $e) {
    echo "OK: readonly class — rejeita preco negativo\n";
}

$status = StatusVenda::Premium;
$desc   = $status->desconto(1000.0);
assert($desc === 200.0);
echo "OK: enum + match — Premium desconta R$" . number_format($desc, 2) . "\n";
