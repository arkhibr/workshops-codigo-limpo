/**
 * VERSÃO REVISADA — processamento de estornos com tratamento de erro explícito
 * Referência: Clean Code, Cap. 7 (Error Handling)
 *
 * Problemas corrigidos em relação à versão gerada:
 *   - catch (e) {} vazio substituído por classes de erro tipadas
 *   - EstornoInvalidoError: campo obrigatório ausente ou tipo incorreto
 *   - ValorEstornoExcedidoError: valor do estorno excede o original
 *   - Mensagens de erro incluem os valores que causaram o problema
 *   - Falhas são propagadas — o chamador decide o que fazer
 *
 * Execute: npx ts-node sessao-5/tutorial-11-tratamento-de-erros/exemplos/estorno_revisado.ts
 */

class EstornoInvalidoError extends Error {
  constructor(mensagem: string) {
    super(mensagem);
    this.name = "EstornoInvalidoError";
  }
}

class ValorEstornoExcedidoError extends Error {
  constructor(mensagem: string) {
    super(mensagem);
    this.name = "ValorEstornoExcedidoError";
  }
}

interface DadosEstorno {
  id: string;
  valor: number;
  valorOriginal: number;
}

interface ResultadoEstorno {
  id: string;
  status: string;
  valor: number;
}

function validarCamposEstorno(estorno: Partial<DadosEstorno>): void {
  for (const campo of ["id", "valor", "valorOriginal"] as const) {
    if (estorno[campo] === undefined) {
      throw new EstornoInvalidoError(
        `Campo obrigatório ausente no estorno: '${campo}'.`
      );
    }
  }
  if (typeof estorno.valor !== "number" || estorno.valor <= 0) {
    throw new EstornoInvalidoError(
      `Campo 'valor' deve ser um número positivo; recebido: ${estorno.valor}.`
    );
  }
}

function verificarLimiteEstorno(valor: number, valorOriginal: number): void {
  if (valor > valorOriginal) {
    throw new ValorEstornoExcedidoError(
      `Estorno de R$ ${valor.toFixed(2)} excede o valor original de R$ ${valorOriginal.toFixed(2)}.`
    );
  }
}

function processarEstorno(estorno: Partial<DadosEstorno>): ResultadoEstorno {
  validarCamposEstorno(estorno);
  verificarLimiteEstorno(estorno.valor!, estorno.valorOriginal!);
  return {
    id: estorno.id!,
    status: "aprovado",
    valor: estorno.valor!,
  };
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

const estornos: Partial<DadosEstorno>[] = [
  { id: "EST-001", valor: 150.00, valorOriginal: 300.00 },
  { id: "EST-002", valor: 80.00 },                             // valorOriginal ausente
  { id: "EST-003", valor: 500.00, valorOriginal: 300.00 },     // excede original
];

console.log("=== Demonstração: estorno_revisado.ts ===");
console.log();

const sucessos: ResultadoEstorno[] = [];
const falhas: { id: string; erro: string }[] = [];

for (const estorno of estornos) {
  try {
    const resultado = processarEstorno(estorno);
    sucessos.push(resultado);
  } catch (erro) {
    if (erro instanceof EstornoInvalidoError || erro instanceof ValorEstornoExcedidoError) {
      falhas.push({ id: estorno.id ?? "?", erro: erro.message });
    } else {
      throw erro;
    }
  }
}

console.log(`Estornos aprovados: ${sucessos.length}`);
for (const s of sucessos) {
  console.log(`  [${s.id}] R$ ${s.valor.toFixed(2)} — ${s.status}`);
}

console.log();
console.log(`Estornos com falha: ${falhas.length}`);
for (const f of falhas) {
  console.log(`  [${f.id}] ${f.erro}`);
}

console.log();
console.log("Cada falha agora é visível com tipo e mensagem descritiva.");
