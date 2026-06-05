/**
 * VERSÃO REVISADA — importação de clientes a partir de CSV após refatoração assistida
 * Referência: Clean Code, Cap. 3 (Funções)
 *
 * Problemas corrigidos em relação à versão gerada:
 *   - Função monolítica dividida em responsabilidades únicas
 *   - lerLinhas: lê e descarta o cabeçalho
 *   - validarCliente: verifica campos obrigatórios e formato de e-mail
 *   - converterCliente: monta o objeto com campos normalizados
 *   - importarClientes: orquestra as três funções acima
 *   - Nomes descritivos em português para todos os identificadores
 *
 * Nota didática: o comportamento é idêntico ao da versão gerada — apenas
 * a estrutura interna foi reorganizada em passos pequenos e verificáveis.
 *
 * Execute: npx ts-node sessao-5/tutorial-10-refatoracao-assistida/exemplos/importacao_revisado.ts
 */

const SEPARADOR_CSV = ",";
const INDICE_NOME = 0;
const INDICE_EMAIL = 1;
const INDICE_CIDADE = 2;
const TOTAL_CAMPOS_ESPERADO = 3;

interface Cliente {
  nome: string;
  email: string;
  cidade: string;
}


function lerLinhas(conteudoCsv: string): string[] {
  const linhas = conteudoCsv.trim().split("\n");
  return linhas.slice(1);  // descarta cabeçalho
}


function validarCliente(campos: string[]): boolean {
  if (campos.length !== TOTAL_CAMPOS_ESPERADO) {
    return false;
  }
  const nome = campos[INDICE_NOME].trim();
  const email = campos[INDICE_EMAIL].trim();
  return nome.length > 0 && email.length > 0 && email.includes("@");
}


function converterCliente(campos: string[]): Cliente {
  return {
    nome: campos[INDICE_NOME].trim(),
    email: campos[INDICE_EMAIL].trim(),
    cidade: campos[INDICE_CIDADE].trim(),
  };
}


function importarClientes(conteudoCsv: string): Cliente[] {
  const clientes: Cliente[] = [];
  for (const linha of lerLinhas(conteudoCsv)) {
    const campos = linha.split(SEPARADOR_CSV);
    if (validarCliente(campos)) {
      clientes.push(converterCliente(campos));
    }
  }
  return clientes;
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

const dados =
  "nome,email,cidade\n" +
  "Ana Silva,ana@exemplo.com,São Paulo\n" +
  "Carlos,carlos-invalido,Rio de Janeiro\n" +
  "Beatriz Santos,beatriz@exemplo.com,Curitiba\n" +
  ",email@vazio.com,Belo Horizonte\n" +
  "Diego Lima,diego@exemplo.com,Porto Alegre\n";

const clientes = importarClientes(dados);
console.log(`Clientes importados: ${clientes.length}`);
for (const cliente of clientes) {
  console.log(`  ${cliente.nome} <${cliente.email}> — ${cliente.cidade}`);
}
