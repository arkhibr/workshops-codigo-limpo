<?php
// equivalente.php — Integração ponta-a-ponta API+Banco em PHPUnit 11 + Guzzle + PDO/SQLite
// Contra um servidor real (embutido) que persiste em SQLite :memory: injetado —
// a request HTTP percorre a stack real até o banco, e o teste verifica os DOIS
// lados: a resposta HTTP e o estado gravado (relendo via PDO diretamente).
// Execute: vendor/bin/phpunit equivalente.php (com o servidor no ar)
//
// Ilustrativo: PHP/PHPUnit não estão instalados neste ambiente de workshop.
// O objetivo é mostrar o padrão de verificação dos dois lados, não rodar.

use GuzzleHttp\Client;

// criarApp(PDO $pdo) — mesma ideia de app.py: a conexão é injetada, então o
// teste pode passar um PDO sqlite::memory: e checar a stack inteira.
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

final class PedidosIntegracaoApiBancoTest extends PHPUnit\Framework\TestCase
{
    private Client $cliente;
    private PDO $pdo;

    // ✅ Cada teste recebe um PDO :memory: novo (isolamento real) e um client
    // apontando para o servidor que injeta essa mesma conexão.
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

    public function testPostPedidoPersisteNoBanco(): void
    {
        $resposta = $this->cliente->post('/pedidos', ['json' => [
            'cliente' => 'Ana',
            'itens' => [['produto' => 'Livro', 'quantidade' => 3, 'preco_unitario' => 10.0]],
        ]]);

        $this->assertSame(201, $resposta->getStatusCode());
        $corpo = json_decode((string) $resposta->getBody(), true);

        // ✅ verifica o OUTRO lado: o dado realmente foi ao banco
        $stmt = $this->pdo->prepare('SELECT cliente, total FROM pedidos WHERE id = ?');
        $stmt->execute([$corpo['id']]);
        $linha = $stmt->fetch(PDO::FETCH_ASSOC);
        $this->assertSame('Ana', $linha['cliente']);
        $this->assertSame(30.0, $linha['total']);
    }

    public function testGetLePedidoPersistido(): void
    {
        $criado = json_decode((string) $this->cliente->post('/pedidos', ['json' => [
            'cliente' => 'Bob',
            'itens' => [['produto' => 'Caneta', 'quantidade' => 2, 'preco_unitario' => 5.0]],
        ]])->getBody(), true);

        $resposta = $this->cliente->get("/pedidos/{$criado['id']}");

        $this->assertSame(200, $resposta->getStatusCode());
        $corpo = json_decode((string) $resposta->getBody(), true);
        $this->assertSame(10.0, $corpo['total']);
    }
}

// ❌ Contraponto (anti-padrão, não incluído na suíte acima): "integração
// vertical falsa" — mocka a própria camada de banco, então a request HTTP
// nunca chega a rodar SQL de verdade; e só confere a resposta, nunca o banco.
final class PedidosIntegracaoFalsaTest extends PHPUnit\Framework\TestCase
{
    public function testCriaPedidoComBancoMockado(): void
    {
        // ❌ mocka o repositório/PDO — nenhum INSERT roda de verdade
        $pdoFalso = new class {
            public function inserirPedido(string $cliente, float $total): int
            {
                return 1; // ❌ nunca toca o banco — sempre "funciona"
            }
        };

        $pedidoId = $pdoFalso->inserirPedido('Ana', 30.0);

        // ❌ só confirma o retorno simulado — nunca relê o banco para
        // confirmar que o pedido foi realmente persistido
        $this->assertSame(1, $pedidoId);
    }
}
