<?php
// equivalente.php — Testes de Integração de Banco de Dados em PHPUnit 11 + PDO/SQLite
// Cria um banco SQLite em memória (:memory:) por teste — SQL, constraints
// (FK, CHECK) e transações reais são exercitados, não simulados.
// Execute: vendor/bin/phpunit equivalente.php
//
// Ilustrativo: PHP/PHPUnit não estão instalados neste ambiente de workshop.
// O objetivo é mostrar o padrão de isolamento (setUp cria uma conexão nova
// por teste) e a verificação de efeitos colaterais reais no banco, não rodar.

function criarSchema(PDO $pdo): void
{
    $pdo->exec('PRAGMA foreign_keys = ON');
    $pdo->exec(
        'CREATE TABLE clientes (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT    NOT NULL,
            vip  INTEGER NOT NULL DEFAULT 0
        )'
    );
    $pdo->exec(
        'CREATE TABLE pedidos (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL REFERENCES clientes(id),
            total      REAL    NOT NULL CHECK (total >= 0),
            status     TEXT    NOT NULL DEFAULT \'aberto\'
        )'
    );
}

function inserirCliente(PDO $pdo, string $nome, bool $vip = false): int
{
    $stmt = $pdo->prepare('INSERT INTO clientes (nome, vip) VALUES (?, ?)');
    $stmt->execute([$nome, (int) $vip]);
    return (int) $pdo->lastInsertId();
}

function inserirPedido(PDO $pdo, int $clienteId, float $total): int
{
    $stmt = $pdo->prepare('INSERT INTO pedidos (cliente_id, total) VALUES (?, ?)');
    $stmt->execute([$clienteId, $total]);
    return (int) $pdo->lastInsertId();
}

function buscarPedido(PDO $pdo, int $pedidoId): ?array
{
    $stmt = $pdo->prepare('SELECT id, cliente_id, total, status FROM pedidos WHERE id = ?');
    $stmt->execute([$pedidoId]);
    $linha = $stmt->fetch(PDO::FETCH_ASSOC);
    return $linha === false ? null : $linha;
}

final class PedidosIntegrationTest extends PHPUnit\Framework\TestCase
{
    private PDO $pdo;

    // ✅ setUp roda antes de CADA teste — banco :memory: novo, sem estado
    // vazado entre testes (isolamento real).
    protected function setUp(): void
    {
        $this->pdo = new PDO('sqlite::memory:');
        $this->pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        criarSchema($this->pdo);
    }

    public function testInsereERecuperaPedidoDoCliente(): void
    {
        $clienteId = inserirCliente($this->pdo, 'Ana', vip: true);
        $pedidoId = inserirPedido($this->pdo, $clienteId, 90.0);

        $pedido = buscarPedido($this->pdo, $pedidoId);

        $this->assertSame($clienteId, $pedido['cliente_id']);
        $this->assertSame(90.0, $pedido['total']);
        $this->assertSame('aberto', $pedido['status']);
    }

    public function testRejeitaPedidoComClienteInexistente(): void
    {
        $this->expectException(PDOException::class);
        inserirPedido($this->pdo, clienteId: 999, total: 10.0);
    }

    public function testRejeitaPedidoComTotalNegativo(): void
    {
        $clienteId = inserirCliente($this->pdo, 'Ana');
        $this->expectException(PDOException::class);
        inserirPedido($this->pdo, $clienteId, total: -5.0);
    }
}

// ❌ Contraponto (anti-padrão, não incluído na suíte acima): mocka o próprio
// acesso a dados (via um "repositório" duplo/stub) — nenhum SQL roda, então
// uma constraint violada nunca seria detectada.
final class PedidosTestRuim extends PHPUnit\Framework\TestCase
{
    public function testInserePedido(): void
    {
        $repositorioFalso = new class {
            public function inserirPedido(int $clienteId, float $total): int
            {
                return 1; // ❌ nunca toca o banco — sempre "funciona"
            }
        };

        $pedidoId = $repositorioFalso->inserirPedido(clienteId: 999, total: -50.0);

        $this->assertSame(1, $pedidoId); // ❌ não prova que o banco aceitaria isso
    }
}
