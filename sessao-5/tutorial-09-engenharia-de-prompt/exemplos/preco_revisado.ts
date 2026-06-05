/**
 * VERSÃO REVISADA — cálculo de preço com descontos após revisão de código gerado por IA
 * Referência: Clean Code, Cap. 2–3; engenharia de contexto em prompts de código
 *
 * Problemas corrigidos em relação à versão gerada:
 *   - Nomes descritivos em português para todos os identificadores
 *   - Parâmetros soltos substituídos por interface ItemPedido tipada
 *   - Números mágicos extraídos como constantes nomeadas
 *   - Regras de desconto separadas em funções próprias
 *   - Acumulação indevida de descontos eliminada (aplica apenas o maior)
 *   - Validação com exceção descritiva em vez de comportamento silencioso
 *
 * Nota didática: mesmo a partir de um prompt estruturado, a IA gerou a
 * comparação de descontos inline na função principal — foi preciso extrair
 * `selecionarMaiorDesconto` manualmente para manter a responsabilidade única.
 *
 * Execute: npx ts-node sessao-5/tutorial-09-engenharia-de-prompt/exemplos/preco_revisado.ts
 */

const DESCONTO_VOLUME_PCT = 0.10;       // desconto por quantidade elevada
const QUANTIDADE_MINIMA_VOLUME = 5;     // quantidade mínima para desconto por volume
const DESCONTO_PREMIUM_PCT = 0.15;      // desconto para itens da categoria premium
const SEM_DESCONTO = 0.0;              // sentinela para ausência de desconto

interface ItemPedido {
  descricao: string;
  precoUnitario: number;
  quantidade: number;
  categoria: string;
}


function descontoPorVolume(item: ItemPedido): number {
  if (item.quantidade >= QUANTIDADE_MINIMA_VOLUME) {
    return DESCONTO_VOLUME_PCT;
  }
  return SEM_DESCONTO;
}


function descontoPorCategoria(item: ItemPedido): number {
  if (item.categoria === "premium") {
    return DESCONTO_PREMIUM_PCT;
  }
  return SEM_DESCONTO;
}


function selecionarMaiorDesconto(item: ItemPedido): number {
  return Math.max(descontoPorVolume(item), descontoPorCategoria(item));
}


function calcularPrecoFinal(item: ItemPedido): number {
  if (item.precoUnitario <= 0) {
    throw new Error(
      `Preço unitário inválido para '${item.descricao}': ${item.precoUnitario}. ` +
      "O valor deve ser maior que zero."
    );
  }

  const desconto = selecionarMaiorDesconto(item);
  const precoComDesconto = item.precoUnitario * (1 - desconto) * item.quantidade;
  return Math.round(precoComDesconto * 100) / 100;
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

const itemSimples: ItemPedido = {
  descricao: "Camiseta Básica",
  precoUnitario: 50.0,
  quantidade: 3,
  categoria: "padrao",
};
console.log("Preço item simples (sem desconto):", calcularPrecoFinal(itemSimples));

const itemVolume: ItemPedido = {
  descricao: "Camiseta Básica",
  precoUnitario: 50.0,
  quantidade: 6,
  categoria: "padrao",
};
console.log("Preço com desconto por volume:", calcularPrecoFinal(itemVolume));

const itemPremium: ItemPedido = {
  descricao: "Tênis Premium",
  precoUnitario: 200.0,
  quantidade: 2,
  categoria: "premium",
};
console.log("Preço com desconto premium:", calcularPrecoFinal(itemPremium));

// volume + premium: aplica apenas o maior (premium = 15% > volume = 10%)
const itemPremiumVolume: ItemPedido = {
  descricao: "Tênis Premium",
  precoUnitario: 200.0,
  quantidade: 6,
  categoria: "premium",
};
console.log("Preço premium com volume (aplica apenas o maior):", calcularPrecoFinal(itemPremiumVolume));

// preço inválido — deve lançar exceção
try {
  const itemInvalido: ItemPedido = {
    descricao: "Produto Inválido",
    precoUnitario: 0.0,
    quantidade: 1,
    categoria: "padrao",
  };
  calcularPrecoFinal(itemInvalido);
} catch (erro) {
  console.log(`\nValidação: ${(erro as Error).message}`);
}
