/**
 * exercicio.ts — Endpoint de busca de produtos por descrição.
 *
 * Gerado por IA como ponto de partida. O código parece seguro — inspecione
 * toda a construção da query antes de concluir.
 *
 * Exercício:
 *   (1) Ache a brecha sutil — toda a query é realmente segura?
 *   (2) Endureça o código corrigindo a brecha encontrada.
 *   (3) Liste o que faltava no código original.
 *
 * Execute: npx ts-node exercicio.ts
 */

// ---------------------------------------------------------------------------
// Constantes de domínio
// ---------------------------------------------------------------------------

const CATEGORIAS_VALIDAS = new Set(["eletronicos", "vestuario", "alimentos", "livraria"]);

const CAMPOS_ORDENACAO_PERMITIDOS = new Set(["preco", "nomeProduto", "estoqueDisponivel"]);

// ---------------------------------------------------------------------------
// Modelos de dados
// ---------------------------------------------------------------------------

interface FiltroProduto {
  categoria:   string;
  termoBusca:  string;
}

interface Produto {
  id:                number;
  nomeProduto:       string;
  categoria:         string;
  descricao:         string;
  preco:             number;
  estoqueDisponivel: number;
}

function validarFiltros(filtros: FiltroProduto): void {
  if (!CATEGORIAS_VALIDAS.has(filtros.categoria)) {
    throw new Error(`Categoria inválida: '${filtros.categoria}'`);
  }
}

// ---------------------------------------------------------------------------
// Banco de dados simulado em memória
// ---------------------------------------------------------------------------

const BANCO_PRODUTOS: Produto[] = [
  { id: 1, nomeProduto: "Notebook Pro",     categoria: "eletronicos", descricao: "Notebook 15 polegadas Intel i7",     preco: 4500.00, estoqueDisponivel: 12 },
  { id: 2, nomeProduto: "Fone Bluetooth",   categoria: "eletronicos", descricao: "Fone sem fio cancelamento de ruído",  preco:  350.00, estoqueDisponivel: 45 },
  { id: 3, nomeProduto: "Camiseta Algodão", categoria: "vestuario",   descricao: "Camiseta 100% algodão lavada",         preco:   89.90, estoqueDisponivel: 80 },
  { id: 4, nomeProduto: "Calça Jeans",      categoria: "vestuario",   descricao: "Calça jeans slim fit masculina",       preco:  199.00, estoqueDisponivel: 30 },
  { id: 5, nomeProduto: "Café Especial",    categoria: "alimentos",   descricao: "Café arábica torrado médio 500g",      preco:   42.00, estoqueDisponivel: 200 },
  { id: 6, nomeProduto: "Clean Code",       categoria: "livraria",    descricao: "Livro Clean Code Robert C. Martin",    preco:   95.00, estoqueDisponivel: 15 },
];

// ---------------------------------------------------------------------------
// Validação de segurança (parcial)
// ---------------------------------------------------------------------------

/**
 * Valida que o campo de ordenação pertence ao allow-list.
 */
function campoOrdenacaoSeguro(ordenacao: string): keyof Produto {
  const campo = ordenacao.trim();
  if (!CAMPOS_ORDENACAO_PERMITIDOS.has(campo)) {
    throw new Error(
      `Campo de ordenação inválido: '${ordenacao}'. ` +
      `Permitidos: ${[...CAMPOS_ORDENACAO_PERMITIDOS].sort().join(", ")}`,
    );
  }
  return campo as keyof Produto;
}

// ---------------------------------------------------------------------------
// Lógica de busca
// ---------------------------------------------------------------------------

/**
 * Busca produtos por categoria e filtra por termo na descrição.
 *
 * Categoria é validada antes do filtro para prevenir entradas inválidas.
 * Ordenação é validada por allow-list antes de ser usada.
 * Filtro de descrição aplica o termoBusca diretamente — sem sanitização.
 */
function buscarProdutos(filtros: FiltroProduto, ordenacao: string = "nomeProduto"): Produto[] {
  validarFiltros(filtros);
  const campo = campoOrdenacaoSeguro(ordenacao);

  // WHERE: categoria parametrizada (segura). termoBusca concatenado no LIKE — sem escape.
  const filtrados = BANCO_PRODUTOS.filter(
    (p) =>
      p.categoria === filtros.categoria &&
      p.descricao.toLowerCase().includes(filtros.termoBusca.toLowerCase()),
  );

  return [...filtrados].sort((a, b) => {
    const va = a[campo];
    const vb = b[campo];
    if (typeof va === "number" && typeof vb === "number") return va - vb;
    return String(va ?? "").localeCompare(String(vb ?? ""));
  });
}

// ---------------------------------------------------------------------------
// Demo
// ---------------------------------------------------------------------------

function demonstrarBuscaNormal(): void {
  const filtros: FiltroProduto = { categoria: "eletronicos", termoBusca: "fio" };
  const resultados = buscarProdutos(filtros, "preco");

  console.log("Busca normal (categoria=eletronicos, termo=fio, ordem=preco):");
  console.log(`  ${"Nome".padEnd(20)} ${"Preço".padStart(10)}  ${"Estoque".padStart(8)}`);
  console.log("  " + "-".repeat(44));
  for (const p of resultados) {
    console.log(`  ${p.nomeProduto.padEnd(20)} R$${p.preco.toFixed(2).padStart(9)}  ${String(p.estoqueDisponivel).padStart(8)}`);
  }
  console.log();
}

function demonstrarBuscaSemFiltroTermo(): void {
  const filtros: FiltroProduto = { categoria: "vestuario", termoBusca: "" };
  const resultados = buscarProdutos(filtros);

  console.log("Busca sem filtro de termo (categoria=vestuario, termo=''):");
  console.log("  " + "Nome".padEnd(20) + "Preço".padStart(10) + "  " + "Estoque".padStart(8));
  console.log("  " + "-".repeat(44));
  for (const p of resultados) {
    console.log("  " + p.nomeProduto.padEnd(20) + ("R$" + p.preco.toFixed(2)).padStart(10) + "  " + String(p.estoqueDisponivel).padStart(8));
  }
  console.log();
}

function demonstrarBrechaLike(): void {
  /**
   * Demonstra a brecha no LIKE por concatenação (equivalente TypeScript).
   *
   * O filtro usa includes() com o termoBusca diretamente — sem escape.
   * Em SQL puro (WHERE descricao LIKE '%{termoBusca}%'), o vetor é ainda
   * mais direto: o termo é concatenado na query string, e um '%' passado
   * como termo resulta em LIKE '%%%' — equivalente a LIKE '%', que retorna
   * todos os registros da categoria.
   *
   * Aqui simulamos o mesmo efeito: termoBusca vazio retorna tudo, mostrando
   * que o filtro de texto é bypassável sem validação de entrada.
   */
  const casos: Array<[string, string]> = [
    ["jeans",  "busca legítima — retorna apenas o esperado"],
    ["",       "string vazia — retorna todos (equivale a LIKE '%%' em SQL)"],
  ];

  console.log("Demonstração da brecha no LIKE por concatenação:");
  console.log("  Query SQL equivalente: WHERE descricao LIKE '%{termoBusca}%'");
  console.log("  (termoBusca concatenado diretamente — sem escape, sem parâmetro posicional)");
  console.log();

  for (const [termoBusca, descricao] of casos) {
    const filtros: FiltroProduto = { categoria: "vestuario", termoBusca };
    const resultados = buscarProdutos(filtros);
    console.log("  termoBusca: " + JSON.stringify(termoBusca) + " (" + descricao + ")");
    console.log("  " + "Nome".padEnd(20) + "Preço".padStart(10));
    console.log("  " + "-".repeat(34));
    for (const p of resultados) {
      console.log("  " + p.nomeProduto.padEnd(20) + ("R$" + p.preco.toFixed(2)).padStart(10));
    }
    console.log();
  }

  console.log("  Questão: o ORDER BY está protegido por allow-list. O termoBusca não está.");
  console.log("  Em SQL, LIKE '%' + termoBusca + '%' sem escape aceita wildcards como texto.");
  console.log("  Essa é a brecha sutil — o código parece seguro, mas o LIKE está exposto.");
  console.log();
}

// ─── Execução ────────────────────────────────────────────────────────────────

console.log("=== Busca de Produtos — exercício de segurança ===\n");

demonstrarBuscaNormal();
demonstrarBuscaSemFiltroTermo();
demonstrarBrechaLike();
