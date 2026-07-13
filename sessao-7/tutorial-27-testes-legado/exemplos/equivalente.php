<?php
// equivalente.php — Testes de Unidade em Código Legado em PHPUnit 11
// Execute: vendor/bin/phpunit equivalente.php

final class ConexaoBancoReal
{
    public function buscarEstoque(string $produtoId): int
    {
        throw new RuntimeException('Não há banco de dados real disponível neste ambiente');
    }

    public function atualizarEstoque(string $produtoId, int $quantidade, float $valorTotal): void
    {
        throw new RuntimeException('Não há banco de dados real disponível neste ambiente');
    }
}

final class ServicoPrecoExternoReal
{
    public function consultar(string $produtoId): float
    {
        throw new RuntimeException('Não há serviço de preço real disponível neste ambiente');
    }
}

// Sem seam: GerenciadorEstoqueLegado instancia as dependências reais
// diretamente no construtor — impossível testar em isolamento.
final class GerenciadorEstoqueLegado
{
    private ConexaoBancoReal $banco;
    private ServicoPrecoExternoReal $servicoPrecos;

    public function __construct()
    {
        $this->banco = new ConexaoBancoReal();
        $this->servicoPrecos = new ServicoPrecoExternoReal();
    }

    public function recalcularEstoque(string $produtoId, int $quantidadeVendida): int
    {
        $preco = $this->servicoPrecos->consultar($produtoId);
        $estoqueAtual = $this->banco->buscarEstoque($produtoId);
        $novoEstoque = $estoqueAtual - $quantidadeVendida;
        $valorTotal = $novoEstoque * $preco;
        $this->banco->atualizarEstoque($produtoId, $novoEstoque, $valorTotal);
        return $novoEstoque;
    }
}

// Ruim: o único teste possível sem seam documenta a impossibilidade de
// testar em isolamento — falha por falta de infraestrutura real, não por
// um bug de lógica.
final class GerenciadorEstoqueLegadoTestRuim extends PHPUnit\Framework\TestCase
{
    public function testImpossivelTestarSemInfraestruturaReal(): void
    {
        $this->expectException(RuntimeException::class);
        $gerenciador = new GerenciadorEstoqueLegado();
        $gerenciador->recalcularEstoque('PROD1', 10);
    }
}

interface ConexaoBanco
{
    public function buscarEstoque(string $produtoId): int;
    public function atualizarEstoque(string $produtoId, int $quantidade, float $valorTotal): void;
}

interface ServicoPreco
{
    public function consultar(string $produtoId): float;
}

// Bom: seam via injeção de construtor.
final class GerenciadorEstoque
{
    private array $cachePrecos;

    public function __construct(
        private ConexaoBanco $banco,
        private ServicoPreco $servicoPrecos,
        ?array $cachePrecos = null,
    ) {
        $this->cachePrecos = $cachePrecos ?? [];
    }

    public function recalcularEstoque(string $produtoId, int $quantidadeVendida): int
    {
        $preco = $this->cachePrecos[$produtoId] ?? null;
        if ($preco === null) {
            $preco = $this->servicoPrecos->consultar($produtoId);
            $this->cachePrecos[$produtoId] = $preco;
        }
        $estoqueAtual = $this->banco->buscarEstoque($produtoId);
        $novoEstoque = $estoqueAtual - $quantidadeVendida;
        $valorTotal = $novoEstoque * $preco;
        $this->banco->atualizarEstoque($produtoId, $novoEstoque, $valorTotal);
        return $novoEstoque;
    }
}

// Fake em memória — também atua como builder do estado inicial (comEstoque).
final class BancoEstoqueFake implements ConexaoBanco
{
    private array $estoques = [];
    public ?float $ultimoValorTotal = null;

    public function comEstoque(string $produtoId, int $quantidade): self
    {
        $this->estoques[$produtoId] = $quantidade;
        return $this;
    }

    public function buscarEstoque(string $produtoId): int
    {
        return $this->estoques[$produtoId] ?? 0;
    }

    public function atualizarEstoque(string $produtoId, int $quantidade, float $valorTotal): void
    {
        $this->estoques[$produtoId] = $quantidade;
        $this->ultimoValorTotal = $valorTotal;
    }
}

final class ServicoPrecoStub implements ServicoPreco
{
    public int $chamadas = 0;

    public function __construct(private float $preco)
    {
    }

    public function consultar(string $produtoId): float
    {
        $this->chamadas++;
        return $this->preco;
    }
}

final class GerenciadorEstoqueTest extends PHPUnit\Framework\TestCase
{
    public function testCaracterizacaoRecalculoComEstoqueSuficiente(): void
    {
        // Teste de caracterização: congela o comportamento atual do legado
        // como oráculo, sem julgar se a regra de negócio está correta.
        $banco = (new BancoEstoqueFake())->comEstoque('PROD1', 100);
        $precos = new ServicoPrecoStub(preco: 10.0);
        $gerenciador = new GerenciadorEstoque($banco, $precos);

        $novoEstoque = $gerenciador->recalcularEstoque('PROD1', 30);

        $this->assertSame(70, $novoEstoque);
        $this->assertSame(700.0, $banco->ultimoValorTotal);
    }

    public function testRecalculoComVendaMaiorQueEstoqueGeraSaldoNegativo(): void
    {
        // Caso de borda descoberto durante a caracterização: o legado não
        // valida estoque insuficiente. Documentamos o comportamento atual;
        // decidir se corrige é uma decisão de produto, não deste teste.
        $banco = (new BancoEstoqueFake())->comEstoque('PROD1', 10);
        $precos = new ServicoPrecoStub(preco: 5.0);
        $gerenciador = new GerenciadorEstoque($banco, $precos);

        $novoEstoque = $gerenciador->recalcularEstoque('PROD1', 30);

        $this->assertSame(-20, $novoEstoque);
    }

    public function testRecalculoReaproveitaPrecoEmCacheNaSegundaChamada(): void
    {
        $banco = (new BancoEstoqueFake())->comEstoque('PROD1', 100);
        $precos = new ServicoPrecoStub(preco: 10.0);
        $gerenciador = new GerenciadorEstoque($banco, $precos);

        $gerenciador->recalcularEstoque('PROD1', 10);
        $gerenciador->recalcularEstoque('PROD1', 5);

        $this->assertSame(1, $precos->chamadas);
    }
}
