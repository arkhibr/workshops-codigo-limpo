<?php
// GABARITO 27 — Testes de Unidade em Código Legado (Âncora) (PHPUnit 11)
// Seam via construtor: ProcessadorReembolso(gateway, auditoria). GatewayPagamentoStub
// devolve ['status' => 'estornado', 'valor' => ...]; ServicoAuditoriaFake guarda os
// eventos registrados em um array, para inspeção. O primeiro teste é de
// caracterização — congela o comportamento atual antes de qualquer melhoria.
// Execute: vendor/bin/phpunit gabarito.php

interface GatewayPagamento
{
    public function estornar(string $transacaoId, float $valor): array;
}

interface ServicoAuditoria
{
    public function registrar(string $evento, array $detalhes): void;
}

final class ProcessadorReembolso
{
    public function __construct(
        private GatewayPagamento $gateway,
        private ServicoAuditoria $auditoria,
    ) {
    }

    public function processarReembolso(string $transacaoId, float $valor): array
    {
        $resultado = $this->gateway->estornar($transacaoId, $valor);
        $this->auditoria->registrar('reembolso', ['transacao_id' => $transacaoId, 'valor' => $valor]);
        return $resultado;
    }
}

// Stub: devolve resposta fixa e pré-programada, sem chamada de rede real.
final class GatewayPagamentoStub implements GatewayPagamento
{
    public function __construct(private string $status = 'estornado')
    {
    }

    public function estornar(string $transacaoId, float $valor): array
    {
        return ['status' => $this->status, 'valor' => $valor];
    }
}

// Fake: guarda os eventos registrados em memória, para inspeção posterior.
final class ServicoAuditoriaFake implements ServicoAuditoria
{
    public array $eventosRegistrados = [];

    public function registrar(string $evento, array $detalhes): void
    {
        $this->eventosRegistrados[] = ['evento' => $evento, 'detalhes' => $detalhes];
    }
}

final class ProcessadorReembolsoTest extends PHPUnit\Framework\TestCase
{
    public function testCaracterizacaoProcessaReembolsoComSucesso(): void
    {
        // Teste de caracterização: congela o comportamento atual do
        // ProcessadorReembolso como oráculo, agora que o seam permite isolá-lo.
        $gateway = new GatewayPagamentoStub(status: 'estornado');
        $auditoria = new ServicoAuditoriaFake();
        $processador = new ProcessadorReembolso($gateway, $auditoria);

        $resultado = $processador->processarReembolso('TX001', 150.0);

        $this->assertSame(['status' => 'estornado', 'valor' => 150.0], $resultado);
    }

    public function testReembolsoRegistraEventoDeAuditoria(): void
    {
        $gateway = new GatewayPagamentoStub();
        $auditoria = new ServicoAuditoriaFake();
        $processador = new ProcessadorReembolso($gateway, $auditoria);

        $processador->processarReembolso('TX002', 80.0);

        $this->assertCount(1, $auditoria->eventosRegistrados);
        $this->assertSame('reembolso', $auditoria->eventosRegistrados[0]['evento']);
        $this->assertSame(
            ['transacao_id' => 'TX002', 'valor' => 80.0],
            $auditoria->eventosRegistrados[0]['detalhes'],
        );
    }
}
