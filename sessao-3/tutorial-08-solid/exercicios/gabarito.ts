// GABARITO 16 — SOLID na Prática (TypeScript)
// Execute: npx ts-node gabarito.ts
//
// Correções aplicadas:
//   SRP — ValidadorFatura, CalculadorFatura, RepositorioFatura separados
//   DIP — GeradorFatura recebe INotificador no construtor, não instancia EmailSMTP

interface ItemFatura {
    descricao: string;
    valor:     number;
}

class Fatura {
    status: string = "pendente";
    constructor(
        public readonly id:        string,
        public readonly clienteId: string,
        public readonly itens:     ItemFatura[],
    ) {}
}

// ─── Interfaces (DIP) ────────────────────────────────────────────────────────

interface INotificador {
    notificar(destinatario: string, mensagem: string): void;
}

interface IRepositorioFatura {
    salvar(fatura: Fatura): void;
}

// ─── Classes com responsabilidade única (SRP) ────────────────────────────────

class ValidadorFatura {
    validar(fatura: Fatura): boolean {
        return fatura.itens.length > 0 && fatura.clienteId.length > 0;
    }
}

class CalculadorFatura {
    calcularTotal(fatura: Fatura): number {
        return Math.round(fatura.itens.reduce((acc, i) => acc + i.valor, 0) * 100) / 100;
    }
}

class RepositorioFatura implements IRepositorioFatura {
    salvar(fatura: Fatura): void {
        console.log(`  [BD] fatura ${fatura.id} salva (${fatura.status})`);
    }
}

class NotificadorEmail implements INotificador {
    notificar(destinatario: string, mensagem: string): void {
        console.log(`  [SMTP] → ${destinatario}: ${mensagem}`);
    }
}

// ─── GeradorFatura: orquestra, não executa (DIP + SRP) ───────────────────────

class GeradorFatura {
    constructor(
        private readonly validador:   ValidadorFatura,
        private readonly calculador:  CalculadorFatura,
        private readonly repositorio: IRepositorioFatura,
        private readonly notificador: INotificador,
    ) {}

    processar(fatura: Fatura): number {
        if (!this.validador.validar(fatura)) {
            throw new Error("Fatura inválida");
        }
        const total = this.calculador.calcularTotal(fatura);
        this.repositorio.salvar(fatura);
        this.notificador.notificar(fatura.clienteId, `Fatura ${fatura.id}: R$${total.toFixed(2)}`);
        return total;
    }
}

// ─── Demo ────────────────────────────────────────────────────────────────────

const itens: ItemFatura[] = [
    { descricao: "Consultoria", valor: 1500.0 },
    { descricao: "Suporte",     valor: 300.0  },
];
const fatura = new Fatura("FAT-001", "CLI-200", itens);

const gerador = new GeradorFatura(
    new ValidadorFatura(),
    new CalculadorFatura(),
    new RepositorioFatura(),
    new NotificadorEmail(),
);

const total = gerador.processar(fatura);
console.log(`Total: R$${total.toFixed(2)}`);
console.log("OK: SRP — ValidadorFatura, CalculadorFatura, RepositorioFatura separados");
console.log("OK: DIP — GeradorFatura recebe INotificador no construtor");
