<?php
// equivalente.php — Dublês de Teste em PHPUnit 11
// Execute: vendor/bin/phpunit equivalente.php

final class ResultadoPagamento
{
    public function __construct(
        public readonly string $status,
        public readonly float $valor,
    ) {
    }
}

final class GatewayPagamentoReal
{
    public function cobrar(float $valor): ResultadoPagamento
    {
        usleep(300_000); // simula latência de rede real
        return new ResultadoPagamento(status: 'aprovado', valor: $valor);
    }
}

interface GatewayPagamento
{
    public function cobrar(float $valor): ResultadoPagamento;
}

interface ServicoNotificacao
{
    public function enviar(string $destinatario, string $mensagem): bool;
}

final class ProcessadorPagamento
{
    public function __construct(
        private GatewayPagamento $gateway,
        private ServicoNotificacao $notificacao,
    ) {
    }

    public function processar(float $valor, string $destinatario): ResultadoPagamento
    {
        $resultado = $this->gateway->cobrar($valor);
        if ($resultado->status === 'aprovado') {
            $this->notificacao->enviar($destinatario, 'Pagamento aprovado');
        }
        return $resultado;
    }
}

// Ruim: sem nenhum double — depende de infraestrutura real e é lento (viola o F de FIRST)
final class ProcessadorPagamentoTestRuim extends PHPUnit\Framework\TestCase
{
    public function testProcessaPagamentoSemNenhumDouble(): void
    {
        $gatewayReal = new GatewayPagamentoReal();
        $notificacaoReal = new class implements ServicoNotificacao {
            public function enviar(string $destinatario, string $mensagem): bool
            {
                usleep(200_000);
                return true;
            }
        };
        $processador = new ProcessadorPagamento($gatewayReal, $notificacaoReal);

        $resultado = $processador->processar(100.0, 'cliente@teste.com');

        $this->assertSame('aprovado', $resultado->status);
    }
}

// Bom: createStub() para resposta fixa, createMock() para verificar interação
final class ProcessadorPagamentoTest extends PHPUnit\Framework\TestCase
{
    public function testProcessaPagamentoAprovadoNotificaCliente(): void
    {
        // Arrange — Stub para o gateway, Mock para verificar a notificação
        $gateway = $this->createStub(GatewayPagamento::class);
        $gateway->method('cobrar')->willReturn(new ResultadoPagamento(status: 'aprovado', valor: 100.0));

        $notificacao = $this->createMock(ServicoNotificacao::class);
        $notificacao->expects($this->once())
            ->method('enviar')
            ->with('cliente@teste.com', 'Pagamento aprovado');

        $processador = new ProcessadorPagamento($gateway, $notificacao);

        // Act
        $resultado = $processador->processar(100.0, 'cliente@teste.com');

        // Assert — comportamento observável, não implementação interna
        $this->assertSame('aprovado', $resultado->status);
    }

    public function testPagamentoRecusadoNaoNotificaCliente(): void
    {
        $gateway = $this->createStub(GatewayPagamento::class);
        $gateway->method('cobrar')->willReturn(new ResultadoPagamento(status: 'recusado', valor: 100.0));

        $notificacao = $this->createMock(ServicoNotificacao::class);
        $notificacao->expects($this->never())->method('enviar');

        $processador = new ProcessadorPagamento($gateway, $notificacao);
        $processador->processar(100.0, 'cliente@teste.com');
    }

    public function testDummyNotificacaoNaoEExercitadaQuandoPagamentoRecusado(): void
    {
        // Dummy: precisa implementar ServicoNotificacao para satisfazer o
        // construtor de ProcessadorPagamento, mas nunca é de fato invocado
        // neste caminho — quando o pagamento é recusado, o `if` dentro de
        // processar() pula a chamada a notificacao->enviar(...). Lança uma
        // exceção se for chamado, provando que o caminho testado não o exercita.
        $gateway = $this->createStub(GatewayPagamento::class);
        $gateway->method('cobrar')->willReturn(new ResultadoPagamento(status: 'recusado', valor: 100.0));

        $notificacaoDummy = new class implements ServicoNotificacao {
            public function enviar(string $destinatario, string $mensagem): bool
            {
                throw new \LogicException('Dummy não deveria ser chamado');
            }
        };

        $processador = new ProcessadorPagamento($gateway, $notificacaoDummy);

        $resultado = $processador->processar(100.0, 'cliente@teste.com');

        $this->assertSame('recusado', $resultado->status);
    }
}
