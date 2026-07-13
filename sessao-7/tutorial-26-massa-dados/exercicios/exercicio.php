<?php
// EXERCÍCIO 26 — Massa de Dados para Testes (PHPUnit 11)
// Tempo estimado: 15 minutos
//
// INSTRUÇÕES:
//   Os testes abaixo duplicam um literal gigante de nota fiscal em cada
//   teste, mudando só um campo por vez. Extraia um NotaFiscalBuilder com
//   valores padrão sensatos e reduza cada teste ao que é relevante.
//   Execute: vendor/bin/phpunit exercicio.php

function calcularImposto(array $notaFiscal): float
{
    $totalItens = array_sum(array_column($notaFiscal['itens'], 'valor'));
    return $totalItens * $notaFiscal['aliquota'];
}

final class CalcularImpostoTestRuim extends PHPUnit\Framework\TestCase
{
    public function testCalculaImpostoComAliquotaPadrao(): void
    {
        $nota = [
            'numero' => 'NF-001',
            'emitente' => ['cnpj' => '11.111.111/0001-11', 'razaoSocial' => 'Empresa A'],
            'destinatario' => ['cpf' => '111.111.111-11', 'nome' => 'Cliente A'],
            'itens' => [['descricao' => 'Produto X', 'valor' => 1000.0]],
            'aliquota' => 0.18,
            'chaveAcesso' => '35260100000000000000000000000000000000000000',
        ];
        $this->assertSame(180.0, calcularImposto($nota));
    }

    public function testCalculaImpostoComAliquotaReduzida(): void
    {
        $nota = [
            'numero' => 'NF-002',
            'emitente' => ['cnpj' => '11.111.111/0001-11', 'razaoSocial' => 'Empresa A'],
            'destinatario' => ['cpf' => '111.111.111-11', 'nome' => 'Cliente A'],
            'itens' => [['descricao' => 'Produto X', 'valor' => 1000.0]],
            'aliquota' => 0.12,
            'chaveAcesso' => '35260100000000000000000000000000000000000001',
        ];
        $this->assertSame(120.0, calcularImposto($nota));
    }
}
