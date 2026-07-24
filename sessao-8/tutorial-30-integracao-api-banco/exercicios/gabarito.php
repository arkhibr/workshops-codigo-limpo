<?php
// GABARITO 30 — Integração ponta-a-ponta API+Banco (PHPUnit 11 + Guzzle + PDO/SQLite)
// Suíte refatorada: além de conferir a resposta HTTP, relê o pedido
// diretamente via PDO para confirmar que o status "pago" foi realmente
// persistido — verificando os DOIS lados, não só o contrato HTTP.
// Execute: vendor/bin/phpunit gabarito.php

use GuzzleHttp\Client;

function criarSchema(PDO $pdo): void
{
    $pdo->exec(
        'CREATE TABLE IF NOT EXISTS pedidos (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT    NOT NULL,
            total   REAL    NOT NULL CHECK (total >= 0),
            status  TEXT    NOT NULL DEFAULT \'aberto\'
        )'
    );
}

final class GabaritoTest extends PHPUnit\Framework\TestCase
{
    private Client $cliente;
    private PDO $pdo;

    protected function setUp(): void
    {
        $this->pdo = new PDO('sqlite::memory:');
        $this->pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        criarSchema($this->pdo);
        $this->cliente = new Client([
            'base_uri' => 'http://localhost:8080',
            'http_errors' => false,
        ]);
    }

    private function criaPedidoAberto(): array
    {
        return json_decode((string) $this->cliente->post('/pedidos', ['json' => [
            'cliente' => 'Ana',
            'itens' => [['produto' => 'Livro', 'quantidade' => 1, 'preco_unitario' => 10.0]],
        ]])->getBody(), true);
    }

    public function testPagarPedidoPersisteStatusPagoNoBanco(): void
    {
        $criado = $this->criaPedidoAberto();

        $resposta = $this->cliente->post("/pedidos/{$criado['id']}/pagar");

        $this->assertSame(200, $resposta->getStatusCode());
        $corpo = json_decode((string) $resposta->getBody(), true);
        $this->assertSame('pago', $corpo['status']);

        // ✅ verifica o OUTRO lado: o status "pago" foi realmente gravado
        $stmt = $this->pdo->prepare('SELECT status FROM pedidos WHERE id = ?');
        $stmt->execute([$criado['id']]);
        $linha = $stmt->fetch(PDO::FETCH_ASSOC);
        $this->assertSame('pago', $linha['status']);
    }

    public function testPagarPedidoInexistenteRetorna404(): void
    {
        $resposta = $this->cliente->post('/pedidos/999/pagar');
        $this->assertSame(404, $resposta->getStatusCode());
    }

    public function testPagarPedidoJaPagoRetorna409ENaoAlteraBanco(): void
    {
        $criado = $this->criaPedidoAberto();
        $this->cliente->post("/pedidos/{$criado['id']}/pagar");

        $resposta = $this->cliente->post("/pedidos/{$criado['id']}/pagar");

        $this->assertSame(409, $resposta->getStatusCode());
        // ✅ confirma que o banco continua com status "pago" (não foi
        // corrompido pela segunda tentativa de pagamento)
        $stmt = $this->pdo->prepare('SELECT status FROM pedidos WHERE id = ?');
        $stmt->execute([$criado['id']]);
        $linha = $stmt->fetch(PDO::FETCH_ASSOC);
        $this->assertSame('pago', $linha['status']);
    }
}
