/**
 * equivalente.ts — Idiom Patterns em TypeScript
 * Execute: npx ts-node equivalente.ts
 */

// ─── Ruim: nullable sem tipo discriminante, catch genérico ────────────────────
interface VendaRuim {
    id: string;
    valor: number;
    vendedor?: string;  // nullable sem discriminante
}

function buscarVendaRuim(id: string): VendaRuim | null {
    if (id === "V001") return { id, valor: 100.0, vendedor: "Ana" };
    return null;
}

// ─── Bom: Discriminated Union (Result type) ───────────────────────────────────
interface ItemVenda { produtoId: string; descricao: string; precoUnitario: number; quantidade: number; mes: number; }

type ResultadoBusca =
    | { ok: true;  dados: ItemVenda }
    | { ok: false; erro: string };

function buscarItem(produtoId: string): ResultadoBusca {
    if (produtoId === "P001") {
        return { ok: true, dados: { produtoId, descricao: "Webcam HD", precoUnitario: 299.90, quantidade: 2, mes: 6 } };
    }
    return { ok: false, erro: `Produto não encontrado: ${produtoId}` };
}

function processarResultado(resultado: ResultadoBusca): string {
    if (!resultado.ok) return `Erro: ${resultado.erro}`;
    return `${resultado.dados.descricao}: R$${resultado.dados.precoUnitario.toFixed(2)}`;
}

// ─── Bom: optional chaining e nullish coalescing ──────────────────────────────
interface Vendedor { nome: string; email?: { principal?: string }; }
interface Venda    { id: string; valor: number; vendedor?: Vendedor; }

function obterEmailVendedor(venda: Venda): string {
    // Ruim: venda.vendedor && venda.vendedor.email && venda.vendedor.email.principal || 'nao-identificado'
    // Bom:
    return venda.vendedor?.email?.principal ?? 'nao-identificado';
}

// ─── Bom: Promise com async/await ─────────────────────────────────────────────
async function buscarVendaAsync(id: string): Promise<ResultadoBusca> {
    // Simula I/O assíncrono
    return buscarItem(id);
}

// ─── Demo ─────────────────────────────────────────────────────────────────────
console.log("=== Idioms TypeScript ===\n");

const r1 = buscarItem("P001");
console.assert(r1.ok === true);
console.log(`OK: Discriminated Union — ${processarResultado(r1)}`);

const r2 = buscarItem("P999");
console.assert(r2.ok === false);
console.log(`OK: Discriminated Union — erro: ${r2.ok ? '' : r2.erro}`);

const venda: Venda = { id: "V001", valor: 100, vendedor: { nome: "Ana" } };
const email = obterEmailVendedor(venda);
console.assert(email === 'nao-identificado');
console.log(`OK: Optional chaining + nullish coalescing — email='${email}'`);

// async/await demo (síncrono aqui para evitar top-level await em ts-node)
buscarVendaAsync("P001").then(r => {
    console.assert(r.ok === true);
    console.log("OK: async/await — buscarVendaAsync resolvido");
});
