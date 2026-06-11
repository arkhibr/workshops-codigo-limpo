<?php
// GABARITO 17 PHP 8.1+ — Padrões de Criação
// Referência: Design Patterns (GoF), Cap. 3
//
// Execute: php gabarito.php

// ─── Classe (mesma do exercício) ──────────────────────────────────────────────

class Contrato
{
    public function __construct(
        public readonly string  $tipo,
        public readonly float   $valorMensal,
        public readonly int     $vigenciaMeses,
        public readonly string  $contratante,
        public readonly ?string $objeto       = null,
        public readonly ?string $endereco     = null,
        public readonly ?string $fornecedorId = null,
        public readonly ?int    $prazoEntrega = null,
        public readonly ?string $observacoes  = null,
    ) {}
}


// ─── Passo 3: Factory registrável ────────────────────────────────────────────

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

FabricaContrato::registrar('servico', fn(array $d) => new Contrato(
    tipo:          'servico',
    valorMensal:   $d['valor_mensal'],
    vigenciaMeses: $d['vigencia_meses'],
    contratante:   $d['contratante'],
    objeto:        $d['objeto'] ?? 'Serviços gerais',
));
FabricaContrato::registrar('locacao', fn(array $d) => new Contrato(
    tipo:          'locacao',
    valorMensal:   $d['valor_mensal'],
    vigenciaMeses: $d['vigencia_meses'],
    contratante:   $d['contratante'],
    objeto:        $d['objeto'] ?? null,
    endereco:      $d['endereco'] ?? null,
));
FabricaContrato::registrar('fornecimento', fn(array $d) => new Contrato(
    tipo:          'fornecimento',
    valorMensal:   $d['valor_mensal'],
    vigenciaMeses: $d['vigencia_meses'],
    contratante:   $d['contratante'],
    fornecedorId:  $d['fornecedor_id'] ?? null,
    prazoEntrega:  $d['prazo_entrega'] ?? null,
));


// ─── Passo 4: Builder ─────────────────────────────────────────────────────────

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

    public function construir(): Contrato
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
        return new Contrato(
            tipo:          'servico',
            valorMensal:   $this->valorMensal,
            vigenciaMeses: $this->vigenciaMeses,
            contratante:   $this->contratante,
            objeto:        $this->objeto,
        );
    }
}


// ─── Verificação ──────────────────────────────────────────────────────────────

echo "=== Gabarito 17 PHP — Factory Method + Builder ===" . PHP_EOL . PHP_EOL;

// Passo 3: factory registrável
$servico = FabricaContrato::criar('servico', [
    'valor_mensal' => 5000.0, 'vigencia_meses' => 12, 'contratante' => 'EMP-001'
]);
assert($servico instanceof Contrato);
assert($servico->valorMensal * $servico->vigenciaMeses === 60000.0);
echo "OK: Passo 3 — FabricaContrato::criar: {$servico->tipo} R\${$servico->valorMensal}/mês" . PHP_EOL;

try {
    FabricaContrato::criar('desconhecido', ['valor_mensal' => 1.0, 'vigencia_meses' => 1, 'contratante' => 'X']);
    echo "FALHOU: deveria rejeitar tipo não registrado" . PHP_EOL;
} catch (\InvalidArgumentException $e) {
    echo "OK: Passo 3 — tipo desconhecido rejeitado com InvalidArgumentException" . PHP_EOL;
}

// Passo 3: novo tipo sem alterar FabricaContrato
FabricaContrato::registrar('obras_civil', fn(array $d) => new Contrato(
    tipo:        'obras_civil',
    valorMensal: $d['valor_mensal'],
    vigenciaMeses: $d['vigencia_meses'],
    contratante: $d['contratante'],
    observacoes: $d['responsavel_tecnico'] ?? null,
));
$obras = FabricaContrato::criar('obras_civil', [
    'valor_mensal' => 25000.0, 'vigencia_meses' => 8,
    'contratante' => 'EMP-004', 'responsavel_tecnico' => 'Eng. Silva CREA-12345'
]);
assert($obras instanceof Contrato);
echo "OK: Passo 3 — novo tipo registrado sem alterar FabricaContrato: {$obras->tipo}" . PHP_EOL;

echo PHP_EOL;

// Passo 4: builder
$c = (new ConstruirContratoServico())
    ->comValorMensal(5000.0)
    ->comVigencia(12)
    ->comContratante('EMP-001')
    ->construir();
assert($c instanceof Contrato);
assert($c->valorMensal * $c->vigenciaMeses === 60000.0);
echo "OK: Passo 4 — builder fluente: {$c->tipo} R\${$c->valorMensal}/mês × {$c->vigenciaMeses} meses" . PHP_EOL;

try {
    (new ConstruirContratoServico())->comValorMensal(5000.0)->construir();
    echo "FALHOU: deveria rejeitar sem vigencia_meses" . PHP_EOL;
} catch (\RuntimeException $e) {
    echo "OK: Passo 4 — rejeita construir() sem vigencia_meses" . PHP_EOL;
}

try {
    (new ConstruirContratoServico())->comVigencia(12)->construir();
    echo "FALHOU: deveria rejeitar sem valor_mensal" . PHP_EOL;
} catch (\RuntimeException $e) {
    echo "OK: Passo 4 — rejeita construir() sem valor_mensal" . PHP_EOL;
}

try {
    (new ConstruirContratoServico())->comValorMensal(5000.0)->comVigencia(12)->construir();
    echo "FALHOU: deveria rejeitar sem contratante" . PHP_EOL;
} catch (\RuntimeException $e) {
    echo "OK: Passo 4 — rejeita construir() sem contratante" . PHP_EOL;
}
