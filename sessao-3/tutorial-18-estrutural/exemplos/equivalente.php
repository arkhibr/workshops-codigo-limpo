<?php
// EQUIVALENTE PHP 8.1+ — Padrões Estruturais: Adapter + Facade
// Execute: php equivalente.php

// ─── ERP legado (funções procedurais — sistema externo imutável) ─────────────

function erp_buscar_cliente(string $clienteId): array {
    echo "  [ERP] buscarCliente({$clienteId})\n";
    $codigo = explode('-', $clienteId)[1];
    return [
        'nCodCliente'   => (int) $codigo,
        'cNomeCliente'  => 'Empresa Exemplo Ltda',
        'cEmailCliente' => 'contato@exemplo.com',
    ];
}

function erp_salvar_pedido(array $dadosPedido): string {
    $nro = $dadosPedido['cNroPedido'] ?? '?';
    echo "  [ERP] salvarPedido({$nro})\n";
    return 'PED-ERP-001';
}

function erp_atualizar_estoque(string $cProduto, int $nQtd): bool {
    echo "  [ERP] atualizarEstoque({$cProduto}, {$nQtd})\n";
    return true;
}

function erp_gerar_nf(string $cNroPedido): string {
    echo "  [ERP] gerarNF({$cNroPedido})\n";
    return 'NF-000042';
}


// ════════════════════════════════════════════════════════════════════════
// ❌ Ruim — código de negócio chama ERP diretamente; orquestração exposta
// ════════════════════════════════════════════════════════════════════════

function buscar_dados_cliente_ruim(string $clienteId): array {
    $raw = erp_buscar_cliente($clienteId);   // acoplamento direto
    return [
        'id'    => (string) $raw['nCodCliente'],
        'nome'  => $raw['cNomeCliente'],
        'email' => $raw['cEmailCliente'],
    ];
}

function registrar_pedido_ruim(string $clienteId, string $produtoId, int $quantidade): string {
    erp_buscar_cliente($clienteId);          // chamada duplicada
    $nro = erp_salvar_pedido([
        'cNroPedido'  => 'PED-TEMP',
        'nCodCliente' => (int) explode('-', $clienteId)[1],
        'cCodProduto' => $produtoId,
        'nQtdPedida'  => $quantidade,
    ]);
    erp_atualizar_estoque($produtoId, -$quantidade);
    return $nro;
}

function processar_pedido_ruim(string $clienteId, string $produtoId, int $qtd): array {
    // Quem chama conhece e orquestra os 5 subsistemas — alto acoplamento
    $cliente   = buscar_dados_cliente_ruim($clienteId);
    $nroPedido = registrar_pedido_ruim($clienteId, $produtoId, $qtd);
    $nf        = erp_gerar_nf($nroPedido);
    echo "  [Email] → {$cliente['email']}: pedido {$nroPedido} confirmado\n";
    return ['pedido' => $nroPedido, 'nf' => $nf, 'cliente' => $cliente['nome']];
}


// ════════════════════════════════════════════════════════════════════════
// ✅ Bom — Adapter isola ERP; Facade simplifica a orquestração
// ════════════════════════════════════════════════════════════════════════

// ─── Modelos de domínio modernos ─────────────────────────────────────────────

readonly class Cliente {
    public function __construct(
        public string $id,
        public string $nome,
        public string $email,
    ) {}
}

readonly class ResultadoPedido {
    public function __construct(
        public string $numeroPedido,
        public string $notaFiscal,
        public string $clienteNome,
    ) {}
}

// ─── Interfaces (contratos do domínio) ───────────────────────────────────────

interface RepositorioCliente {
    public function buscar(string $clienteId): ?Cliente;
}

interface RepositorioPedido {
    public function salvar(string $clienteId, string $produtoId, int $quantidade): string;
    public function atualizarEstoque(string $produtoId, int $quantidade): bool;
    public function gerarNotaFiscal(string $nroPedido): string;
}

// ─── Adapters ────────────────────────────────────────────────────────────────

class ERPClienteAdapter implements RepositorioCliente {
    /**
     * Traduz a API ADVPL (nCod*, cNome*) para o contrato RepositorioCliente.
     */
    public function buscar(string $clienteId): ?Cliente {
        $raw = erp_buscar_cliente($clienteId);
        return new Cliente(
            id:    (string) $raw['nCodCliente'],
            nome:  $raw['cNomeCliente'],
            email: $raw['cEmailCliente'],
        );
    }
}

class ERPPedidoAdapter implements RepositorioPedido {
    /**
     * Isola os detalhes de nomenclatura ADVPL da lógica de negócio.
     */
    public function salvar(string $clienteId, string $produtoId, int $quantidade): string {
        return erp_salvar_pedido([
            'cNroPedido'  => 'PED-TEMP',
            'nCodCliente' => (int) explode('-', $clienteId)[1],
            'cCodProduto' => $produtoId,
            'nQtdPedida'  => $quantidade,
        ]);
    }

    public function atualizarEstoque(string $produtoId, int $quantidade): bool {
        return erp_atualizar_estoque($produtoId, -$quantidade);
    }

    public function gerarNotaFiscal(string $nroPedido): string {
        return erp_gerar_nf($nroPedido);
    }
}

// ─── Facade ──────────────────────────────────────────────────────────────────

class FachadaProcessamentoPedido {
    /**
     * Quem chama passa apenas os dados — não conhece os subsistemas internos.
     */
    public function __construct(
        private readonly RepositorioCliente $repoCliente,
        private readonly RepositorioPedido  $repoPedido,
    ) {}

    public function processar(string $clienteId, string $produtoId, int $quantidade): ResultadoPedido {
        $cliente = $this->repoCliente->buscar($clienteId);
        if ($cliente === null) {
            throw new \RuntimeException("Cliente não encontrado: {$clienteId}");
        }
        $nroPedido = $this->repoPedido->salvar($clienteId, $produtoId, $quantidade);
        $this->repoPedido->atualizarEstoque($produtoId, $quantidade);
        $nf = $this->repoPedido->gerarNotaFiscal($nroPedido);
        echo "  [Email] → {$cliente->email}: pedido {$nroPedido} confirmado\n";
        return new ResultadoPedido($nroPedido, $nf, $cliente->nome);
    }
}


// ─── Demo ─────────────────────────────────────────────────────────────────────

echo "=== Equivalente PHP — ❌ Ruim (sem Adapter, sem Facade) ===\n\n";
$resultadoRuim = processar_pedido_ruim('CLI-100', 'PROD-001', 5);
echo "\nResultado: pedido={$resultadoRuim['pedido']}, nf={$resultadoRuim['nf']}, cliente={$resultadoRuim['cliente']}\n";

echo "\n=== Equivalente PHP — ✅ Bom (Adapter + Facade) ===\n\n";
$fachada = new FachadaProcessamentoPedido(new ERPClienteAdapter(), new ERPPedidoAdapter());
$resultado = $fachada->processar('CLI-100', 'PROD-001', 5);
echo "\nResultado: pedido={$resultado->numeroPedido}, nf={$resultado->notaFiscal}, cliente={$resultado->clienteNome}\n";
