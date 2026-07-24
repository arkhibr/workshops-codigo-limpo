<?php
// equivalente.php — Testes de Integração de API em PHPUnit 11 + Guzzle
// Contra um servidor real (embutido: `php -S localhost:8080 api.php`),
// não um mock — é isso que caracteriza um teste de integração.
// Execute: vendor/bin/phpunit equivalente.php (com o servidor no ar)
//
// Ilustrativo: PHP/PHPUnit não estão instalados neste ambiente de workshop.
// O objetivo é mostrar o padrão de asserção de contrato completo e
// isolamento de estado (setUp cria um client novo por teste), não rodar.

use GuzzleHttp\Client;
use GuzzleHttp\Exception\ClientException;

final class PedidosIntegrationTest extends PHPUnit\Framework\TestCase
{
    private Client $cliente;

    // ✅ setUp roda antes de CADA teste — client novo, sem estado vazado.
    protected function setUp(): void
    {
        $this->cliente = new Client([
            'base_uri' => 'http://localhost:8080',
            'http_errors' => false, // controlamos os status manualmente
        ]);
    }

    public function testCriaPedidoRetorna201ComTotalCalculado(): void
    {
        $resposta = $this->cliente->post('/pedidos', ['json' => [
            'cliente' => 'Ana',
            'itens' => [['produto' => 'Livro', 'quantidade' => 2, 'preco_unitario' => 30.0]],
        ]]);

        // ✅ Contrato completo: status + corpo, não só o status.
        $this->assertSame(201, $resposta->getStatusCode());
        $corpo = json_decode((string) $resposta->getBody(), true);
        $this->assertSame(60.0, $corpo['total']);
        $this->assertSame('aberto', $corpo['status']);
    }

    public function testBuscaPedidoInexistenteRetorna404(): void
    {
        $resposta = $this->cliente->get('/pedidos/999');

        $this->assertSame(404, $resposta->getStatusCode());
        $corpo = json_decode((string) $resposta->getBody(), true);
        $this->assertSame('pedido não encontrado', $corpo['detail']);
    }

    public function testPagaPedidoAbertoMudaStatusParaPago(): void
    {
        $criado = json_decode((string) $this->cliente->post('/pedidos', ['json' => [
            'cliente' => 'Ana',
            'itens' => [['produto' => 'Livro', 'quantidade' => 1, 'preco_unitario' => 10.0]],
        ]])->getBody(), true);

        $resposta = $this->cliente->post("/pedidos/{$criado['id']}/pagar");

        $this->assertSame(200, $resposta->getStatusCode());
        $corpo = json_decode((string) $resposta->getBody(), true);
        $this->assertSame('pago', $corpo['status']);
    }

    public function testPagarPedidoJaPagoRetorna409(): void
    {
        $criado = json_decode((string) $this->cliente->post('/pedidos', ['json' => [
            'cliente' => 'Ana',
            'itens' => [['produto' => 'Livro', 'quantidade' => 1, 'preco_unitario' => 10.0]],
        ]])->getBody(), true);
        $this->cliente->post("/pedidos/{$criado['id']}/pagar");

        $resposta = $this->cliente->post("/pedidos/{$criado['id']}/pagar");

        $this->assertSame(409, $resposta->getStatusCode());
    }
}

// ❌ Contraponto (anti-padrão, não incluído na suíte acima): client estático
// compartilhado entre testes, e asserção só de status_code.
final class PedidosTestRuim extends PHPUnit\Framework\TestCase
{
    private static ?Client $clienteCompartilhado = null; // ❌ vaza estado entre testes

    public function testCriaPedido(): void
    {
        self::$clienteCompartilhado ??= new Client(['base_uri' => 'http://localhost:8080']);
        $resposta = self::$clienteCompartilhado->post('/pedidos', ['json' => [
            'cliente' => 'Ana',
            'itens' => [['produto' => 'Livro', 'quantidade' => 1, 'preco_unitario' => 10.0]],
        ]]);
        $this->assertSame(201, $resposta->getStatusCode()); // ❌ nunca olha o corpo
    }
}
