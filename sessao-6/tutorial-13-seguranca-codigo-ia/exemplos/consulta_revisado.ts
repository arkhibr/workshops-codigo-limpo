/**
 * VERSÃO REVISADA — endpoint de consulta de cliente com segurança aplicada
 * Referência: Tutorial 13 — Segurança em Código Gerado por IA
 *
 * Brechas corrigidas em relação à versão gerada:
 *   1. Credencial lida de configuração separada (simula variável de ambiente)
 *   2. Consulta parametrizada — entrada nunca é concatenada na query
 *   3. Validação explícita da entrada antes de qualquer operação
 *   4. Entrada maliciosa rejeitada com mensagem descritiva
 *
 * Execute: npx ts-node sessao-6/tutorial-13-seguranca-codigo-ia/exemplos/consulta_revisado.ts
 */

// ─── Configuração lida de "ambiente" (sem segredo no código) ──────────────────
// Em produção: as credenciais seriam lidas de variáveis de ambiente.
// Aqui simulamos com um objeto de configuração separado — o segredo não está
// junto ao código de produção, mas em uma camada de configuração isolada.
const configuracaoAmbiente: Record<string, string> = {
  DB_SENHA: "<não configurado>",  // em produção: process.env.DB_SENHA
  API_KEY:  "<não configurado>",  // em produção: process.env.API_KEY
};

const DB_SENHA = configuracaoAmbiente["DB_SENHA"];
const API_KEY  = configuracaoAmbiente["API_KEY"];

// ─── Constantes de validação ──────────────────────────────────────────────────
const FORMATO_ID_VALIDO = /^\d{1,10}$/;  // apenas dígitos, 1–10 caracteres

interface DadosCliente {
  nome: string;
  email: string;
  saldo: number;
}

// ─── Banco de dados simulado em memória ───────────────────────────────────────
const bancoClientes: Record<string, DadosCliente> = {
  "1001": { nome: "Ana Lima",    email: "ana@exemplo.com",    saldo: 1500.00 },
  "2002": { nome: "Carlos Souza",email: "carlos@exemplo.com", saldo: 3200.00 },
};


function validarIdCliente(idCliente: string): void {
  /**
   * Verifica se o ID do cliente tem formato válido.
   * Lança Error se o ID não for composto apenas por dígitos (1–10 caracteres).
   */
  if (!FORMATO_ID_VALIDO.test(idCliente)) {
    throw new Error(
      `ID inválido: '${idCliente}'. Esperado: até 10 dígitos numéricos.`
    );
  }
}


function consultarCliente(idCliente: string): DadosCliente {
  /**
   * Consulta e retorna os dados do cliente pelo ID informado.
   *
   * A consulta é parametrizada: o ID é usado como chave de busca exata
   * no repositório em memória — nunca concatenado em string de query.
   *
   * Lança Error se o ID for inválido ou o cliente não for encontrado.
   */
  validarIdCliente(idCliente);

  // consulta parametrizada — busca por chave exata, sem concatenação de string
  const cliente = bancoClientes[idCliente];

  if (cliente === undefined) {
    throw new Error(`Cliente com ID '${idCliente}' não encontrado.`);
  }

  return cliente;
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

console.log("=== Demonstração: consulta_revisado.ts (seguro) ===");
console.log();

console.log("--- Consulta normal (ID legítimo) ---");
try {
  const resultado = consultarCliente("1001");
  console.log(`  Resultado: ${JSON.stringify(resultado)}`);
} catch (erro) {
  console.log(`  Erro: ${(erro as Error).message}`);
}
console.log();

console.log("--- Consulta com entrada maliciosa (deve ser rejeitada) ---");
const entradaMaliciosa = "1001 OR 1=1";
try {
  const resultado = consultarCliente(entradaMaliciosa);
  console.log(`  Resultado: ${JSON.stringify(resultado)}`);
} catch (erro) {
  console.log(`  Rejeitado corretamente: ${(erro as Error).message}`);
}
console.log();

console.log("--- Consulta com ID inexistente ---");
try {
  const resultado = consultarCliente("9999");
  console.log(`  Resultado: ${JSON.stringify(resultado)}`);
} catch (erro) {
  console.log(`  Não encontrado (esperado): ${(erro as Error).message}`);
}
console.log();

console.log("--- Configuração: segredos fora do código ---");
console.log(`  DB_SENHA lida do ambiente: '${DB_SENHA}'`);
console.log(`  API_KEY lida do ambiente:  '${API_KEY}'`);
console.log();

console.log("Conclusão: entrada maliciosa rejeitada antes de chegar à consulta;");
console.log("credenciais não estão no código-fonte.");
