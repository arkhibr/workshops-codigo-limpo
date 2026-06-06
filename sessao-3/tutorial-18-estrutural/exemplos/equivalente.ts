// EQUIVALENTE TypeScript — Padrões Estruturais: Adapter + Facade
// Execute: npx ts-node equivalente.ts

// ─── ERP legado (funções procedurais — sistema externo imutável) ─────────────

function erp_buscar_cliente(clienteId: string): Record<string, unknown> {
    console.log(`  [ERP] buscarCliente(${clienteId})`);
    const codigo = parseInt(clienteId.split('-')[1], 10);
    return {
        nCodCliente:   codigo,
        cNomeCliente:  'Empresa Exemplo Ltda',
        cEmailCliente: 'contato@exemplo.com',
    };
}

function erp_salvar_pedido(dados: Record<string, unknown>): string {
    console.log(`  [ERP] salvarPedido(${dados['cNroPedido'] ?? '?'})`);
    return 'PED-ERP-001';
}

function erp_atualizar_estoque(cProduto: string, nQtd: number): boolean {
    console.log(`  [ERP] atualizarEstoque(${cProduto}, ${nQtd})`);
    return true;
}

function erp_gerar_nf(cNroPedido: string): string {
    console.log(`  [ERP] gerarNF(${cNroPedido})`);
    return 'NF-000042';
}


// ════════════════════════════════════════════════════════════════════════
// ❌ Ruim — código de negócio chama ERP diretamente; orquestração exposta
// ════════════════════════════════════════════════════════════════════════

function buscarDadosClienteRuim(clienteId: string): Record<string, string> {
    const raw = erp_buscar_cliente(clienteId);   // acoplamento direto
    return {
        id:    String(raw['nCodCliente']),
        nome:  raw['cNomeCliente'] as string,
        email: raw['cEmailCliente'] as string,
    };
}

function registrarPedidoRuim(clienteId: string, produtoId: string, quantidade: number): string {
    erp_buscar_cliente(clienteId);               // chamada duplicada
    const nro = erp_salvar_pedido({
        cNroPedido:  'PED-TEMP',
        nCodCliente: parseInt(clienteId.split('-')[1], 10),
        cCodProduto: produtoId,
        nQtdPedida:  quantidade,
    });
    erp_atualizar_estoque(produtoId, -quantidade);
    return nro;
}

function processarPedidoRuim(clienteId: string, produtoId: string, qtd: number): Record<string, string> {
    // Quem chama conhece e orquestra os 5 subsistemas — alto acoplamento
    const cliente   = buscarDadosClienteRuim(clienteId);
    const nroPedido = registrarPedidoRuim(clienteId, produtoId, qtd);
    const nf        = erp_gerar_nf(nroPedido);
    console.log(`  [Email] → ${cliente['email']}: pedido ${nroPedido} confirmado`);
    return { pedido: nroPedido, nf, cliente: cliente['nome'] };
}


// ════════════════════════════════════════════════════════════════════════
// ✅ Bom — Adapter isola ERP; Facade simplifica a orquestração
// ════════════════════════════════════════════════════════════════════════

// ─── Modelos de domínio modernos ─────────────────────────────────────────────

interface Cliente {
    id:    string;
    nome:  string;
    email: string;
}

interface ResultadoPedido {
    numeroPedido: string;
    notaFiscal:   string;
    clienteNome:  string;
}

// ─── Interfaces (contratos do domínio) ───────────────────────────────────────

interface IRepositorioCliente {
    buscar(clienteId: string): Cliente | null;
}

interface IRepositorioPedido {
    salvar(clienteId: string, produtoId: string, quantidade: number): string;
    atualizarEstoque(produtoId: string, quantidade: number): boolean;
    gerarNotaFiscal(nroPedido: string): string;
}

// ─── Adapters ────────────────────────────────────────────────────────────────

class ERPClienteAdapter implements IRepositorioCliente {
    /** Traduz a API ADVPL (nCod*, cNome*) para o contrato IRepositorioCliente. */
    buscar(clienteId: string): Cliente | null {
        const raw = erp_buscar_cliente(clienteId);
        return {
            id:    String(raw['nCodCliente']),
            nome:  raw['cNomeCliente'] as string,
            email: raw['cEmailCliente'] as string,
        };
    }
}

class ERPPedidoAdapter implements IRepositorioPedido {
    /** Isola os detalhes de nomenclatura ADVPL da lógica de negócio. */
    salvar(clienteId: string, produtoId: string, quantidade: number): string {
        return erp_salvar_pedido({
            cNroPedido:  'PED-TEMP',
            nCodCliente: parseInt(clienteId.split('-')[1], 10),
            cCodProduto: produtoId,
            nQtdPedida:  quantidade,
        });
    }

    atualizarEstoque(produtoId: string, quantidade: number): boolean {
        return erp_atualizar_estoque(produtoId, -quantidade);
    }

    gerarNotaFiscal(nroPedido: string): string {
        return erp_gerar_nf(nroPedido);
    }
}

// ─── Facade ──────────────────────────────────────────────────────────────────

class FachadaProcessamentoPedido {
    /** Quem chama passa apenas os dados — não conhece os subsistemas internos. */
    constructor(
        private readonly repoCliente: IRepositorioCliente,
        private readonly repoPedido:  IRepositorioPedido,
    ) {}

    processar(clienteId: string, produtoId: string, quantidade: number): ResultadoPedido {
        const cliente = this.repoCliente.buscar(clienteId);
        if (cliente === null) {
            throw new Error(`Cliente não encontrado: ${clienteId}`);
        }
        const nroPedido = this.repoPedido.salvar(clienteId, produtoId, quantidade);
        this.repoPedido.atualizarEstoque(produtoId, quantidade);
        const nf = this.repoPedido.gerarNotaFiscal(nroPedido);
        console.log(`  [Email] → ${cliente.email}: pedido ${nroPedido} confirmado`);
        return { numeroPedido: nroPedido, notaFiscal: nf, clienteNome: cliente.nome };
    }
}


// ─── Demo ─────────────────────────────────────────────────────────────────────

console.log('=== Equivalente TypeScript — ❌ Ruim (sem Adapter, sem Facade) ===\n');
const resultadoRuim = processarPedidoRuim('CLI-100', 'PROD-001', 5);
console.log(`\nResultado: pedido=${resultadoRuim['pedido']}, nf=${resultadoRuim['nf']}, cliente=${resultadoRuim['cliente']}`);

console.log('\n=== Equivalente TypeScript — ✅ Bom (Adapter + Facade) ===\n');
const fachada = new FachadaProcessamentoPedido(new ERPClienteAdapter(), new ERPPedidoAdapter());
const resultado = fachada.processar('CLI-100', 'PROD-001', 5);
console.log(`\nResultado: pedido=${resultado.numeroPedido}, nf=${resultado.notaFiscal}, cliente=${resultado.clienteNome}`);
