/**
 * EXERCÍCIO — Testes de Caracterização Antes de Mudanças Assistidas
 * Referência: Feathers (testes de caracterização) + Clean Code, Cap. 9 (Testes)
 *
 * Domínio: cálculo de desconto de fidelidade por faixas de pontos acumulados.
 *
 * Sua tarefa (em três etapas):
 *   (1) Escreva testes de caracterização do comportamento atual usando a
 *       convenção verificar*: funções que imprimem "OK: <caso>" ou
 *       "FALHOU: <caso> (esperado X, obtido Y)". Cubra cada faixa e os
 *       valores-limite.
 *   (2) Só depois que todos os testes passarem com o código intocado,
 *       peça à IA a mudança: adicionar uma nova faixa para clientes com
 *       mais de 2.000 pontos (desconto de 25%).
 *   (3) Rode os testes antes e depois da mudança. Se algum falhar,
 *       encontre e corrija a regressão antes de aceitar o código gerado.
 *
 * Execute: npx ts-node sessao-6/tutorial-14-testes-guard-rails/exercicios/exercicio.ts
 */

// Tabela de faixas de desconto por pontos acumulados:
//   0–499 pontos    → 0% de desconto
//   500–999 pontos  → 5% de desconto
//   1.000–1.999 pts → 10% de desconto
//   2.000+ pontos   → (sem faixa definida — será adicionada pela mudança)

const DESCONTO_SEM_PONTOS = 0.00;
const DESCONTO_BRONZE = 0.05;
const DESCONTO_PRATA = 0.10;

function calcularDescontoFidelidade(pontos: number, valorCompra: number): number {
  /**
   * Calcula o desconto de fidelidade com base nos pontos acumulados.
   * Retorna o valor do desconto (não o valor final da compra).
   */
  let percentual: number;

  if (pontos < 500) {
    percentual = DESCONTO_SEM_PONTOS;
  } else if (pontos < 1000) {
    percentual = DESCONTO_BRONZE;
  } else {
    percentual = DESCONTO_PRATA;
  }

  return Math.round(valorCompra * percentual * 100) / 100;
}

// ─── TODO: escreva suas verificações verificar* aqui ─────────────────────────
//
// Exemplo de estrutura:
//
// function verificarDescontoSemPontos(): void {
//   const resultado = calcularDescontoFidelidade(100, 200.00);
//   const esperado = 0.00;
//   if (Math.abs(resultado - esperado) < 0.01) {
//     console.log("OK: desconto sem pontos");
//   } else {
//     console.log(`FALHOU: desconto sem pontos (esperado ${esperado}, obtido ${resultado})`);
//   }
// }
//
// Lembre-se de cobrir:
//   - cada faixa com um caso típico
//   - os valores exatos de limite (499, 500, 999, 1.000)
//   - valorCompra variado (0.00, valor pequeno, valor grande)

// ─── Execução de demonstração ─────────────────────────────────────────────────

console.log("=== Exercício: exercicio.ts ===");
console.log();
console.log("Comportamento atual da função calcularDescontoFidelidade:");
console.log();

const casos: Array<[number, number, string]> = [
  [100,  200.00, "sem pontos (faixa 0%)"],
  [499,  200.00, "limite inferior bronze (499 pts)"],
  [500,  200.00, "bronze (500 pts, 5%)"],
  [999,  200.00, "limite inferior prata (999 pts)"],
  [1000, 200.00, "prata (1.000 pts, 10%)"],
  [1500, 200.00, "prata alto (1.500 pts, 10%)"],
];

for (const [pontos, valor, descricao] of casos) {
  const desconto = calcularDescontoFidelidade(pontos, valor);
  console.log(`  ${String(pontos).padStart(5)} pts, R$ ${valor.toFixed(2)} → desconto R$ ${desconto.toFixed(2)}  (${descricao})`);
}

console.log();
console.log("Escreva os testes de caracterização ANTES de pedir a mudança à IA.");
