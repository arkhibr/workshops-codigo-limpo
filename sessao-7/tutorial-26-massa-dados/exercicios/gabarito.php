<?php
// GABARITO 26 — Massa de Dados para Testes (PHPUnit 11)
// NotaFiscalBuilder centraliza valores padrão sensatos (emitente,
// destinatario, item e aliquota fixos) e expõe comItem(descricao, valor) e
// comAliquota(valor) para sobrescrever só o que cada teste precisa. Os dois
// testes ficam reduzidos a poucas linhas, declarando apenas a alíquota que varia.
// Execute: vendor/bin/phpunit gabarito.php

final class NotaFiscal
{
    /** @param array<int, array{descricao: string, valor: float}> $itens */
    public function __construct(
        public string $numero = 'NF-000',
        public array $emitente = ['cnpj' => '11.111.111/0001-11', 'razaoSocial' => 'Empresa A'],
        public array $destinatario = ['cpf' => '111.111.111-11', 'nome' => 'Cliente A'],
        public array $itens = [['descricao' => 'Produto X', 'valor' => 1000.0]],
        public float $aliquota = 0.18,
        public string $chaveAcesso = '35260100000000000000000000000000000000000000',
    ) {
    }
}

final class NotaFiscalBuilder
{
    private NotaFiscal $nota;

    public function __construct()
    {
        $this->nota = new NotaFiscal();
    }

    public function comItem(string $descricao, float $valor): self
    {
        $this->nota->itens = [['descricao' => $descricao, 'valor' => $valor]];
        return $this;
    }

    public function comAliquota(float $valor): self
    {
        $this->nota->aliquota = $valor;
        return $this;
    }

    public function construir(): NotaFiscal
    {
        return $this->nota;
    }
}

function calcularImposto(NotaFiscal $notaFiscal): float
{
    $totalItens = array_sum(array_column($notaFiscal->itens, 'valor'));
    return $totalItens * $notaFiscal->aliquota;
}

final class CalcularImpostoTest extends PHPUnit\Framework\TestCase
{
    public function testCalculaImpostoComAliquotaPadrao(): void
    {
        $nota = (new NotaFiscalBuilder())->comItem('Produto X', valor: 1000.0)->construir();
        $this->assertSame(180.0, calcularImposto($nota));
    }

    public function testCalculaImpostoComAliquotaReduzida(): void
    {
        $nota = (new NotaFiscalBuilder())->comItem('Produto X', valor: 1000.0)->comAliquota(0.12)->construir();
        $this->assertSame(120.0, calcularImposto($nota));
    }
}
