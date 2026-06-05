/**
 * GABARITO — Cupom de desconto progressivo (versão aderente ao prompt estruturado)
 * Referência: Clean Code, Cap. 2–3; engenharia de contexto em prompts de código
 *
 * Problemas corrigidos em relação ao exercício:
 *   - Nomes descritivos em português para todos os identificadores
 *   - Interface tipada substituindo Record<string, any>
 *   - Números mágicos extraídos como constantes nomeadas
 *   - Regras de desconto separadas em funções próprias
 *   - Falha silenciosa substituída por exceção descritiva
 *   - Funções com nomes que revelam intenção no domínio
 *
 * Execute: npx ts-node sessao-5/tutorial-09-engenharia-de-prompt/exercicios/gabarito.ts
 */

const MULTIPLICADOR_PROGRESSIVO = 1.5;    // bônus de desconto para compras acima do limiar
const LIMIAR_DESCONTO_PROGRESSIVO = 200.0; // valor mínimo para ativar o desconto progressivo
const PRECO_MINIMO = 0.0;                 // preço final nunca pode ser negativo

type TipoCupom = "percentual" | "valor_fixo";

interface Cupom {
  codigo: string;
  tipo: TipoCupom;
  valor: number;  // percentual (0–1) ou valor fixo em reais
}

const cupomsCadastrados: Map<string, Cupom> = new Map();


function calcularDescontoPercentual(cupom: Cupom, valorCompra: number): number {
  if (valorCompra >= LIMIAR_DESCONTO_PROGRESSIVO) {
    return valorCompra * cupom.valor * MULTIPLICADOR_PROGRESSIVO;
  }
  return valorCompra * cupom.valor;
}


function calcularDescontoFixo(cupom: Cupom, valorCompra: number): number {
  return Math.min(cupom.valor, valorCompra);
}


function calcularDesconto(cupom: Cupom, valorCompra: number): number {
  if (cupom.tipo === "percentual") {
    return calcularDescontoPercentual(cupom, valorCompra);
  }
  return calcularDescontoFixo(cupom, valorCompra);
}


function aplicarCupom(codigo: string, valorCompra: number): number {
  const cupom = cupomsCadastrados.get(codigo);
  if (!cupom) {
    throw new Error(`Cupom '${codigo}' não encontrado.`);
  }

  const desconto = calcularDesconto(cupom, valorCompra);
  return Math.round(Math.max(valorCompra - desconto, PRECO_MINIMO) * 100) / 100;
}


function cadastrarCupom(codigo: string, tipo: TipoCupom, valor: number): void {
  cupomsCadastrados.set(codigo, { codigo, tipo, valor });
}


function removerCupom(codigo: string): void {
  if (!cupomsCadastrados.has(codigo)) {
    throw new Error(`Cupom '${codigo}' não encontrado para remoção.`);
  }
  cupomsCadastrados.delete(codigo);
}


function exibirCuponsCadastrados(): void {
  for (const cupom of cupomsCadastrados.values()) {
    const valorDisplay = cupom.tipo === "percentual"
      ? `${(cupom.valor * 100).toFixed(0)}%`
      : `R$${cupom.valor.toFixed(2)}`;
    console.log(`  [${cupom.codigo}] ${cupom.tipo}: ${valorDisplay}`);
  }
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

cadastrarCupom("VERAO10", "percentual", 0.10);
cadastrarCupom("FRETE", "valor_fixo", 15.0);
cadastrarCupom("VIP20", "percentual", 0.20);

console.log("=== Cupons cadastrados ===");
exibirCuponsCadastrados();

console.log("\n--- Aplicando cupons ---");
// compra de R$ 150 com cupom percentual (sem bônus progressivo)
console.log("Compra R$150 + VERAO10:", aplicarCupom("VERAO10", 150.0));

// compra de R$ 300 com cupom percentual (com bônus progressivo)
console.log("Compra R$300 + VERAO10:", aplicarCupom("VERAO10", 300.0));

// cupom de valor fixo
console.log("Compra R$50 + FRETE:", aplicarCupom("FRETE", 50.0));

// cupom inexistente — deve lançar exceção
try {
  aplicarCupom("INVALIDO", 100.0);
} catch (erro) {
  console.log(`Erro esperado: ${(erro as Error).message}`);
}
