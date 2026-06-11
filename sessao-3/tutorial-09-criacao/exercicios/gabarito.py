"""
GABARITO 17 — Padrões de Criação
Referência: Design Patterns (GoF), Cap. 3

Execute: python3 gabarito.py
"""
from typing import Optional, Callable
from dataclasses import dataclass


# ─── Dataclass (mesma do exercício) ──────────────────────────────────────────

@dataclass
class Contrato:
    tipo:           str
    valor_mensal:   float
    vigencia_meses: int
    contratante:    str
    objeto:         Optional[str] = None
    endereco:       Optional[str] = None
    fornecedor_id:  Optional[str] = None
    prazo_entrega:  Optional[int] = None
    observacoes:    Optional[str] = None


# ─── Passo 2: Factory com dict ────────────────────────────────────────────────

_FABRICA: dict[str, Callable[[dict], Contrato]] = {
    "servico": lambda d: Contrato(
        tipo="servico",
        valor_mensal=d["valor_mensal"],
        vigencia_meses=d["vigencia_meses"],
        contratante=d["contratante"],
        objeto=d.get("objeto", "Serviços gerais"),
    ),
    "locacao": lambda d: Contrato(
        tipo="locacao",
        valor_mensal=d["valor_mensal"],
        vigencia_meses=d["vigencia_meses"],
        contratante=d["contratante"],
        objeto=d.get("objeto"),
        endereco=d.get("endereco"),
    ),
    "fornecimento": lambda d: Contrato(
        tipo="fornecimento",
        valor_mensal=d["valor_mensal"],
        vigencia_meses=d["vigencia_meses"],
        contratante=d["contratante"],
        fornecedor_id=d.get("fornecedor_id"),
        prazo_entrega=d.get("prazo_entrega"),
    ),
}


# ─── Passo 3: Factory registrável ────────────────────────────────────────────

class FabricaContrato:
    _registro: dict[str, Callable[[dict], Contrato]] = {}

    @classmethod
    def registrar(cls, tipo: str, funcao_criadora: Callable[[dict], Contrato]) -> None:
        cls._registro[tipo] = funcao_criadora

    @classmethod
    def criar(cls, tipo: str, dados: dict) -> Contrato:
        if tipo not in cls._registro:
            disponiveis = ", ".join(sorted(cls._registro.keys()))
            raise ValueError(f"Tipo '{tipo}' não registrado. Disponíveis: {disponiveis}")
        return cls._registro[tipo](dados)


FabricaContrato.registrar("servico",      _FABRICA["servico"])
FabricaContrato.registrar("locacao",      _FABRICA["locacao"])
FabricaContrato.registrar("fornecimento", _FABRICA["fornecimento"])


# ─── Passo 4: Builder ─────────────────────────────────────────────────────────

class ConstruirContratoServico:
    def __init__(self) -> None:
        self._valor_mensal:   Optional[float] = None
        self._vigencia_meses: Optional[int]   = None
        self._contratante:    Optional[str]   = None
        self._objeto:         str             = "Serviços gerais"

    def com_valor_mensal(self, valor: float) -> "ConstruirContratoServico":
        self._valor_mensal = valor
        return self

    def com_vigencia(self, meses: int) -> "ConstruirContratoServico":
        self._vigencia_meses = meses
        return self

    def com_contratante(self, contratante: str) -> "ConstruirContratoServico":
        self._contratante = contratante
        return self

    def construir(self) -> Contrato:
        if self._valor_mensal is None:
            raise ValueError("valor_mensal é obrigatório")
        if self._vigencia_meses is None:
            raise ValueError("vigencia_meses é obrigatório")
        if self._contratante is None:
            raise ValueError("contratante é obrigatório")
        return Contrato(
            tipo="servico",
            valor_mensal=self._valor_mensal,
            vigencia_meses=self._vigencia_meses,
            contratante=self._contratante,
            objeto=self._objeto,
        )


# ─── Verificação ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Gabarito 17 — Factory Method + Builder ===\n")

    # Passo 2: factory com dict
    c_dict = _FABRICA["servico"]({"valor_mensal": 5000.0, "vigencia_meses": 12, "contratante": "EMP-001"})
    assert c_dict.tipo == "servico"
    print(f"OK: Passo 2 — factory com dict: {c_dict.tipo} R${c_dict.valor_mensal:.2f}/mês")

    # Passo 3: factory registrável
    servico = FabricaContrato.criar("servico", {
        "valor_mensal": 5000.0, "vigencia_meses": 12, "contratante": "EMP-001"
    })
    assert servico.tipo == "servico"
    assert servico.valor_mensal * servico.vigencia_meses == 60000.0
    print(f"OK: Passo 3 — FabricaContrato.criar: {servico.tipo}")

    try:
        FabricaContrato.criar("desconhecido", {"valor_mensal": 1.0, "vigencia_meses": 1, "contratante": "X"})
        print("FALHOU: deveria rejeitar tipo não registrado")
    except ValueError:
        print("OK: Passo 3 — tipo desconhecido rejeitado com ValueError")

    # Passo 3: novo tipo sem alterar FabricaContrato
    FabricaContrato.registrar("obras_civil", lambda d: Contrato(
        tipo="obras_civil",
        valor_mensal=d["valor_mensal"],
        vigencia_meses=d["vigencia_meses"],
        contratante=d["contratante"],
        observacoes=d.get("responsavel_tecnico"),
    ))
    obras = FabricaContrato.criar("obras_civil", {
        "valor_mensal": 25000.0, "vigencia_meses": 8,
        "contratante": "EMP-004", "responsavel_tecnico": "Eng. Silva CREA-12345"
    })
    assert obras.tipo == "obras_civil"
    print(f"OK: Passo 3 — novo tipo registrado sem alterar FabricaContrato: {obras.tipo}")

    print()

    # Passo 4: builder
    c_builder = (
        ConstruirContratoServico()
        .com_valor_mensal(5000.0)
        .com_vigencia(12)
        .com_contratante("EMP-001")
        .construir()
    )
    assert c_builder.tipo == "servico"
    assert c_builder.valor_mensal * c_builder.vigencia_meses == 60000.0
    print(f"OK: Passo 4 — builder fluente: {c_builder.tipo} R${c_builder.valor_mensal:.2f}/mês")

    try:
        ConstruirContratoServico().com_valor_mensal(5000.0).construir()
        print("FALHOU: deveria rejeitar sem vigencia_meses")
    except ValueError:
        print("OK: Passo 4 — rejeita construir() sem vigencia_meses")

    try:
        ConstruirContratoServico().com_vigencia(12).construir()
        print("FALHOU: deveria rejeitar sem valor_mensal")
    except ValueError:
        print("OK: Passo 4 — rejeita construir() sem valor_mensal")

    try:
        ConstruirContratoServico().com_valor_mensal(5000.0).com_vigencia(12).construir()
        print("FALHOU: deveria rejeitar sem contratante")
    except ValueError:
        print("OK: Passo 4 — rejeita construir() sem contratante")
