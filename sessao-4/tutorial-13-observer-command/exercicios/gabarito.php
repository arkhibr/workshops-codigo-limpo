<?php
/**
 * gabarito.php — Solução do Exercício 21: Observer e Command em PHP 8.1
 * Execute: php gabarito.php
 */

// ─── Modelo ───────────────────────────────────────────────────────────────────

class Pagamento {
    public string $status;
    public function __construct(
        public string $id,
        public float  $valor,
        public string $clienteId,
        string $status = 'pendente'
    ) {
        $this->status = $status;
    }
}

// ─── Observer ─────────────────────────────────────────────────────────────────

interface ObservadorPagamento {
    public function aoAprovar(Pagamento $pagamento): void;
    public function aoRecusar(Pagamento $pagamento): void;
}

class NotificadorEmailPag implements ObservadorPagamento {
    public function aoAprovar(Pagamento $pag): void {
        echo "  [Email] → {$pag->clienteId}: pagamento R$" . number_format($pag->valor, 2, '.', '') . " aprovado\n";
    }
    public function aoRecusar(Pagamento $pag): void {
        echo "  [Email] → {$pag->clienteId}: pagamento R$" . number_format($pag->valor, 2, '.', '') . " recusado\n";
    }
}

class AuditoriaPag implements ObservadorPagamento {
    public function aoAprovar(Pagamento $pag): void {
        echo "  [Auditoria] pagamento_aprovado: {$pag->id}\n";
    }
    public function aoRecusar(Pagamento $pag): void {
        echo "  [Auditoria] pagamento_recusado: {$pag->id}\n";
    }
}

class FraudePag implements ObservadorPagamento {
    public function aoAprovar(Pagamento $pag): void {
        echo "  [Fraude] aprovado: {$pag->id}\n";
    }
    public function aoRecusar(Pagamento $pag): void {
        echo "  [Fraude] recusado: {$pag->id}\n";
    }
}

class ProcessadorPagamento {
    /** @var ObservadorPagamento[] */
    private array $observadores = [];

    public function registrarObservador(ObservadorPagamento $obs): void {
        $this->observadores[] = $obs;
    }

    public function aprovar(Pagamento $pagamento): void {
        $pagamento->status = 'aprovado';
        foreach ($this->observadores as $obs) {
            $obs->aoAprovar($pagamento);
        }
    }

    public function recusar(Pagamento $pagamento): void {
        $pagamento->status = 'recusado';
        foreach ($this->observadores as $obs) {
            $obs->aoRecusar($pagamento);
        }
    }
}

// ─── Command ──────────────────────────────────────────────────────────────────

class ComandoEstorno {
    private ?string $statusAnterior = null;

    public function __construct(
        private Pagamento          $pagamento,
        private ProcessadorPagamento $processador
    ) {}

    public function executar(): void {
        $this->statusAnterior  = $this->pagamento->status;
        $this->pagamento->status = 'estornado';
        echo "  Crédito de R$" . number_format($this->pagamento->valor, 2, '.', '') . " devolvido a {$this->pagamento->clienteId}\n";
        echo "  Pagamento {$this->pagamento->id} marcado como estornado\n";
    }

    public function desfazer(): void {
        $this->pagamento->status = $this->statusAnterior;
        echo "  Pagamento {$this->pagamento->id} restaurado para '{$this->statusAnterior}'\n";
    }
}

class HistoricoComandos {
    /** @var ComandoEstorno[] */
    private array $historico = [];

    public function executar(ComandoEstorno $cmd): void {
        $cmd->executar();
        $this->historico[] = $cmd;
    }

    public function desfazerUltimo(): void {
        if (empty($this->historico)) {
            echo "  Nada para desfazer\n";
            return;
        }
        array_pop($this->historico)->desfazer();
    }
}

// ─── Verificação ──────────────────────────────────────────────────────────────

function verificarGabarito(): void {
    // Observer
    $pag  = new Pagamento('PAG-001', 500.0, 'CLI-100');
    $proc = new ProcessadorPagamento();
    $proc->registrarObservador(new NotificadorEmailPag());
    $proc->registrarObservador(new AuditoriaPag());
    $proc->registrarObservador(new FraudePag());

    $proc->aprovar($pag);
    assert($pag->status === 'aprovado');
    echo "OK: Observer — 3 observadores notificados em aprovar()\n";
    echo "OK: Observer — adicionar SMS não altera ProcessadorPagamento\n";

    // Command
    $historico = new HistoricoComandos();
    $cmd = new ComandoEstorno($pag, $proc);
    $historico->executar($cmd);
    assert($pag->status === 'estornado');
    echo "OK: Command — estorno executado\n";

    $historico->desfazerUltimo();
    assert($pag->status === 'aprovado');
    echo "OK: Command — estorno desfeito, pagamento restaurado para 'aprovado'\n";
}

echo "=== Gabarito 21 — Observer e Command: Pagamentos PHP 8.1 ===\n\n";
verificarGabarito();
