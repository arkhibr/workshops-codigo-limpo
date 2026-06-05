/**
 * EXERCÍCIO — Cupom de desconto progressivo (saída típica de IA, a partir de prompt fraco)
 * Referência: Clean Code, Cap. 2–3; engenharia de contexto em prompts de código
 *
 * Prompt usado para gerar este código:
 *     "cria um módulo de cupom de desconto pra loja"
 *
 * Sua tarefa:
 *     (1) Reescreva o prompt acima para ser mais forte (veja o modelo em exemplos/prompt.md).
 *     (2) Refatore o código abaixo aplicando os princípios de Clean Code.
 *     (3) Liste os problemas que você encontrou (nomes, coesão, idioma, números mágicos, etc.).
 *
 * Execute: npx ts-node sessao-5/tutorial-09-engenharia-de-prompt/exercicios/exercicio.ts
 */

// ⚠️  Código gerado por IA — INTENCIONALMENTE IMPERFEITO. Não corrija antes de listar os problemas.

const cupons: Record<string, any> = {};  // nome vago; o que guarda?


function apply(code: string, val: number): number {  // nome em inglês; "val" — valor do quê?
  if (!(code in cupons)) {
    return val;  // sem exceção — falha silenciosa
  }
  const c = cupons[code];  // "c" — o que é?
  if (c.type === "pct") {  // "pct" — abreviação obscura; "type" em inglês
    let d: number;
    if (val >= 200) {
      d = val * c.amt * 1.5;  // número mágico 1.5 — bônus? progressivo?
    } else {
      d = val * c.amt;
    }
    return Math.round((val - d) * 100) / 100;
  } else if (c.type === "fixed") {  // inglês misturado
    return Math.round(Math.max(val - c.amt, 0) * 100) / 100;  // max sem comentário — por quê?
  }
  return val;
}


function add(code: string, tp: string, amt: number): void {  // "tp" — tipo? temperatura? turno?
  cupons[code] = { type: tp, amt };
}


function rm(code: string): void {  // "rm" — nome de comando Unix, não de domínio
  if (code in cupons) {
    delete cupons[code];
  }
  // sem aviso se não existir
}


function show_all(): void {  // mistura de idioma; "show" vago
  for (const [k, v] of Object.entries(cupons)) {
    console.log(`  ${k}:`, v);
  }
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

add("VERAO10", "pct", 0.10);
add("FRETE", "fixed", 15.0);
add("VIP20", "pct", 0.20);

console.log("=== Cupons cadastrados ===");
show_all();

console.log("\n--- Aplicando cupons ---");
// compra de R$ 150 com cupom percentual (sem bônus progressivo)
console.log("Compra R$150 + VERAO10:", apply("VERAO10", 150.0));

// compra de R$ 300 com cupom percentual (com bônus progressivo)
console.log("Compra R$300 + VERAO10:", apply("VERAO10", 300.0));

// cupom de valor fixo
console.log("Compra R$50 + FRETE:", apply("FRETE", 50.0));

// cupom inexistente — falha silenciosa
console.log("Compra R$100 + INVALIDO:", apply("INVALIDO", 100.0));
