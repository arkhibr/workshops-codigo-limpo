/**
 * SAÍDA TÍPICA DE IA — processamento de estornos (a partir de prompt sem requisitos de erro)
 * Referência: Clean Code, Cap. 7 (Error Handling)
 *
 * ⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
 *     Note o tratamento de erro silencioso: erros são engolidos com
 *     catch (e) {} vazio e a função retorna null em falha.
 *     O caminho feliz funciona, mas um estorno inválido some sem aviso.
 *
 * Execute: npx ts-node sessao-5/tutorial-11-tratamento-de-erros/exemplos/estorno_gerado.ts
 */

// Prompt usado: "cria uma função que processa um estorno e retorna o resultado"

interface Estorno {
  id?: string;
  valor?: number;       // opcional no tipo — a IA não forçou obrigatoriedade
  valorOriginal?: number;
}

interface ResultadoEstorno {
  id: string;
  status: string;
  valor: number;
}

// nome com erro de grafia ("procesar" em vez de "processar") — a IA não revisa ortografia
function procesarEstorno(estorno: Estorno): ResultadoEstorno | null {
  try {
    const valor = estorno.valor!;        // non-null assertion sem validação
    const valorOriginal = estorno.valorOriginal!;
    if (valor <= 0) {
      return null;  // falha silenciosa — quem chamou não sabe o que houve
    }
    if (valor > valorOriginal) {
      return null;  // regra de negócio violada, mas sem aviso
    }
    return {
      id: estorno.id ?? "sem-id",
      status: "aprovado",
      valor,
    };
  } catch (e) {
    return null;  // engole qualquer erro — TypeError, o que vier
  }
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

const estornoValido: Estorno = { id: "EST-001", valor: 150.00, valorOriginal: 300.00 };
const estornoSemCampo: Estorno = { id: "EST-002", valor: 80.00 };           // valorOriginal ausente
const estornoExcedido: Estorno = { id: "EST-003", valor: 500.00, valorOriginal: 300.00 };

console.log("=== Demonstração: estorno_gerado.ts ===");
console.log();

const r1 = procesarEstorno(estornoValido);
console.log(`EST-001 (válido): ${JSON.stringify(r1)}`);

const r2 = procesarEstorno(estornoSemCampo);
console.log(`EST-002 (campo ausente): ${JSON.stringify(r2)}`);  // aprovado indevidamente — falha invisível

const r3 = procesarEstorno(estornoExcedido);
console.log(`EST-003 (valor excedido): ${r3}`);                 // retorna null — falha invisível

console.log();
console.log("⚠ EST-002 foi aprovado indevidamente (valorOriginal undefined não dispara guarda).");
console.log("  EST-003 retornou null sem levantar erro.");
console.log("  O sistema continua rodando como se tudo estivesse bem.");
