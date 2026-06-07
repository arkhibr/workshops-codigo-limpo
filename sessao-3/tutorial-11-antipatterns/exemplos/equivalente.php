<?php
/**
 * equivalente.php — Anti-patterns Clássicos em PHP 8.1
 * Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3
 * Execute: php equivalente.php
 */

declare(strict_types=1);

// ============================================================================
// ❌ RUIM — God Object + Magic Strings/Numbers
// ============================================================================

class ClienteRuim
{
    public function __construct(
        public string $id,
        public string $nome,
        public string $email,
        public string $nivelFidelidade,
        public float  $historicoCompras = 0.0,
        public int    $pontosAcumulados = 0,
    ) {}
}

class ItemPedidoRuim
{
    public function __construct(
        public string $produtoId,
        public float  $preco,
        public int    $quantidade,
    ) {}
}

/**
 * God Object: CRUD, cálculo, notificação, relatório, cobrança — tudo em uma classe.
 */
class GestorPedidos
{
    public function buscarCliente(string $clienteId): ClienteRuim
    {
        echo "  [BD] buscar cliente {$clienteId}\n";
        return new ClienteRuim($clienteId, 'Empresa X', 'x@x.com', 'ouro', 5000.0, 200);
    }

    public function salvarCliente(ClienteRuim $cliente): void
    {
        echo "  [BD] salvar cliente {$cliente->id}\n";
    }

    public function validarCpf(string $cpf): bool
    {
        return strlen(str_replace(['.', '-'], '', $cpf)) === 11;
    }

    /** @param ItemPedidoRuim[] $itens */
    public function calcularTotal(array $itens): float
    {
        return array_sum(array_map(fn($i) => $i->preco * $i->quantidade, $itens));
    }

    public function aplicarDesconto(float $total, float $percentual): float
    {
        return round($total * (1 - $percentual), 2);
    }

    public function enviarEmail(string $email, string $assunto): void
    {
        echo "  [Email] → {$email}: {$assunto}\n";
    }

    public function gerarBoleto(float $valor, string $vencimento): string
    {
        return 'BOL-' . (int)$valor . '-' . $vencimento;
    }

    public function atualizarEstoque(string $produtoId, int $quantidade): void
    {
        echo "  [Estoque] {$produtoId}: -{$quantidade}\n";
    }

    public function gerarRelatorio(string $clienteId): string
    {
        return "Relatório do cliente {$clienteId}";
    }

    public function exportarCsv(array $dados): string
    {
        return "id,valor\n" . implode("\n", array_map('strval', $dados));
    }
}

/**
 * Magic Strings e Magic Numbers: sem nomes, sem contexto.
 */
function processarPorStatusRuim(string $status, string $tipo, float $valor, int $prazo): array
{
    $resultado = [];
    if ($status === 'A') {           // "A" = Ativo? Aprovado? Aberto?
        $resultado['ativo'] = true;
        if ($tipo === 'P') {         // "P" = Premium? Prioritário? Parcial?
            if ($valor > 1500) {     // por que 1500?
                $prazo = 30;         // 30 dias? horas? úteis?
            }
            $resultado['taxaExtra'] = $valor * 0.02;
        } elseif ($tipo === 'N') {
            $resultado['taxaExtra'] = 0.0;
        }
    } elseif ($status === 'I') {
        $resultado['ativo'] = false;
    }
    $resultado['prazo'] = $prazo;
    $resultado['tipo']  = $tipo;
    return $resultado;
}

// ============================================================================
// ✅ BOM — Responsabilidade única + Enums + Constantes nomeadas
// ============================================================================

enum NivelFidelidade: string
{
    case Bronze = 'bronze';
    case Prata  = 'prata';
    case Ouro   = 'ouro';
}

enum StatusPedido: string
{
    case Ativo   = 'ativo';
    case Inativo = 'inativo';
}

enum TipoPedido: string
{
    case Premium = 'premium';
    case Normal  = 'normal';
}

const LIMITE_FRETE_GRATIS  = 1500.0;
const PRAZO_PAGAMENTO_DIAS = 30;
const TAXA_PREMIUM         = 0.02;

class Cliente
{
    public function __construct(
        public string          $id,
        public string          $nome,
        public string          $email,
        public NivelFidelidade $nivelFidelidade,
        public float           $historicoCompras = 0.0,
        public int             $pontosAcumulados = 0,
        public string          $dataCadastro     = '2020-01-01',
    ) {}

    /** Feature Envy corrigido: método vive onde os dados vivem. */
    public function calcularDescontoFidelidade(): float
    {
        if ($this->nivelFidelidade === NivelFidelidade::Ouro) {
            $base  = $this->historicoCompras * 0.05;
            $bonus = $this->pontosAcumulados * 0.001;
            $anos  = (int)(new \DateTime())->format('Y') - (int)substr($this->dataCadastro, 0, 4);
            return min($base + $bonus + $anos * 2.0, 200.0);
        }
        if ($this->nivelFidelidade === NivelFidelidade::Prata) {
            return min($this->pontosAcumulados * 0.001, 50.0);
        }
        return 0.0;
    }
}

class ItemPedido
{
    public function __construct(
        public string $produtoId,
        public float  $preco,
        public int    $quantidade,
    ) {}
}

class RepositorioCliente
{
    public function buscar(string $clienteId): Cliente
    {
        echo "  [BD] buscar cliente {$clienteId}\n";
        return new Cliente($clienteId, 'Empresa X', 'x@x.com', NivelFidelidade::Ouro, 5000.0, 200);
    }

    public function salvar(Cliente $cliente): void
    {
        echo "  [BD] salvar cliente {$cliente->id}\n";
    }
}

class ValidadorDocumento
{
    public function validarCpf(string $cpf): bool
    {
        return strlen(str_replace(['.', '-'], '', $cpf)) === 11;
    }
}

class ServicoNotificacao
{
    public function enviarEmail(string $email, string $assunto): void
    {
        echo "  [Email] → {$email}: {$assunto}\n";
    }
}

class ServicoCobranca
{
    public function gerarBoleto(float $valor, string $vencimento): string
    {
        return 'BOL-' . (int)$valor . '-' . $vencimento;
    }
}

class GeradorRelatorio
{
    public function gerar(string $clienteId): string
    {
        return "Relatório do cliente {$clienteId}";
    }

    public function exportarCsv(array $dados): string
    {
        return "id,valor\n" . implode("\n", array_map('strval', $dados));
    }
}

function processarPorStatusBom(StatusPedido $status, TipoPedido $tipo, float $valor, int $prazo): array
{
    $resultado = [];
    if ($status === StatusPedido::Ativo) {
        $resultado['ativo'] = true;
        if ($tipo === TipoPedido::Premium && $valor > LIMITE_FRETE_GRATIS) {
            $prazo = PRAZO_PAGAMENTO_DIAS;
            $resultado['taxaExtra'] = round($valor * TAXA_PREMIUM, 2);
        } else {
            $resultado['taxaExtra'] = 0.0;
        }
    } else {
        $resultado['ativo'] = false;
    }
    $resultado['prazo'] = $prazo;
    $resultado['tipo']  = $tipo->value;
    return $resultado;
}

// ============================================================================
// Demo
// ============================================================================

echo "=== Anti-patterns — PHP 8.1 ===\n\n";

echo "❌ God Object:\n";
$gestor  = new GestorPedidos();
$metodos = array_filter(
    get_class_methods($gestor),
    fn($m) => !str_starts_with($m, '_')
);
echo "  GestorPedidos tem " . count($metodos) . " métodos públicos\n";

echo "\n✅ God Object corrigido:\n";
foreach ([RepositorioCliente::class, ValidadorDocumento::class, ServicoNotificacao::class,
          ServicoCobranca::class, GeradorRelatorio::class] as $classe) {
    $obj = new $classe();
    $qtd = count(array_filter(get_class_methods($obj), fn($m) => !str_starts_with($m, '_')));
    echo "  {$classe}: {$qtd} método(s)\n";
}

echo "\n❌ Magic Strings/Numbers:\n";
$r = processarPorStatusRuim('A', 'P', 2000.0, 15);
echo "  status='A', tipo='P' → prazo={$r['prazo']}, taxaExtra={$r['taxaExtra']}\n";

echo "\n✅ Enums e constantes:\n";
$r = processarPorStatusBom(StatusPedido::Ativo, TipoPedido::Premium, 2000.0, 15);
echo "  StatusPedido::Ativo, TipoPedido::Premium → prazo={$r['prazo']}, taxaExtra={$r['taxaExtra']}\n";

echo "\n✅ Feature Envy corrigido:\n";
$cliente  = new Cliente('CLI-100', 'X', 'x@x.com', NivelFidelidade::Ouro, 5000.0, 200);
$desconto = $cliente->calcularDescontoFidelidade();
echo "  Cliente::calcularDescontoFidelidade() → R$" . number_format($desconto, 2, '.', '') . "\n";
