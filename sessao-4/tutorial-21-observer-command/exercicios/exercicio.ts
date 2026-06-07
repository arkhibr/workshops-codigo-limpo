/**
 * EXERCÍCIO 21 — Observer e Command em TypeScript
 * Tempo estimado: 20 minutos
 *
 * INSTRUÇÕES:
 *   O código abaixo tem dois problemas:
 *   1. ProcessadorPagamento.processar() conhece e chama 3 serviços diretamente
 *      (acoplamento). Adicionar notificação por SMS exige alterar processar().
 *   2. estornarPagamento() não tem undo — uma vez executado, não há como reverter.
 *
 *   1. Refatore para Observer: crie interface ObservadorPagamento com
 *      aoAprovar()/aoRecusar(), e ProcessadorPagamento com registrarObservador().
 *   2. Refatore para Command: crie ComandoEstorno com executar()/desfazer(),
 *      e HistoricoComandos.
 *   3. Execute: npx ts-node exercicio.ts (deve rodar antes e depois)
 */

// ─── Modelo ───────────────────────────────────────────────────────────────────

interface Pagamento {
    id:        string;
    valor:     number;
    clienteId: string;
    status:    string;
}

// ─── Serviços acoplados diretamente ──────────────────────────────────────────

class ServicoEmail {
    notificarAprovacao(clienteId: string, valor: number): void {
        console.log(`  [Email] → ${clienteId}: pagamento R$${valor.toFixed(2)} aprovado`);
    }
}

class ServicoAuditoria {
    registrar(evento: string, pagamentoId: string): void {
        console.log(`  [Auditoria] ${evento}: ${pagamentoId}`);
    }
}

class ServicoFraude {
    marcarAprovado(pagamentoId: string): void {
        console.log(`  [Fraude] aprovado: ${pagamentoId}`);
    }
}

// ─── Sem Observer: ProcessadorPagamento conhece os 3 serviços ────────────────

class ProcessadorPagamento {
    private email:     ServicoEmail;
    private auditoria: ServicoAuditoria;
    private fraude:    ServicoFraude;

    constructor() {
        this.email     = new ServicoEmail();
        this.auditoria = new ServicoAuditoria();
        this.fraude    = new ServicoFraude();
    }

    processar(pagamento: Pagamento): void {
        pagamento.status = 'aprovado';
        // Adicionar SMS exige alterar processar()
        this.email.notificarAprovacao(pagamento.clienteId, pagamento.valor);
        this.auditoria.registrar('pagamento_aprovado', pagamento.id);
        this.fraude.marcarAprovado(pagamento.id);
    }
}

// ─── Sem Command: estornar sem undo ──────────────────────────────────────────

function estornarPagamento(pagamento: Pagamento): void {
    // Sem estado anterior. Sem histórico. Sem desfazer.
    pagamento.status = 'estornado';
    console.log(`  Crédito de R$${pagamento.valor.toFixed(2)} devolvido a ${pagamento.clienteId}`);
    console.log(`  Pagamento ${pagamento.id} marcado como estornado`);
}

// ─── Demo ─────────────────────────────────────────────────────────────────────
const pag: Pagamento = { id: 'PAG-001', valor: 500.0, clienteId: 'CLI-100', status: 'pendente' };
const proc = new ProcessadorPagamento();
proc.processar(pag);
console.log(`Status: ${pag.status}\n`);

estornarPagamento(pag);
console.log(`Status: ${pag.status}`);
console.log('(sem desfazer disponível)');
