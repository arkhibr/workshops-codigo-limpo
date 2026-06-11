// EXERCÍCIO 16 — SOLID na Prática (TypeScript)
// Execute: npx ts-node exercicio.ts
//
// PASSOS (faça um de cada vez, em ordem):
//
//   PASSO 1 — IDENTIFICAR (5 min)
//     Leia GeradorFatura e adicione comentários // SRP: e // DIP: antes de
//     cada trecho problemático.
//     Meta: encontrar pelo menos 4 violações antes de alterar código.
//
//   PASSO 2 — EXTRAIR ValidadorFatura (8 min)
//     Mova validar() para uma nova classe ValidadorFatura.
//     GeradorFatura passa a receber ValidadorFatura no construtor.
//     Verifique que o demo ainda roda: npx ts-node exercicio.ts
//
//   PASSO 3 — EXTRAIR CalculadorFatura + RepositorioFatura (8 min)
//     Repita para calcularTotal() e salvar().
//     GeradorFatura.processar() delega para os colaboradores injetados.
//     Verifique que o demo ainda roda: npx ts-node exercicio.ts
//
//   PASSO 4 — INVERTER DEPENDÊNCIA DE EMAIL (8 min)
//     Crie interface INotificador { notificar(dest: string, msg: string): void }
//     Substitua this.email = new EmailSMTP() por injeção no construtor.
//     Verifique que o demo ainda roda: npx ts-node exercicio.ts

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

// -----------------------------------------------------------------------
// PASSO 4 — stub para verificar a injeção de dependência.
// Após criar INotificador, descomente e rode npx ts-node exercicio.ts.
// -----------------------------------------------------------------------
// class NotificadorLog implements INotificador {
//     chamado = false;
//     notificar(_dest: string, _msg: string): void { this.chamado = true; }
// }
//
// const notifLog = new NotificadorLog();
// const gerador2 = new GeradorFatura(
//     new ValidadorFatura(), new CalculadorFatura(), new RepositorioFatura(), notifLog
// );
// gerador2.processar(fatura);
// console.assert(notifLog.chamado, "FALHOU: notificador substituto não foi chamado");
// console.log("OK: DIP — GeradorFatura aceita qualquer INotificador");
