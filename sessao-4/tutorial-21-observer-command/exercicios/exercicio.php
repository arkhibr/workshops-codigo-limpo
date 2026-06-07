<?php
/**
 * EXERCÍCIO 21 — Observer e Command em PHP 8.1
 * Tempo estimado: 20 minutos
 *
 * INSTRUÇÕES:
 *   O código abaixo tem dois problemas:
 *   1. ProcessadorPagamento::processar() conhece e chama 3 serviços diretamente
 *      (acoplamento). Adicionar notificação por SMS exige alterar processar().
 *   2. estornarPagamento() não tem undo — uma vez executado, não há como reverter.
 *
 *   1. Refatore para Observer: crie interface ObservadorPagamento com
 *      aoAprovar()/aoRecusar(), e ProcessadorPagamento com registrarObservador().
 *   2. Refatore para Command: crie ComandoEstorno com executar()/desfazer(),
 *      e HistoricoComandos.
 *   3. Execute: php exercicio.php (deve rodar antes e depois)
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

// ─── Serviços acoplados diretamente ──────────────────────────────────────────

class ServicoEmail {
    public function notificarAprovacao(string $clienteId, float $valor): void {
        echo "  [Email] → {$clienteId}: pagamento R$" . number_format($valor, 2, '.', '') . " aprovado\n";
    }
}

class ServicoAuditoria {
    public function registrar(string $evento, string $pagamentoId): void {
        echo "  [Auditoria] {$evento}: {$pagamentoId}\n";
    }
}

class ServicoFraude {
    public function marcarAprovado(string $pagamentoId): void {
        echo "  [Fraude] aprovado: {$pagamentoId}\n";
    }
}

// ─── Sem Observer: ProcessadorPagamento conhece os 3 serviços ────────────────

class ProcessadorPagamento {
    private ServicoEmail    $email;
    private ServicoAuditoria $auditoria;
    private ServicoFraude   $fraude;

    public function __construct() {
        $this->email     = new ServicoEmail();
        $this->auditoria = new ServicoAuditoria();
        $this->fraude    = new ServicoFraude();
    }

    public function processar(Pagamento $pagamento): void {
        $pagamento->status = 'aprovado';
        // Adicionar SMS exige alterar processar()
        $this->email->notificarAprovacao($pagamento->clienteId, $pagamento->valor);
        $this->auditoria->registrar('pagamento_aprovado', $pagamento->id);
        $this->fraude->marcarAprovado($pagamento->id);
    }
}

// ─── Sem Command: estornar sem undo ──────────────────────────────────────────

function estornarPagamento(Pagamento $pagamento): void {
    // Sem estado anterior. Sem histórico. Sem desfazer.
    $pagamento->status = 'estornado';
    echo "  Crédito de R$" . number_format($pagamento->valor, 2, '.', '') . " devolvido a {$pagamento->clienteId}\n";
    echo "  Pagamento {$pagamento->id} marcado como estornado\n";
}

// ─── Demo ─────────────────────────────────────────────────────────────────────
$pag  = new Pagamento('PAG-001', 500.0, 'CLI-100');
$proc = new ProcessadorPagamento();
$proc->processar($pag);
echo "Status: {$pag->status}\n\n";

estornarPagamento($pag);
echo "Status: {$pag->status}\n";
echo "(sem desfazer disponível)\n";
