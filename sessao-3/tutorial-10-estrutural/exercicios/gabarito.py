"""
GABARITO 18 — Padrões Estruturais: Adapter + Facade
Execute: python3 gabarito.py

Passos aplicados:
  Passo 1 — Identificar: comentários # ACOPLAMENTO: nas funções emitir/verificar/estornar_cobranca
  Passo 2 — Modelo de domínio: dataclass Boleto com id, codigo_barras, status, valor
  Passo 3 — Adapter: LegadoCobrancaAdapter isola a API legada (nId*, cCodigo*, cStatus*)
  Passo 4 — Facade: FachadaCobranca orquestra emitir + consultar + cancelar
"""
from typing import Protocol, Optional
from dataclasses import dataclass


# ─── API legada (não pode ser alterada) ───────────────────────────────────────

def gerar_boleto_legado(nValor: float, cVencimento: str, cPagador: str) -> dict:
    print(f"  [Legado] gerarBoleto({cPagador}, R${nValor:.2f})")
    return {
        "nIdBoleto":     12345,
        "cCodigoBarras": "9999.99999 99999.999999",
        "cStatusBoleto": "ATIVO",
        "nValorBoleto":  nValor,
    }

def consultar_status_legado(nIdBoleto: int) -> str:
    print(f"  [Legado] consultarStatus({nIdBoleto})")
    return "ATIVO"

def cancelar_boleto_legado(nIdBoleto: int, cMotivo: str) -> bool:
    print(f"  [Legado] cancelarBoleto({nIdBoleto}, {cMotivo})")
    return True


# ─── Passo 2 — Modelo de domínio ─────────────────────────────────────────────

@dataclass
class Boleto:
    id:            int
    codigo_barras: str
    status:        str
    valor:         float


# ─── Passo 3 — Adapter ───────────────────────────────────────────────────────
# Contrato (Protocol)

class IServicoCobranca(Protocol):
    def emitir(self, valor: float, vencimento: str, cliente_id: str) -> Boleto: ...
    def consultar(self, boleto_id: int) -> str: ...
    def cancelar(self, boleto_id: int) -> bool: ...


# ─── Adapter: isola a API legada do código de negócio ──────────────────────

class LegadoCobrancaAdapter:
    """Traduz a API legada (nId*, cCodigo*, cStatus*) para o contrato IServicoCobranca."""

    def emitir(self, valor: float, vencimento: str, cliente_id: str) -> Boleto:
        raw = gerar_boleto_legado(valor, vencimento, cliente_id)
        return Boleto(
            id=raw["nIdBoleto"],
            codigo_barras=raw["cCodigoBarras"],
            status=raw["cStatusBoleto"].lower(),
            valor=raw["nValorBoleto"],
        )

    def consultar(self, boleto_id: int) -> str:
        status_raw = consultar_status_legado(boleto_id)
        return status_raw.lower()

    def cancelar(self, boleto_id: int) -> bool:
        return cancelar_boleto_legado(boleto_id, "SOLICITACAO_CLIENTE")


# ─── Passo 4 — Facade ────────────────────────────────────────────────────────

class FachadaCobranca:
    """Quem chama executa o fluxo completo passando apenas os dados essenciais."""

    def __init__(self, servico: IServicoCobranca) -> None:
        self._servico = servico

    def processar_cobranca_completa(
        self,
        valor: float,
        vencimento: str,
        cliente_id: str,
    ) -> dict:
        boleto  = self._servico.emitir(valor, vencimento, cliente_id)
        status  = self._servico.consultar(boleto.id)
        cancelado = self._servico.cancelar(boleto.id)
        return {
            "boleto_id":   boleto.id,
            "codigo":      boleto.codigo_barras,
            "status_final": status,
            "cancelado":   cancelado,
        }


# ─── Verificação ──────────────────────────────────────────────────────────────

def verificar_adapter() -> None:
    adapter = LegadoCobrancaAdapter()

    boleto = adapter.emitir(500.0, "2026-08-15", "CLI-200")
    assert isinstance(boleto, Boleto), "esperado Boleto, obtido outro tipo"
    assert boleto.id == 12345, f"esperado 12345, obtido {boleto.id}"
    assert boleto.status == "ativo", f"esperado 'ativo', obtido '{boleto.status}'"
    assert not hasattr(boleto, "nIdBoleto"), "campo legado nIdBoleto não deve ser exposto"
    print("OK: Adapter — emitir() retorna Boleto sem campos legados")

    status = adapter.consultar(12345)
    assert status == "ativo", f"esperado 'ativo', obtido '{status}'"
    print("OK: Adapter — consultar() normaliza status para minúsculas")

    cancelado = adapter.cancelar(12345)
    assert cancelado is True, f"esperado True, obtido {cancelado}"
    print("OK: Adapter — cancelar() passa motivo fixo ao sistema legado")


def verificar_facade() -> None:
    fachada = FachadaCobranca(LegadoCobrancaAdapter())
    resultado = fachada.processar_cobranca_completa(300.0, "2026-09-01", "CLI-300")

    assert resultado["boleto_id"] == 12345, f"esperado 12345, obtido {resultado['boleto_id']}"
    assert resultado["status_final"] == "ativo", f"esperado 'ativo', obtido '{resultado['status_final']}'"
    assert resultado["cancelado"] is True, f"esperado True, obtido {resultado['cancelado']}"
    print("OK: Facade — processar_cobranca_completa() executa emitir + consultar + cancelar")
    print("OK: Facade — chamador não conhece API legada nem sequência de passos")


if __name__ == "__main__":
    print("=== Gabarito 18 — Adapter + Facade (boletos) ===\n")
    verificar_adapter()
    print()
    verificar_facade()
