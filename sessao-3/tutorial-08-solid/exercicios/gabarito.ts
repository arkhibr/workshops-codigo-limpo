// GABARITO 16 — SOLID na Prática (TypeScript)
// Execute: npx ts-node gabarito.ts
//
// Quatro passos aplicados em sequência sobre o código original:
//   Passo 1: violações anotadas (// SRP: e // DIP:)
//   Passo 2: ValidadorFatura extraído; GeradorFatura recebe no construtor
//   Passo 3: CalculadorFatura e RepositorioFatura extraídos
//   Passo 4: interface INotificador; EmailSMTP substituído por injeção

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

// ── Passo 4 — Interfaces (DIP) ───────────────────────────────────────────────

interface INotificador {
    notificar(destinatario: string, mensagem: string): void;
}

interface IRepositorioFatura {
    salvar(fatura: Fatura): void;
}

// ── Passo 2 — ValidadorFatura (SRP) ──────────────────────────────────────────

class ValidadorFatura {
    validar(fatura: Fatura): boolean {
        return fatura.itens.length > 0 && fatura.clienteId.length > 0;
    }
}

// ── Passo 3 — CalculadorFatura + RepositorioFatura (SRP) ─────────────────────

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

// ── Passo 4 — Implementação concreta de INotificador ─────────────────────────

class NotificadorEmail implements INotificador {
    notificar(destinatario: string, mensagem: string): void {
        console.log(`  [SMTP] → ${destinatario}: ${mensagem}`);
    }
}

// ── Passo 2–4 — GeradorFatura: orquestra, não executa (DIP + SRP) ────────────

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

// ── Demo ─────────────────────────────────────────────────────────────────────

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
