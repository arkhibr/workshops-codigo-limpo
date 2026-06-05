/**
 * SAÍDA TÍPICA DE IA — agendamento de consultas (a partir de prompt fraco)
 * Referência: Clean Code, Cap. 2–3
 *
 * ⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
 *     Representa o tipo de código que uma IA gera a partir de um prompt vago.
 *     Analise os problemas antes de ver a versão revisada.
 *
 * Execute: npx ts-node sessao-5/tutorial-08-clean-code-com-ia/exemplos/agendamento_gerado.ts
 */

// Prompt usado: "faz uma função de agendar consulta"

// lista global de consultas agendadas
const data: any[] = [];  // "data" — não diz o que contém


function processar(d: string, p: string, h: string): any {  // o que é d? p? h?
  // checa se pode agendar
  let ok = true;
  for (const item of data) {
    if (item.date === d && item.p === p) {  // mistura de idioma
      ok = false;
    }
  }
  if (!ok) {
    return -1;  // código de erro em vez de exceção
  }

  // cria o registro
  const consulta = {
    date: d,       // "date" em inglês
    p: p,          // "p" — o que significa?
    h: h,          // "h" — horário? hora? hospital?
    dur: 30,       // número mágico — por que 30?
    status: "ok",  // "ok" — aprovado? confirmado? ativo?
  };
  data.push(consulta);
  return consulta;
}


function get_consultas(p: string): any[] {  // mistura de idioma no nome
  const result: any[] = [];
  for (const item of data) {
    if (item.p === p) {
      result.push(item);
    }
  }
  return result;
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

const c1 = processar("2026-07-10", "Ana Lima", "09:00");
console.log("Agendamento 1:", c1);

// tenta agendar o mesmo paciente no mesmo dia
const c2 = processar("2026-07-10", "Ana Lima", "14:00");
console.log("Agendamento 2 (mesmo dia):", c2);

// agendamento diferente
const c3 = processar("2026-07-11", "Carlos Souza", "10:30");
console.log("Agendamento 3:", c3);

console.log("\nConsultas de Ana Lima:", get_consultas("Ana Lima"));
