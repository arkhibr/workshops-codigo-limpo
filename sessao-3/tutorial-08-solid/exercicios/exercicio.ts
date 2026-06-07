// EXERCÍCIO 16 — SOLID na Prática (TypeScript)
// Execute: npx ts-node exercicio.ts
//
// INSTRUÇÕES:
//   A classe GeradorFatura abaixo viola SRP (valida, calcula, persiste e envia
//   email) e DIP (instancia EmailSMTP diretamente).
//
//   1. Separe em classes com responsabilidade única.
//   2. Inverta a dependência de email: GeradorFatura deve receber um INotificador.
//   3. Execute: npx ts-node exercicio.ts (deve rodar antes e depois da refatoração)

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

class EmailSMTP {
    enviar(dest: string, msg: string): void {
        console.log(`  [SMTP] → ${dest}: ${msg}`);
    }
}

class GeradorFatura {
    private email: EmailSMTP;

    // DIP violation: instancia dependência concreta
    constructor() {
        this.email = new EmailSMTP();
    }

    // SRP violation: valida fatura
    validar(fatura: Fatura): boolean {
        return fatura.itens.length > 0 && fatura.clienteId.length > 0;
    }

    // SRP violation: calcula total
    calcularTotal(fatura: Fatura): number {
        return fatura.itens.reduce((acc, i) => acc + i.valor, 0);
    }

    // SRP violation: persiste no banco
    salvar(fatura: Fatura): void {
        console.log(`  [BD] fatura ${fatura.id} salva`);
    }

    processar(fatura: Fatura): number {
        if (!this.validar(fatura)) {
            throw new Error("Fatura inválida");
        }
        const total = this.calcularTotal(fatura);
        this.salvar(fatura);
        this.email.enviar(fatura.clienteId, `Fatura ${fatura.id}: R$${total.toFixed(2)}`);
        return total;
    }
}

// Demo
const itens: ItemFatura[] = [
    { descricao: "Consultoria", valor: 1500.0 },
    { descricao: "Suporte",     valor: 300.0  },
];
const fatura  = new Fatura("FAT-001", "CLI-200", itens);
const gerador = new GeradorFatura();
const total   = gerador.processar(fatura);
console.log(`Total: R$${total.toFixed(2)}`);
