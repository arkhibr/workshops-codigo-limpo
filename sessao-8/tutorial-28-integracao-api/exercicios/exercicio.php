<?php
// EXERCÍCIO 28 — Testes de Integração de API (PHPUnit 11 + Guzzle)
// Tempo estimado: 20 minutos
//
// INSTRUÇÕES:
//   A suíte abaixo testa POST /pedidos/{id}/pagar mas tem 3 problemas
//   estruturais (os mesmos de exemplos/equivalente.php):
//     1. Client estático compartilhado entre os testes (estado vaza).
//     2. Só verifica getStatusCode() — nunca olha o corpo da resposta.
//     3. Ordem importa — um teste assume que o pedido criado por outro
//        teste ainda existe, com o id que ele espera.
//
//   Refatore aplicando os padrões de exemplos/equivalente.php: setUp()
//   cria um Client novo por teste, nomes comportamentais, e asserções
//   sobre o contrato completo (status + corpo).
//   Execute: vendor/bin/phpunit exercicio.php (com o servidor no ar)
//
// Ilustrativo: PHP/PHPUnit não estão instalados neste ambiente de workshop.

use GuzzleHttp\Client;

final class PedidosExercicioTest extends PHPUnit\Framework\TestCase
{
    // ❌ 1. Client estático — reaproveitado por todos os testes da classe.
    private static ?Client $cliente = null;

    private static function clienteCompartilhado(): Client
    {
        return self::$cliente ??= new Client(['base_uri' => 'http://localhost:8080']);
    }

    public function testCriaPedidoParaPagarDepois(): void
    {
        // ❌ 2. Só checa o status — não confirma id, total ou status "aberto".
        $resposta = self::clienteCompartilhado()->post('/pedidos', ['json' => [
            'cliente' => 'Bruno',
            'itens' => [['produto' => 'Caneta', 'quantidade' => 3, 'preco_unitario' => 5.0]],
        ]]);
        $this->assertSame(201, $resposta->getStatusCode());
    }

    public function testPagaPedido(): void
    {
        // ❌ 3. Ordem importa: assume que o pedido id=1, criado pelo teste
        // anterior via client estático, ainda existe e está "aberto".
        $resposta = self::clienteCompartilhado()->post('/pedidos/1/pagar');
        $this->assertSame(200, $resposta->getStatusCode());
    }

    public function testPagarPedidoNovamenteFalha(): void
    {
        // ❌ 3 (de novo): depende do teste anterior já ter pago o pedido id=1.
        $resposta = self::clienteCompartilhado()->post('/pedidos/1/pagar');
        $this->assertSame(409, $resposta->getStatusCode());
    }
}
