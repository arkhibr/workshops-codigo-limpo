<?php
// equivalente.php — Fundamentos de Testes de Unidade em PHPUnit 11
// Execute: vendor/bin/phpunit equivalente.php

function calcularDesconto(float $valor, bool $clienteVip): float
{
    return $clienteVip ? $valor * 0.9 : $valor;
}

function calcularFrete(float $valor): float
{
    return $valor > 200 ? 0.0 : 25.0;
}

// Ruim: nome não descreve comportamento, duas asserções não relacionadas
final class CalculoTestRuim extends PHPUnit\Framework\TestCase
{
    public function testCalculo(): void
    {
        $this->assertSame(90.0, calcularDesconto(100.0, true));
        $this->assertSame(25.0, calcularFrete(100.0));
    }
}

// Bom: AAA explícito, nomes comportamentais, parametrização via DataProvider
final class CalculoDescontoTest extends PHPUnit\Framework\TestCase
{
    public static function valoresDesconto(): array
    {
        return [
            'sem desconto para valor zero' => [0.0, true, 0.0],
            'sem desconto para cliente comum' => [100.0, false, 100.0],
            'desconto vip de 10 por cento' => [200.0, true, 180.0],
        ];
    }

    #[PHPUnit\Framework\Attributes\DataProvider('valoresDesconto')]
    public function testCalculaDescontoParaVariosValores(float $valor, bool $vip, float $esperado): void
    {
        // Arrange: valores vêm do provider
        // Act
        $resultado = calcularDesconto($valor, $vip);
        // Assert
        $this->assertSame($esperado, $resultado);
    }
}
