/**
 * EXERCÍCIO — Tutorial 08: O novo fluxo: dirigir e revisar
 * Referência: Tutorial 08 — O novo fluxo: dirigir e revisar
 * Execute: npx ts-node exercicio.ts
 *
 * Este módulo de categorias foi gerado por um modelo de fronteira sem contexto
 * de convenção do projeto. O código é limpo e funciona corretamente, mas diverge
 * do padrão estabelecido nas sessões anteriores.
 *
 * Tarefa:
 *   (1) Liste as divergências de convenção em relação ao padrão do repositório.
 *       Consulte: sessao-1/tutorial-02-funcoes/exemplos/equivalente.ts
 *                 sessao-2/tutorial-06-divida-tecnica/exemplos/equivalente.ts
 *   (2) Reescreva o prompt que originou este código, adicionando o contexto de
 *       convenção do projeto (CLAUDE.md, trecho de equivalente.ts, etc.).
 *   (3) Alinhe este código ao padrão do repositório (ver gabarito.ts).
 */

// ─── Tipos ────────────────────────────────────────────────────────────────────

interface Category {
  id:       string;
  name:     string;
  parentId: string | null;
  active:   boolean;
}

type ServiceResult<T> =
  | { status: "ok";    data: T }
  | { status: "error"; message: string };

// ─── Serviço ──────────────────────────────────────────────────────────────────

class CategoryService {
  private categories = new Map<string, Category>();

  create(id: string, name: string, parentId: string | null = null): ServiceResult<Category> {
    if (!id || !name) {
      return { status: "error", message: "ID and name are required" };
    }
    if (this.categories.has(id)) {
      return { status: "error", message: `Category '${id}' already exists` };
    }
    if (parentId && !this.categories.has(parentId)) {
      return { status: "error", message: `Parent '${parentId}' not found` };
    }

    const category: Category = { id, name, parentId, active: true };
    this.categories.set(id, category);
    return { status: "ok", data: category };
  }

  get(id: string): ServiceResult<Category> {
    const category = this.categories.get(id);
    if (!category) {
      return { status: "error", message: `Category '${id}' not found` };
    }
    return { status: "ok", data: category };
  }

  listAll(activeOnly = false): ServiceResult<Category[]> {
    let items = Array.from(this.categories.values());
    if (activeOnly) {
      items = items.filter((c) => c.active);
    }
    return { status: "ok", data: items };
  }

  deactivate(id: string): ServiceResult<Category> {
    const result = this.get(id);
    if (result.status === "error") return result;
    const updated = { ...result.data, active: false };
    this.categories.set(id, updated);
    return { status: "ok", data: updated };
  }
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

console.log("=== Módulo de Categorias (exercício — saída sem convenção do projeto) ===\n");

const service = new CategoryService();

const r1 = service.create("CAT01", "Eletrônicos");
console.log("Criar CAT01:", r1);

const r2 = service.create("CAT02", "Informática", "CAT01");
console.log("Criar CAT02 (filha de CAT01):", r2);

const r3 = service.create("", "Sem ID");
console.log("Criar sem ID:", r3);

const r4 = service.get("CAT01");
console.log("\nBuscar CAT01:", r4);

const r5 = service.get("X999");
console.log("Buscar inexistente:", r5);

const r6 = service.listAll();
console.log("\nListar todas:", r6);

const r7 = service.deactivate("CAT02");
console.log("\nDesativar CAT02:", r7);

const r8 = service.listAll(true);
console.log("Listar apenas ativas:", r8);
