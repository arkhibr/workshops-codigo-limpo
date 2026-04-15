/**
 * EXERCÍCIO 01 — Nomes Significativos
 * Tempo estimado: 10 minutos
 * Referência: Clean Code, Cap. 2
 *
 * INSTRUÇÕES:
 *   Renomeie todas as variáveis, parâmetros, funções e interfaces abaixo
 *   para que os nomes revelem claramente a intenção do código.
 *   Não altere a lógica — apenas os nomes.
 *
 * Execute: npx ts-node exercicio.ts
 */

// ─── Problema 1 ───────────────────────────────────────────────────────────────
// O que este código calcula? Renomeie para tornar óbvio.

const x = 86400;
const y = 7;
const z = x * y;

function calc(a: number, b: number): number {
    return a * b / 100;
}

// ─── Problema 2 ───────────────────────────────────────────────────────────────
// Esta classe gerencia um carrinho de compras.
// Renomeie tudo para refletir isso.

interface Itm { itm: string; prc: number; }

class Mgr {
    private lst: Itm[] = [];
    private cnt = 0;
    private ttl = 0;

    add(itm: string, prc: number): void {
        this.lst.push({ itm, prc });
        this.cnt++;
        this.ttl += prc;
    }

    rmv(itm: string): void {
        this.lst = this.lst.filter(i => i.itm !== itm);
        this.cnt = this.lst.length;
        this.ttl = this.lst.reduce((s, i) => s + i.prc, 0);
    }

    gtAll(): Itm[] { return this.lst; }
    gtTtl(): number { return this.ttl; }
}

// ─── Problema 3 ───────────────────────────────────────────────────────────────
// Esta função verifica se um usuário pode acessar um recurso.
// Renomeie os parâmetros e a função.

interface Usr { nome: string; prms: string[]; }

function proc(u: Usr, r: string, adm: boolean): boolean {
    if (adm) return true;
    return u.prms.includes(r);
}

// ─── Verificação (não altere este bloco) ──────────────────────────────────────

console.log("=== Problema 1 ===");
console.log(`x=${x}, y=${y}, z=${z}`);
console.log(`calc(200, 10) = ${calc(200, 10)}`);

console.log("\n=== Problema 2 ===");
const m = new Mgr();
m.add("Camiseta", 89.90);
m.add("Calça", 159.90);
console.log("Itens:", m.gtAll());
console.log(`Total: R$ ${m.gtTtl().toFixed(2)}`);
m.rmv("Camiseta");
console.log(`Após remover Camiseta: R$ ${m.gtTtl().toFixed(2)}`);

console.log("\n=== Problema 3 ===");
const usuario: Usr = { nome: "João", prms: ["leitura", "escrita"] };
console.log("Acesso leitura:", proc(usuario, "leitura", false));
console.log("Acesso admin:  ", proc(usuario, "exclusao", true));
