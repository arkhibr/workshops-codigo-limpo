// EQUIVALENTE TypeScript — SOLID na Prática
// Execute: npx ts-node equivalente.ts

// ============================================================
// Estrutura de dados compartilhada
// ============================================================

interface ItemPedido {
    produtoId:   string;
    descricao:   string;
    preco:       number;
    quantidade:  number;
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
// ❌ Ruim — SRP + DIP violados
// ============================================================

class EmailSmtp {
    enviar(dest: string, msg: string): void {
        console.log(`  [Email] → ${dest}: ${msg.substring(0, 40)}`);
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
        if (tipo === "vendas") {
            return `Relatório Vendas | Pedido ${pedido.id} | Total: R$${total.toFixed(2)}`;
        } else if (tipo === "financeiro") {
            return `Relatório Financeiro | Receita: R$${total.toFixed(2)}`;
        } else if (tipo === "estoque") {
            return `Relatório Estoque | ${pedido.itens.length} item(ns) movimentado(s)`;
        } else {
            throw new Error(`Tipo desconhecido: ${tipo}`);
        }
    }
}

// ============================================================
// ✅ Bom — SRP + DIP aplicados
// ============================================================

interface INotificador {
    notificar(destinatario: string, mensagem: string): void;
}

interface IRepositorioPedido {
    salvar(pedido: Pedido): void;
}

interface IFormatador {
    formatar(pedido: Pedido, total: number): string;
}

class ValidadorPedido {
    validar(pedido: Pedido): boolean {
        return pedido.itens.length > 0 && pedido.clienteId.length > 0;
    }
}

class CalculadorTotal {
    calcular(pedido: Pedido): number {
        return Math.round(
            pedido.itens.reduce((acc, i) => acc + i.preco * i.quantidade, 0) * 100
        ) / 100;
    }
}

class NotificadorEmail implements INotificador {
    notificar(destinatario: string, mensagem: string): void {
        console.log(`  [Email] → ${destinatario}: ${mensagem.substring(0, 40)}`);
    }
}

class RepositorioPedido implements IRepositorioPedido {
    salvar(pedido: Pedido): void {
        console.log(`  [BD] salvo: ${pedido.id} (${pedido.status})`);
    }
}

class FormatadorVendas implements IFormatador {
    formatar(pedido: Pedido, total: number): string {
        return `Relatório Vendas | Pedido ${pedido.id} | Total: R$${total.toFixed(2)}`;
    }
}

class FormatadorFinanceiro implements IFormatador {
    formatar(pedido: Pedido, total: number): string {
        return `Relatório Financeiro | Receita: R$${total.toFixed(2)}`;
    }
}

class FormatadorEstoque implements IFormatador {
    formatar(pedido: Pedido, total: number): string {
        return `Relatório Estoque | ${pedido.itens.length} item(ns) movimentado(s)`;
    }
}

// DIP aplicado: GeradorRelatorio recebe abstrações via construtor
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
        this.notificador.notificar(pedido.clienteId, `Pedido ${pedido.id} salvo`);
        return this.formatador.formatar(pedido, total);
    }
}

// ============================================================
// Demo
// ============================================================

const itens: ItemPedido[]  = [{ produtoId: "P001", descricao: "Webcam HD", preco: 299.90, quantidade: 1 }];
const pedido               = new Pedido("PED-001", "CLI-100", itens);

console.log("=== TypeScript — SOLID na Prática ===\n");

console.log("❌ Ruim (SRP+DIP violados):");
const geradorRuim = new GeradorRelatorioRuim();
geradorRuim.salvarPedido(pedido);
geradorRuim.enviarConfirmacao(pedido);
console.log(geradorRuim.gerar("vendas", pedido));

console.log("\n✅ Bom (SRP+DIP aplicados):");
const formatadores: Array<[string, IFormatador]> = [
    ["vendas",     new FormatadorVendas()],
    ["financeiro", new FormatadorFinanceiro()],
    ["estoque",    new FormatadorEstoque()],
];
for (const [tipo, fmt] of formatadores) {
    const gerador   = new GeradorRelatorio(new RepositorioPedido(), new NotificadorEmail(), fmt, new CalculadorTotal());
    const resultado = gerador.processar(pedido);
    console.log(`  [${tipo}] ${resultado}`);
}
