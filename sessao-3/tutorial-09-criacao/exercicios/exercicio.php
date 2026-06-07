<?php
// EXERCÍCIO 17 PHP 8.1+ — Padrões de Criação
// Tempo estimado: 15 minutos
// Referência: Design Patterns (GoF), Cap. 3
//
// INSTRUÇÕES:
//   O código abaixo tem dois problemas:
//   1. Construtor gordo: Contrato tem 9 parâmetros, maioria opcional.
//   2. Função criarContrato() com if/else — adicionar novo tipo exige alterá-la.
//
//   Aplique:
//   1. Factory Method: crie uma FabricaContrato registrável.
//   2. Builder: crie ConstruirContratoServico com métodos fluentes.
//
//   Execute: php exercicio.php

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
