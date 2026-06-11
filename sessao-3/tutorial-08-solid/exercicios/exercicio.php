<?php
// EXERCÍCIO 16 — SOLID na Prática (PHP 8.1+)
// Execute: php exercicio.php
//
// PASSOS (faça um de cada vez, em ordem):
//
//   PASSO 1 — IDENTIFICAR (5 min)
//     Leia GeradorFatura e adicione comentários // SRP: e // DIP: antes de
//     cada trecho problemático.
//     Meta: encontrar pelo menos 4 violações antes de alterar código.
//
//   PASSO 2 — EXTRAIR ValidadorFatura (8 min)
//     Mova validar() para uma nova classe ValidadorFatura.
//     GeradorFatura passa a receber ValidadorFatura no construtor.
//     Verifique que o demo ainda roda: php exercicio.php
//
//   PASSO 3 — EXTRAIR CalculadorFatura + RepositorioFatura (8 min)
//     Repita para calcularTotal() e salvar().
//     GeradorFatura::processar() delega para os colaboradores injetados.
//     Verifique que o demo ainda roda: php exercicio.php
//
//   PASSO 4 — INVERTER DEPENDÊNCIA DE EMAIL (8 min)
//     Crie interface INotificador com notificar(string $dest, string $msg): void
//     Substitua new EmailSMTP() por injeção no construtor.
//     Verifique que o demo ainda roda: php exercicio.php

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

// -----------------------------------------------------------------------
// PASSO 4 — stub para verificar a injeção de dependência.
// Após criar INotificador, descomente e rode php exercicio.php.
// -----------------------------------------------------------------------
// class NotificadorLog implements INotificador {
//     public bool $chamado = false;
//     public function notificar(string $dest, string $msg): void {
//         $this->chamado = true;
//     }
// }
//
// $notifLog = new NotificadorLog();
// $gerador2 = new GeradorFatura(
//     new ValidadorFatura(), new CalculadorFatura(), new RepositorioFatura(), $notifLog
// );
// $gerador2->processar($fatura);
// assert($notifLog->chamado, 'FALHOU: notificador substituto não foi chamado');
// echo 'OK: DIP — GeradorFatura aceita qualquer INotificador' . PHP_EOL;
