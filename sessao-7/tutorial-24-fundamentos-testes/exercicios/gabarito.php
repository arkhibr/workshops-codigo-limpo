<?php
// GABARITO 24 — Fundamentos de Testes de Unidade (PHPUnit 11)
// Suíte refatorada: AAA explícito, nomes comportamentais, sem estado
// compartilhado, sem dependência do relógio real.
// Execute: vendor/bin/phpunit gabarito.php

function calcularComissao(float $valorVenda, bool $metaBatida): float
{
    return $metaBatida ? $valorVenda * 0.08 : $valorVenda * 0.03;
}

final class CalculoComissaoTest extends PHPUnit\Framework\TestCase
{
    public function testPaga8PorcentoQuandoBateMeta(): void
    {
        // Arrange
        $valorVenda = 1000.0;
        // Act
        $resultado = calcularComissao($valorVenda, metaBatida: true);
        // Assert
        $this->assertSame(80.0, $resultado);
    }

    public function testPaga3PorcentoQuandoNaoBateMeta(): void
    {
        $resultado = calcularComissao(1000.0, metaBatida: false);
        $this->assertSame(30.0, $resultado);
    }

    public static function valoresComissao(): array
    {
        return [
            'valor zero com meta batida' => [0.0, true, 0.0],
            'valor zero sem meta batida' => [0.0, false, 0.0],
            'meta batida' => [500.0, true, 40.0],
            'meta nao batida' => [500.0, false, 15.0],
            'valor alto com meta batida' => [10_000.0, true, 800.0],
        ];
    }

    #[PHPUnit\Framework\Attributes\DataProvider('valoresComissao')]
    public function testCalculaComissaoParaVariosValores(float $valorVenda, bool $metaBatida, float $esperado): void
    {
        // Arrange: valores vêm do provider
        // Act
        $resultado = calcularComissao($valorVenda, $metaBatida);
        // Assert
        $this->assertSame($esperado, $resultado);
    }
}
