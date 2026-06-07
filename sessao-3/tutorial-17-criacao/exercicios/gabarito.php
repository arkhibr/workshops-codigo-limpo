<?php
// GABARITO 17 PHP 8.1+ — Padrões de Criação
// Referência: Design Patterns (GoF), Cap. 3
//
// SOLUÇÃO:
//   1. Factory Method: FabricaContrato com registrar/criar.
//   2. Builder: ConstruirContratoServico com interface fluente.
//
// Execute: php gabarito.php

// ─── Factory Method ───────────────────────────────────────────────────────────

interface Contrato
{
    public function descricao(): string;
    public function getValorMensal(): float;
    public function getVigenciaMeses(): int;
    public function getContratante(): string;
    public function getValorTotal(): float;
}

abstract class ContratoBase implements Contrato
{
    public function __construct(
        protected readonly float  $valorMensal,
        protected readonly int    $vigenciaMeses,
        protected readonly string $contratante,
    ) {
        if ($valorMensal <= 0) {
            throw new \InvalidArgumentException("Valor mensal deve ser positivo, recebido: $valorMensal");
        }
        if ($vigenciaMeses <= 0) {
            throw new \InvalidArgumentException("Vigência deve ser positiva, recebida: $vigenciaMeses");
        }
    }

    public function getValorMensal(): float    { return $this->valorMensal; }
    public function getVigenciaMeses(): int     { return $this->vigenciaMeses; }
    public function getContratante(): string    { return $this->contratante; }
    public function getValorTotal(): float      { return $this->valorMensal * $this->vigenciaMeses; }
}

class ContratoServico extends ContratoBase
{
    public function __construct(
        float  $valorMensal,
        int    $vigenciaMeses,
        string $contratante,
        public readonly string $objeto,
    ) {
        parent::__construct($valorMensal, $vigenciaMeses, $contratante);
    }

    public function descricao(): string
    {
        return sprintf(
            'Serviço: %s | %s | R$%.2f/mês × %d meses',
            $this->objeto, $this->contratante, $this->valorMensal, $this->vigenciaMeses
        );
    }
}

class ContratoLocacao extends ContratoBase
{
    public function __construct(
        float  $valorMensal,
        int    $vigenciaMeses,
        string $contratante,
        public readonly string $objeto,
        public readonly string $endereco,
    ) {
        parent::__construct($valorMensal, $vigenciaMeses, $contratante);
    }

    public function descricao(): string
    {
        return sprintf(
            'Locação: %s | %s | %s | R$%.2f/mês × %d meses',
            $this->objeto, $this->endereco, $this->contratante,
            $this->valorMensal, $this->vigenciaMeses
        );
    }
}

class ContratoFornecimento extends ContratoBase
{
    public function __construct(
        float  $valorMensal,
        int    $vigenciaMeses,
        string $contratante,
        public readonly string $fornecedorId,
        public readonly int    $prazoEntrega,
    ) {
        parent::__construct($valorMensal, $vigenciaMeses, $contratante);
    }

    public function descricao(): string
    {
        return sprintf(
            'Fornecimento: %s | prazo %dd | R$%.2f/mês × %d meses',
            $this->fornecedorId, $this->prazoEntrega, $this->valorMensal, $this->vigenciaMeses
        );
    }
}

class FabricaContrato
{
    /** @var array<string, callable> */
    private static array $registro = [];

    public static function registrar(string $tipo, callable $fabrica): void
    {
        self::$registro[$tipo] = $fabrica;
    }

    public static function criar(string $tipo, array $dados): Contrato
    {
        if (!isset(self::$registro[$tipo])) {
            $disponiveis = implode(', ', array_keys(self::$registro));
            throw new \InvalidArgumentException(
                "Tipo '$tipo' não registrado. Disponíveis: $disponiveis"
            );
        }
        return (self::$registro[$tipo])($dados);
    }
}

FabricaContrato::registrar('servico', fn(array $d) => new ContratoServico(
    $d['valor_mensal'], $d['vigencia_meses'], $d['contratante'],
    $d['objeto'] ?? 'Serviços gerais'
));
FabricaContrato::registrar('locacao', fn(array $d) => new ContratoLocacao(
    $d['valor_mensal'], $d['vigencia_meses'], $d['contratante'],
    $d['objeto'] ?? '', $d['endereco'] ?? ''
));
FabricaContrato::registrar('fornecimento', fn(array $d) => new ContratoFornecimento(
    $d['valor_mensal'], $d['vigencia_meses'], $d['contratante'],
    $d['fornecedor_id'] ?? '', $d['prazo_entrega'] ?? 30
));


// ─── Builder ──────────────────────────────────────────────────────────────────

class ConstruirContratoServico
{
    private ?float  $valorMensal   = null;
    private ?int    $vigenciaMeses = null;
    private ?string $contratante   = null;
    private string  $objeto        = 'Serviços gerais';

    public function comValorMensal(float $valor): static
    {
        $this->valorMensal = $valor;
        return $this;
    }

    public function comVigencia(int $meses): static
    {
        $this->vigenciaMeses = $meses;
        return $this;
    }

    public function comContratante(string $contratante): static
    {
        $this->contratante = $contratante;
        return $this;
    }

    public function comObjeto(string $objeto): static
    {
        $this->objeto = $objeto;
        return $this;
    }

    public function construir(): ContratoServico
    {
        if ($this->valorMensal === null) {
            throw new \RuntimeException('valor_mensal é obrigatório');
        }
        if ($this->vigenciaMeses === null) {
            throw new \RuntimeException('vigencia_meses é obrigatório');
        }
        if ($this->contratante === null) {
            throw new \RuntimeException('contratante é obrigatório');
        }
        return new ContratoServico(
            $this->valorMensal, $this->vigenciaMeses,
            $this->contratante, $this->objeto
        );
    }
}


// ─── Verificação ──────────────────────────────────────────────────────────────

echo "=== Gabarito 17 PHP — Factory Method + Builder ===" . PHP_EOL . PHP_EOL;

// Factory
$servico = FabricaContrato::criar('servico', [
    'valor_mensal' => 5000.0, 'vigencia_meses' => 12,
    'contratante' => 'EMP-001', 'objeto' => 'Consultoria em TI'
]);
assert($servico instanceof ContratoServico);
assert($servico->getValorTotal() === 60000.0);
echo "OK: Factory — ContratoServico criado via FabricaContrato" . PHP_EOL;
echo "  " . $servico->descricao() . PHP_EOL;

$locacao = FabricaContrato::criar('locacao', [
    'valor_mensal' => 3500.0, 'vigencia_meses' => 24,
    'contratante' => 'EMP-002', 'objeto' => 'Sala comercial 40m²',
    'endereco' => 'Av. Paulista, 1000 — SP'
]);
assert($locacao instanceof ContratoLocacao);
echo "OK: Factory — ContratoLocacao criado via FabricaContrato" . PHP_EOL;

try {
    FabricaContrato::criar('obras_civil', ['valor_mensal' => 1000.0, 'vigencia_meses' => 6, 'contratante' => 'X']);
    echo "FALHOU: Factory — deveria rejeitar tipo não registrado" . PHP_EOL;
} catch (\InvalidArgumentException $e) {
    echo "OK: Factory — tipo desconhecido rejeitado com InvalidArgumentException" . PHP_EOL;
}

echo PHP_EOL;

// Builder
$contrato = (new ConstruirContratoServico())
    ->comValorMensal(5000.0)
    ->comVigencia(12)
    ->comContratante('EMP-001')
    ->comObjeto('Desenvolvimento de software')
    ->construir();
assert($contrato instanceof ContratoServico);
assert($contrato->getValorTotal() === 60000.0);
echo "OK: Builder — ContratoServico construído com encadeamento fluente" . PHP_EOL;
echo "  " . $contrato->descricao() . PHP_EOL;

try {
    (new ConstruirContratoServico())->comValorMensal(5000.0)->construir();
    echo "FALHOU: Builder — deveria rejeitar contrato sem vigencia_meses" . PHP_EOL;
} catch (\RuntimeException $e) {
    echo "OK: Builder — rejeita contrato incompleto — {$e->getMessage()}" . PHP_EOL;
}
