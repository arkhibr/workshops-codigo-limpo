/**
 * GABARITO — importação de catálogo de produtos após refatoração assistida
 * Referência: Clean Code, Cap. 3 (Funções)
 *
 * Responsabilidades separadas:
 *   - lerLinhas: lê e descarta o cabeçalho do CSV
 *   - validarProduto: verifica campos obrigatórios e formatos
 *   - converterProduto: converte tipos e monta o objeto
 *   - filtrarProduto: aplica regras de negócio (preço e estoque)
 *   - importarProdutos: orquestra as quatro funções acima
 *
 * Execute: npx ts-node sessao-5/tutorial-10-refatoracao-assistida/exercicios/gabarito.ts
 */

const SEPARADOR_CSV = ",";
const INDICE_NOME = 0;
const INDICE_CATEGORIA = 1;
const INDICE_PRECO = 2;
const INDICE_QUANTIDADE = 3;
const TOTAL_CAMPOS_ESPERADO = 4;
const PRECO_MINIMO = 0.0;
const QUANTIDADE_MINIMA = 0;

interface Produto {
  nome: string;
  categoria: string;
  preco: number;
  quantidade: number;
}


function lerLinhas(conteudoCsv: string): string[] {
  const linhas = conteudoCsv.trim().split("\n");
  return linhas.slice(1);  // descarta cabeçalho
}


function validarProduto(campos: string[]): boolean {
  if (campos.length !== TOTAL_CAMPOS_ESPERADO) {
    return false;
  }
  const nome = campos[INDICE_NOME].trim();
  const categoria = campos[INDICE_CATEGORIA].trim();
  if (!nome || !categoria) {
    return false;
  }
  const preco = parseFloat(campos[INDICE_PRECO].trim());
  const quantidade = parseInt(campos[INDICE_QUANTIDADE].trim(), 10);
  return !isNaN(preco) && !isNaN(quantidade);
}


function converterProduto(campos: string[]): Produto {
  return {
    nome: campos[INDICE_NOME].trim(),
    categoria: campos[INDICE_CATEGORIA].trim(),
    preco: parseFloat(campos[INDICE_PRECO].trim()),
    quantidade: parseInt(campos[INDICE_QUANTIDADE].trim(), 10),
  };
}


function filtrarProduto(produto: Produto): boolean {
  return produto.preco > PRECO_MINIMO && produto.quantidade >= QUANTIDADE_MINIMA;
}


function importarProdutos(conteudoCsv: string): Produto[] {
  const produtos: Produto[] = [];
  for (const linha of lerLinhas(conteudoCsv)) {
    const campos = linha.split(SEPARADOR_CSV);
    if (!validarProduto(campos)) {
      continue;
    }
    const produto = converterProduto(campos);
    if (filtrarProduto(produto)) {
      produtos.push(produto);
    }
  }
  return produtos;
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

const produtos = importarProdutos(catalogoCsv);
console.log(`Produtos importados: ${produtos.length}`);
for (const produto of produtos) {
  console.log(`  [${produto.categoria}] ${produto.nome} — R$ ${produto.preco.toFixed(2)} (${produto.quantidade} un.)`);
}
