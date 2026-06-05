/**
 * EXERCÍCIO — Lista de espera da clínica (saída típica de IA, a partir de prompt fraco)
 * Referência: Clean Code, Cap. 2–3 aplicados a código assistido por IA
 *
 * Prompt usado para gerar este código:
 *     "cria um módulo de lista de espera pra clínica"
 *
 * Sua tarefa:
 *     (1) Reescreva o prompt acima para ser mais forte (veja o modelo em exemplos/prompt.md).
 *     (2) Refatore o código abaixo aplicando os princípios de Clean Code.
 *     (3) Liste os problemas que você encontrou (nomes, coesão, idioma, etc.).
 *
 * Execute: npx ts-node sessao-5/tutorial-08-clean-code-com-ia/exercicios/exercicio.ts
 */

// ⚠️  Código gerado por IA — INTENCIONALMENTE IMPERFEITO. Não corrija antes de listar os problemas.

const queue: any[] = [];  // nome em inglês — o que representa?
let _id = 0;              // variável global sem contexto


function add(n: string, t: string): number {  // o que é n? o que é t?
  _id += 1;
  const entry = {
    id: _id,
    n: n,       // "n" — nome? número? nível?
    t: t,       // "t" — tipo? tempo? turno?
    ts: new Date().toISOString(),  // "ts" — timestamp? tipo serviço?
    done: false,  // mistura de idioma
  };
  queue.push(entry);
  return _id;  // retorna id E adiciona (viola CQS)
}


function remove(id: number): boolean {  // "remove" — do quê?
  const index = queue.findIndex((e) => e.id === id);
  if (index === -1) {
    return false;  // código de retorno sem exceção
  }
  queue.splice(index, 1);
  return true;
}


function show(): void {  // o que "show" mostra? de quem?
  for (const entry of queue) {
    const s = entry.done ? "✓" : "·";
    console.log(`[${s}] #${entry.id} ${entry.n} (${entry.t})`);
  }
}


function next_p(): any | null {  // mistura de idioma ("next" + "p")
  for (const entry of queue) {
    if (!entry.done) {
      entry.done = true;  // modifica E implica retorno
      return entry;
    }
  }
  return null;
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

add("Maria Oliveira", "retorno");
add("João Costa", "primeira consulta");
add("Beatriz Ferreira", "exame");

console.log("=== Lista de espera ===");
show();

console.log("\nChamando próximo paciente...");
const proximo = next_p();
console.log("Chamado:", proximo);

console.log("\n=== Lista atualizada ===");
show();
