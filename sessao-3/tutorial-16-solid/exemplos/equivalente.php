<?php
// EQUIVALENTE PHP 8.1+ — SOLID na Prática
// Execute: php equivalente.php

// ============================================================
// Estrutura de dados compartilhada
// ============================================================

class ItemPedido {
    public function __construct(
        public readonly string $produtoId,
        public readonly string $descricao,
        public readonly float  $preco,
        public readonly int    $quantidade,
    ) {}
}

class Pedido {
    public string $status = 'pendente';

    public function __construct(
        public readonly string $id,
        public readonly string $clienteId,
        /** @var ItemPedido[] */
        public readonly array  $itens,
    ) {}

    public function confirmar(): void {
        $this->status = 'confirmado';
    }
}

// ============================================================
// ❌ Ruim — SRP + DIP violados
// ============================================================

class EmailSmtp {
    public function enviar(string $dest, string $msg): void {
        echo "  [Email] → {$dest}: " . substr($msg, 0, 40) . PHP_EOL;
    }
}

class BancoDadosSQLite {
    public function salvar(string $tabela, array $dados): void {
        echo "  [BD] salvo em {$tabela}: {$dados['id']}" . PHP_EOL;
    }
}

class GeradorRelatorioRuim {
    private EmailSmtp        $email;
    private BancoDadosSQLite $db;

    // DIP violation: instancia dependências concretas
    public function __construct() {
        $this->email = new EmailSmtp();
        $this->db    = new BancoDadosSQLite();
    }

    // SRP violation: valida pedido
    public function validarPedido(Pedido $pedido): bool {
        return !empty($pedido->itens) && !empty($pedido->clienteId);
    }

    // SRP violation: calcula total
    public function calcularTotal(Pedido $pedido): float {
        return array_sum(array_map(
            fn(ItemPedido $i) => $i->preco * $i->quantidade,
            $pedido->itens
        ));
    }

    // SRP violation: envia e-mail
    public function enviarConfirmacao(Pedido $pedido): void {
        $this->email->enviar($pedido->clienteId, "Pedido {$pedido->id} confirmado");
    }

    // SRP violation: persiste no banco
    public function salvarPedido(Pedido $pedido): void {
        $this->db->salvar('pedidos', ['id' => $pedido->id, 'status' => $pedido->status]);
    }

    // OCP violation: adicionar novo tipo exige alterar este método
    public function gerar(string $tipo, Pedido $pedido): string {
        $total = $this->calcularTotal($pedido);
        return match ($tipo) {
            'vendas'     => "Relatório Vendas | Pedido {$pedido->id} | Total: R$" . number_format($total, 2),
            'financeiro' => "Relatório Financeiro | Receita: R$" . number_format($total, 2),
            'estoque'    => "Relatório Estoque | " . count($pedido->itens) . " item(ns) movimentado(s)",
            default      => throw new \InvalidArgumentException("Tipo desconhecido: {$tipo}"),
        };
    }
}

// ============================================================
// ✅ Bom — SRP + DIP aplicados
// ============================================================

interface INotificador {
    public function notificar(string $destinatario, string $mensagem): void;
}

interface IRepositorioPedido {
    public function salvar(Pedido $pedido): void;
}

interface IFormatador {
    public function formatar(Pedido $pedido, float $total): string;
}

class ValidadorPedido {
    public function validar(Pedido $pedido): bool {
        return !empty($pedido->itens) && !empty($pedido->clienteId);
    }
}

class CalculadorTotal {
    public function calcular(Pedido $pedido): float {
        return round(array_sum(array_map(
            fn(ItemPedido $i) => $i->preco * $i->quantidade,
            $pedido->itens
        )), 2);
    }
}

class NotificadorEmail implements INotificador {
    public function notificar(string $destinatario, string $mensagem): void {
        echo "  [Email] → {$destinatario}: " . substr($mensagem, 0, 40) . PHP_EOL;
    }
}

class RepositorioPedido implements IRepositorioPedido {
    public function salvar(Pedido $pedido): void {
        echo "  [BD] salvo: {$pedido->id} ({$pedido->status})" . PHP_EOL;
    }
}

class FormatadorVendas implements IFormatador {
    public function formatar(Pedido $pedido, float $total): string {
        return "Relatório Vendas | Pedido {$pedido->id} | Total: R$" . number_format($total, 2);
    }
}

class FormatadorFinanceiro implements IFormatador {
    public function formatar(Pedido $pedido, float $total): string {
        return "Relatório Financeiro | Receita: R$" . number_format($total, 2);
    }
}

class FormatadorEstoque implements IFormatador {
    public function formatar(Pedido $pedido, float $total): string {
        return "Relatório Estoque | " . count($pedido->itens) . " item(ns) movimentado(s)";
    }
}

// DIP aplicado: GeradorRelatorio recebe abstrações via construtor
readonly class GeradorRelatorio {
    public function __construct(
        private IRepositorioPedido $repo,
        private INotificador       $notificador,
        private IFormatador        $formatador,
        private CalculadorTotal    $calculador,
    ) {}

    public function processar(Pedido $pedido): string {
        $total = $this->calculador->calcular($pedido);
        $this->repo->salvar($pedido);
        $this->notificador->notificar($pedido->clienteId, "Pedido {$pedido->id} salvo");
        return $this->formatador->formatar($pedido, $total);
    }
}

// ============================================================
// Demo
// ============================================================

$itens  = [new ItemPedido('P001', 'Webcam HD', 299.90, 1)];
$pedido = new Pedido('PED-001', 'CLI-100', $itens);

echo "=== PHP 8.1 — SOLID na Prática ===" . PHP_EOL . PHP_EOL;

echo "❌ Ruim (SRP+DIP violados):" . PHP_EOL;
$geradorRuim = new GeradorRelatorioRuim();
$geradorRuim->salvarPedido($pedido);
$geradorRuim->enviarConfirmacao($pedido);
echo $geradorRuim->gerar('vendas', $pedido) . PHP_EOL;

echo PHP_EOL . "✅ Bom (SRP+DIP aplicados):" . PHP_EOL;
$formatadores = [
    ['vendas',     new FormatadorVendas()],
    ['financeiro', new FormatadorFinanceiro()],
    ['estoque',    new FormatadorEstoque()],
];
foreach ($formatadores as [$tipo, $fmt]) {
    $gerador   = new GeradorRelatorio(new RepositorioPedido(), new NotificadorEmail(), $fmt, new CalculadorTotal());
    $resultado = $gerador->processar($pedido);
    echo "  [{$tipo}] {$resultado}" . PHP_EOL;
}

/*
 * Nota ADVPL/TLPP:
 * Interfaces não existem em AdvPL clássico. TLPP 4.0+ tem classes e herança,
 * mas sem interfaces formais — use protocolos implícitos por convenção de
 * nomenclatura. Para DIP, simule injeção via codeblocks:
 *   bNotificador := {|cId, cMsg| NotificarCliente(cId, cMsg)}
 *   Eval(bNotificador, "CLI-100", "pedido confirmado")
 */
