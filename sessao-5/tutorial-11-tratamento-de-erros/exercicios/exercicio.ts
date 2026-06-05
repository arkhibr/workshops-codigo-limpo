/**
 * EXERCÍCIO — cancelamento de assinatura (saída de IA com erros silenciados)
 * Referência: Clean Code, Cap. 7 (Error Handling)
 *
 * ⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
 *     A função mistura validação, cálculo e persistência EM UMA ÚNICA função
 *     E silencia os erros com catch (e) {} vazio.
 *     Sua tarefa:
 *
 *     (1) Torne cada falha visível com uma exceção específica.
 *     (2) Separe as responsabilidades (validação / cálculo / persistência).
 *     (3) Liste os erros que estavam sendo silenciados.
 *
 * Execute: npx ts-node sessao-5/tutorial-11-tratamento-de-erros/exercicios/exercicio.ts
 */

// Prompt usado: "cria uma função que cancela uma assinatura e calcula o reembolso"

interface DadosAssinatura {
  plano: string;
  valor: number;
  diasRestantes: number;
  ativa: boolean;
}

interface ResultadoCancelamento {
  id: string;
  reembolso: number;
  status: string;
}

const bancoAssinaturas: Record<string, DadosAssinatura> = {
  "ASS-001": { plano: "mensal", valor: 49.90, diasRestantes: 18, ativa: true },
  "ASS-002": { plano: "anual",  valor: 499.00, diasRestantes: 0,  ativa: false },
  "ASS-003": { plano: "mensal", valor: 29.90, diasRestantes: 10, ativa: true },
};

const cancelamentosRegistrados: { id: string; motivo: string | null; reembolso: number }[] = [];

function cancelar(id: string, motivo: string | null): ResultadoCancelamento | null {
  try {
    const dados = bancoAssinaturas[id];
    if (!dados) {
      return null;  // assinatura não encontrada — falha silenciosa
    }
    if (!dados.ativa) {
      return null;  // já cancelada — falha silenciosa
    }
    let reembolso: number;
    if (dados.diasRestantes <= 0) {
      reembolso = 0;
    } else if (dados.plano === "mensal") {
      reembolso = Math.round(dados.valor * (dados.diasRestantes / 30) * 100) / 100;
    } else {
      reembolso = Math.round(dados.valor * (dados.diasRestantes / 365) * 100) / 100;
    }
    dados.ativa = false;  // persiste o cancelamento inline
    cancelamentosRegistrados.push({ id, motivo, reembolso });
    return { id, reembolso, status: "cancelado" };
  } catch (e) {
    return null;  // qualquer erro desaparece sem rastro
  }
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

console.log("=== Demonstração: exercicio.ts (cancelamento de assinatura) ===");
console.log();

// Caso 1: cancelamento válido
const r1 = cancelar("ASS-001", "cliente solicitou");
console.log(`ASS-001 (ativa, 18 dias restantes): ${JSON.stringify(r1)}`);

// Caso 2: assinatura já cancelada
const r2 = cancelar("ASS-002", "cliente solicitou");
console.log(`ASS-002 (já cancelada): ${r2}`);   // retorna null — falha invisível

// Caso 3: ID inexistente
const r3 = cancelar("ASS-999", "cliente solicitou");
console.log(`ASS-999 (não existe): ${r3}`);      // retorna null — falha invisível

// Caso 4: motivo ausente — aceito sem validação (deveria falhar)
const r4 = cancelar("ASS-003", null);
console.log(`ASS-003 (motivo null): ${JSON.stringify(r4)}`);  // cancela mesmo sem motivo — falha silenciosa por omissão

console.log();
console.log("⚠ ASS-002 e ASS-999 sumiram como null; o motivo ausente foi aceito sem validação — três falhas sem erro.");
console.log("  O chamador recebe null mas não sabe o que houve.");
