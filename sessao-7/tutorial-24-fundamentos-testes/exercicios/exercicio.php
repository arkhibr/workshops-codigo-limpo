<?php
// EXERCÍCIO 24 — Fundamentos de Testes de Unidade (PHPUnit 11)
// Tempo estimado: 15 minutos
//
// INSTRUÇÕES:
//   A suíte abaixo testa calcularComissao() mas tem 4 problemas:
//     1. Nomes que não dizem o que é testado (testCalculo, testValor)
//     2. Um teste verificando comportamentos não relacionados
//     3. Estado estático compartilhado entre testes (ordem importa)
//     4. Dependência do relógio real (não-determinístico)
//
//   Refatore aplicando AAA, FIRST e nomes comportamentais. Use
//   #[DataProvider] para as variações de valor/meta.
//   Execute: vendor/bin/phpunit exercicio.php (deve passar antes e depois da refatoração)

function calcularComissao(float $valorVenda, bool $metaBatida): float
{
    return $metaBatida ? $valorVenda * 0.08 : $valorVenda * 0.03;
}

final class ComissaoTestRuim extends PHPUnit\Framework\TestCase
{
    private static ?float $ultimaComissao = null;

    public function testCalculo(): void
    {
        // dois comportamentos não relacionados no mesmo teste
        $this->assertSame(80.0, calcularComissao(1000.0, true));
        $this->assertSame(30.0, calcularComissao(1000.0, false));
    }

    public function testValor(): void
    {
        // depende de estado estático deixado por outro teste — ordem importa
        self::$ultimaComissao = calcularComissao(500.0, true);
        $this->assertSame(40.0, self::$ultimaComissao);
    }

    public function testComissao(): void
    {
        // nome genérico; não-determinístico: depende do dia real da execução
        $hoje = new DateTime();
        $metaBatida = (int) $hoje->format('N') === 1; // segunda-feira
        $resultado = calcularComissao(1000.0, $metaBatida);
        $this->assertGreaterThanOrEqual(0.0, $resultado);
    }
}
