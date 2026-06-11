<?php
// EXERCÍCIO 18 PHP — Padrões Estruturais: Adapter + Facade
// Execute: php exercicio.php
//
// PASSOS:
//
//   PASSO 1 — IDENTIFICAR (5 min)
//     Nas 3 funções de negócio (emitir_cobranca, verificar_cobranca, estornar_cobranca),
//     adicione um comentário // ACOPLAMENTO: antes de cada chamada à API legada.
//     Meta: marcar os 3 acoplamentos antes de alterar código.
//
//   PASSO 2 — MODELO DE DOMÍNIO (5 min)
//     Crie a readonly class Boleto com propriedades:
//       id: int, codigoBarras: string, status: string, valor: float
//     (sem alterar mais nada ainda)
//
//   PASSO 3 — ADAPTER (10 min)
//     Crie a classe LegadoCobrancaAdapter com 3 métodos:
//       emitir(float $valor, string $vencimento, string $clienteId): Boleto
//       consultar(int $boletoId): string
//       cancelar(int $boletoId): bool
//     Cada método chama uma função *_legado e normaliza os campos.
//     Verifique: $adapter->emitir(500.0, '2026-08-15', 'CLI-200') retorna um Boleto.
//
//   PASSO 4 — FACADE (8 min)
//     Crie FachadaCobranca recebendo um adapter no construtor, com:
//       processarCobrancaCompleta(float $valor, string $vencimento, string $clienteId): array
//     Que chama emitir + consultar + cancelar e devolve resumo.
//     Verifique que o caller não precisa mais conhecer a API legada.

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


// ─── Código de negócio — chama legado diretamente ────────────────────────────

function emitir_cobranca(float $valor, string $vencimento, string $clienteId): array {
    $raw = gerar_boleto_legado($valor, $vencimento, $clienteId);   // acoplamento direto
    return [
        'id'     => $raw['nIdBoleto'],
        'codigo' => $raw['cCodigoBarras'],
        'status' => strtolower($raw['cStatusBoleto']),
        'valor'  => $raw['nValorBoleto'],
    ];
}

function verificar_cobranca(int $boletoId): string {
    $statusRaw = consultar_status_legado($boletoId);               // acoplamento direto
    return strtolower($statusRaw);
}

function estornar_cobranca(int $boletoId): bool {
    return cancelar_boleto_legado($boletoId, 'SOLICITACAO_CLIENTE'); // acoplamento direto
}


// ─── Passo 2: implemente readonly class Boleto aqui ──────────────────────────
// readonly class Boleto {
//     public function __construct(
//         public int    $id,
//         public string $codigoBarras,
//         public string $status,
//         public float  $valor,
//     ) {}
// }


// ─── Passo 3: implemente LegadoCobrancaAdapter aqui ──────────────────────────
// class LegadoCobrancaAdapter {
//     public function emitir(float $valor, string $vencimento, string $clienteId): Boleto { ... }
//     public function consultar(int $boletoId): string { ... }
//     public function cancelar(int $boletoId): bool { ... }
// }


// ─── Passo 4: implemente FachadaCobranca aqui ────────────────────────────────
// class FachadaCobranca {
//     public function __construct(private readonly LegadoCobrancaAdapter $adapter) {}
//     public function processarCobrancaCompleta(float $valor, string $vencimento, string $clienteId): array { ... }
// }


// Demo (código original)
// Passo 1: adicione // ACOPLAMENTO: nas linhas de chamada legada dentro das funções acima
$boleto = emitir_cobranca(500.0, '2026-08-15', 'CLI-200');
echo "Boleto: id={$boleto['id']}, status={$boleto['status']}\n";
$status = verificar_cobranca($boleto['id']);
echo "Status: {$status}\n";
$cancelado = estornar_cobranca($boleto['id']) ? 'true' : 'false';
echo "Cancelado: {$cancelado}\n";

// Passo 3 — descomente para verificar o Adapter:
// $adapter = new LegadoCobrancaAdapter();
// $b = $adapter->emitir(500.0, '2026-08-15', 'CLI-200');
// echo "[Adapter] Boleto: id={$b->id}, status={$b->status}\n";

// Passo 4 — descomente para verificar a Facade:
// $fachada = new FachadaCobranca(new LegadoCobrancaAdapter());
// $resultado = $fachada->processarCobrancaCompleta(500.0, '2026-08-15', 'CLI-200');
// print_r($resultado);
