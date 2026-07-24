<?php
// EXERCÍCIO 29 — Testes de Integração de Banco de Dados (PHPUnit 11 + PDO/SQLite)
// Tempo estimado: 20 minutos
//
// INSTRUÇÕES:
//   A suíte abaixo testa totalGastoPeloCliente(PDO $pdo, int $clienteId)
//   mas tem os mesmos 3 problemas estruturais de exemplos/equivalente.php:
//     1. Mocka o próprio acesso a dados — nenhum SQL roda de verdade.
//     2. Depende de um banco em arquivo (teste.db), persistente e nunca
//        limpo entre execuções.
//     3. Sem schema isolado por teste — assume que a tabela e os dados já
//        existem (deixados por uma execução anterior).
//
//   Refatore aplicando os padrões de exemplos/equivalente.php: setUp() cria
//   um PDO sqlite::memory: novo por teste, chama criarSchema(), e verifica
//   a soma real (e o isolamento entre clientes).
//   Execute: vendor/bin/phpunit exercicio.php
//
// Ilustrativo: PHP/PHPUnit não estão instalados neste ambiente de workshop.
//
// NOTA DE AUTOCONTENÇÃO: as funções de repositório abaixo são uma cópia
// local do SUT (idênticas a exemplos/equivalente.php) — o repositório não
// permite que um arquivo importe de outro diretório.

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

function totalGastoPeloClienteRuim(PDO $pdo, int $clienteId): float
{
    $pedidos = listarPedidosDoCliente($pdo, $clienteId);
    return array_sum(array_column($pedidos, 'total'));
}

final class ExercicioTestRuim extends PHPUnit\Framework\TestCase
{
    public function testTotalGastoSomaOsPedidosDoCliente(): void
    {
        // ❌ 1. Mocka o próprio PDO — nenhum SQL roda. O teste "passa"
        // porque o stub devolve exatamente os dados programados, não
        // porque a query de listarPedidosDoCliente está correta.
        $pdoFalso = new class {
            public function listarPedidosDoCliente(): array
            {
                return [
                    ['id' => 1, 'cliente_id' => 1, 'total' => 30.0, 'status' => 'aberto'],
                    ['id' => 2, 'cliente_id' => 1, 'total' => 20.0, 'status' => 'aberto'],
                ];
            }
        };

        $total = array_sum(array_column($pdoFalso->listarPedidosDoCliente(), 'total'));

        $this->assertSame(50.0, $total);
    }

    public function testTotalGastoNoBancoCompartilhado(): void
    {
        // ❌ 2 e 3. Banco em arquivo compartilhado, sem schema isolado —
        // assume que a tabela `pedidos` já existe (criada por uma execução
        // anterior). Cada rodada da suíte insere mais uma linha no mesmo
        // arquivo, então o total cresce a cada execução.
        $caminho = sys_get_temp_dir() . '/exercicio_29_teste.db';
        $pdo = new PDO("sqlite:{$caminho}");
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->exec(
            'CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                total REAL NOT NULL,
                status TEXT NOT NULL DEFAULT \'aberto\'
            )'
        );
        inserirPedido($pdo, 1, 15.0);

        $total = totalGastoPeloClienteRuim($pdo, 1);

        // ❌ Esse assert só funciona por acaso: o total cresce a cada
        // execução da suíte — não é repetível nem independente.
        $this->assertGreaterThanOrEqual(15.0, $total);
    }
}
