"""
criacao_bons.py — Factory Method + Builder + Singleton para documentos de cobrança.
Execute: python3 criacao_bons.py
"""
from typing import Optional, Dict
from dataclasses import dataclass
from abc import ABC, abstractmethod


# ══════════════════════════════════════════════
# DOMÍNIO — hierarquia de documentos de cobrança
# ══════════════════════════════════════════════

class DocumentoCobranca(ABC):
    def __init__(self, valor: float, vencimento: str, beneficiario: str) -> None:
        if valor <= 0:
            raise ValueError(f"Valor deve ser positivo, recebido: {valor}")
        if not vencimento:
            raise ValueError("vencimento é obrigatório")
        if not beneficiario:
            raise ValueError("beneficiario é obrigatório")
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
        return (
            f"Boleto R${self.valor:.2f} | venc {self.vencimento} "
            f"| benef {self.beneficiario} | {self.codigo_barras}"
        )


class Pix(DocumentoCobranca):
    def __init__(self, valor: float, vencimento: str, beneficiario: str,
                 chave_pix: str) -> None:
        super().__init__(valor, vencimento, beneficiario)
        if not chave_pix:
            raise ValueError("chave_pix é obrigatória para Pix")
        self.chave_pix = chave_pix

    def descricao(self) -> str:
        return f"Pix R${self.valor:.2f} | venc {self.vencimento} → {self.chave_pix}"


class NotaFiscal(DocumentoCobranca):
    def __init__(self, valor: float, vencimento: str, beneficiario: str,
                 numero_nf: str, cfop: str) -> None:
        super().__init__(valor, vencimento, beneficiario)
        self.numero_nf = numero_nf
        self.cfop      = cfop

    def descricao(self) -> str:
        return f"NF {self.numero_nf} CFOP {self.cfop} R${self.valor:.2f} | benef {self.beneficiario}"


# ══════════════════════════════════════════════
# FACTORY METHOD — registro extensível de tipos
# ══════════════════════════════════════════════
#
# Cada novo tipo de documento é registrado em uma linha.
# FabricaDocumento nunca precisa ser aberta para adicionar tipos.
# OCP aplicado: aberto para extensão, fechado para modificação.

class FabricaDocumento:
    _registro: Dict[str, type] = {}

    @classmethod
    def registrar(cls, tipo: str, classe: type) -> None:
        cls._registro[tipo] = classe

    @classmethod
    def criar(cls, tipo: str, **dados) -> DocumentoCobranca:
        if tipo not in cls._registro:
            disponiveis = ", ".join(sorted(cls._registro.keys()))
            raise ValueError(
                f"Tipo '{tipo}' não registrado. Disponíveis: {disponiveis}"
            )
        return cls._registro[tipo](**dados)

    @classmethod
    def tipos_registrados(cls) -> list:
        return sorted(cls._registro.keys())


FabricaDocumento.registrar("boleto",      Boleto)
FabricaDocumento.registrar("pix",         Pix)
FabricaDocumento.registrar("nota_fiscal", NotaFiscal)
# Para adicionar TED: FabricaDocumento.registrar("ted", Ted) — uma linha, zero alterações acima.


# ══════════════════════════════════════════════
# BUILDER — construção fluente com validação na barreira
# ══════════════════════════════════════════════
#
# construir() é a barreira: o objeto só existe quando está completo e válido.
# Sem o builder, é possível criar DocumentoCobranca sem os campos obrigatórios.

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


class ConstruirPix:
    def __init__(self) -> None:
        self._valor:        Optional[float] = None
        self._vencimento:   Optional[str]   = None
        self._beneficiario: Optional[str]   = None
        self._chave_pix:    Optional[str]   = None

    def com_valor(self, valor: float) -> "ConstruirPix":
        self._valor = valor
        return self

    def com_vencimento(self, vencimento: str) -> "ConstruirPix":
        self._vencimento = vencimento
        return self

    def com_beneficiario(self, beneficiario: str) -> "ConstruirPix":
        self._beneficiario = beneficiario
        return self

    def com_chave_pix(self, chave: str) -> "ConstruirPix":
        self._chave_pix = chave
        return self

    def construir(self) -> Pix:
        if self._valor is None:
            raise ValueError("valor é obrigatório")
        if self._vencimento is None:
            raise ValueError("vencimento é obrigatório")
        if self._beneficiario is None:
            raise ValueError("beneficiario é obrigatório")
        if self._chave_pix is None:
            raise ValueError("chave_pix é obrigatória")
        return Pix(self._valor, self._vencimento, self._beneficiario,
                   self._chave_pix)


# ══════════════════════════════════════════════
# SINGLETON — registro central, instância única
# ══════════════════════════════════════════════
#
# Singleton controla QUANTAS instâncias existem (uma).
# SOLID controla O QUE cada classe faz e como se relaciona com outras.
# Eles operam em eixos diferentes e se complementam.
#
# ARMADILHA CLÁSSICA — anti-pattern:
#   def processar(self):
#       registro = RegistroDocumentos.get_instancia()  # dependência oculta!
#       ...
#
# FORMA SOLID:
#   def __init__(self, registro: RegistroDocumentos):  # DIP: injetado no construtor
#       self._registro = registro                       # sem acoplamento oculto

class RegistroDocumentos:
    """Registro central de fábricas de documentos — Singleton.

    Uma única instância por aplicação garante que todos os processadores
    enxergam os mesmos tipos registrados. A instância é injetada via DIP —
    o consumidor não sabe (e não precisa saber) que é um Singleton.
    """
    _instancia: Optional["RegistroDocumentos"] = None

    def __new__(cls) -> "RegistroDocumentos":
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._registro: Dict[str, type] = {}
        return cls._instancia

    def registrar(self, tipo: str, classe: type) -> None:
        self._registro[tipo] = classe

    def criar(self, tipo: str, **dados) -> DocumentoCobranca:
        if tipo not in self._registro:
            disponiveis = ", ".join(sorted(self._registro.keys()))
            raise ValueError(
                f"Tipo '{tipo}' não registrado. Disponíveis: {disponiveis}"
            )
        return self._registro[tipo](**dados)

    def tipos_registrados(self) -> list:
        return sorted(self._registro.keys())


class ProcessadorDocumento:
    """Orquestra a criação e processamento de documentos.

    Depende de RegistroDocumentos via DIP — recebe no construtor.
    Não chama RegistroDocumentos.get_instancia() internamente.
    Isso permite testar ProcessadorDocumento com um registro parcial.
    """
    def __init__(self, registro: RegistroDocumentos) -> None:
        self._registro = registro

    def processar(self, tipo: str, **dados) -> str:
        doc = self._registro.criar(tipo, **dados)
        resultado = doc.descricao()
        print(f"  [Processado] {resultado}")
        return resultado

    def listar_tipos(self) -> list:
        return self._registro.tipos_registrados()


# ══════════════════════════════════════════════
# DEMONSTRAÇÃO
# ══════════════════════════════════════════════

def verificar_factory() -> None:
    print("── Factory Method ────────────────────────────────────")

    boleto = FabricaDocumento.criar(
        "boleto", valor=1500.0, vencimento="2026-07-15",
        beneficiario="CLI-100", codigo_barras="1234.56789 00000.000000"
    )
    assert isinstance(boleto, Boleto)
    print(f"  OK: {boleto.descricao()}")

    pix = FabricaDocumento.criar(
        "pix", valor=250.0, vencimento="2026-07-10",
        beneficiario="CLI-200", chave_pix="empresa@exemplo.com.br"
    )
    assert isinstance(pix, Pix)
    print(f"  OK: {pix.descricao()}")

    nf = FabricaDocumento.criar(
        "nota_fiscal", valor=890.0, vencimento="2026-07-30",
        beneficiario="CLI-300", numero_nf="NF-000042", cfop="5102"
    )
    assert isinstance(nf, NotaFiscal)
    print(f"  OK: {nf.descricao()}")

    try:
        FabricaDocumento.criar("ted", valor=100.0, vencimento="2026-07-15", beneficiario="X")
    except ValueError as e:
        print(f"  OK: tipo desconhecido rejeitado — {e}")

    print(f"  Tipos registrados: {FabricaDocumento.tipos_registrados()}")


def verificar_builder() -> None:
    print("── Builder ───────────────────────────────────────────")

    boleto = (
        ConstruirBoleto()
        .com_valor(750.0)
        .com_vencimento("2026-08-01")
        .com_beneficiario("CLI-300")
        .com_codigo_barras("9876.54321 00000.000000")
        .construir()
    )
    assert isinstance(boleto, Boleto)
    print(f"  OK: {boleto.descricao()}")

    try:
        ConstruirBoleto().com_valor(100.0).construir()
    except ValueError as e:
        print(f"  OK: boleto incompleto rejeitado — {e}")

    pix = (
        ConstruirPix()
        .com_valor(300.0)
        .com_vencimento("2026-08-15")
        .com_beneficiario("CLI-400")
        .com_chave_pix("11999999999")
        .construir()
    )
    assert isinstance(pix, Pix)
    print(f"  OK: {pix.descricao()}")

    try:
        ConstruirPix().com_valor(50.0).com_vencimento("2026-08-01").com_beneficiario("CLI-X").construir()
    except ValueError as e:
        print(f"  OK: pix sem chave rejeitado — {e}")


def verificar_singleton_com_solid() -> None:
    print("── Singleton + SOLID ─────────────────────────────────")

    # Singleton: mesma instância em qualquer ponto da aplicação
    reg1 = RegistroDocumentos()
    reg2 = RegistroDocumentos()
    assert reg1 is reg2, "Singleton violado — instâncias diferentes!"
    print("  OK: RegistroDocumentos é Singleton (reg1 is reg2)")

    # Configurado uma vez no startup da aplicação
    reg1.registrar("boleto",      Boleto)
    reg1.registrar("pix",         Pix)
    reg1.registrar("nota_fiscal", NotaFiscal)

    # DIP: ProcessadorDocumento recebe o registro via construtor
    # — não chama RegistroDocumentos() internamente
    processador = ProcessadorDocumento(reg1)
    print(f"  Tipos disponíveis: {processador.listar_tipos()}")

    processador.processar(
        "boleto", valor=500.0, vencimento="2026-09-01",
        beneficiario="CLI-500", codigo_barras="5555.55555 55555.555555"
    )
    processador.processar(
        "pix", valor=120.0, vencimento="2026-09-01",
        beneficiario="CLI-600", chave_pix="cliente@exemplo.com.br"
    )

    # Teste: passa um registro limpo — ProcessadorDocumento não sabe que é Singleton
    RegistroDocumentos._instancia = None   # reset para demonstrar testabilidade
    registro_teste = RegistroDocumentos()
    registro_teste.registrar("boleto", Boleto)
    processador_teste = ProcessadorDocumento(registro_teste)
    try:
        processador_teste.processar("pix", valor=10.0, vencimento="2026-09-01",
                                    beneficiario="X", chave_pix="x")
    except ValueError as e:
        print(f"  OK: processador de teste isolado — {e}")

    # Restaura o estado original
    RegistroDocumentos._instancia = None


if __name__ == "__main__":
    print("=== Criação _bons — Factory Method + Builder + Singleton ===\n")
    verificar_factory()
    print()
    verificar_builder()
    print()
    verificar_singleton_com_solid()
