/**
 * Saída do modelo de IA (sem contexto de convenção do projeto) — Catálogo de Produtos
 * Referência: Tutorial 08 — O novo fluxo: dirigir e revisar
 * Execute: npx ts-node catalogo_gerado.ts
 *
 * Este arquivo representa a saída de um modelo de fronteira sem contexto de convenção.
 * O código é limpo e idiomático em si, mas diverge das convenções do repositório:
 *   - Retorna objetos com campos 'success'/'error' em vez de lançar exceções
 *   - Usa estrutura de camadas (repository/service) não adotada nas sessões anteriores
 *   - Identificadores em inglês ('product', 'catalog') em vez de domínio em PT
 *   - Sem constantes nomeadas para limites de negócio (magic values inline)
 */

// ─── Tipos ────────────────────────────────────────────────────────────────────

interface Product {
  id: string;
  name: string;
  price: number;
  category: string;
}

type Result<T> = { success: true; data: T } | { success: false; error: string };

// ─── Repository ───────────────────────────────────────────────────────────────

class ProductRepository {
  private store = new Map<string, Product>();

  save(product: Product): Result<Product> {
    if (!product.id) {
      return { success: false, error: "Product ID is required" };
    }
    this.store.set(product.id, product);
    return { success: true, data: product };
  }

  findById(productId: string): Result<Product> {
    const product = this.store.get(productId);
    if (!product) {
      return { success: false, error: `Product '${productId}' not found` };
    }
    return { success: true, data: product };
  }

  findAll(): Result<Product[]> {
    return { success: true, data: Array.from(this.store.values()) };
  }

  findByCategory(category: string): Result<Product[]> {
    const results = Array.from(this.store.values()).filter(
      (p) => p.category === category
    );
    return { success: true, data: results };
  }
}

// ─── Service ──────────────────────────────────────────────────────────────────

class CatalogService {
  constructor(private readonly repository: ProductRepository) {}

  addProduct(id: string, name: string, price: number, category: string): Result<Product> {
    if (!id || !name) {
      return { success: false, error: "ID and name are required" };
    }
    if (price < 0) {
      return { success: false, error: "Price cannot be negative" };
    }
    return this.repository.save({ id, name, price, category });
  }

  getProduct(productId: string): Result<Product> {
    return this.repository.findById(productId);
  }

  listProducts(category?: string): Result<Product[]> {
    if (category) {
      return this.repository.findByCategory(category);
    }
    return this.repository.findAll();
  }

  updatePrice(productId: string, newPrice: number): Result<Product> {
    const result = this.repository.findById(productId);
    if (!result.success) return result;
    if (newPrice < 0) {
      return { success: false, error: "Price cannot be negative" };
    }
    const updated = { ...result.data, price: newPrice };
    return this.repository.save(updated);
  }
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

const repository = new ProductRepository();
const service = new CatalogService(repository);

console.log("=== Catálogo de Produtos (saída do modelo — sem convenção do projeto) ===\n");

const r1 = service.addProduct("P001", "Notebook Pro 15", 4_500.00, "informatica");
console.log("Cadastro produto 1:", r1);

const r2 = service.addProduct("P002", "Mouse Sem Fio", 89.90, "perifericos");
console.log("Cadastro produto 2:", r2);

const r3 = service.addProduct("", "Sem ID", 10.0, "geral");
console.log("Cadastro sem ID:", r3);

const r4 = service.getProduct("P001");
console.log("\nBusca P001:", r4);

const r5 = service.getProduct("X999");
console.log("Busca inexistente:", r5);

const r6 = service.listProducts();
console.log("\nListagem completa:", r6);

const r7 = service.listProducts("informatica");
console.log("Por categoria 'informatica':", r7);

const r8 = service.updatePrice("P001", 3_999.00);
console.log("\nAtualização de preço:", r8);
