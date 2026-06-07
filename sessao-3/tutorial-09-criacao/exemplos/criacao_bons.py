"""
criacao_bons.py — Factory Method + Builder para documentos de cobrança.
Execute: python3 criacao_bons.py
"""
from typing import Optional, Dict
from dataclasses import dataclass
from abc import ABC, abstractmethod


# ─── Factory Method ───────────────────────────────────────────────────────────

class DocumentoCobranca(ABC):
    def __init__(self, valor: float, vencimento: str, beneficiario: str) -> None:
        if valor <= 0:
            raise ValueError(f"Valor deve ser positivo, recebido: {valor}")
        self.valor        = valor
        self.vencimento   = vencimento
        self.beneficiario = beneficiario

    @abstractmethod
    def descricao(self) -> str: ...


class Boleto(DocumentoCobranca):
    def __init__(self, valor: float, vencimento: str, beneficiario: str,
                 codigo_barras: str) -> None:
        super().__init__(valor, vencimento, beneficiario)
        self.codigo_barras = codigo_barras

    def descricao(self) -> str:
        return f"Boleto R${self.valor:.2f} venc {self.vencimento} | {self.codigo_barras}"


class Pix(DocumentoCobranca):
    def __init__(self, valor: float, vencimento: str, beneficiario: str,
                 chave_pix: str) -> None:
        super().__init__(valor, vencimento, beneficiario)
        self.chave_pix = chave_pix

    def descricao(self) -> str:
        return f"Pix R${self.valor:.2f} → {self.chave_pix}"


class NotaFiscal(DocumentoCobranca):
    def __init__(self, valor: float, vencimento: str, beneficiario: str,
                 numero_nf: str, cfop: str) -> None:
        super().__init__(valor, vencimento, beneficiario)
        self.numero_nf = numero_nf
        self.cfop      = cfop

    def descricao(self) -> str:
        return f"NF {self.numero_nf} CFOP {self.cfop} R${self.valor:.2f}"


class FabricaDocumento:
    _registro: Dict[str, type] = {}

    @classmethod
    def registrar(cls, tipo: str, classe: type) -> None:
        cls._registro[tipo] = classe

    @classmethod
    def criar(cls, tipo: str, **dados) -> DocumentoCobranca:
        if tipo not in cls._registro:
            disponiveis = ", ".join(sorted(cls._registro.keys()))
            raise ValueError(f"Tipo '{tipo}' não registrado. Disponíveis: {disponiveis}")
        return cls._registro[tipo](**dados)


FabricaDocumento.registrar("boleto",      Boleto)
FabricaDocumento.registrar("pix",         Pix)
FabricaDocumento.registrar("nota_fiscal", NotaFiscal)


# ─── Builder ──────────────────────────────────────────────────────────────────

class ConstruirBoleto:
    def __init__(self) -> None:
        self._valor:         Optional[float] = None
        self._vencimento:    Optional[str]   = None
        self._beneficiario:  Optional[str]   = None
        self._codigo_barras: str             = "0000.00000 00000.000000"

    def com_valor(self, valor: float) -> "ConstruirBoleto":
        self._valor = valor
        return self

    def com_vencimento(self, vencimento: str) -> "ConstruirBoleto":
        self._vencimento = vencimento
        return self

    def com_beneficiario(self, beneficiario: str) -> "ConstruirBoleto":
        self._beneficiario = beneficiario
        return self

    def com_codigo_barras(self, codigo: str) -> "ConstruirBoleto":
        self._codigo_barras = codigo
        return self

    def construir(self) -> Boleto:
        if self._valor is None:
            raise ValueError("valor é obrigatório")
        if self._vencimento is None:
            raise ValueError("vencimento é obrigatório")
        if self._beneficiario is None:
            raise ValueError("beneficiario é obrigatório")
        return Boleto(self._valor, self._vencimento, self._beneficiario,
                      self._codigo_barras)


# ─── Verificação ──────────────────────────────────────────────────────────────

def verificar_factory() -> None:
    boleto = FabricaDocumento.criar(
        "boleto", valor=1500.0, vencimento="2026-07-15",
        beneficiario="CLI-100", codigo_barras="1234.56789 00000.000000"
    )
    assert isinstance(boleto, Boleto)
    assert boleto.valor == 1500.0
    print("OK: Factory — Boleto criado via FabricaDocumento")

    pix = FabricaDocumento.criar(
        "pix", valor=250.0, vencimento="2026-07-10",
        beneficiario="CLI-200", chave_pix="empresa@exemplo.com.br"
    )
    assert isinstance(pix, Pix)
    print("OK: Factory — Pix criado via FabricaDocumento")

    nf = FabricaDocumento.criar(
        "nota_fiscal", valor=890.0, vencimento="2026-07-30",
        beneficiario="CLI-300", numero_nf="NF-000042", cfop="5102"
    )
    assert isinstance(nf, NotaFiscal)
    print("OK: Factory — NotaFiscal criada via FabricaDocumento")

    try:
        FabricaDocumento.criar("ted", valor=100.0, vencimento="2026-07-15", beneficiario="X")
        print("FALHOU: Factory — deveria rejeitar tipo não registrado")
    except ValueError:
        print("OK: Factory — tipo desconhecido rejeitado com ValueError")

    print("OK: Factory — extensível por registro sem alterar FabricaDocumento")


def verificar_builder() -> None:
    boleto = (
        ConstruirBoleto()
        .com_valor(750.0)
        .com_vencimento("2026-08-01")
        .com_beneficiario("CLI-300")
        .construir()
    )
    assert isinstance(boleto, Boleto)
    assert boleto.valor == 750.0
    print("OK: Builder — Boleto construído com encadeamento fluente")

    try:
        ConstruirBoleto().com_valor(100.0).construir()
        print("FALHOU: Builder — deveria rejeitar boleto sem vencimento")
    except ValueError:
        print("OK: Builder — rejeita boleto incompleto (sem vencimento)")

    try:
        ConstruirBoleto().com_vencimento("2026-08-01").construir()
        print("FALHOU: Builder — deveria rejeitar boleto sem valor")
    except ValueError:
        print("OK: Builder — rejeita boleto incompleto (sem valor)")


if __name__ == "__main__":
    print("=== Criação _bons — Factory Method + Builder ===\n")
    verificar_factory()
    print()
    verificar_builder()
