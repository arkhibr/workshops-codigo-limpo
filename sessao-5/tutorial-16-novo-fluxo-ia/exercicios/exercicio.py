"""
EXERCÍCIO — Tutorial 08: O novo fluxo: dirigir e revisar
Referência: Tutorial 08 — O novo fluxo: dirigir e revisar
Execute: python3 exercicio.py

Este módulo de categorias foi gerado por um modelo de fronteira sem contexto
de convenção do projeto. O código é limpo e funciona corretamente, mas diverge
do padrão estabelecido nas sessões anteriores.

Tarefa:
  (1) Liste as divergências de convenção em relação ao padrão do repositório.
      Consulte: sessao-1/tutorial-02-funcoes/exemplos/funcoes_boas.py
                sessao-2/tutorial-06-divida-tecnica/exemplos/divida_depois.py
  (2) Reescreva o prompt que originou este código, adicionando o contexto de
      convenção do projeto (CLAUDE.md, trecho de funcoes_boas.py, etc.).
  (3) Alinhe este código ao padrão do repositório (ver gabarito.py).
"""

from typing import Optional


class CategoryService:
    """Gerencia categorias de produtos em memória."""

    def __init__(self):
        self._categories: dict[str, dict] = {}

    def create(self, category_id: str, name: str, parent_id: Optional[str] = None) -> dict:
        if not category_id or not name:
            return {"status": "error", "message": "ID and name are required"}
        if category_id in self._categories:
            return {"status": "error", "message": f"Category '{category_id}' already exists"}
        if parent_id and parent_id not in self._categories:
            return {"status": "error", "message": f"Parent '{parent_id}' not found"}

        category = {
            "id": category_id,
            "name": name,
            "parent_id": parent_id,
            "active": True,
        }
        self._categories[category_id] = category
        return {"status": "ok", "data": category}

    def get(self, category_id: str) -> dict:
        category = self._categories.get(category_id)
        if category is None:
            return {"status": "error", "message": f"Category '{category_id}' not found"}
        return {"status": "ok", "data": category}

    def list_all(self, active_only: bool = False) -> dict:
        items = list(self._categories.values())
        if active_only:
            items = [c for c in items if c.get("active")]
        return {"status": "ok", "data": items}

    def deactivate(self, category_id: str) -> dict:
        result = self.get(category_id)
        if result["status"] == "error":
            return result
        self._categories[category_id]["active"] = False
        return {"status": "ok", "data": self._categories[category_id]}


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Módulo de Categorias (exercício — saída sem convenção do projeto) ===\n")

    service = CategoryService()

    r1 = service.create("CAT01", "Eletrônicos")
    print("Criar CAT01:", r1)

    r2 = service.create("CAT02", "Informática", parent_id="CAT01")
    print("Criar CAT02 (filha de CAT01):", r2)

    r3 = service.create("", "Sem ID")
    print("Criar sem ID:", r3)

    r4 = service.get("CAT01")
    print("\nBuscar CAT01:", r4)

    r5 = service.get("X999")
    print("Buscar inexistente:", r5)

    r6 = service.list_all()
    print("\nListar todas:", r6)

    r7 = service.deactivate("CAT02")
    print("\nDesativar CAT02:", r7)

    r8 = service.list_all(active_only=True)
    print("Listar apenas ativas:", r8)
