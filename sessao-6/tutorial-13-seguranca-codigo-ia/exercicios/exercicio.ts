/**
 * EXERCÍCIO — busca de pedidos gerada por IA (com brechas de segurança)
 * Referência: Tutorial 13 — Segurança em Código Gerado por IA
 *
 * ⚠️  Este arquivo é INTENCIONALMENTE INSEGURO — é a saída da IA que você vai corrigir.
 *
 * Tarefas:
 *   (1) Tire o segredo do código — mova para variável de configuração ou ambiente.
 *   (2) Parametrize e valide a entrada do usuário antes de usá-la na busca.
 *   (3) Liste todas as brechas que você identificou antes de começar a corrigir.
 *
 * Execute: npx ts-node sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/exercicio.ts
 * Gabarito: npx ts-node sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/gabarito.ts
 */

// Prompt usado (fraco): "cria uma função que busca pedidos de um cliente pelo nome"

// ─── Brecha 1: chave de integração hardcoded ───────────────────────────────────
const CHAVE_INTEGRACAO = "tok-pedidos-abc987xyz";  // exposta no código-fonte

interface Pedido {
  id: string;
  cliente: string;
  valor: number;
  status: string;
}

// pedidos simulados em memória (substitui banco real)
const pedidos: Pedido[] = [
  { id: "PED-001", cliente: "Ana Lima",    valor: 250.00, status: "entregue" },
  { id: "PED-002", cliente: "Carlos Souza",valor: 89.90,  status: "em_transito" },
  { id: "PED-003", cliente: "Ana Lima",    valor: 410.00, status: "processando" },
  { id: "PED-004", cliente: "Julia Rocha", valor: 75.00,  status: "entregue" },
];


function buscarPedidos(nomeCliente: string): Pedido[] {
  // ─── Brecha 2: filtro montado por concatenação de string ────────────────────
  // A IA concatenou o valor diretamente no "filtro" de busca.
  // Em um banco real, isso seria vulnerável a injeção de SQL.
  const filtro = "SELECT * FROM pedidos WHERE cliente = '" + nomeCliente + "'";
  console.log(`  Filtro aplicado: ${filtro}`);

  // ─── Brecha 3: sem validação do parâmetro ───────────────────────────────────
  // Aceita qualquer valor sem verificar tipo, formato ou tamanho.
  // Uma entrada com aspas quebra o SQL em bancos reais.

  // simulação do efeito de injeção por aspas simples na entrada
  if (nomeCliente.includes("'") || nomeCliente.includes("--")) {
    console.log("  [INJEÇÃO SIMULADA] Aspas/comentário na entrada — em SQL real quebraria a query ou vazaria dados.");
    return [...pedidos];  // simula retorno de todos os registros
  }

  return pedidos.filter(p => p.cliente === nomeCliente);
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

console.log("=== Exercício: busca de pedidos (INTENCIONALMENTE INSEGURO) ===");
console.log();

console.log("--- Busca normal ---");
const resultados = buscarPedidos("Ana Lima");
console.log(`  Pedidos encontrados: ${resultados.length}`);
for (const p of resultados) {
  console.log(`    ${JSON.stringify(p)}`);
}
console.log();

console.log("--- Busca com entrada maliciosa (aspas simples) ---");
const entradaMaliciosa = "Ana Lima' OR '1'='1";
const resultadosInjetados = buscarPedidos(entradaMaliciosa);
console.log(`  Registros retornados: ${resultadosInjetados.length}`);
for (const p of resultadosInjetados) {
  console.log(`    ${JSON.stringify(p)}`);
}
console.log();

console.log("--- Brecha: chave de integração visível ---");
console.log(`  CHAVE_INTEGRACAO = '${CHAVE_INTEGRACAO}'`);
