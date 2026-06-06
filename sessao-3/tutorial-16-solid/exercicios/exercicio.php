<?php
// EXERCÍCIO 16 — SOLID na Prática (PHP 8.1+)
// Execute: php exercicio.php
//
// INSTRUÇÕES:
//   A classe GeradorFatura abaixo viola SRP (valida, calcula, persiste e envia
//   email) e DIP (instancia EmailSMTP diretamente).
//
//   1. Separe em classes com responsabilidade única.
//   2. Inverta a dependência de email: GeradorFatura deve receber um INotificador.
//   3. Execute: php exercicio.php (deve rodar antes e depois da refatoração)

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

class EmailSMTP {
    public function enviar(string $dest, string $msg): void {
        echo "  [SMTP] → {$dest}: {$msg}" . PHP_EOL;
    }
}

class GeradorFatura {
    private EmailSMTP $email;

    // DIP violation: instancia dependência concreta
    public function __construct() {
        $this->email = new EmailSMTP();
    }

    // SRP violation: valida fatura
    public function validar(Fatura $fatura): bool {
        return !empty($fatura->itens) && !empty($fatura->clienteId);
    }

    // SRP violation: calcula total
    public function calcularTotal(Fatura $fatura): float {
        return array_sum(array_map(fn(ItemFatura $i) => $i->valor, $fatura->itens));
    }

    // SRP violation: persiste no banco
    public function salvar(Fatura $fatura): void {
        echo "  [BD] fatura {$fatura->id} salva" . PHP_EOL;
    }

    public function processar(Fatura $fatura): float {
        if (!$this->validar($fatura)) {
            throw new \InvalidArgumentException('Fatura inválida');
        }
        $total = $this->calcularTotal($fatura);
        $this->salvar($fatura);
        $this->email->enviar($fatura->clienteId, "Fatura {$fatura->id}: R$" . number_format($total, 2));
        return $total;
    }
}

// Demo
$itens   = [new ItemFatura('Consultoria', 1500.0), new ItemFatura('Suporte', 300.0)];
$fatura  = new Fatura('FAT-001', 'CLI-200', $itens);
$gerador = new GeradorFatura();
$total   = $gerador->processar($fatura);
echo "Total: R$" . number_format($total, 2) . PHP_EOL;
