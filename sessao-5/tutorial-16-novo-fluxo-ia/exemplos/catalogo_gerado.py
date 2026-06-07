"""
Saída do modelo de IA (sem contexto de convenção do projeto) — Catálogo de Produtos
Referência: Tutorial 08 — O novo fluxo: dirigir e revisar
Execute: python3 catalogo_gerado.py

Este arquivo representa a saída de um modelo de fronteira sem contexto de convenção.
O código é limpo e idiomático em si, mas diverge das convenções do repositório:
  - Retorna dicionários com campos 'success'/'error' em vez de levantar exceções
  - Usa estrutura de camadas (repository/service) não adotada nas sessões anteriores
  - Identificadores em inglês ('product', 'catalog') em vez de domínio em PT
  - Ausência de @dataclass e constantes nomeadas no estilo do repositório
"""

from typing import Optional


# ─── Camada de repositório ────────────────────────────────────────────────────

class ProductRepository:
    """Armazena produtos em memória."""

    def __init__(self):
        self._store: dict[str, dict] = {}

    def save(self, product: dict) -> dict:
        product_id = product.get("id")
        if not product_id:
            return {"success": False, "error": "Product ID is required"}
        self._store[product_id] = product
        return {"success": True, "data": product}

    def find_by_id(self, product_id: str) -> dict:
        product = self._store.get(product_id)
        if product is None:
            return {"success": False, "error": f"Product '{product_id}' not found"}
        return {"success": True, "data": product}

    def find_all(self) -> dict:
        return {"success": True, "data": list(self._store.values())}

    def find_by_category(self, category: str) -> dict:
        results = [p for p in self._store.values() if p.get("category") == category]
        return {"success": True, "data": results}


# ─── Camada de serviço ────────────────────────────────────────────────────────

class CatalogService:
    """Lógica de negócio do catálogo."""

    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def add_product(self, product_id: str, name: str, price: float, category: str) -> dict:
        if not product_id or not name:
            return {"success": False, "error": "ID and name are required"}
        if price < 0:
            return {"success": False, "error": "Price cannot be negative"}

        product = {
            "id": product_id,
            "name": name,
            "price": price,
            "category": category,
        }
        return self._repository.save(product)

    def get_product(self, product_id: str) -> dict:
        return self._repository.find_by_id(product_id)

    def list_products(self, category: Optional[str] = None) -> dict:
        if category:
            return self._repository.find_by_category(category)
        return self._repository.find_all()

    def update_price(self, product_id: str, new_price: float) -> dict:
        result = self._repository.find_by_id(product_id)
        if not result["success"]:
            return result
        if new_price < 0:
            return {"success": False, "error": "Price cannot be negative"}
        product = result["data"]
        product["price"] = new_price
        return self._repository.save(product)


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Catálogo de Produtos (saída do modelo — sem convenção do projeto) ===\n")

    repository = ProductRepository()
    service = CatalogService(repository)

    r1 = service.add_product("P001", "Notebook Pro 15", 4_500.00, "informatica")
    print("Cadastro produto 1:", r1)

    r2 = service.add_product("P002", "Mouse Sem Fio", 89.90, "perifericos")
    print("Cadastro produto 2:", r2)

    r3 = service.add_product("", "Sem ID", 10.0, "geral")
    print("Cadastro sem ID:", r3)

    r4 = service.get_product("P001")
    print("\nBusca P001:", r4)

    r5 = service.get_product("X999")
    print("Busca inexistente:", r5)

    r6 = service.list_products()
    print("\nListagem completa:", r6)

    r7 = service.list_products(category="informatica")
    print("Por categoria 'informatica':", r7)

    r8 = service.update_price("P001", 3_999.00)
    print("\nAtualização de preço:", r8)
