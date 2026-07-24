<?php
// GABARITO 28 — Testes de Integração de API (PHPUnit 11 + Guzzle)
// Suíte refatorada: client novo por teste (setUp), nomes comportamentais,
// contrato completo verificado (status + corpo), sem dependência de ordem.
// Execute: vendor/bin/phpunit gabarito.php (com o servidor no ar)

use GuzzleHttp\Client;

final class PedidosGabaritoTest extends PHPUnit\Framework\TestCase
{
    private Client $cliente;

    // ✅ setUp roda antes de CADA teste — client novo, sem estado vazado.
    protected function setUp(): void
    {
        $this->cliente = new Client([
            'base_uri' => 'http://localhost:8080',
            'http_errors' => false,
        ]);
    }

    private function criaPedidoAberto(): array
    {
        $resposta = $this->cliente->post('/pedidos', ['json' => [
            'cliente' => 'Bruno',
            'itens' => [['produto' => 'Caneta', 'quantidade' => 3, 'preco_unitario' => 5.0]],
        ]]);
        return json_decode((string) $resposta->getBody(), true);
    }

    public function testCriaPedidoRetorna201ComStatusAberto(): void
    {
        $resposta = $this->cliente->post('/pedidos', ['json' => [
            'cliente' => 'Bruno',
            'itens' => [['produto' => 'Caneta', 'quantidade' => 3, 'preco_unitario' => 5.0]],
        ]]);

        $this->assertSame(201, $resposta->getStatusCode());
        $corpo = json_decode((string) $resposta->getBody(), true);
        $this->assertSame(15.0, $corpo['total']);
        $this->assertSame('aberto', $corpo['status']);
    }

    public function testPagaPedidoAbertoMudaStatusParaPago(): void
    {
        $pedido = $this->criaPedidoAberto();

        $resposta = $this->cliente->post("/pedidos/{$pedido['id']}/pagar");

        $this->assertSame(200, $resposta->getStatusCode());
        $corpo = json_decode((string) $resposta->getBody(), true);
        $this->assertSame('pago', $corpo['status']);
    }

    public function testPagarPedidoJaPagoRetorna409(): void
    {
        $pedido = $this->criaPedidoAberto();
        $this->cliente->post("/pedidos/{$pedido['id']}/pagar");

        $resposta = $this->cliente->post("/pedidos/{$pedido['id']}/pagar");

        $this->assertSame(409, $resposta->getStatusCode());
    }

    public function testPagarPedidoInexistenteRetorna404(): void
    {
        $resposta = $this->cliente->post('/pedidos/999/pagar');

        $this->assertSame(404, $resposta->getStatusCode());
    }
}
