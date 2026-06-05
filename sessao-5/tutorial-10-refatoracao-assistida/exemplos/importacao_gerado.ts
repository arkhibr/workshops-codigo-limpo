/**
 * SAÍDA TÍPICA DE IA — importação de clientes a partir de CSV (a partir de prompt aberto)
 * Referência: Clean Code, Cap. 3 (Funções)
 *
 * ⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
 *     Representa o tipo de código monolítico que uma IA gera a partir de um prompt aberto.
 *     Analise os problemas de coesão antes de ver a versão revisada.
 *
 * Execute: npx ts-node sessao-5/tutorial-10-refatoracao-assistida/exemplos/importacao_gerado.ts
 */

// Prompt usado: "importa clientes de um CSV"


function importar(csv: string): any[] {  // faz tudo: lê, valida, converte e acumula
  const r: any[] = [];
  const linhas = csv.trim().split("\n").slice(1);  // descarta cabeçalho inline
  for (const l of linhas) {
    const p = l.split(",");
    if (p.length !== 3) {  // validação misturada com leitura
      continue;
    }
    const n = p[0].trim(), e = p[1].trim(), c = p[2].trim();
    if (!n || !e || !e.includes("@")) {  // mais validação no mesmo loop
      continue;
    }
    r.push({ nome: n, email: e, cidade: c });  // conversão inline
  }
  return r;
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

const dados =
  "nome,email,cidade\n" +
  "Ana Silva,ana@exemplo.com,São Paulo\n" +
  "Carlos,carlos-invalido,Rio de Janeiro\n" +
  "Beatriz Santos,beatriz@exemplo.com,Curitiba\n" +
  ",email@vazio.com,Belo Horizonte\n" +
  "Diego Lima,diego@exemplo.com,Porto Alegre\n";

const clientes = importar(dados);
console.log(`Clientes importados: ${clientes.length}`);
for (const c of clientes) {
  console.log(`  ${c.nome} <${c.email}> — ${c.cidade}`);
}
