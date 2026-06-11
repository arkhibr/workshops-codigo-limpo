<?php
// EQUIVALENTE PHP 8.1+ — SOLID na Prática
// Execute: php equivalente.php

// ============================================================
// DOMÍNIO COMPARTILHADO
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
        public readonly array $itens,
    ) {}

    public function confirmar(): void {
        $this->status = 'confirmado';
    }
}

// ============================================================
// ❌ Ruim — SRP + DIP + OCP violados (para referência)
// ============================================================

class EmailSmtp {
    public function enviar(string $dest, string $msg): void {
        echo "  [Email] → {$dest}: " . substr($msg, 0, 50) . PHP_EOL;
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
// S — SRP: interfaces e classes com responsabilidade única
// ============================================================

interface INotificador {
    public function notificar(string $destinatario, string $mensagem): void;
}

interface IRepositorioPedido {
    public function salvar(Pedido $pedido): void;
    public function buscar(string $pedidoId): ?array;
}

interface IFormatador {
    public function formatar(Pedido $pedido, float $total): string;
}

class ValidadorPedido {
    public function validar(Pedido $pedido): bool {
        if (empty($pedido->itens)) {
            echo "  [Validação] Pedido {$pedido->id}: sem itens" . PHP_EOL;
            return false;
        }
        if (empty($pedido->clienteId)) {
            echo "  [Validação] Pedido {$pedido->id}: cliente ausente" . PHP_EOL;
            return false;
        }
        foreach ($pedido->itens as $item) {
            if ($item->preco <= 0 || $item->quantidade <= 0) {
                echo "  [Validação] Pedido {$pedido->id}: item inválido ({$item->descricao})" . PHP_EOL;
                return false;
            }
        }
        return true;
    }
}

class CalculadorTotal {
    private const TAXA_IMPOSTO = 0.10;

    public function calcular(Pedido $pedido): float {
        $subtotal = array_sum(array_map(
            fn(ItemPedido $i) => $i->preco * $i->quantidade,
            $pedido->itens
        ));
        return round($subtotal * (1 + self::TAXA_IMPOSTO), 2);
    }

    public function calcularSubtotal(Pedido $pedido): float {
        return round(array_sum(array_map(
            fn(ItemPedido $i) => $i->preco * $i->quantidade,
            $pedido->itens
        )), 2);
    }

    public function calcularImposto(Pedido $pedido): float {
        $subtotal = array_sum(array_map(
            fn(ItemPedido $i) => $i->preco * $i->quantidade,
            $pedido->itens
        ));
        return round($subtotal * self::TAXA_IMPOSTO, 2);
    }
}

class NotificadorEmail implements INotificador {
    public function notificar(string $destinatario, string $mensagem): void {
        echo "  [Email] → {$destinatario}: {$mensagem}" . PHP_EOL;
    }
}

class NotificadorLog implements INotificador {
    // Alternativa sem SMTP — mesma interface, zero alteração no chamador
    public function notificar(string $destinatario, string $mensagem): void {
        echo "  [Log] {$destinatario}: {$mensagem}" . PHP_EOL;
    }
}

class RepositorioPedido implements IRepositorioPedido {
    private array $dados = [];

    public function salvar(Pedido $pedido): void {
        $this->dados[$pedido->id] = [
            'id'      => $pedido->id,
            'status'  => $pedido->status,
            'cliente' => $pedido->clienteId,
            'itens'   => count($pedido->itens),
        ];
        echo "  [BD] salvo: {$pedido->id} → {$pedido->status}" . PHP_EOL;
    }

    public function buscar(string $pedidoId): ?array {
        return $this->dados[$pedidoId] ?? null;
    }
}

class RepositorioEmMemoria implements IRepositorioPedido {
    private array $dados = [];

    public function salvar(Pedido $pedido): void {
        $this->dados[$pedido->id] = ['id' => $pedido->id, 'status' => $pedido->status];
        echo "  [Mem] salvo: {$pedido->id} → {$pedido->status}" . PHP_EOL;
    }

    public function buscar(string $pedidoId): ?array {
        return $this->dados[$pedidoId] ?? null;
    }
}

// ============================================================
// O — OCP: novos formatadores sem alterar GeradorRelatorio
// ============================================================

class FormatadorVendas implements IFormatador {
    public function formatar(Pedido $pedido, float $total): string {
        $itens = implode(', ', array_map(
            fn(ItemPedido $i) => "{$i->descricao} x{$i->quantidade}",
            $pedido->itens
        ));
        return "[Vendas] Pedido {$pedido->id} | {$itens} | Total: R$" . number_format($total, 2);
    }
}

class FormatadorFinanceiro implements IFormatador {
    public function formatar(Pedido $pedido, float $total): string {
        $calc     = new CalculadorTotal();
        $subtotal = $calc->calcularSubtotal($pedido);
        $imposto  = $calc->calcularImposto($pedido);
        return "[Financeiro] Pedido {$pedido->id} | Subtotal: R$" . number_format($subtotal, 2)
             . " | Imposto: R$" . number_format($imposto, 2)
             . " | Total: R$" . number_format($total, 2);
    }
}

class FormatadorEstoque implements IFormatador {
    public function formatar(Pedido $pedido, float $total): string {
        $linhas = array_map(
            fn(ItemPedido $i) => "  • {$i->descricao} (ref: {$i->produtoId}): {$i->quantidade} un",
            $pedido->itens
        );
        return "[Estoque] Pedido {$pedido->id} — movimentação:\n" . implode("\n", $linhas);
    }
}

class FormatadorNFe implements IFormatador {
    // Adicionado sem nenhuma alteração em GeradorRelatorio — OCP respeitado
    public function formatar(Pedido $pedido, float $total): string {
        return "[NF-e] DANFE | Dest: {$pedido->clienteId} | Nr: {$pedido->id} | Valor: R$" . number_format($total, 2);
    }
}

// ============================================================
// L — LSP: subtipos honram o contrato da base
// ============================================================

class PedidoAmostra extends Pedido {
    public function calcularTotalEspecial(): float {
        return 0.0;  // amostras têm custo zero para o cliente
    }
    // confirmar() herdado sem alteração — contrato mantido
}

class PedidoPrioritario extends Pedido {
    public function __construct(
        string $id,
        string $clienteId,
        array  $itens,
        public readonly int $prioridade = 1,
    ) {
        parent::__construct($id, $clienteId, $itens);
    }

    public function confirmar(): void {
        parent::confirmar();  // honra o contrato base
        echo "  [Fila] Pedido {$this->id} inserido com prioridade {$this->prioridade}" . PHP_EOL;
    }
}

function confirmarEExibir(Pedido $pedido): void {
    $pedido->confirmar();
    assert($pedido->status === 'confirmado', 'Contrato violado: status deve ser confirmado');
    echo "  " . get_class($pedido) . " {$pedido->id} → status: {$pedido->status}" . PHP_EOL;
}

// ============================================================
// I — ISP: interfaces pequenas e coesas
// ============================================================

interface IValidavel {
    public function validar(): bool;
}

interface ICalculavel {
    public function calcular(): float;
}

interface IArquivavel {
    public function arquivar(): void;
    public function exportarCsv(): string;
}

interface IExportavelPDF {
    public function exportarPdf(): string;
}

class ProcessadorSimples implements IValidavel, ICalculavel {
    // Só precisa de validar e calcular — sem métodos mortos
    public function __construct(private readonly Pedido $pedido) {}

    public function validar(): bool {
        return !empty($this->pedido->itens) && !empty($this->pedido->clienteId);
    }

    public function calcular(): float {
        return round(array_sum(array_map(
            fn(ItemPedido $i) => $i->preco * $i->quantidade,
            $this->pedido->itens
        )), 2);
    }
}

class ProcessadorCompleto implements IValidavel, ICalculavel, IArquivavel, IExportavelPDF {
    public function __construct(private readonly Pedido $pedido) {}

    public function validar(): bool {
        return !empty($this->pedido->itens) && !empty($this->pedido->clienteId);
    }

    public function calcular(): float {
        return round(array_sum(array_map(
            fn(ItemPedido $i) => $i->preco * $i->quantidade,
            $this->pedido->itens
        )), 2);
    }

    public function arquivar(): void {
        echo "  [Arquivo] Pedido {$this->pedido->id} arquivado em storage frio" . PHP_EOL;
    }

    public function exportarCsv(): string {
        $linhas = ['produto_id,descricao,preco,quantidade'];
        foreach ($this->pedido->itens as $i) {
            $linhas[] = "{$i->produtoId},{$i->descricao},{$i->preco},{$i->quantidade}";
        }
        return implode("\n", $linhas);
    }

    public function exportarPdf(): string {
        $linhas = ["PEDIDO {$this->pedido->id}", "Cliente: {$this->pedido->clienteId}"];
        foreach ($this->pedido->itens as $i) {
            $linhas[] = "  {$i->descricao}: {$i->quantidade} x R$" . number_format($i->preco, 2);
        }
        return implode("\n", $linhas);
    }
}

// ============================================================
// D — DIP: GeradorRelatorio recebe abstrações via construtor
// ============================================================

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
        $this->notificador->notificar(
            $pedido->clienteId,
            "Pedido {$pedido->id} processado. Total: R$" . number_format($total, 2)
        );
        return $this->formatador->formatar($pedido, $total);
    }
}

// ============================================================
// DEMONSTRAÇÃO
// ============================================================

$itens  = [
    new ItemPedido('P001', 'Webcam HD',  299.90, 1),
    new ItemPedido('P002', 'Cabo USB-C',  49.90, 2),
];
$pedido = new Pedido('PED-001', 'CLI-100', $itens);

echo "=== PHP 8.1 — SOLID na Prática ===" . PHP_EOL . PHP_EOL;

// ── S — SRP ──────────────────────────────────────────────────
echo "── S — SRP: cada classe tem uma responsabilidade ──────" . PHP_EOL;
$validador  = new ValidadorPedido();
$calculador = new CalculadorTotal();
$repoReal   = new RepositorioPedido();
$notifEmail = new NotificadorEmail();
echo "  Válido: " . ($validador->validar($pedido) ? 'sim' : 'não') . PHP_EOL;
echo "  Subtotal: R$" . number_format($calculador->calcularSubtotal($pedido), 2) . PHP_EOL;
echo "  Imposto:  R$" . number_format($calculador->calcularImposto($pedido), 2) . PHP_EOL;
echo "  Total:    R$" . number_format($calculador->calcular($pedido), 2) . PHP_EOL;
$repoReal->salvar($pedido);
$notifEmail->notificar($pedido->clienteId, "Pedido {$pedido->id} registrado");

// ── O — OCP ──────────────────────────────────────────────────
echo PHP_EOL . "── O — OCP: novos formatadores sem alterar GeradorRelatorio ──" . PHP_EOL;
$formatadores = [
    ['vendas',     new FormatadorVendas()],
    ['financeiro', new FormatadorFinanceiro()],
    ['estoque',    new FormatadorEstoque()],
    ['nfe',        new FormatadorNFe()],
];
foreach ($formatadores as [$nome, $fmt]) {
    $gerador = new GeradorRelatorio(new RepositorioEmMemoria(), new NotificadorLog(), $fmt, new CalculadorTotal());
    echo PHP_EOL . "  [{$nome}] " . $gerador->processar($pedido) . PHP_EOL;
}

// ── L — LSP ──────────────────────────────────────────────────
echo PHP_EOL . "── L — LSP: todos os subtipos honram o contrato de Pedido ──" . PHP_EOL;
$casos = [
    new Pedido('PED-002', 'CLI-200', $itens),
    new PedidoAmostra('PED-003', 'CLI-300', $itens),
    new PedidoPrioritario('PED-004', 'CLI-400', $itens, prioridade: 3),
];
foreach ($casos as $p) {
    confirmarEExibir($p);
}

// ── I — ISP ──────────────────────────────────────────────────
echo PHP_EOL . "── I — ISP: ProcessadorSimples usa 2 interfaces, sem métodos mortos ──" . PHP_EOL;
$simples = new ProcessadorSimples($pedido);
echo "  validar=" . ($simples->validar() ? 'true' : 'false')
   . ", calcular=R$" . number_format($simples->calcular(), 2) . PHP_EOL;

$completo = new ProcessadorCompleto($pedido);
$completo->arquivar();
echo "  CSV:\n" . $completo->exportarCsv() . PHP_EOL;
echo "  PDF:\n" . $completo->exportarPdf() . PHP_EOL;

// ── D — DIP ──────────────────────────────────────────────────
echo PHP_EOL . "── D — DIP: trocar Email por Log sem alterar GeradorRelatorio ──" . PHP_EOL;
$geradorProd  = new GeradorRelatorio($repoReal,               $notifEmail,           new FormatadorVendas(), new CalculadorTotal());
$geradorTeste = new GeradorRelatorio(new RepositorioEmMemoria(), new NotificadorLog(), new FormatadorVendas(), new CalculadorTotal());
echo "  [Produção]: "     . $geradorProd->processar($pedido) . PHP_EOL;
echo "  [Teste/mock]: "   . $geradorTeste->processar($pedido) . PHP_EOL;
