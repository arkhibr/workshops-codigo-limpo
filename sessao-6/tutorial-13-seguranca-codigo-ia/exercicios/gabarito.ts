/**
 * GABARITO — busca de pedidos com segurança aplicada
 * Referência: Tutorial 13 — Segurança em Código Gerado por IA
 *
 * Brechas corrigidas em relação ao exercício:
 *   1. Chave de integração lida de variável de ambiente (sem segredo no código)
 *   2. Nome do cliente validado antes de qualquer operação de busca
 *   3. Busca parametrizada — filtragem por comparação exata, sem concatenação de string
 *   4. Entrada maliciosa rejeitada com mensagem clara antes de processar
 *
 * Execute: npx ts-node sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/gabarito.ts
 */

// ─── Configuração lida de "ambiente" (sem segredo no código) ──────────────────
// Em produção: process.env.CHAVE_INTEGRACAO leria da variável de ambiente real.
// Aqui simulamos com um objeto de configuração separado — o segredo não está
// junto ao código de produção, mas em uma camada de configuração isolada.
const configuracaoAmbiente: Record<string, string> = {
  CHAVE_INTEGRACAO: "<não configurado>",  // em produção: process.env.CHAVE_INTEGRACAO
};

const CHAVE_INTEGRACAO = configuracaoAmbiente["CHAVE_INTEGRACAO"];

// ─── Constantes de validação ──────────────────────────────────────────────────
const FORMATO_NOME_VALIDO = /^[A-Za-zÀ-ÿ\s]{2,80}$/;  // letras e espaços, 2–80 chars

interface Pedido {
  id: string;
  cliente: string;
  valor: number;
  status: string;
}

// ─── Pedidos simulados em memória ─────────────────────────────────────────────
const pedidos: Pedido[] = [
  { id: "PED-001", cliente: "Ana Lima",    valor: 250.00, status: "entregue" },
  { id: "PED-002", cliente: "Carlos Souza",valor: 89.90,  status: "em_transito" },
  { id: "PED-003", cliente: "Ana Lima",    valor: 410.00, status: "processando" },
  { id: "PED-004", cliente: "Julia Rocha", valor: 75.00,  status: "entregue" },
];


function validarNomeCliente(nomeCliente: string): void {
  /**
   * Verifica se o nome do cliente tem formato válido.
   * Lança Error se o nome contiver caracteres não permitidos ou estiver fora do tamanho esperado.
   */
  if (!FORMATO_NOME_VALIDO.test(nomeCliente)) {
    throw new Error(
      `Nome inválido: '${nomeCliente}'. ` +
      "Esperado: letras e espaços, entre 2 e 80 caracteres."
    );
  }
}


function buscarPedidosDoCliente(nomeCliente: string): Pedido[] {
  /**
   * Retorna todos os pedidos do cliente informado.
   *
   * A busca é parametrizada: o nome é comparado por igualdade exata
   * — nunca concatenado em string de query SQL.
   *
   * Lança Error se o nome do cliente tiver formato inválido.
   */
  validarNomeCliente(nomeCliente);

  // busca parametrizada — comparação exata, sem concatenação de string
  return pedidos.filter(p => p.cliente === nomeCliente);
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

console.log("=== Gabarito: busca de pedidos (seguro) ===");
console.log();

console.log("--- Busca normal ---");
try {
  const resultados = buscarPedidosDoCliente("Ana Lima");
  console.log(`  Pedidos encontrados: ${resultados.length}`);
  for (const p of resultados) {
    console.log(`    ${JSON.stringify(p)}`);
  }
} catch (erro) {
  console.log(`  Erro: ${(erro as Error).message}`);
}
console.log();

console.log("--- Busca com entrada maliciosa (deve ser rejeitada) ---");
const entradaMaliciosa = "Ana Lima' OR '1'='1";
try {
  const resultados = buscarPedidosDoCliente(entradaMaliciosa);
  console.log(`  Pedidos encontrados: ${resultados.length}`);
} catch (erro) {
  console.log(`  Rejeitado corretamente: ${(erro as Error).message}`);
}
console.log();

console.log("--- Busca com nome inexistente ---");
try {
  const resultados = buscarPedidosDoCliente("Maria Silva");
  console.log(`  Pedidos encontrados: ${resultados.length}`);
} catch (erro) {
  console.log(`  Erro: ${(erro as Error).message}`);
}
console.log();

console.log("--- Configuração: chave fora do código ---");
console.log(`  CHAVE_INTEGRACAO lida do ambiente: '${CHAVE_INTEGRACAO}'`);
console.log();

console.log("Conclusão: entrada maliciosa rejeitada pela validação;");
console.log("chave de integração não está no código-fonte.");
