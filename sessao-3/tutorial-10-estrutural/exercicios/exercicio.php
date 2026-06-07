<?php
// EXERCÍCIO 18 PHP — Padrões Estruturais: Adapter + Facade
// Execute: php exercicio.php
//
// INSTRUÇÕES:
//   O sistema de boletos bancários abaixo tem uma API legada com nomes e
//   estruturas de dados inconsistentes. O código de negócio chama essas
//   funções diretamente em 3 lugares diferentes.
//
//   1. Crie um Adapter que isole o sistema legado do código de negócio.
//   2. Crie uma Facade que simplifique o fluxo completo (emitir + consultar + cancelar).

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


// ─── TODO: Implemente aqui ────────────────────────────────────────────────────
//
// 1. Crie uma readonly class Boleto com propriedades:
//    id, codigoBarras, status, valor
//
// 2. Crie uma interface ServicoCobranca com os métodos:
//    - emitir(float $valor, string $vencimento, string $clienteId): Boleto
//    - consultar(int $boletoId): string
//    - cancelar(int $boletoId): bool
//
// 3. Crie a classe LegadoCobrancaAdapter implements ServicoCobranca
//    que chama as funções *_legado e normaliza os resultados
//
// 4. Crie a classe FachadaCobranca com o método:
//    - processarCobrancaCompleta(float $valor, string $vencimento, string $clienteId): array
//      (emite + consulta + cancela e retorna um resumo)
//
// ─────────────────────────────────────────────────────────────────────────────


// Demo
$boleto = emitir_cobranca(500.0, '2026-08-15', 'CLI-200');
echo "Boleto: id={$boleto['id']}, status={$boleto['status']}\n";
$status = verificar_cobranca($boleto['id']);
echo "Status: {$status}\n";
$cancelado = estornar_cobranca($boleto['id']) ? 'true' : 'false';
echo "Cancelado: {$cancelado}\n";
