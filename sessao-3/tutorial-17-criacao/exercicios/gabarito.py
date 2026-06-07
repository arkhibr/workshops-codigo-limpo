"""
GABARITO 17 — Padrões de Criação
Referência: Design Patterns (GoF), Cap. 3

SOLUÇÃO:
  1. Factory Method: FabricaContrato com registrar/criar registrável.
  2. Builder: ConstruirContratoServico com interface fluente.

Execute: python3 gabarito.py
"""
from typing import Optional, Dict
from abc import ABC, abstractmethod


# ─── Factory Method ───────────────────────────────────────────────────────────

class Contrato(ABC):
    def __init__(self, valor_mensal: float, vigencia_meses: int, contratante: str) -> None:
        if valor_mensal <= 0:
            raise ValueError(f"Valor mensal deve ser positivo, recebido: {valor_mensal}")
        if vigencia_meses <= 0:
            raise ValueError(f"Vigência deve ser positiva, recebida: {vigencia_meses}")
        self.valor_mensal   = valor_mensal
        self.vigencia_meses = vigencia_meses
        self.contratante    = contratante

    @abstractmethod
    def descricao(self) -> str: ...

    @property
    def valor_total(self) -> float:
        return self.valor_mensal * self.vigencia_meses


class ContratoServico(Contrato):
    def __init__(self, valor_mensal: float, vigencia_meses: int,
                 contratante: str, objeto: str) -> None:
        super().__init__(valor_mensal, vigencia_meses, contratante)
        self.objeto = objeto

    def descricao(self) -> str:
        return (f"Serviço: {self.objeto} | {self.contratante} | "
                f"R${self.valor_mensal:.2f}/mês × {self.vigencia_meses} meses")


class ContratoLocacao(Contrato):
    def __init__(self, valor_mensal: float, vigencia_meses: int,
                 contratante: str, objeto: str, endereco: str) -> None:
        super().__init__(valor_mensal, vigencia_meses, contratante)
        self.objeto   = objeto
        self.endereco = endereco

    def descricao(self) -> str:
        return (f"Locação: {self.objeto} | {self.endereco} | {self.contratante} | "
                f"R${self.valor_mensal:.2f}/mês × {self.vigencia_meses} meses")


class ContratoFornecimento(Contrato):
    def __init__(self, valor_mensal: float, vigencia_meses: int,
                 contratante: str, fornecedor_id: str, prazo_entrega: int) -> None:
        super().__init__(valor_mensal, vigencia_meses, contratante)
        self.fornecedor_id = fornecedor_id
        self.prazo_entrega = prazo_entrega

    def descricao(self) -> str:
        return (f"Fornecimento: {self.fornecedor_id} | prazo {self.prazo_entrega}d | "
                f"R${self.valor_mensal:.2f}/mês × {self.vigencia_meses} meses")


class FabricaContrato:
    _registro: Dict[str, type] = {}

    @classmethod
    def registrar(cls, tipo: str, classe: type) -> None:
        cls._registro[tipo] = classe

    @classmethod
    def criar(cls, tipo: str, **dados) -> Contrato:
        if tipo not in cls._registro:
            disponiveis = ", ".join(sorted(cls._registro.keys()))
            raise ValueError(f"Tipo '{tipo}' não registrado. Disponíveis: {disponiveis}")
        return cls._registro[tipo](**dados)


FabricaContrato.registrar("servico",     ContratoServico)
FabricaContrato.registrar("locacao",     ContratoLocacao)
FabricaContrato.registrar("fornecimento", ContratoFornecimento)


# ─── Builder ──────────────────────────────────────────────────────────────────

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

    def com_objeto(self, objeto: str) -> "ConstruirContratoServico":
        self._objeto = objeto
        return self

    def construir(self) -> ContratoServico:
        if self._valor_mensal is None:
            raise ValueError("valor_mensal é obrigatório")
        if self._vigencia_meses is None:
            raise ValueError("vigencia_meses é obrigatório")
        if self._contratante is None:
            raise ValueError("contratante é obrigatório")
        return ContratoServico(
            self._valor_mensal, self._vigencia_meses,
            self._contratante, self._objeto
        )


# ─── Verificação ──────────────────────────────────────────────────────────────

def verificar_factory() -> None:
    servico = FabricaContrato.criar(
        "servico", valor_mensal=5000.0, vigencia_meses=12,
        contratante="EMP-001", objeto="Consultoria em TI"
    )
    assert isinstance(servico, ContratoServico)
    assert servico.valor_total == 60000.0
    print("OK: Factory — ContratoServico criado via FabricaContrato")

    locacao = FabricaContrato.criar(
        "locacao", valor_mensal=3500.0, vigencia_meses=24,
        contratante="EMP-002", objeto="Sala comercial 40m²",
        endereco="Av. Paulista, 1000 — SP"
    )
    assert isinstance(locacao, ContratoLocacao)
    print("OK: Factory — ContratoLocacao criado via FabricaContrato")

    fornecimento = FabricaContrato.criar(
        "fornecimento", valor_mensal=8000.0, vigencia_meses=6,
        contratante="EMP-003", fornecedor_id="FORN-42", prazo_entrega=15
    )
    assert isinstance(fornecimento, ContratoFornecimento)
    print("OK: Factory — ContratoFornecimento criado via FabricaContrato")

    try:
        FabricaContrato.criar("obras_civil", valor_mensal=1000.0,
                              vigencia_meses=6, contratante="X")
        print("FALHOU: Factory — deveria rejeitar tipo não registrado")
    except ValueError:
        print("OK: Factory — tipo desconhecido rejeitado com ValueError")

    # Extensão sem alterar FabricaContrato
    class ContratoObrasCivil(Contrato):
        def __init__(self, valor_mensal: float, vigencia_meses: int,
                     contratante: str, responsavel_tecnico: str) -> None:
            super().__init__(valor_mensal, vigencia_meses, contratante)
            self.responsavel_tecnico = responsavel_tecnico
        def descricao(self) -> str:
            return f"Obras: RT {self.responsavel_tecnico} | R${self.valor_mensal:.2f}/mês"

    FabricaContrato.registrar("obras_civil", ContratoObrasCivil)
    obras = FabricaContrato.criar(
        "obras_civil", valor_mensal=25000.0, vigencia_meses=8,
        contratante="EMP-004", responsavel_tecnico="Eng. Silva CREA-12345"
    )
    assert isinstance(obras, ContratoObrasCivil)
    print("OK: Factory — novo tipo registrado sem alterar FabricaContrato")


def verificar_builder() -> None:
    contrato = (
        ConstruirContratoServico()
        .com_valor_mensal(5000.0)
        .com_vigencia(12)
        .com_contratante("EMP-001")
        .com_objeto("Desenvolvimento de software")
        .construir()
    )
    assert isinstance(contrato, ContratoServico)
    assert contrato.valor_total == 60000.0
    print("OK: Builder — ContratoServico construído com encadeamento fluente")

    try:
        ConstruirContratoServico().com_valor_mensal(5000.0).construir()
        print("FALHOU: Builder — deveria rejeitar contrato sem vigencia_meses")
    except ValueError:
        print("OK: Builder — rejeita contrato incompleto (sem vigencia_meses)")

    try:
        ConstruirContratoServico().com_vigencia(12).construir()
        print("FALHOU: Builder — deveria rejeitar contrato sem valor_mensal")
    except ValueError:
        print("OK: Builder — rejeita contrato incompleto (sem valor_mensal)")

    try:
        ConstruirContratoServico().com_valor_mensal(5000.0).com_vigencia(12).construir()
        print("FALHOU: Builder — deveria rejeitar contrato sem contratante")
    except ValueError:
        print("OK: Builder — rejeita contrato incompleto (sem contratante)")


if __name__ == "__main__":
    print("=== Gabarito 17 — Factory Method + Builder ===\n")
    verificar_factory()
    print()
    verificar_builder()
