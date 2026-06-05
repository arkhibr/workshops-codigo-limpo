/**
 * EXERCÍCIO — importação de catálogo de produtos (saída de IA com baixa coesão)
 * Referência: Clean Code, Cap. 3 (Funções)
 *
 * ⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
 *     Representa o tipo de código monolítico que uma IA gera a partir de um prompt aberto.
 *     Sua tarefa:
 *
 *     (1) Refatore em passos pequenos, extraindo uma responsabilidade por vez.
 *     (2) Rode o arquivo após cada passo para confirmar que a saída é preservada.
 *     (3) Liste as responsabilidades que você separou.
 *
 * Execute: npx ts-node sessao-5/tutorial-10-refatoracao-assistida/exercicios/exercicio.ts
 */

// Prompt usado: "importa produtos de um CSV"


function processar(data: string): any[] {  // lê, valida, converte, filtra e acumula tudo junto
  const res: any[] = [];
  const rows = data.trim().split("\n").slice(1);  // descarta cabeçalho inline
  for (const r of rows) {
    const cols = r.split(",");
    if (cols.length !== 4) {  // validação misturada com leitura
      continue;
    }
    const nm = cols[0].trim(), cat = cols[1].trim();
    const pr = cols[2].trim(), qt = cols[3].trim();
    if (!nm || !cat) {  // validação de campos obrigatórios inline
      continue;
    }
    const preco = parseFloat(pr);  // conversão de tipo inline
    const qtd = parseInt(qt, 10);
    if (isNaN(preco) || isNaN(qtd)) {
      continue;
    }
    if (preco <= 0 || qtd < 0) {  // regra de negócio inline
      continue;
    }
    res.push({ nome: nm, categoria: cat, preco, quantidade: qtd });  // conversão inline
  }
  return res;
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

const catalogoCsv =
  "nome,categoria,preco,quantidade\n" +
  "Teclado Mecânico,Periféricos,350.00,15\n" +
  "Mouse Sem Fio,Periféricos,120.00,30\n" +
  "Monitor 24pol,Monitores,-50.00,5\n" +
  "Headset Gamer,Periféricos,280.00,0\n" +
  "Webcam HD,,90.00,12\n" +
  "Hub USB,Acessórios,abc,8\n" +
  "SSD 1TB,Armazenamento,450.00,20\n";

const produtos = processar(catalogoCsv);
console.log(`Produtos importados: ${produtos.length}`);
for (const p of produtos) {
  console.log(`  [${p.categoria}] ${p.nome} — R$ ${p.preco.toFixed(2)} (${p.quantidade} un.)`);
}
