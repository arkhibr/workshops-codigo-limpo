<?php
// EXERCÍCIO 17 PHP 8.1+ — Padrões de Criação
// Referência: Design Patterns (GoF), Cap. 3
//
// PASSOS (31 min no total):
//
//   PASSO 1 — IDENTIFICAR (5 min)
//     Leia o código abaixo e adicione comentários marcando os dois problemas:
//       // PROBLEMA: construtor gordo (9 parâmetros, maioria opcional)
//       // PROBLEMA: if/else rígido — adicionar tipo exige alterar criarContrato()
//     Meta: encontrar os 2 problemas e anotar onde estão antes de alterar código.
//
//   PASSO 2 — FACTORY COM ARRAY (8 min)
//     Substitua o if/else de criarContrato() por um array associativo:
//       $fabrica = ["servico" => fn($d) => ..., "locacao" => ..., "fornecimento" => ...]
//     criarContrato() consulta o array e chama a entrada correspondente.
//     Verifique que o demo ainda roda.
//
//   PASSO 3 — FACTORY REGISTRÁVEL (8 min)
//     Transforme $fabrica em FabricaContrato com:
//       FabricaContrato::registrar(string $tipo, callable $fabrica): void
//       FabricaContrato::criar(string $tipo, array $dados): Contrato
//     Use private static array $registro = [] para guardar os callables.
//     Registre os 3 tipos existentes externamente.
//     Verifique que o demo ainda roda e que um novo tipo pode ser registrado
//     sem alterar FabricaContrato.
//
//   PASSO 4 — BUILDER (10 min)
//     Crie ConstruirContratoServico com métodos fluentes:
//       comValorMensal(float $valor): static
//       comVigencia(int $meses): static
//       comContratante(string $c): static
//       construir(): Contrato  (lança RuntimeException se campos obrigatórios faltarem)
//     Verifique que o demo roda com a nova sintaxe fluente.
//
// Execute: php exercicio.php (deve rodar antes e depois de cada passo)

class Contrato
{
    public function __construct(
        public readonly string  $tipo,
        public readonly float   $valorMensal,
        public readonly int     $vigenciaMeses,
        public readonly string  $contratante,
        public readonly ?string $objeto       = null,    // serviço ou bem locado
        public readonly ?string $endereco     = null,    // para locação
        public readonly ?string $fornecedorId = null,    // para fornecimento
        public readonly ?int    $prazoEntrega = null,    // dias, para fornecimento
        public readonly ?string $observacoes  = null,
    ) {}
}

function criarContrato(string $tipo, array $dados): Contrato
{
    // Adicionar ContratoObrasCivil exige alterar esta função
    if ($tipo === 'servico') {
        return new Contrato(
            tipo:          'servico',
            valorMensal:   $dados['valor_mensal'],
            vigenciaMeses: $dados['vigencia_meses'],
            contratante:   $dados['contratante'],
            objeto:        $dados['objeto'] ?? 'Serviços gerais',
        );
    } elseif ($tipo === 'locacao') {
        return new Contrato(
            tipo:          'locacao',
            valorMensal:   $dados['valor_mensal'],
            vigenciaMeses: $dados['vigencia_meses'],
            contratante:   $dados['contratante'],
            objeto:        $dados['objeto'] ?? null,
            endereco:      $dados['endereco'] ?? null,
        );
    } elseif ($tipo === 'fornecimento') {
        return new Contrato(
            tipo:          'fornecimento',
            valorMensal:   $dados['valor_mensal'],
            vigenciaMeses: $dados['vigencia_meses'],
            contratante:   $dados['contratante'],
            fornecedorId:  $dados['fornecedor_id'] ?? null,
            prazoEntrega:  $dados['prazo_entrega'] ?? null,
        );
    } else {
        throw new \InvalidArgumentException("Tipo desconhecido: $tipo");
    }
}

// Demo
$c1 = criarContrato('servico', [
    'valor_mensal' => 5000.0, 'vigencia_meses' => 12, 'contratante' => 'EMP-001'
]);
echo "Contrato: {$c1->tipo} R\${$c1->valorMensal}/mês × {$c1->vigenciaMeses} meses" . PHP_EOL;
echo "  campos não usados: endereco={$c1->endereco}, fornecedorId={$c1->fornecedorId}" . PHP_EOL;

// --- Stub Passo 3: registrar novo tipo sem alterar FabricaContrato ---
// Após implementar FabricaContrato, descomente e verifique:
// FabricaContrato::registrar('obras_civil', fn(array $d) => new Contrato(
//     tipo:          'obras_civil',
//     valorMensal:   $d['valor_mensal'],
//     vigenciaMeses: $d['vigencia_meses'],
//     contratante:   $d['contratante'],
// ));
// $obras = FabricaContrato::criar('obras_civil', [
//     'valor_mensal' => 25000.0, 'vigencia_meses' => 8, 'contratante' => 'EMP-004'
// ]);
// echo "Novo tipo: {$obras->tipo} R\${$obras->valorMensal}/mês" . PHP_EOL;

// --- Stub Passo 4: sintaxe fluente do Builder ---
// Após implementar ConstruirContratoServico, descomente e verifique:
// $c2 = (new ConstruirContratoServico())
//     ->comValorMensal(5000.0)
//     ->comVigencia(12)
//     ->comContratante('EMP-001')
//     ->construir();
// echo "Builder: {$c2->tipo} R\${$c2->valorMensal}/mês × {$c2->vigenciaMeses} meses" . PHP_EOL;
