<?php
// EXERCÍCIO 30 — Integração ponta-a-ponta API+Banco (PHPUnit 11 + Guzzle + PDO/SQLite)
// Tempo estimado: 25 minutos
//
// INSTRUÇÕES:
//   A suíte abaixo testa a rota POST /pedidos/{id}/pagar mas tem o mesmo
//   problema estrutural de exemplos/equivalente.php (anti-padrão 2 do
//   tutorial): só verifica a resposta HTTP — nunca confere o banco. O teste
//   "prova" que a API respondeu com status "pago", mas não prova que o
//   status foi realmente persistido.
//
//   Refatore aplicando o padrão de exemplos/equivalente.php: depois de
//   chamar a rota, releia o pedido diretamente via PDO e confirme que o
//   status "pago" está lá — não só na resposta HTTP.
//   Execute: vendor/bin/phpunit exercicio.php
//
// Ilustrativo: PHP/PHPUnit não estão instalados neste ambiente de workshop.
//
// NOTA DE AUTOCONTENÇÃO: o schema/rota de pagamento abaixo são uma cópia
// local do SUT (idênticos a exemplos/equivalente.php, com a rota adicional
// POST /pedidos/{id}/pagar) — o repositório não permite que um arquivo
// importe de outro diretório.

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

final class ExercicioTestRuim extends PHPUnit\Framework\TestCase
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

    public function testPagarPedidoMudaStatusParaPago(): void
    {
        $criado = json_decode((string) $this->cliente->post('/pedidos', ['json' => [
            'cliente' => 'Ana',
            'itens' => [['produto' => 'Livro', 'quantidade' => 1, 'preco_unitario' => 10.0]],
        ]])->getBody(), true);

        $resposta = $this->cliente->post("/pedidos/{$criado['id']}/pagar");

        // ❌ Só confere a resposta HTTP — nunca relê o banco para confirmar
        // que o status "pago" foi de fato persistido em `pedidos`.
        $this->assertSame(200, $resposta->getStatusCode());
        $corpo = json_decode((string) $resposta->getBody(), true);
        $this->assertSame('pago', $corpo['status']);
    }
}
