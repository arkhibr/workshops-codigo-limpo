<?php
// GABARITO 18 PHP — Padrões Estruturais: Adapter + Facade
// Execute: php gabarito.php

// ─── API legada (não pode ser alterada) ───────────────────────────────────────

function gerar_boleto_legado(float $nValor, string $cVencimento, string $cPagador): array {
    echo "  [Legado] gerarBoleto({$cPagador}, R$" . number_format($nValor, 2) . ")\n";
    return [
        'nIdBoleto'     => 12345,
        'cCodigoBarras' => '9999.99999 99999.999999',
        'cStatusBoleto' => 'ATIVO',
        'nValorBoleto'  => $nValor,
    ];
}

function consultar_status_legado(int $nIdBoleto): string {
    echo "  [Legado] consultarStatus({$nIdBoleto})\n";
    return 'ATIVO';
}

function cancelar_boleto_legado(int $nIdBoleto, string $cMotivo): bool {
    echo "  [Legado] cancelarBoleto({$nIdBoleto}, {$cMotivo})\n";
    return true;
}


// ─── Modelo de domínio moderno ────────────────────────────────────────────────

readonly class Boleto {
    public function __construct(
        public int    $id,
        public string $codigoBarras,
        public string $status,
        public float  $valor,
    ) {}
}


// ─── Contrato (interface) ────────────────────────────────────────────────────

interface ServicoCobranca {
    public function emitir(float $valor, string $vencimento, string $clienteId): Boleto;
    public function consultar(int $boletoId): string;
    public function cancelar(int $boletoId): bool;
}


// ─── Adapter: isola a API legada do código de negócio ────────────────────────

class LegadoCobrancaAdapter implements ServicoCobranca {
    /**
     * Traduz a API legada (nId*, cCodigo*, cStatus*) para o contrato ServicoCobranca.
     */
    public function emitir(float $valor, string $vencimento, string $clienteId): Boleto {
        $raw = gerar_boleto_legado($valor, $vencimento, $clienteId);
        return new Boleto(
            id:           $raw['nIdBoleto'],
            codigoBarras: $raw['cCodigoBarras'],
            status:       strtolower($raw['cStatusBoleto']),
            valor:        $raw['nValorBoleto'],
        );
    }

    public function consultar(int $boletoId): string {
        $statusRaw = consultar_status_legado($boletoId);
        return strtolower($statusRaw);
    }

    public function cancelar(int $boletoId): bool {
        return cancelar_boleto_legado($boletoId, 'SOLICITACAO_CLIENTE');
    }
}


// ─── Facade: orquestra o fluxo completo de cobrança ──────────────────────────

class FachadaCobranca {
    /**
     * Quem chama executa o fluxo completo passando apenas os dados essenciais.
     */
    public function __construct(
        private readonly ServicoCobranca $servico,
    ) {}

    public function processarCobrancaCompleta(float $valor, string $vencimento, string $clienteId): array {
        $boleto    = $this->servico->emitir($valor, $vencimento, $clienteId);
        $status    = $this->servico->consultar($boleto->id);
        $cancelado = $this->servico->cancelar($boleto->id);
        return [
            'boleto_id'    => $boleto->id,
            'codigo'       => $boleto->codigoBarras,
            'status_final' => $status,
            'cancelado'    => $cancelado,
        ];
    }
}


// ─── Verificação ──────────────────────────────────────────────────────────────

function verificar_adapter(): void {
    $adapter = new LegadoCobrancaAdapter();

    $boleto = $adapter->emitir(500.0, '2026-08-15', 'CLI-200');
    assert($boleto instanceof Boleto, 'esperado Boleto, obtido outro tipo');
    assert($boleto->id === 12345, "esperado 12345, obtido {$boleto->id}");
    assert($boleto->status === 'ativo', "esperado 'ativo', obtido '{$boleto->status}'");
    echo "OK: Adapter — emitir() retorna Boleto sem campos legados\n";

    $status = $adapter->consultar(12345);
    assert($status === 'ativo', "esperado 'ativo', obtido '{$status}'");
    echo "OK: Adapter — consultar() normaliza status para minúsculas\n";

    $cancelado = $adapter->cancelar(12345);
    assert($cancelado === true, 'esperado true, obtido false');
    echo "OK: Adapter — cancelar() passa motivo fixo ao sistema legado\n";
}

function verificar_facade(): void {
    $fachada   = new FachadaCobranca(new LegadoCobrancaAdapter());
    $resultado = $fachada->processarCobrancaCompleta(300.0, '2026-09-01', 'CLI-300');

    assert($resultado['boleto_id'] === 12345, "esperado 12345, obtido {$resultado['boleto_id']}");
    assert($resultado['status_final'] === 'ativo', "esperado 'ativo', obtido '{$resultado['status_final']}'");
    assert($resultado['cancelado'] === true, 'esperado true');
    echo "OK: Facade — processarCobrancaCompleta() executa emitir + consultar + cancelar\n";
    echo "OK: Facade — chamador não conhece API legada nem sequência de passos\n";
}

echo "=== Gabarito 18 PHP — Adapter + Facade (boletos) ===\n\n";
verificar_adapter();
echo "\n";
verificar_facade();
