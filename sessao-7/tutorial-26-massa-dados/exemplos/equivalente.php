<?php
// equivalente.php — Massa de Dados para Testes em PHPUnit 11
// Execute: vendor/bin/phpunit equivalente.php

final class Pedido
{
    /** @param array<int, array{produto: string, preco: float, quantidade: int}> $itens */
    public function __construct(
        public string $id = 'P000',
        public array $itens = [['produto' => 'Item Padrão', 'preco' => 100.0, 'quantidade' => 1]],
        public ?string $cupomDesconto = null,
        public string $status = 'pendente',
    ) {
    }
}

// Test Data Builder: valores padrão sensatos, sobrescreve só o relevante.
final class PedidoBuilder
{
    private Pedido $pedido;

    public function __construct()
    {
        $this->pedido = new Pedido();
    }

    public function comItem(string $produto, float $preco, int $quantidade = 1): self
    {
        $this->pedido->itens = [['produto' => $produto, 'preco' => $preco, 'quantidade' => $quantidade]];
        return $this;
    }

    public function comCupom(string $codigo): self
    {
        $this->pedido->cupomDesconto = $codigo;
        return $this;
    }

    public function construir(): Pedido
    {
        return $this->pedido;
    }
}

function aplicarCupom(Pedido $pedido, ?string $codigo): Pedido
{
    if ($codigo === 'PROMO10') {
        foreach ($pedido->itens as &$item) {
            $item['preco'] = round($item['preco'] * 0.9, 2);
        }
        unset($item);
    }
    return $pedido;
}

// Ruim: literal gigante duplicado em cada teste — só o cupom importa aqui,
// mas o teste repete cliente, endereço e forma de pagamento por inteiro.
final class AplicarCupomTestRuim extends PHPUnit\Framework\TestCase
{
    public function testCupomAplicaDesconto(): void
    {
        $pedido = new Pedido(
            id: 'P001',
            itens: [['produto' => 'Notebook', 'preco' => 3000.0, 'quantidade' => 1]],
            cupomDesconto: 'PROMO10',
        );
        $resultado = aplicarCupom($pedido, 'PROMO10');
        $this->assertSame(2700.0, $resultado->itens[0]['preco']);
    }

    public function testPedidoSemCupomMantemPreco(): void
    {
        $pedido = new Pedido(
            id: 'P002',
            itens: [['produto' => 'Notebook', 'preco' => 3000.0, 'quantidade' => 1]],
            cupomDesconto: null,
        );
        $resultado = aplicarCupom($pedido, null);
        $this->assertSame(3000.0, $resultado->itens[0]['preco']);
    }
}

// ClienteFactory: gera dados de cliente com fakerphp/faker — nunca literais
// fixos e repetitivos.
final class ClienteFactory
{
    /** @return array{nome: string, email: string, cpf: string} */
    public static function criar(): array
    {
        $faker = Faker\Factory::create('pt_BR');
        return [
            'nome' => $faker->name(),
            'email' => $faker->email(),
            'cpf' => $faker->cpf(),
        ];
    }
}

// Bom: PedidoBuilder fluente + ClienteFactory com Faker.
final class AplicarCupomTest extends PHPUnit\Framework\TestCase
{
    public function testCupomAplica10PorCentoDeDesconto(): void
    {
        $pedido = (new PedidoBuilder())->comItem('Notebook', preco: 3000.0)->comCupom('PROMO10')->construir();

        $resultado = aplicarCupom($pedido, 'PROMO10');

        $this->assertSame(2700.0, $resultado->itens[0]['preco']);
    }

    public function testPedidoSemCupomMantemPrecoOriginal(): void
    {
        $pedido = (new PedidoBuilder())->comItem('Notebook', preco: 3000.0)->construir();

        $resultado = aplicarCupom($pedido, null);

        $this->assertSame(3000.0, $resultado->itens[0]['preco']);
    }

    public function testClienteGeradoPelaFactoryTemEmailValido(): void
    {
        $cliente = ClienteFactory::criar();
        $this->assertStringContainsString('@', $cliente['email']);
    }
}
