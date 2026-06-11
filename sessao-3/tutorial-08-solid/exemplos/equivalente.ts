// EQUIVALENTE TypeScript — SOLID na Prática
// Execute: npx ts-node equivalente.ts

// ============================================================
// DOMÍNIO COMPARTILHADO
// ============================================================

interface ItemPedido {
    produtoId:  string;
    descricao:  string;
    preco:      number;
    quantidade: number;
}

class Pedido {
    status: string = "pendente";
    constructor(
        public readonly id:        string,
        public readonly clienteId: string,
        public readonly itens:     ItemPedido[],
    ) {}

    confirmar(): void {
        this.status = "confirmado";
    }
}

// ============================================================
// ❌ Ruim — SRP + DIP + OCP violados (para referência)
// ============================================================

class EmailSmtp {
    enviar(dest: string, msg: string): void {
        console.log(`  [Email] → ${dest}: ${msg.substring(0, 50)}`);
    }
}

class BancoDadosSQLite {
    salvar(tabela: string, dados: Record<string, string>): void {
        console.log(`  [BD] salvo em ${tabela}: ${dados["id"]}`);
    }
}

class GeradorRelatorioRuim {
    private email: EmailSmtp;
    private db:    BancoDadosSQLite;

    // DIP violation: instancia dependências concretas
    constructor() {
        this.email = new EmailSmtp();
        this.db    = new BancoDadosSQLite();
    }

    // SRP violation: valida pedido
    validarPedido(pedido: Pedido): boolean {
        return pedido.itens.length > 0 && pedido.clienteId.length > 0;
    }

    // SRP violation: calcula total
    calcularTotal(pedido: Pedido): number {
        return pedido.itens.reduce((acc, i) => acc + i.preco * i.quantidade, 0);
    }

    // SRP violation: envia e-mail
    enviarConfirmacao(pedido: Pedido): void {
        this.email.enviar(pedido.clienteId, `Pedido ${pedido.id} confirmado`);
    }

    // SRP violation: persiste no banco
    salvarPedido(pedido: Pedido): void {
        this.db.salvar("pedidos", { id: pedido.id, status: pedido.status });
    }

    // OCP violation: adicionar novo tipo exige alterar este método
    gerar(tipo: string, pedido: Pedido): string {
        const total = this.calcularTotal(pedido);
        if      (tipo === "vendas")     return `Relatório Vendas | Pedido ${pedido.id} | Total: R$${total.toFixed(2)}`;
        else if (tipo === "financeiro") return `Relatório Financeiro | Receita: R$${total.toFixed(2)}`;
        else if (tipo === "estoque")    return `Relatório Estoque | ${pedido.itens.length} item(ns) movimentado(s)`;
        else throw new Error(`Tipo desconhecido: ${tipo}`);
    }
}

// ============================================================
// S — SRP: interfaces e classes com responsabilidade única
// ============================================================

interface INotificador {
    notificar(destinatario: string, mensagem: string): void;
}

interface IRepositorioPedido {
    salvar(pedido: Pedido): void;
    buscar(pedidoId: string): Record<string, unknown> | undefined;
}

interface IFormatador {
    formatar(pedido: Pedido, total: number): string;
}

class ValidadorPedido {
    validar(pedido: Pedido): boolean {
        if (pedido.itens.length === 0) {
            console.log(`  [Validação] Pedido ${pedido.id}: sem itens`);
            return false;
        }
        if (!pedido.clienteId) {
            console.log(`  [Validação] Pedido ${pedido.id}: cliente ausente`);
            return false;
        }
        if (pedido.itens.some(i => i.preco <= 0 || i.quantidade <= 0)) {
            console.log(`  [Validação] Pedido ${pedido.id}: item com valor inválido`);
            return false;
        }
        return true;
    }
}

class CalculadorTotal {
    private static readonly TAXA_IMPOSTO = 0.10;

    calcular(pedido: Pedido): number {
        const subtotal = pedido.itens.reduce((acc, i) => acc + i.preco * i.quantidade, 0);
        return Math.round(subtotal * (1 + CalculadorTotal.TAXA_IMPOSTO) * 100) / 100;
    }

    calcularSubtotal(pedido: Pedido): number {
        return Math.round(
            pedido.itens.reduce((acc, i) => acc + i.preco * i.quantidade, 0) * 100
        ) / 100;
    }

    calcularImposto(pedido: Pedido): number {
        const subtotal = pedido.itens.reduce((acc, i) => acc + i.preco * i.quantidade, 0);
        return Math.round(subtotal * CalculadorTotal.TAXA_IMPOSTO * 100) / 100;
    }
}

class NotificadorEmail implements INotificador {
    notificar(destinatario: string, mensagem: string): void {
        console.log(`  [Email] → ${destinatario}: ${mensagem}`);
    }
}

class NotificadorLog implements INotificador {
    // Alternativa sem SMTP — mesma interface, zero alteração no chamador
    notificar(destinatario: string, mensagem: string): void {
        console.log(`  [Log] ${destinatario}: ${mensagem}`);
    }
}

class RepositorioPedido implements IRepositorioPedido {
    private dados = new Map<string, Record<string, unknown>>();

    salvar(pedido: Pedido): void {
        this.dados.set(pedido.id, {
            id:      pedido.id,
            status:  pedido.status,
            cliente: pedido.clienteId,
            itens:   pedido.itens.length,
        });
        console.log(`  [BD] salvo: ${pedido.id} → ${pedido.status}`);
    }

    buscar(pedidoId: string): Record<string, unknown> | undefined {
        return this.dados.get(pedidoId);
    }
}

class RepositorioEmMemoria implements IRepositorioPedido {
    private dados = new Map<string, Record<string, unknown>>();

    salvar(pedido: Pedido): void {
        this.dados.set(pedido.id, { id: pedido.id, status: pedido.status });
        console.log(`  [Mem] salvo: ${pedido.id} → ${pedido.status}`);
    }

    buscar(pedidoId: string): Record<string, unknown> | undefined {
        return this.dados.get(pedidoId);
    }
}

// ============================================================
// O — OCP: novos formatadores sem alterar GeradorRelatorio
// ============================================================

class FormatadorVendas implements IFormatador {
    formatar(pedido: Pedido, total: number): string {
        const itens = pedido.itens.map(i => `${i.descricao} x${i.quantidade}`).join(", ");
        return `[Vendas] Pedido ${pedido.id} | ${itens} | Total: R$${total.toFixed(2)}`;
    }
}

class FormatadorFinanceiro implements IFormatador {
    formatar(pedido: Pedido, total: number): string {
        const calc     = new CalculadorTotal();
        const subtotal = calc.calcularSubtotal(pedido);
        const imposto  = calc.calcularImposto(pedido);
        return `[Financeiro] Pedido ${pedido.id} | Subtotal: R$${subtotal.toFixed(2)} | Imposto: R$${imposto.toFixed(2)} | Total: R$${total.toFixed(2)}`;
    }
}

class FormatadorEstoque implements IFormatador {
    formatar(pedido: Pedido, total: number): string {
        const linhas = pedido.itens.map(i => `  • ${i.descricao} (ref: ${i.produtoId}): ${i.quantidade} un`);
        return `[Estoque] Pedido ${pedido.id} — movimentação:\n${linhas.join("\n")}`;
    }
}

class FormatadorNFe implements IFormatador {
    // Adicionado sem nenhuma alteração em GeradorRelatorio — OCP respeitado
    formatar(pedido: Pedido, total: number): string {
        return `[NF-e] DANFE | Dest: ${pedido.clienteId} | Nr: ${pedido.id} | Valor: R$${total.toFixed(2)}`;
    }
}

// ============================================================
// L — LSP: subtipos honram o contrato da base
// ============================================================

class PedidoAmostra extends Pedido {
    calcularTotalEspecial(): number {
        return 0;  // amostras têm custo zero para o cliente
    }
    // confirmar() herdado sem alteração — contrato mantido
}

class PedidoPrioritario extends Pedido {
    constructor(
        id: string,
        clienteId: string,
        itens: ItemPedido[],
        public readonly prioridade: number = 1,
    ) {
        super(id, clienteId, itens);
    }

    confirmar(): void {
        super.confirmar();  // honra o contrato base
        console.log(`  [Fila] Pedido ${this.id} inserido com prioridade ${this.prioridade}`);
    }
}

function confirmarEExibir(pedido: Pedido): void {
    pedido.confirmar();
    console.assert(pedido.status === "confirmado", "Contrato violado");
    console.log(`  ${pedido.constructor.name} ${pedido.id} → status: ${pedido.status}`);
}

// ============================================================
// I — ISP: interfaces pequenas e coesas
// ============================================================

interface IValidavel {
    validar(): boolean;
}

interface ICalculavel {
    calcular(): number;
}

interface IArquivavel {
    arquivar(): void;
    exportarCsv(): string;
}

interface IExportavelPDF {
    exportarPdf(): Uint8Array;
}

class ProcessadorSimples implements IValidavel, ICalculavel {
    // Só precisa de validar e calcular — sem métodos mortos
    constructor(private readonly pedido: Pedido) {}

    validar(): boolean {
        return this.pedido.itens.length > 0 && this.pedido.clienteId.length > 0;
    }

    calcular(): number {
        return Math.round(
            this.pedido.itens.reduce((acc, i) => acc + i.preco * i.quantidade, 0) * 100
        ) / 100;
    }
}

class ProcessadorCompleto implements IValidavel, ICalculavel, IArquivavel, IExportavelPDF {
    constructor(private readonly pedido: Pedido) {}

    validar(): boolean {
        return this.pedido.itens.length > 0 && this.pedido.clienteId.length > 0;
    }

    calcular(): number {
        return Math.round(
            this.pedido.itens.reduce((acc, i) => acc + i.preco * i.quantidade, 0) * 100
        ) / 100;
    }

    arquivar(): void {
        console.log(`  [Arquivo] Pedido ${this.pedido.id} arquivado em storage frio`);
    }

    exportarCsv(): string {
        const linhas = ["produto_id,descricao,preco,quantidade"];
        for (const i of this.pedido.itens) {
            linhas.push(`${i.produtoId},${i.descricao},${i.preco},${i.quantidade}`);
        }
        return linhas.join("\n");
    }

    exportarPdf(): Uint8Array {
        const linhas = [
            `PEDIDO ${this.pedido.id}`,
            `Cliente: ${this.pedido.clienteId}`,
            ...this.pedido.itens.map(i => `  ${i.descricao}: ${i.quantidade} x R$${i.preco.toFixed(2)}`),
        ];
        return new TextEncoder().encode(linhas.join("\n"));
    }
}

// ============================================================
// D — DIP: GeradorRelatorio recebe abstrações via construtor
// ============================================================

class GeradorRelatorio {
    constructor(
        private readonly repo:        IRepositorioPedido,
        private readonly notificador: INotificador,
        private readonly formatador:  IFormatador,
        private readonly calculador:  CalculadorTotal,
    ) {}

    processar(pedido: Pedido): string {
        const total = this.calculador.calcular(pedido);
        this.repo.salvar(pedido);
        this.notificador.notificar(
            pedido.clienteId,
            `Pedido ${pedido.id} processado. Total: R$${total.toFixed(2)}`
        );
        return this.formatador.formatar(pedido, total);
    }
}

// ============================================================
// DEMONSTRAÇÃO
// ============================================================

const itens: ItemPedido[] = [
    { produtoId: "P001", descricao: "Webcam HD",  preco: 299.90, quantidade: 1 },
    { produtoId: "P002", descricao: "Cabo USB-C", preco:  49.90, quantidade: 2 },
];
const pedido = new Pedido("PED-001", "CLI-100", itens);

console.log("=== TypeScript — SOLID na Prática ===\n");

// ── S — SRP ──────────────────────────────────────────────────
console.log("── S — SRP: cada classe tem uma responsabilidade ──────");
const validador   = new ValidadorPedido();
const calculador  = new CalculadorTotal();
const repoReal    = new RepositorioPedido();
const notifEmail  = new NotificadorEmail();
console.log(`  Válido: ${validador.validar(pedido)}`);
console.log(`  Subtotal: R$${calculador.calcularSubtotal(pedido).toFixed(2)}`);
console.log(`  Imposto:  R$${calculador.calcularImposto(pedido).toFixed(2)}`);
console.log(`  Total:    R$${calculador.calcular(pedido).toFixed(2)}`);
repoReal.salvar(pedido);
notifEmail.notificar(pedido.clienteId, `Pedido ${pedido.id} registrado`);

// ── O — OCP ──────────────────────────────────────────────────
console.log("\n── O — OCP: novos formatadores sem alterar GeradorRelatorio ──");
const formatadores: Array<[string, IFormatador]> = [
    ["vendas",     new FormatadorVendas()],
    ["financeiro", new FormatadorFinanceiro()],
    ["estoque",    new FormatadorEstoque()],
    ["nfe",        new FormatadorNFe()],
];
for (const [nome, fmt] of formatadores) {
    const gerador = new GeradorRelatorio(new RepositorioEmMemoria(), new NotificadorLog(), fmt, new CalculadorTotal());
    console.log(`\n  [${nome}] ${gerador.processar(pedido)}`);
}

// ── L — LSP ──────────────────────────────────────────────────
console.log("\n── L — LSP: todos os subtipos honram o contrato de Pedido ──");
const casos: Pedido[] = [
    new Pedido("PED-002", "CLI-200", itens),
    new PedidoAmostra("PED-003", "CLI-300", itens),
    new PedidoPrioritario("PED-004", "CLI-400", itens, 3),
];
for (const p of casos) {
    confirmarEExibir(p);
}

// ── I — ISP ──────────────────────────────────────────────────
console.log("\n── I — ISP: ProcessadorSimples usa 2 interfaces, sem métodos mortos ──");
const simples = new ProcessadorSimples(pedido);
console.log(`  validar=${simples.validar()}, calcular=R$${simples.calcular().toFixed(2)}`);

const completo = new ProcessadorCompleto(pedido);
completo.arquivar();
console.log(`  CSV:\n${completo.exportarCsv()}`);
const pdfBytes = completo.exportarPdf();
console.log(`  PDF (${pdfBytes.length}B): ${new TextDecoder().decode(pdfBytes.subarray(0, 40))}...`);

// ── D — DIP ──────────────────────────────────────────────────
console.log("\n── D — DIP: trocar Email por Log sem alterar GeradorRelatorio ──");
const geradorProd  = new GeradorRelatorio(repoReal,                new NotificadorEmail(), new FormatadorVendas(), new CalculadorTotal());
const geradorTeste = new GeradorRelatorio(new RepositorioEmMemoria(), new NotificadorLog(), new FormatadorVendas(), new CalculadorTotal());
console.log("  [Produção]:",    geradorProd.processar(pedido));
console.log("  [Teste/mock]:",  geradorTeste.processar(pedido));
