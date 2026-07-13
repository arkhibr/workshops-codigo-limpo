<?php
// GABARITO 25 — Dublês de Teste (PHPUnit 11)
// Seam via construtor: ServicoEntrega(ApiCep $apiCep, RepositorioEndereco $repositorio).
// ApiCepStub devolve cidade/uf fixos; RepositorioEnderecoFake guarda em
// memória e expõe foiSalvo() para inspeção. Sem usleep — roda em milissegundos.
// Execute: vendor/bin/phpunit gabarito.php

interface ApiCep
{
    public function consultar(string $cep): array;
}

interface RepositorioEndereco
{
    public function salvar(string $pedidoId, array $endereco): void;
}

final class ServicoEntrega
{
    public function __construct(
        private ApiCep $apiCep,
        private RepositorioEndereco $repositorio,
    ) {
    }

    public function confirmarEndereco(string $pedidoId, string $cep): array
    {
        $endereco = $this->apiCep->consultar($cep);
        $this->repositorio->salvar($pedidoId, $endereco);
        return $endereco;
    }
}

// Stub: devolve resposta fixa e pré-programada, sem chamada de rede real.
final class ApiCepStub implements ApiCep
{
    public function __construct(
        private string $cidade = 'São Paulo',
        private string $uf = 'SP',
    ) {
    }

    public function consultar(string $cep): array
    {
        return ['cep' => $cep, 'cidade' => $this->cidade, 'uf' => $this->uf];
    }
}

// Fake: implementação funcional leve, em memória — sem banco real.
final class RepositorioEnderecoFake implements RepositorioEndereco
{
    private array $enderecos = [];

    public function salvar(string $pedidoId, array $endereco): void
    {
        $this->enderecos[$pedidoId] = $endereco;
    }

    public function foiSalvo(string $pedidoId): bool
    {
        return isset($this->enderecos[$pedidoId]);
    }
}

final class ServicoEntregaTest extends PHPUnit\Framework\TestCase
{
    public function testConfirmaEnderecoRetornaUfDoCepConsultado(): void
    {
        // Arrange
        $apiCep = new ApiCepStub(cidade: 'São Paulo', uf: 'SP');
        $repositorio = new RepositorioEnderecoFake();
        $servico = new ServicoEntrega($apiCep, $repositorio);

        // Act
        $resultado = $servico->confirmarEndereco('P001', '01000-000');

        // Assert
        $this->assertSame('SP', $resultado['uf']);
    }

    public function testConfirmaEnderecoSalvaEnderecoNoRepositorio(): void
    {
        $apiCep = new ApiCepStub();
        $repositorio = new RepositorioEnderecoFake();
        $servico = new ServicoEntrega($apiCep, $repositorio);

        $servico->confirmarEndereco('P002', '20000-000');

        $this->assertTrue($repositorio->foiSalvo('P002'));
    }

    public function testConfirmaEnderecoUsaCidadeConfiguradaNoStub(): void
    {
        $apiCep = new ApiCepStub(cidade: 'Rio de Janeiro', uf: 'RJ');
        $repositorio = new RepositorioEnderecoFake();
        $servico = new ServicoEntrega($apiCep, $repositorio);

        $resultado = $servico->confirmarEndereco('P003', '20000-000');

        $this->assertSame('Rio de Janeiro', $resultado['cidade']);
    }
}
