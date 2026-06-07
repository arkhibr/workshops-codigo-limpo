/**
 * Revisão alinhada às convenções do projeto — Catálogo de Produtos
 * Referência: Tutorial 08 — O novo fluxo: dirigir e revisar
 * Execute: npx ts-node catalogo_revisado.ts
 *
 * Divergências corrigidas em relação a catalogo_gerado.ts:
 *   - Exceções explícitas (Error) em vez de objetos de resultado
 *   - Interfaces em português para modelagem de entidade
 *   - Constantes nomeadas para limites de negócio
 *   - Identificadores 100 % em português (produto, catalogo, preco, categoria)
 *   - Sem camadas Repository/Service separadas — módulo plano como no repo
 */

// ─── Constantes de domínio ────────────────────────────────────────────────────

const PRECO_MINIMO = 0.0;
const TAMANHO_MINIMO_NOME = 2;
const TAMANHO_MINIMO_ID = 3;

// ─── Entidade ─────────────────────────────────────────────────────────────────

interface Produto {
  id:        string;
  nome:      string;
  preco:     number;
  categoria: string;
}

// ─── Estado em memória ────────────────────────────────────────────────────────

const _produtos = new Map<string, Produto>();

// ─── Operações do catálogo ────────────────────────────────────────────────────

function cadastrarProduto(id: string, nome: string, preco: number, categoria: string): Produto {
  if (!id || id.length < TAMANHO_MINIMO_ID) {
    throw new Error(`ID do produto deve ter ao menos ${TAMANHO_MINIMO_ID} caracteres`);
  }
  if (!nome || nome.length < TAMANHO_MINIMO_NOME) {
    throw new Error(`Nome do produto deve ter ao menos ${TAMANHO_MINIMO_NOME} caracteres`);
  }
  if (preco < PRECO_MINIMO) {
    throw new Error("Preço não pode ser negativo");
  }

  const produto: Produto = { id, nome, preco, categoria };
  _produtos.set(id, produto);
  return produto;
}

function buscarProduto(id: string): Produto {
  const produto = _produtos.get(id);
  if (!produto) {
    throw new Error(`Produto '${id}' não encontrado no catálogo`);
  }
  return produto;
}

function listarProdutos(categoria?: string): Produto[] {
  const todos = Array.from(_produtos.values());
  if (categoria) {
    return todos.filter((p) => p.categoria === categoria);
  }
  return todos;
}

function atualizarPreco(id: string, novoPreco: number): Produto {
  if (novoPreco < PRECO_MINIMO) {
    throw new Error("Preço não pode ser negativo");
  }
  const produto = buscarProduto(id);
  const atualizado: Produto = { ...produto, preco: novoPreco };
  _produtos.set(id, atualizado);
  return atualizado;
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

console.log("=== Catálogo de Produtos (revisado — alinhado às convenções do projeto) ===\n");

const p1 = cadastrarProduto("P001", "Notebook Pro 15", 4_500.00, "informatica");
console.log("Produto cadastrado:", p1);

const p2 = cadastrarProduto("P002", "Mouse Sem Fio", 89.90, "perifericos");
console.log("Produto cadastrado:", p2);

try {
  cadastrarProduto("", "Sem ID", 10.0, "geral");
} catch (erro) {
  console.log("\nErro esperado no cadastro:", (erro as Error).message);
}

const encontrado = buscarProduto("P001");
console.log("\nBusca por P001:", encontrado);

try {
  buscarProduto("X999");
} catch (erro) {
  console.log("Erro esperado na busca:", (erro as Error).message);
}

const todos = listarProdutos();
console.log(`\nTodos os produtos (${todos.length}):`, todos);

const filtrados = listarProdutos("informatica");
console.log(`Categoria 'informatica' (${filtrados.length}):`, filtrados);

const atualizado = atualizarPreco("P001", 3_999.00);
console.log("\nPreço atualizado:", atualizado);
