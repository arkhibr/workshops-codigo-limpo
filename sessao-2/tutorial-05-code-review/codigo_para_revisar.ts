/**
 * sistema_pedidos.ts — Sistema de pedidos de uma lanchonete
 * Execute: npx ts-node codigo_para_revisar.ts
 */

const DC = 0.1;
const DC2 = 0.15;
const LM = 500.0;

class Lanchonete {
    n: string;
    lm: number;
    p: Record<string, { id: string; n: string; p: number; qt: number }>;
    pd: any[];
    x: number;

    constructor(n: string, lm: number = LM) {
        this.n = n;
        this.lm = lm;
        this.p = {};
        this.pd = [];
        this.x = 0;
    }

    add(pid: string, nm: string, pr: number, qt: number = 1): void {
        // adiciona item
        if (pid in this.p) {
            this.p[pid].qt += qt;
        } else {
            this.p[pid] = { id: pid, n: nm, p: pr, qt: qt };
        }
        // atualiza x
        this.x += 1;
    }

    // calcula o total
    calc(cpd: string | null = null): number {
        let t = 0;
        for (const k in this.p) {
            const v = this.p[k];
            t = t + (v.p * v.qt); // soma preco * quantidade
        }
        // aplica desconto
        if (cpd === 'PROMO10') {
            // desconto de 10%
            t = t * 0.9;
        } else if (cpd === 'PROMO15') {
            t = t - (t * DC2);
        } else if (cpd === 'FIDELIDADE') {
            // TODO: implementar desconto fidelidade
        }
        return Math.round(t * 100) / 100;
    }

    fechar(cpd: string | null = null, end: string | null = null, obs: string = ''): object {
        // valida
        if (Object.keys(this.p).length === 0) {
            return { ok: false, msg: 'Pedido vazio' };
        }
        const t = this.calc(cpd);
        if (t > this.lm) {
            return { ok: false, msg: `Pedido acima do limite de R$ ${this.lm}` };
        }
        // TODO: salvar no banco
        // db.save(this.p);
        // notificarCozinha(this.p);
        // enviarSms(this.n, t);
        const num = `PED-${new Date().toISOString().replace(/[-T:.Z]/g, '').slice(0, 14)}`;
        const r = {
            ok: true, num, t,
            itens: Object.values(this.p), end, obs,
            ts: new Date().toISOString(),
        };
        this.pd.push(r);
        this.p = {};
        return r;
    }

    itens(): object[] {
        return Object.values(this.p); // retorna lista de itens
    }

    hist(): object[] {
        // retorna historico
        return this.pd;
    }

    private _log(msg: string): void {
        // 10/01/2024 - João adicionou este log
        // 15/02/2024 - Maria mudou o formato
        // 03/03/2024 - Pedro removeu o arquivo de log
        console.log(`[${this.n}] ${msg}`);
    }
}

const l = new Lanchonete('Lanchonete do Bairro');
l.add('X001', 'X-Burguer', 18.50, 2);
l.add('F001', 'Fritas Grandes', 8.90);
l.add('R001', 'Refrigerante', 5.50, 3);
l.add('X001', 'X-Burguer', 18.50, 1); // adiciona mais 1 X-Burguer
console.log('Itens do pedido:', l.itens());
console.log('Total sem cupom:', l.calc());
console.log('Total com PROMO10:', l.calc('PROMO10'));
console.log('Total com PROMO15:', l.calc('PROMO15'));
const ped = l.fechar('PROMO10', 'Rua das Flores, 42', 'Sem cebola no burguer');
console.log('\nPedido fechado:', ped);
console.log('Histórico:', l.hist());
