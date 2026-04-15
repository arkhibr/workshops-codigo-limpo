/**
 * GABARITO 01 — Nomes Significativos
 * Abra este arquivo apenas após tentar o exercício por conta própria.
 */

// ─── Solução 1 ────────────────────────────────────────────────────────────────

const SEGUNDOS_POR_DIA    = 86400;
const DIAS_POR_SEMANA     = 7;
const SEGUNDOS_POR_SEMANA = SEGUNDOS_POR_DIA * DIAS_POR_SEMANA;

function calcularDesconto(preco: number, percentual: number): number {
    return preco * percentual / 100;
}

// ─── Solução 2 ────────────────────────────────────────────────────────────────

interface Item { produto: string; preco: number; }

class CarrinhoDeCompras {
    private itens: Item[]  = [];
    private quantidade     = 0;
    private total          = 0;

    adicionarItem(nomeProduto: string, preco: number): void {
        this.itens.push({ produto: nomeProduto, preco });
        this.quantidade++;
        this.total += preco;
    }

    removerItem(nomeProduto: string): void {
        this.itens     = this.itens.filter(i => i.produto !== nomeProduto);
        this.quantidade = this.itens.length;
        this.total      = this.itens.reduce((s, i) => s + i.preco, 0);
    }

    listarItens(): Item[] { return this.itens; }
    obterTotal(): number  { return this.total;  }
}

// ─── Solução 3 ────────────────────────────────────────────────────────────────

interface Usuario { nome: string; permissoes: string[]; }

function usuarioTemAcessoAoRecurso(usuario: Usuario, recurso: string, ehAdministrador: boolean): boolean {
    if (ehAdministrador) return true;
    return usuario.permissoes.includes(recurso);
}

// ─── Verificação ──────────────────────────────────────────────────────────────

console.log("=== Solução 1 ===");
console.log(`Segundos por semana: ${SEGUNDOS_POR_SEMANA}`);
console.log(`Desconto de 10% em R$200: R$ ${calcularDesconto(200, 10).toFixed(2)}`);

console.log("\n=== Solução 2 ===");
const carrinho = new CarrinhoDeCompras();
carrinho.adicionarItem("Camiseta", 89.90);
carrinho.adicionarItem("Calça", 159.90);
console.log("Itens:", carrinho.listarItens());
console.log(`Total: R$ ${carrinho.obterTotal().toFixed(2)}`);
carrinho.removerItem("Camiseta");
console.log(`Após remover Camiseta: R$ ${carrinho.obterTotal().toFixed(2)}`);

console.log("\n=== Solução 3 ===");
const usuario: Usuario = { nome: "João", permissoes: ["leitura", "escrita"] };
console.log("Acesso leitura:", usuarioTemAcessoAoRecurso(usuario, "leitura", false));
console.log("Acesso admin:  ", usuarioTemAcessoAoRecurso(usuario, "exclusao", true));
