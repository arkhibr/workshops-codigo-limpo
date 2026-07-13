<?php
// EXERCÍCIO 27 — Testes de Unidade em Código Legado (Âncora) (PHPUnit 11)
// Tempo estimado: 10 minutos
//
// INSTRUÇÕES:
//   ProcessadorReembolso abaixo não tem seams nem testes: instancia
//   GatewayPagamentoReal e ServicoAuditoriaReal diretamente.
//
//   1. Introduza seams (injeção via construtor).
//   2. Escreva um teste de CARACTERIZAÇÃO para o comportamento atual.
//   3. Use doubles (Stub para o gateway, Fake para a auditoria).
//   Execute: vendor/bin/phpunit exercicio.php

final class GatewayPagamentoReal
{
    public function estornar(string $transacaoId, float $valor): array
    {
        throw new RuntimeException('Gateway real não disponível neste ambiente');
    }
}

final class ServicoAuditoriaReal
{
    public function registrar(string $evento, array $detalhes): void
    {
        throw new RuntimeException('Serviço de auditoria real não disponível neste ambiente');
    }
}

final class ProcessadorReembolso
{
    private GatewayPagamentoReal $gateway;
    private ServicoAuditoriaReal $auditoria;

    public function __construct()
    {
        $this->gateway = new GatewayPagamentoReal();
        $this->auditoria = new ServicoAuditoriaReal();
    }

    public function processarReembolso(string $transacaoId, float $valor): array
    {
        $resultado = $this->gateway->estornar($transacaoId, $valor);
        $this->auditoria->registrar('reembolso', ['transacao_id' => $transacaoId, 'valor' => $valor]);
        return $resultado;
    }
}
