<?php
// EXERCÍCIO 25 — Dublês de Teste (PHPUnit 11)
// Tempo estimado: 15 minutos
//
// INSTRUÇÕES:
//   ServicoEntrega abaixo depende de ApiCepReal (chamada de rede real, lenta)
//   e RepositorioEnderecoReal (banco real). O teste fornecido não usa nenhum
//   double e é lento e frágil.
//
//   1. Crie um Stub para a API de CEP (resposta fixa) com createStub().
//   2. Crie um Fake para o repositório de endereço (em memória).
//   3. Reescreva o teste para não depender de infraestrutura real.
//   Execute: vendor/bin/phpunit exercicio.php

final class ApiCepReal
{
    public function consultar(string $cep): array
    {
        usleep(300_000);
        return ['cep' => $cep, 'cidade' => 'São Paulo', 'uf' => 'SP'];
    }
}

final class RepositorioEnderecoReal
{
    public function salvar(string $pedidoId, array $endereco): void
    {
        usleep(200_000);
    }
}

final class ServicoEntrega
{
    private ApiCepReal $apiCep;
    private RepositorioEnderecoReal $repositorio;

    public function __construct()
    {
        $this->apiCep = new ApiCepReal();
        $this->repositorio = new RepositorioEnderecoReal();
    }

    public function confirmarEndereco(string $pedidoId, string $cep): array
    {
        $endereco = $this->apiCep->consultar($cep);
        $this->repositorio->salvar($pedidoId, $endereco);
        return $endereco;
    }
}

final class ServicoEntregaTestRuim extends PHPUnit\Framework\TestCase
{
    public function testConfirmaEnderecoSemNenhumDouble(): void
    {
        // lento: ~0.5s simulando chamadas reais
        $servico = new ServicoEntrega();
        $resultado = $servico->confirmarEndereco('P001', '01000-000');
        $this->assertSame('SP', $resultado['uf']);
    }
}
