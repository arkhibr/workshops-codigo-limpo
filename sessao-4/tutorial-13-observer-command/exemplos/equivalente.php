<?php
/**
 * equivalente.php — Observer e Command em PHP 8.1
 * Execute: php equivalente.php
 */

// ─── Observer ─────────────────────────────────────────────────────────────────
interface ObservadorPedido {
    public function aoConfirmar(array $pedido): void;
    public function aoCancelar(array $pedido): void;
}

class NotificadorEmailPHP implements ObservadorPedido {
    public function aoConfirmar(array $pedido): void {
        echo "  [Email] confirmação → {$pedido['cliente_id']}: {$pedido['id']}\n";
    }
    public function aoCancelar(array $pedido): void {
        echo "  [Email] cancelamento → {$pedido['cliente_id']}: {$pedido['id']}\n";
    }
}

class GestorEstoquePHP implements ObservadorPedido {
    public function aoConfirmar(array $pedido): void {
        echo "  [Estoque] reservado: {$pedido['id']}\n";
    }
    public function aoCancelar(array $pedido): void {
        echo "  [Estoque] liberado: {$pedido['id']}\n";
    }
}

class GerenciadorPedidoPHP {
    /** @var ObservadorPedido[] */
    private array $observadores = [];

    public function registrarObservador(ObservadorPedido $obs): void {
        $this->observadores[] = $obs;
    }

    public function confirmar(array &$pedido): void {
        $pedido['status'] = 'confirmado';
        foreach ($this->observadores as $obs) {
            $obs->aoConfirmar($pedido);
        }
    }

    public function cancelar(array &$pedido): void {
        $pedido['status'] = 'cancelado';
        foreach ($this->observadores as $obs) {
            $obs->aoCancelar($pedido);
        }
    }
}

// ─── Command ──────────────────────────────────────────────────────────────────
interface Comando {
    public function executar(): void;
    public function desfazer(): void;
}

class ComandoCancelamentoPHP implements Comando {
    private ?string $statusAnterior = null;

    public function __construct(
        private array             &$pedido,
        private GerenciadorPedidoPHP $gerenciador
    ) {}

    public function executar(): void {
        $this->statusAnterior  = $this->pedido['status'];
        $this->gerenciador->cancelar($this->pedido);
        echo "  Valor estornado para {$this->pedido['cliente_id']}\n";
    }

    public function desfazer(): void {
        $this->pedido['status'] = $this->statusAnterior;
        echo "  Pedido {$this->pedido['id']} restaurado para '{$this->statusAnterior}'\n";
    }
}

class HistoricoComandosPHP {
    /** @var Comando[] */
    private array $historico = [];

    public function executar(Comando $cmd): void {
        $cmd->executar();
        $this->historico[] = $cmd;
    }

    public function desfazerUltimo(): void {
        if (empty($this->historico)) { echo "  Nada para desfazer\n"; return; }
        array_pop($this->historico)->desfazer();
    }
}

// ─── Demo ─────────────────────────────────────────────────────────────────────
echo "=== Observer + Command PHP 8.1 ===\n\n";

$pedido     = ['id' => 'PED-001', 'cliente_id' => 'CLI-100', 'status' => 'pendente'];
$gerenciador = new GerenciadorPedidoPHP();
$gerenciador->registrarObservador(new NotificadorEmailPHP());
$gerenciador->registrarObservador(new GestorEstoquePHP());
$gerenciador->confirmar($pedido);
assert($pedido['status'] === 'confirmado');
echo "OK: Observer — 2 observadores notificados\n";

$pedido2    = ['id' => 'PED-002', 'cliente_id' => 'CLI-200', 'status' => 'confirmado'];
$gerenciador2 = new GerenciadorPedidoPHP();
$historico  = new HistoricoComandosPHP();
$cmd        = new ComandoCancelamentoPHP($pedido2, $gerenciador2);
$historico->executar($cmd);
assert($pedido2['status'] === 'cancelado');
echo "OK: Command — cancelamento executado\n";

$historico->desfazerUltimo();
assert($pedido2['status'] === 'confirmado');
echo "OK: Command — desfazer restaurou status\n";
