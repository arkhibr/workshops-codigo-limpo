<?php
// GABARITO 29 — Testes de Integração de Banco de Dados (PHPUnit 11 + PDO/SQLite)
// Suíte refatorada: setUp() cria um PDO sqlite::memory: novo por teste,
// schema isolado, e verificação da soma real (SQL de verdade) — sem mock,
// sem arquivo compartilhado.
// Execute: vendor/bin/phpunit gabarito.php

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

function listarPedidosDoCliente(PDO $pdo, int $clienteId): array
{
    $stmt = $pdo->prepare('SELECT id, cliente_id, total, status FROM pedidos WHERE cliente_id = ?');
    $stmt->execute([$clienteId]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

function totalGastoPeloCliente(PDO $pdo, int $clienteId): float
{
    $pedidos = listarPedidosDoCliente($pdo, $clienteId);
    return array_sum(array_column($pedidos, 'total'));
}

final class GabaritoTest extends PHPUnit\Framework\TestCase
{
    private PDO $pdo;

    // ✅ setUp roda antes de CADA teste — banco :memory: novo, sem estado
    // vazado entre testes.
    protected function setUp(): void
    {
        $this->pdo = new PDO('sqlite::memory:');
        $this->pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        criarSchema($this->pdo);
    }

    public function testTotalGastoSomaOsPedidosDoCliente(): void
    {
        $clienteId = inserirCliente($this->pdo, 'Ana');
        inserirPedido($this->pdo, $clienteId, 30.0);
        inserirPedido($this->pdo, $clienteId, 20.0);

        $total = totalGastoPeloCliente($this->pdo, $clienteId);

        $this->assertSame(50.0, $total);
    }

    public function testTotalGastoEZeroParaClienteSemPedidos(): void
    {
        $clienteId = inserirCliente($this->pdo, 'Ana');

        $total = totalGastoPeloCliente($this->pdo, $clienteId);

        $this->assertSame(0.0, $total);
    }

    public function testTotalGastoNaoSomaPedidosDeOutroCliente(): void
    {
        $ana = inserirCliente($this->pdo, 'Ana');
        $bob = inserirCliente($this->pdo, 'Bob');
        inserirPedido($this->pdo, $ana, 30.0);
        inserirPedido($this->pdo, $bob, 100.0);

        $totalAna = totalGastoPeloCliente($this->pdo, $ana);

        $this->assertSame(30.0, $totalAna);
    }
}
