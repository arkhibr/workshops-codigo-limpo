/**
 * GABARITO — Tutorial 08: O novo fluxo: dirigir e revisar
 * Referência: Tutorial 08 — O novo fluxo: dirigir e revisar
 * Execute: npx ts-node gabarito.ts
 *
 * Versão alinhada às convenções do projeto. Consulte gabarito_revisao.md para
 * a tabela de divergências e o prompt com contexto de convenção sugerido.
 *
 * Divergências corrigidas:
 *   - Exceções explícitas (Error) em vez de objetos de resultado
 *   - Interfaces em português para modelagem de entidade
 *   - Constantes nomeadas para limites de negócio
 *   - Identificadores 100 % em português (categoria, idPai, etc.)
 *   - Sem classe de serviço separada — funções planas no módulo
 */

// ─── Constantes de domínio ────────────────────────────────────────────────────

const TAMANHO_MINIMO_ID = 3;
const TAMANHO_MINIMO_NOME = 2;

// ─── Entidade ─────────────────────────────────────────────────────────────────

interface Categoria {
  id:     string;
  nome:   string;
  idPai:  string | null;
  ativa:  boolean;
}

// ─── Estado em memória ────────────────────────────────────────────────────────

const _categorias = new Map<string, Categoria>();

// ─── Operações de categorias ──────────────────────────────────────────────────

function criarCategoria(id: string, nome: string, idPai: string | null = null): Categoria {
  if (!id || id.length < TAMANHO_MINIMO_ID) {
    throw new Error(`ID da categoria deve ter ao menos ${TAMANHO_MINIMO_ID} caracteres`);
  }
  if (!nome || nome.length < TAMANHO_MINIMO_NOME) {
    throw new Error(`Nome da categoria deve ter ao menos ${TAMANHO_MINIMO_NOME} caracteres`);
  }
  if (_categorias.has(id)) {
    throw new Error(`Categoria '${id}' já existe`);
  }
  if (idPai && !_categorias.has(idPai)) {
    throw new Error(`Categoria pai '${idPai}' não encontrada`);
  }

  const categoria: Categoria = { id, nome, idPai, ativa: true };
  _categorias.set(id, categoria);
  return categoria;
}

function buscarCategoria(id: string): Categoria {
  const categoria = _categorias.get(id);
  if (!categoria) {
    throw new Error(`Categoria '${id}' não encontrada`);
  }
  return categoria;
}

function listarCategorias(apenasAtivas = false): Categoria[] {
  const todas = Array.from(_categorias.values());
  if (apenasAtivas) {
    return todas.filter((c) => c.ativa);
  }
  return todas;
}

function desativarCategoria(id: string): Categoria {
  const categoria = buscarCategoria(id);
  const desativada: Categoria = { ...categoria, ativa: false };
  _categorias.set(id, desativada);
  return desativada;
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

console.log("=== Módulo de Categorias (gabarito — alinhado às convenções do projeto) ===\n");

const c1 = criarCategoria("CAT01", "Eletrônicos");
console.log("Categoria criada:", c1);

const c2 = criarCategoria("CAT02", "Informática", "CAT01");
console.log("Categoria criada (filha):", c2);

try {
  criarCategoria("", "Sem ID");
} catch (erro) {
  console.log("\nErro esperado no cadastro:", (erro as Error).message);
}

const encontrada = buscarCategoria("CAT01");
console.log("\nBusca por CAT01:", encontrada);

try {
  buscarCategoria("X999");
} catch (erro) {
  console.log("Erro esperado na busca:", (erro as Error).message);
}

const todas = listarCategorias();
console.log(`\nTodas as categorias (${todas.length}):`, todas);

const desativada = desativarCategoria("CAT02");
console.log("\nCategoria desativada:", desativada);

const ativas = listarCategorias(true);
console.log(`Apenas ativas (${ativas.length}):`, ativas);
