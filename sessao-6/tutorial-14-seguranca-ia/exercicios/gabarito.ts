/**
 * gabarito.ts — Endpoint de busca de produtos (versão endurecida).
 *
 * Corrige a brecha sutil de exercicio.ts:
 *   - O filtro de termoBusca era aplicado com includes() sem escape ou validação.
 *   - Em SQL equivalente: WHERE descricao LIKE '%{termoBusca}%' — concatenação direta.
 *   - Agora: validação de entrada bloqueia %, _, ;, aspas e outros caracteres perigosos.
 *   - O term vai para filter/includes após validação — sem concatenação na query.
 *   - ORDER BY continua via allow-list (já estava correto no exercício).
 *
 * Execute: npx ts-node gabarito.ts
 */

// ---------------------------------------------------------------------------
// Constantes de domínio
// ---------------------------------------------------------------------------

const CATEGORIAS_VALIDAS = new Set(["eletronicos", "vestuario", "alimentos", "livraria"]);

const CAMPOS_ORDENACAO_PERMITIDOS = new Set(["preco", "nomeProduto", "estoqueDisponivel"]);

// Padrão restrito: apenas letras (incluindo acentuadas), dígitos e espaço.
// Bloqueia %, _, ;, aspas, parênteses — caracteres que tornariam o LIKE perigoso.
const PADRAO_TERMO_SEGURO = /^[a-zA-ZÀ-ÿ0-9 ]{1,50}$/;

// ---------------------------------------------------------------------------
// Modelos de dados
// ---------------------------------------------------------------------------

interface FiltroProduto {
  categoria:  string;
  termoBusca: string;
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
  if (filtros.termoBusca && !PADRAO_TERMO_SEGURO.test(filtros.termoBusca)) {
    throw new Error(
      `Termo de busca inválido: '${filtros.termoBusca}'. ` +
      "Use apenas letras, dígitos e espaços (máx. 50 caracteres).",
    );
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
// Validação de segurança
// ---------------------------------------------------------------------------

/**
 * Valida que o campo de ordenação pertence ao allow-list.
 *
 * Em query builders e ORMs, ORDER BY frequentemente não aceita parâmetro
 * posicional — a coluna precisa ser interpolada. Esta função garante que
 * apenas campos conhecidos sejam usados na ordenação.
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

/**
 * Executa a busca simulada com filtros validados e ordenação via allow-list.
 * O termo vai para includes() após validação — nunca concatenado na query.
 */
function executarQuery(filtros: FiltroProduto, campo: keyof Produto): Produto[] {
  const termo = filtros.termoBusca.toLowerCase();
  const filtrados = BANCO_PRODUTOS.filter(
    (p) =>
      p.categoria === filtros.categoria &&
      (termo === "" || p.descricao.toLowerCase().includes(termo)),
  );
  return [...filtrados].sort((a, b) => {
    const va = a[campo];
    const vb = b[campo];
    if (typeof va === "number" && typeof vb === "number") return va - vb;
    return String(va ?? "").localeCompare(String(vb ?? ""));
  });
}

// ---------------------------------------------------------------------------
// Lógica de busca
// ---------------------------------------------------------------------------

/**
 * Busca produtos por categoria e filtra por termo na descrição.
 *
 * Categoria e termoBusca validados antes de qualquer uso.
 * ORDER BY validado por allow-list antes de qualquer uso na ordenação.
 * Levanta Error para qualquer entrada fora dos critérios aceitos.
 */
function buscarProdutos(filtros: FiltroProduto, ordenacao: string = "nomeProduto"): Produto[] {
  validarFiltros(filtros);
  const campo = campoOrdenacaoSeguro(ordenacao);
  return executarQuery(filtros, campo);
}

// ---------------------------------------------------------------------------
// Demo
// ---------------------------------------------------------------------------

function demonstrarBuscaNormal(): void {
  const filtros: FiltroProduto = { categoria: "eletronicos", termoBusca: "fio" };
  const resultados = buscarProdutos(filtros, "preco");

  console.log("Busca normal (categoria=eletronicos, termo=fio, ordem=preco):");
  console.log("  " + "Nome".padEnd(20) + "Preço".padStart(10) + "  " + "Estoque".padStart(8));
  console.log("  " + "-".repeat(44));
  for (const p of resultados) {
    console.log("  " + p.nomeProduto.padEnd(20) + ("R$" + p.preco.toFixed(2)).padStart(10) + "  " + String(p.estoqueDisponivel).padStart(8));
  }
  console.log();
}

function demonstrarRejeicaoWildcardLike(): void {
  const termos = ["%", "_%_", "x'; --"];

  console.log("Tentativa com wildcards LIKE como termo de busca:");
  for (const termo of termos) {
    try {
      validarFiltros({ categoria: "eletronicos", termoBusca: termo });
      console.log("  " + JSON.stringify(termo).padEnd(20) + "Aceito (FALHOU — deveria rejeitar)");
    } catch (erro) {
      console.log("  " + JSON.stringify(termo).padEnd(20) + "Rejeitado: " + (erro as Error).message);
    }
  }
  console.log();
}

function demonstrarRejeicaoOrdenacaoMaliciosa(): void {
  const filtros: FiltroProduto = { categoria: "eletronicos", termoBusca: "" };
  const ordenacaoMaliciosa = "preco DESC; DROP TABLE produtos--";

  console.log("Tentativa com ordenacao maliciosa:");
  console.log("  ordenacao recebida: " + JSON.stringify(ordenacaoMaliciosa));
  try {
    buscarProdutos(filtros, ordenacaoMaliciosa);
    console.log("  FALHOU: a busca executou sem erro.");
  } catch (erro) {
    console.log("  Bloqueado: " + (erro as Error).message);
  }
  console.log();
}

function demonstrarBuscaComTermoSeguro(): void {
  const filtros: FiltroProduto = { categoria: "vestuario", termoBusca: "slim" };
  const resultados = buscarProdutos(filtros, "preco");

  console.log("Busca com termo legítimo 'slim' (categoria=vestuario):");
  console.log("  " + "Nome".padEnd(20) + "Preço".padStart(10));
  console.log("  " + "-".repeat(34));
  for (const p of resultados) {
    console.log("  " + p.nomeProduto.padEnd(20) + ("R$" + p.preco.toFixed(2)).padStart(10));
  }
  console.log();
}

// ─── Execução ────────────────────────────────────────────────────────────────

console.log("=== Busca de Produtos — gabarito (versão endurecida) ===\n");

demonstrarBuscaNormal();
demonstrarRejeicaoWildcardLike();
demonstrarRejeicaoOrdenacaoMaliciosa();
demonstrarBuscaComTermoSeguro();
