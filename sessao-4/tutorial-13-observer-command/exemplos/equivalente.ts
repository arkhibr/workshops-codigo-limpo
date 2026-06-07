/**
 * equivalente.ts — Observer e Command em TypeScript
 * Execute: npx ts-node equivalente.ts
 */

// ─── Observer ─────────────────────────────────────────────────────────────────
interface ItemPedido { produtoId: string; quantidade: number; preco: number; }
interface Pedido     { id: string; clienteId: string; itens: ItemPedido[]; status: string; }

interface ObservadorPedido {
    aoConfirmar(pedido: Pedido): void;
    aoCancelar(pedido: Pedido): void;
}

class NotificadorEmailTS implements ObservadorPedido {
    aoConfirmar(p: Pedido): void { console.log(`  [Email] confirmação → ${p.clienteId}: ${p.id}`); }
    aoCancelar(p: Pedido):  void { console.log(`  [Email] cancelamento → ${p.clienteId}: ${p.id}`); }
}

class GestorEstoqueTS implements ObservadorPedido {
    aoConfirmar(p: Pedido): void { p.itens.forEach(i => console.log(`  [Estoque] reservado ${i.quantidade}× ${i.produtoId}`)); }
    aoCancelar(p: Pedido):  void { p.itens.forEach(i => console.log(`  [Estoque] liberado ${i.quantidade}× ${i.produtoId}`)); }
}

class GerenciadorPedidoTS {
    private observadores: ObservadorPedido[] = [];
    registrarObservador(obs: ObservadorPedido): void { this.observadores.push(obs); }
    removerObservador(obs: ObservadorPedido): void {
        this.observadores = this.observadores.filter(o => o !== obs);
    }
    confirmar(pedido: Pedido): void {
        pedido.status = 'confirmado';
        this.observadores.forEach(obs => obs.aoConfirmar(pedido));
    }
    cancelar(pedido: Pedido): void {
        pedido.status = 'cancelado';
        this.observadores.forEach(obs => obs.aoCancelar(pedido));
    }
}

// ─── Command ──────────────────────────────────────────────────────────────────
interface Comando { executar(): void; desfazer(): void; }

class ComandoCancelamentoTS implements Comando {
    private statusAnterior: string | null = null;
    constructor(private pedido: Pedido, private gerenciador: GerenciadorPedidoTS) {}

    executar(): void {
        this.statusAnterior = this.pedido.status;
        this.gerenciador.cancelar(this.pedido);
        console.log(`  Valor estornado para ${this.pedido.clienteId}`);
    }

    desfazer(): void {
        if (this.statusAnterior === null) throw new Error('desfazer() antes de executar()');
        this.pedido.status = this.statusAnterior;
        this.pedido.itens.forEach(i => console.log(`  [Estoque] re-reservado ${i.quantidade}× ${i.produtoId}`));
        console.log(`  Pedido ${this.pedido.id} restaurado para '${this.statusAnterior}'`);
    }
}

class HistoricoComandosTS {
    private historico: Comando[] = [];
    executar(cmd: Comando): void { cmd.executar(); this.historico.push(cmd); }
    desfazerUltimo(): void {
        if (!this.historico.length) { console.log('  Nada para desfazer'); return; }
        this.historico.pop()!.desfazer();
    }
}

// ─── Demo ─────────────────────────────────────────────────────────────────────
console.log("=== Observer + Command TypeScript ===\n");

const pedido1: Pedido = { id: 'PED-001', clienteId: 'CLI-100', itens: [{produtoId:'PROD-001',quantidade:2,preco:299.90}], status: 'pendente' };
const ger1 = new GerenciadorPedidoTS();
ger1.registrarObservador(new NotificadorEmailTS());
ger1.registrarObservador(new GestorEstoqueTS());
ger1.confirmar(pedido1);
console.assert(pedido1.status === 'confirmado');
console.log("OK: Observer — 2 observadores notificados");

const pedido2: Pedido = { id: 'PED-002', clienteId: 'CLI-200', itens: [{produtoId:'PROD-002',quantidade:1,preco:150.0}], status: 'confirmado' };
const ger2 = new GerenciadorPedidoTS();
const hist = new HistoricoComandosTS();
const cmd  = new ComandoCancelamentoTS(pedido2, ger2);
hist.executar(cmd);
console.assert(pedido2.status === 'cancelado');
console.log("OK: Command — cancelamento executado");
hist.desfazerUltimo();
console.assert(pedido2.status === 'confirmado');
console.log("OK: Command — desfazer restaurou status");
