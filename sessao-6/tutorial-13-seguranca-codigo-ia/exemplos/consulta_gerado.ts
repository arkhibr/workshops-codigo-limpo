/**
 * SAÍDA TÍPICA DE IA — endpoint de consulta de cliente (prompt funcional puro)
 * Referência: Tutorial 13 — Segurança em Código Gerado por IA
 *
 * ⚠️  Este arquivo é INTENCIONALMENTE INSEGURO.
 *     Representa o código que uma IA gera quando segurança não é especificada no prompt.
 *     Analise as brechas antes de ver a versão revisada.
 *
 * Brechas demonstradas:
 *   1. Credencial hardcoded no código-fonte
 *   2. Query montada por concatenação de string (injeção simulada)
 *   3. Sem validação do parâmetro de entrada
 *
 * Execute: npx ts-node sessao-6/tutorial-13-seguranca-codigo-ia/exemplos/consulta_gerado.ts
 */

// Prompt usado: "cria uma função que consulta cliente por ID no banco de dados"

// ─── Brecha 1: credencial hardcoded ───────────────────────────────────────────
const DB_SENHA = "s3nh4_producao_2024";       // visível para qualquer um com acesso ao repo
const API_KEY  = "sk-abc123xyz789secret";     // token de API hardcoded

interface DadosCliente {
  nome: string;
  email: string;
  saldo: number;
}

// banco de dados simulado em memória (substitui conexão real para a demonstração)
const banco: Record<string, DadosCliente> = {
  "1001": { nome: "Ana Lima",    email: "ana@exemplo.com",    saldo: 1500.00 },
  "2002": { nome: "Carlos Souza",email: "carlos@exemplo.com", saldo: 3200.00 },
};


function consultar_cliente(parametro: string): DadosCliente | DadosCliente[] | undefined {
  // ─── Brecha 2: concatenação de string ───────────────────────────────────────
  // A IA montou a "query" juntando o parâmetro diretamente na string.
  // Em um banco real, isso permitiria injeção de SQL.
  // Aqui simulamos o efeito: a entrada controla quais registros são retornados.
  const query = "SELECT * FROM clientes WHERE id = " + parametro;
  console.log(`  Query executada: ${query}`);

  // ─── Simulação do efeito da injeção ─────────────────────────────────────────
  // Sem parametrização, a entrada controla a lógica de busca.
  // Uma entrada como "1001 OR true" faz a condição sempre ser verdadeira
  // e retorna TODOS os registros — como aconteceria em SQL real.
  if (parametro.toUpperCase().includes(" OR ") || parametro.includes("%")) {
    // simula o efeito de uma condição sempre-verdadeira (injeção bem-sucedida)
    console.log("  [INJEÇÃO DETECTADA NA SIMULAÇÃO] Condição sempre verdadeira — retornando todos os registros:");
    return Object.values(banco);
  }

  // ─── Brecha 3: sem validação ─────────────────────────────────────────────────
  // Aceita qualquer valor sem verificar formato ou tipo.
  return banco[parametro];
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

console.log("=== Demonstração: consulta_gerado.ts (INTENCIONALMENTE INSEGURO) ===");
console.log();

console.log("--- Consulta normal (ID legítimo) ---");
const resultado = consultar_cliente("1001");
console.log(`  Resultado: ${JSON.stringify(resultado)}`);
console.log();

console.log("--- Consulta com entrada maliciosa (injeção simulada) ---");
// em SQL real: WHERE id = 1001 OR 1=1  → retorna todos os registros
const entradaMaliciosa = "1001 OR 1=1";
const resultadoInjetado = consultar_cliente(entradaMaliciosa) as DadosCliente[];
console.log(`  Registros retornados: ${resultadoInjetado.length}`);
for (const cliente of resultadoInjetado) {
  console.log(`    ${JSON.stringify(cliente)}`);
}
console.log();

console.log("--- Brecha 1: segredos visíveis no código ---");
console.log(`  DB_SENHA = '${DB_SENHA}'`);
console.log(`  API_KEY  = '${API_KEY}'`);
console.log();

console.log("Conclusão: sem validação e sem parametrização, a entrada do usuário");
console.log("controla quais dados são retornados — e as credenciais estão expostas.");
