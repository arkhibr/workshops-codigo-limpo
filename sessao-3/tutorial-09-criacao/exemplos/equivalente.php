<?php
// EQUIVALENTE PHP 8.1+ — Padrões de Criação
// Referência: Design Patterns (GoF), Cap. 3 — Creational Patterns
// Execute: php equivalente.php

// ─────────────────────────────────────────────────────────────────────────────
// ❌ Ruim — construtor gordo com 10 parâmetros + if/else de instanciação
// ─────────────────────────────────────────────────────────────────────────────

class DocumentoCobrancaRuim
{
    public function __construct(
        public readonly string  $tipo,
        public readonly float   $valor,
        public readonly string  $vencimento,
        public readonly string  $beneficiario,
        public readonly ?string $codigoBarras = null,   // só boleto
        public readonly ?string $chavePix     = null,   // só pix
        public readonly ?string $numeroNf     = null,   // só nota fiscal
        public readonly ?string $cfop         = null,   // só nota fiscal
        public readonly ?string $descricao    = null,
        public readonly ?string $observacoes  = null,
    ) {}
}

function criarDocumentoRuim(string $tipo, array $dados): DocumentoCobrancaRuim
{
    // Adicionar 'TED' exige alterar esta função
    if ($tipo === 'boleto') {
        return new DocumentoCobrancaRuim(
            tipo:         'boleto',
            valor:        $dados['valor'],
            vencimento:   $dados['vencimento'],
            beneficiario: $dados['beneficiario'],
            codigoBarras: $dados['codigo_barras'] ?? '9999.99999 99999.999999',
        );
    } elseif ($tipo === 'pix') {
        return new DocumentoCobrancaRuim(
            tipo:         'pix',
            valor:        $dados['valor'],
            vencimento:   $dados['vencimento'],
            beneficiario: $dados['beneficiario'],
            chavePix:     $dados['chave_pix'] ?? 'chave@exemplo.com.br',
        );
    } elseif ($tipo === 'nota_fiscal') {
        return new DocumentoCobrancaRuim(
            tipo:         'nota_fiscal',
            valor:        $dados['valor'],
            vencimento:   $dados['vencimento'],
            beneficiario: $dados['beneficiario'],
            numeroNf:     $dados['numero_nf'] ?? 'NF-000001',
            cfop:         $dados['cfop'] ?? '5102',
        );
    } else {
        throw new \InvalidArgumentException("Tipo desconhecido: $tipo");
    }
}


// ─────────────────────────────────────────────────────────────────────────────
// ✅ Bom — Factory Method + Builder
// ─────────────────────────────────────────────────────────────────────────────

interface DocumentoCobranca
{
    public function descricao(): string;
    public function getValor(): float;
    public function getVencimento(): string;
    public function getBeneficiario(): string;
}

class Boleto implements DocumentoCobranca
{
    public function __construct(
        private readonly float  $valor,
        private readonly string $vencimento,
        private readonly string $beneficiario,
        private readonly string $codigoBarras,
    ) {
        if ($valor <= 0) {
            throw new \InvalidArgumentException("Valor deve ser positivo, recebido: $valor");
        }
    }

    public function descricao(): string
    {
        return sprintf(
            'Boleto R$%.2f venc %s | %s',
            $this->valor, $this->vencimento, $this->codigoBarras
        );
    }

    public function getValor(): float       { return $this->valor; }
    public function getVencimento(): string  { return $this->vencimento; }
    public function getBeneficiario(): string { return $this->beneficiario; }
    public function getCodigoBarras(): string { return $this->codigoBarras; }
}

class Pix implements DocumentoCobranca
{
    public function __construct(
        private readonly float  $valor,
        private readonly string $vencimento,
        private readonly string $beneficiario,
        private readonly string $chavePix,
    ) {
        if ($valor <= 0) {
            throw new \InvalidArgumentException("Valor deve ser positivo, recebido: $valor");
        }
    }

    public function descricao(): string
    {
        return sprintf('Pix R$%.2f → %s', $this->valor, $this->chavePix);
    }

    public function getValor(): float        { return $this->valor; }
    public function getVencimento(): string   { return $this->vencimento; }
    public function getBeneficiario(): string { return $this->beneficiario; }
    public function getChavePix(): string     { return $this->chavePix; }
}

class NotaFiscal implements DocumentoCobranca
{
    public function __construct(
        private readonly float  $valor,
        private readonly string $vencimento,
        private readonly string $beneficiario,
        private readonly string $numeroNf,
        private readonly string $cfop,
    ) {
        if ($valor <= 0) {
            throw new \InvalidArgumentException("Valor deve ser positivo, recebido: $valor");
        }
    }

    public function descricao(): string
    {
        return sprintf('NF %s CFOP %s R$%.2f', $this->numeroNf, $this->cfop, $this->valor);
    }

    public function getValor(): float        { return $this->valor; }
    public function getVencimento(): string   { return $this->vencimento; }
    public function getBeneficiario(): string { return $this->beneficiario; }
    public function getNumeroNf(): string     { return $this->numeroNf; }
    public function getCfop(): string         { return $this->cfop; }
}

class FabricaDocumento
{
    /** @var array<string, callable> */
    private static array $registro = [];

    public static function registrar(string $tipo, callable $fabrica): void
    {
        self::$registro[$tipo] = $fabrica;
    }

    public static function criar(string $tipo, array $dados): DocumentoCobranca
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

FabricaDocumento::registrar('boleto', fn(array $d) => new Boleto(
    $d['valor'], $d['vencimento'], $d['beneficiario'],
    $d['codigo_barras'] ?? '0000.00000 00000.000000'
));
FabricaDocumento::registrar('pix', fn(array $d) => new Pix(
    $d['valor'], $d['vencimento'], $d['beneficiario'],
    $d['chave_pix'] ?? 'chave@exemplo.com.br'
));
FabricaDocumento::registrar('nota_fiscal', fn(array $d) => new NotaFiscal(
    $d['valor'], $d['vencimento'], $d['beneficiario'],
    $d['numero_nf'] ?? 'NF-000001', $d['cfop'] ?? '5102'
));


class ConstruirBoleto
{
    private ?float  $valor        = null;
    private ?string $vencimento   = null;
    private ?string $beneficiario = null;
    private string  $codigoBarras = '0000.00000 00000.000000';

    public function comValor(float $valor): static
    {
        $this->valor = $valor;
        return $this;
    }

    public function comVencimento(string $vencimento): static
    {
        $this->vencimento = $vencimento;
        return $this;
    }

    public function comBeneficiario(string $beneficiario): static
    {
        $this->beneficiario = $beneficiario;
        return $this;
    }

    public function comCodigoBarras(string $codigo): static
    {
        $this->codigoBarras = $codigo;
        return $this;
    }

    public function construir(): Boleto
    {
        if ($this->valor === null) {
            throw new \RuntimeException('valor é obrigatório');
        }
        if ($this->vencimento === null) {
            throw new \RuntimeException('vencimento é obrigatório');
        }
        if ($this->beneficiario === null) {
            throw new \RuntimeException('beneficiario é obrigatório');
        }
        return new Boleto($this->valor, $this->vencimento, $this->beneficiario, $this->codigoBarras);
    }
}


// ─────────────────────────────────────────────────────────────────────────────
// SINGLETON — registro central, instância única
// ─────────────────────────────────────────────────────────────────────────────
//
// Singleton controla QUANTAS instâncias existem (uma).
// SOLID controla O QUE cada classe faz e como se relaciona com outras.
// A forma SOLID de usar Singleton é injetá-lo via DIP — o consumidor
// não chama getInstance() internamente; recebe via construtor.

class RegistroDocumentos
{
    private static ?self $instancia = null;

    /** @var array<string, callable> */
    private array $registro = [];

    private function __construct() {}

    public static function getInstance(): static
    {
        if (static::$instancia === null) {
            static::$instancia = new static();
        }
        return static::$instancia;
    }

    public function registrar(string $tipo, callable $fabrica): void
    {
        $this->registro[$tipo] = $fabrica;
    }

    public function criar(string $tipo, array $dados): DocumentoCobranca
    {
        if (!isset($this->registro[$tipo])) {
            $disponiveis = implode(', ', array_keys($this->registro));
            throw new \InvalidArgumentException(
                "Tipo '$tipo' não registrado. Disponíveis: $disponiveis"
            );
        }
        return ($this->registro[$tipo])($dados);
    }

    public function tiposRegistrados(): array
    {
        return array_keys($this->registro);
    }

    public static function resetar(): void
    {
        static::$instancia = null;
    }
}

class ProcessadorDocumento
{
    // DIP: recebe RegistroDocumentos via construtor
    // — não chama RegistroDocumentos::getInstance() internamente
    public function __construct(private readonly RegistroDocumentos $registro) {}

    public function processar(string $tipo, array $dados): string
    {
        $doc = $this->registro->criar($tipo, $dados);
        $resultado = $doc->descricao();
        echo "  [Processado] {$resultado}" . PHP_EOL;
        return $resultado;
    }

    public function listarTipos(): array
    {
        return $this->registro->tiposRegistrados();
    }
}


// ─── Demo ─────────────────────────────────────────────────────────────────────

echo "=== Equivalente PHP 8.1+ — Padrões de Criação ===" . PHP_EOL . PHP_EOL;

echo "--- ❌ Ruim ---" . PHP_EOL;
$boletoRuim = criarDocumentoRuim('boleto', [
    'valor' => 1500.00, 'vencimento' => '2026-07-15', 'beneficiario' => 'CLI-100'
]);
echo "Boleto: R\${$boletoRuim->valor}, venc {$boletoRuim->vencimento}" . PHP_EOL;
echo "  campos não usados: chavePix={$boletoRuim->chavePix}, numeroNf={$boletoRuim->numeroNf}" . PHP_EOL;

echo PHP_EOL . "--- ✅ Bom — Factory ---" . PHP_EOL;
$boleto = FabricaDocumento::criar('boleto', [
    'valor' => 1500.00, 'vencimento' => '2026-07-15',
    'beneficiario' => 'CLI-100', 'codigo_barras' => '1234.56789 00000.000000'
]);
echo $boleto->descricao() . PHP_EOL;

$pix = FabricaDocumento::criar('pix', [
    'valor' => 250.00, 'vencimento' => '2026-07-10',
    'beneficiario' => 'CLI-200', 'chave_pix' => 'empresa@exemplo.com.br'
]);
echo $pix->descricao() . PHP_EOL;

$nf = FabricaDocumento::criar('nota_fiscal', [
    'valor' => 890.00, 'vencimento' => '2026-07-30',
    'beneficiario' => 'CLI-300', 'numero_nf' => 'NF-000042', 'cfop' => '5102'
]);
echo $nf->descricao() . PHP_EOL;

echo PHP_EOL . "--- ✅ Bom — Builder ---" . PHP_EOL;
$boletoBuilder = (new ConstruirBoleto())
    ->comValor(750.00)
    ->comVencimento('2026-08-01')
    ->comBeneficiario('CLI-300')
    ->comCodigoBarras('9876.54321 00000.000000')
    ->construir();
echo $boletoBuilder->descricao() . PHP_EOL;

try {
    (new ConstruirBoleto())->comValor(100.0)->construir();
    echo "FALHOU: deveria rejeitar boleto sem vencimento" . PHP_EOL;
} catch (\RuntimeException $e) {
    echo "OK: Builder rejeita boleto incompleto — {$e->getMessage()}" . PHP_EOL;
}

echo PHP_EOL . "--- ✅ Bom — Singleton + SOLID ---" . PHP_EOL;

$registro1 = RegistroDocumentos::getInstance();
$registro2 = RegistroDocumentos::getInstance();
echo ($registro1 === $registro2 ? "OK: Singleton — mesma instância" : "FALHOU: instâncias diferentes") . PHP_EOL;

$registro1->registrar('boleto', fn(array $d) => new Boleto(
    $d['valor'], $d['vencimento'], $d['beneficiario'],
    $d['codigo_barras'] ?? '0000.00000 00000.000000'
));
$registro1->registrar('pix', fn(array $d) => new Pix(
    $d['valor'], $d['vencimento'], $d['beneficiario'],
    $d['chave_pix'] ?? 'chave@exemplo.com.br'
));

// DIP: processador recebe o registro via construtor — não chama getInstance()
$processador = new ProcessadorDocumento($registro1);
echo implode(', ', $processador->listarTipos()) . PHP_EOL;
$processador->processar('boleto', [
    'valor' => 500.00, 'vencimento' => '2026-09-01',
    'beneficiario' => 'CLI-500', 'codigo_barras' => '5555.55555 55555.555555'
]);

// Teste: registro isolado — ProcessadorDocumento não sabe que o global é Singleton
RegistroDocumentos::resetar();
$registroTeste = RegistroDocumentos::getInstance();
$registroTeste->registrar('boleto', fn(array $d) => new Boleto(
    $d['valor'], $d['vencimento'], $d['beneficiario'], ''
));
$processadorTeste = new ProcessadorDocumento($registroTeste);
try {
    $processadorTeste->processar('pix', ['valor' => 10.0, 'vencimento' => '2026-09-01', 'beneficiario' => 'X', 'chave_pix' => 'x']);
} catch (\InvalidArgumentException $e) {
    echo "OK: processador de teste isolado — {$e->getMessage()}" . PHP_EOL;
}
