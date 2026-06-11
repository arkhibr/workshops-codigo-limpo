<?php
// GABARITO 16 — SOLID na Prática (PHP 8.1+)
// Execute: php gabarito.php
//
// Quatro passos aplicados em sequência sobre o código original:
//   Passo 1: violações anotadas (// SRP: e // DIP:)
//   Passo 2: ValidadorFatura extraído; GeradorFatura recebe no construtor
//   Passo 3: CalculadorFatura e RepositorioFatura extraídos
//   Passo 4: interface INotificador; EmailSMTP substituído por injeção

class ItemFatura {
    public function __construct(
        public readonly string $descricao,
        public readonly float  $valor,
    ) {}
}

class Fatura {
    public string $status = 'pendente';

    public function __construct(
        public readonly string $id,
        public readonly string $clienteId,
        /** @var ItemFatura[] */
        public readonly array  $itens,
    ) {}
}

// ── Passo 4 — Interfaces (DIP) ───────────────────────────────────────────────

interface INotificador {
    public function notificar(string $destinatario, string $mensagem): void;
}

interface IRepositorioFatura {
    public function salvar(Fatura $fatura): void;
}

// ── Passo 2 — ValidadorFatura (SRP) ──────────────────────────────────────────

class ValidadorFatura {
    public function validar(Fatura $fatura): bool {
        return !empty($fatura->itens) && !empty($fatura->clienteId);
    }
}

// ── Passo 3 — CalculadorFatura + RepositorioFatura (SRP) ─────────────────────

class CalculadorFatura {
    public function calcularTotal(Fatura $fatura): float {
        return round(array_sum(array_map(fn(ItemFatura $i) => $i->valor, $fatura->itens)), 2);
    }
}

class RepositorioFatura implements IRepositorioFatura {
    public function salvar(Fatura $fatura): void {
        echo "  [BD] fatura {$fatura->id} salva ({$fatura->status})" . PHP_EOL;
    }
}

// ── Passo 4 — Implementação concreta de INotificador ─────────────────────────

class NotificadorEmail implements INotificador {
    public function notificar(string $destinatario, string $mensagem): void {
        echo "  [SMTP] → {$destinatario}: {$mensagem}" . PHP_EOL;
    }
}

// ── Passo 2–4 — GeradorFatura: orquestra, não executa (DIP + SRP) ────────────

readonly class GeradorFatura {
    public function __construct(
        private ValidadorFatura    $validador,
        private CalculadorFatura   $calculador,
        private IRepositorioFatura $repositorio,
        private INotificador       $notificador,
    ) {}

    public function processar(Fatura $fatura): float {
        if (!$this->validador->validar($fatura)) {
            throw new \InvalidArgumentException('Fatura inválida');
        }
        $total = $this->calculador->calcularTotal($fatura);
        $this->repositorio->salvar($fatura);
        $this->notificador->notificar($fatura->clienteId, "Fatura {$fatura->id}: R$" . number_format($total, 2));
        return $total;
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

$itens  = [new ItemFatura('Consultoria', 1500.0), new ItemFatura('Suporte', 300.0)];
$fatura = new Fatura('FAT-001', 'CLI-200', $itens);

$gerador = new GeradorFatura(
    new ValidadorFatura(),
    new CalculadorFatura(),
    new RepositorioFatura(),
    new NotificadorEmail(),
);

$total = $gerador->processar($fatura);
echo "Total: R$" . number_format($total, 2) . PHP_EOL;
echo "OK: SRP — ValidadorFatura, CalculadorFatura, RepositorioFatura separados" . PHP_EOL;
echo "OK: DIP — GeradorFatura recebe INotificador no construtor" . PHP_EOL;
