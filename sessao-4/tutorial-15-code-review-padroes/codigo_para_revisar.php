<?php
/**
 * codigo_para_revisar.php — Módulo de cobrança. Revise em busca de padrões a melhorar.
 * Execute: php codigo_para_revisar.php
 */

declare(strict_types=1);

class Cliente
{
    public function __construct(
        public readonly string $id,
        public readonly string $nome,
        public readonly string $cpf,
        public readonly string $email,
        public readonly string $nivelFidelidade,   // "O", "P", "B"
        public readonly int    $pontos = 0,
        public readonly float  $historicoCompras = 0.0,
    ) {}
}

class Cobranca
{
    public string $status    = 'pendente';
    public string $vencimento = '';

    public function __construct(
        public readonly string $id,
        public readonly string $clienteId,
        public readonly float  $valor,
        public readonly string $tipo,              // "B", "P", "C"
    ) {}

    public function calcularDescontoFidelidade(Cliente $cliente): float
    {
        if ($cliente->nivelFidelidade === 'O') {
            $base  = $cliente->historicoCompras * 0.03;
            $bonus = $cliente->pontos * 0.002;
            return min($base + $bonus, 150.0);
        } elseif ($cliente->nivelFidelidade === 'P') {
            return min($cliente->pontos * 0.001, 50.0);
        }
        return 0.0;
    }
}

class SmtpEmailSender
{
    public function send(string $to, string $subject, string $body): void
    {
        echo "  [SMTP] → {$to}: {$subject}\n";
    }
}

class BancoDadosPostgres
{
    public function execute(string $sql, array $params): void
    {
        echo '  [PG] ' . substr($sql, 0, 40) . "...\n";
    }
}

class BoletoSimples
{
    public function __construct(
        public readonly string $numero,
        public readonly float  $valor,
        public readonly string $vencimento,
    ) {}

    public function validarVencimento(): bool
    {
        $partes = explode('-', $this->vencimento);
        if (count($partes) !== 3) {
            return false;
        }
        $dataVenc = mktime(0, 0, 0, (int)$partes[1], (int)$partes[2], (int)$partes[0]);
        return $dataVenc >= mktime(0, 0, 0, (int)date('m'), (int)date('d'), (int)date('Y'));
    }
}

class BoletoParcelado
{
    public function __construct(
        public readonly string $numero,
        public readonly float  $valorTotal,
        public readonly int    $numParcelas,
        public readonly string $vencimento,
    ) {}

    public function validarVencimento(): bool
    {
        $partes = explode('-', $this->vencimento);
        if (count($partes) !== 3) {
            return false;
        }
        $dataVenc = mktime(0, 0, 0, (int)$partes[1], (int)$partes[2], (int)$partes[0]);
        return $dataVenc >= mktime(0, 0, 0, (int)date('m'), (int)date('d'), (int)date('Y'));
    }

    public function valorParcela(): float
    {
        return round($this->valorTotal / $this->numParcelas, 2);
    }
}

class GestorCobranca
{
    private SmtpEmailSender    $notificador;
    private BancoDadosPostgres $banco;

    public function __construct()
    {
        $this->notificador = new SmtpEmailSender();
        $this->banco       = new BancoDadosPostgres();
    }

    public function validarCpf(string $cpf): bool
    {
        return strlen(str_replace(['.', '-'], '', $cpf)) === 11;
    }

    public function buscarCliente(string $clienteId): Cliente
    {
        echo "  buscando cliente {$clienteId}\n";
        return new Cliente($clienteId, 'Empresa Exemplo', '000.000.000-00',
                           'empresa@exemplo.com', 'O', pontos: 500, historicoCompras: 8000.0);
    }

    public function criarCobranca(string $clienteId, float $valor, string $tipo): Cobranca
    {
        $cob = new Cobranca("COB-{$clienteId}-001", $clienteId, $valor, $tipo);
        $this->banco->execute('INSERT INTO cobrancas VALUES (%s,%s,%s)',
                              [$cob->id, $cob->clienteId, $cob->valor]);
        return $cob;
    }

    public function calcularDesconto(Cobranca $cobranca, Cliente $cliente): float
    {
        return $cobranca->calcularDescontoFidelidade($cliente);
    }

    public function processarPagamento(Cobranca $cobranca): array
    {
        if ($cobranca->tipo === 'B') {
            $boleto = new BoletoSimples("BOL-{$cobranca->id}", $cobranca->valor, '2026-07-31');
            if (!$boleto->validarVencimento()) {
                throw new RuntimeException('Boleto vencido');
            }
            $resultado = ['metodo' => 'boleto', 'codigo' => $boleto->numero];
        } elseif ($cobranca->tipo === 'P') {
            $resultado = ['metodo' => 'pix', 'chave' => "chave-{$cobranca->clienteId}"];
        } elseif ($cobranca->tipo === 'C') {
            $resultado = ['metodo' => 'cartao', 'parcelas' => 1];
        } else {
            throw new RuntimeException("Tipo desconhecido: {$cobranca->tipo}");
        }
        return $resultado;
    }

    public function enviarEmail(Cliente $cliente, Cobranca $cobranca): void
    {
        $this->notificador->send(
            $cliente->email,
            "Cobrança {$cobranca->id}",
            sprintf('Valor: R$%.2f', $cobranca->valor)
        );
    }

    public function gerarBoleto(Cobranca $cobranca): string
    {
        return sprintf('BOL-%s-%.2f', $cobranca->id, $cobranca->valor);
    }

    public function arquivar(Cobranca $cobranca): void
    {
        $this->banco->execute("UPDATE cobrancas SET status='arquivado' WHERE id=%s",
                              [$cobranca->id]);
    }

    public function gerarRelatorio(string $clienteId): string
    {
        return "Relatório de cobranças: cliente {$clienteId}";
    }

    public function exportarCsv(string $clienteId): string
    {
        return "id,valor,status\nCOB-{$clienteId}-001,100.00,pendente";
    }

    public function atualizarStatus(string $cobrancaId, string $novoStatus): void
    {
        $this->banco->execute('UPDATE cobrancas SET status=%s WHERE id=%s',
                              [$novoStatus, $cobrancaId]);
    }

    public function reprocessarFalha(string $cobrancaId): bool
    {
        echo "  reprocessando {$cobrancaId}\n";
        return true;
    }

    public function consultarHistorico(string $clienteId): array
    {
        return [['id' => "COB-{$clienteId}-001", 'valor' => 100.0, 'status' => 'pago']];
    }
}

// --- Demo ---
echo "=== Módulo de Cobrança — revise em busca de padrões a melhorar ===\n\n";

$gestor   = new GestorCobranca();
$cliente  = $gestor->buscarCliente('CLI-100');
$cobranca = $gestor->criarCobranca('CLI-100', 500.0, 'B');
$desconto = $gestor->calcularDesconto($cobranca, $cliente);
printf("Desconto fidelidade: R$%.2f\n", $desconto);
$resultado = $gestor->processarPagamento($cobranca);
echo 'Pagamento: ' . json_encode($resultado) . "\n";
$gestor->enviarEmail($cliente, $cobranca);
echo "Relatório: " . $gestor->gerarRelatorio('CLI-100') . "\n";
