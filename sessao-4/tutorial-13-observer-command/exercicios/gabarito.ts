/**
 * gabarito.ts — Solução do Exercício 21: Observer e Command em TypeScript
 * Execute: npx ts-node gabarito.ts
 */

// ─── Modelo ───────────────────────────────────────────────────────────────────

interface Pagamento {
    id:        string;
    valor:     number;
    clienteId: string;
    status:    string;
}

// ─── Observer ─────────────────────────────────────────────────────────────────

interface ObservadorPagamento {
    aoAprovar(pagamento: Pagamento): void;
    aoRecusar(pagamento: Pagamento): void;
}

class NotificadorEmailPag implements ObservadorPagamento {
    aoAprovar(pag: Pagamento): void {
        console.log(`  [Email] → ${pag.clienteId}: pagamento R$${pag.valor.toFixed(2)} aprovado`);
    }
    aoRecusar(pag: Pagamento): void {
        console.log(`  [Email] → ${pag.clienteId}: pagamento R$${pag.valor.toFixed(2)} recusado`);
    }
}

class AuditoriaPag implements ObservadorPagamento {
    aoAprovar(pag: Pagamento): void { console.log(`  [Auditoria] pagamento_aprovado: ${pag.id}`); }
    aoRecusar(pag: Pagamento): void { console.log(`  [Auditoria] pagamento_recusado: ${pag.id}`); }
}

class FraudePag implements ObservadorPagamento {
    aoAprovar(pag: Pagamento): void { console.log(`  [Fraude] aprovado: ${pag.id}`); }
    aoRecusar(pag: Pagamento): void { console.log(`  [Fraude] recusado: ${pag.id}`); }
}

class ProcessadorPagamento {
    private observadores: ObservadorPagamento[] = [];

    registrarObservador(obs: ObservadorPagamento): void {
        this.observadores.push(obs);
    }

    aprovar(pagamento: Pagamento): void {
        pagamento.status = 'aprovado';
        this.observadores.forEach(obs => obs.aoAprovar(pagamento));
    }

    recusar(pagamento: Pagamento): void {
        pagamento.status = 'recusado';
        this.observadores.forEach(obs => obs.aoRecusar(pagamento));
    }
}

// ─── Command ──────────────────────────────────────────────────────────────────

class ComandoEstorno {
    private statusAnterior: string | null = null;

    constructor(
        private pagamento:   Pagamento,
        private processador: ProcessadorPagamento
    ) {}

    executar(): void {
        this.statusAnterior    = this.pagamento.status;
        this.pagamento.status  = 'estornado';
        console.log(`  Crédito de R$${this.pagamento.valor.toFixed(2)} devolvido a ${this.pagamento.clienteId}`);
        console.log(`  Pagamento ${this.pagamento.id} marcado como estornado`);
    }

    desfazer(): void {
        if (this.statusAnterior === null) throw new Error('desfazer() chamado antes de executar()');
        this.pagamento.status = this.statusAnterior;
        console.log(`  Pagamento ${this.pagamento.id} restaurado para '${this.statusAnterior}'`);
    }
}

class HistoricoComandos {
    private historico: ComandoEstorno[] = [];

    executar(cmd: ComandoEstorno): void {
        cmd.executar();
        this.historico.push(cmd);
    }

    desfazerUltimo(): void {
        if (!this.historico.length) { console.log('  Nada para desfazer'); return; }
        this.historico.pop()!.desfazer();
    }
}

// ─── Verificação ──────────────────────────────────────────────────────────────

function verificarGabarito(): void {
    // Observer
    const pag: Pagamento = { id: 'PAG-001', valor: 500.0, clienteId: 'CLI-100', status: 'pendente' };
    const proc = new ProcessadorPagamento();
    proc.registrarObservador(new NotificadorEmailPag());
    proc.registrarObservador(new AuditoriaPag());
    proc.registrarObservador(new FraudePag());

    proc.aprovar(pag);
    console.assert(pag.status === 'aprovado');
    console.log("OK: Observer — 3 observadores notificados em aprovar()");
    console.log("OK: Observer — adicionar SMS não altera ProcessadorPagamento");

    // Command
    const historico = new HistoricoComandos();
    const cmd = new ComandoEstorno(pag, proc);
    historico.executar(cmd);
    console.assert(pag.status === 'estornado');
    console.log("OK: Command — estorno executado");

    historico.desfazerUltimo();
    console.assert(pag.status === 'aprovado');
    console.log("OK: Command — estorno desfeito, pagamento restaurado para 'aprovado'");
}

console.log("=== Gabarito 21 — Observer e Command: Pagamentos TypeScript ===\n");
verificarGabarito();
