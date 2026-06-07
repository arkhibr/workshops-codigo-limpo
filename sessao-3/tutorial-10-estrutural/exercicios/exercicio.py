"""
EXERCÍCIO 18 — Padrões Estruturais: Adapter + Facade
Tempo estimado: 15 minutos
Referência: Design Patterns (GoF), Cap. 4

INSTRUÇÕES:
  O sistema de boletos bancários abaixo tem uma API legada com nomes e
  estruturas de dados inconsistentes. O código de negócio chama essas
  funções diretamente em 3 lugares diferentes.

  1. Crie um Adapter que isole o sistema legado do código de negócio.
  2. Crie uma Facade que simplifique o fluxo completo (criar + consultar + cancelar).

  Execute: python3 exercicio.py (deve rodar antes e depois)
"""
from typing import Optional
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


# ─── Código de negócio — chama legado diretamente ────────────────────────────

def emitir_cobranca(valor: float, vencimento: str, cliente_id: str) -> dict:
    raw = gerar_boleto_legado(valor, vencimento, cliente_id)   # acoplamento direto
    return {
        "id":     raw["nIdBoleto"],
        "codigo": raw["cCodigoBarras"],
        "status": raw["cStatusBoleto"].lower(),
        "valor":  raw["nValorBoleto"],
    }

def verificar_cobranca(boleto_id: int) -> str:
    status_raw = consultar_status_legado(boleto_id)            # acoplamento direto
    return status_raw.lower()

def estornar_cobranca(boleto_id: int) -> bool:
    return cancelar_boleto_legado(boleto_id, "SOLICITACAO_CLIENTE")  # acoplamento direto


# ─── TODO: Implemente aqui ────────────────────────────────────────────────────
#
# 1. Crie um dataclass Boleto com campos: id, codigo_barras, status, valor
#
# 2. Crie um Protocol IServicoCobranca com os métodos:
#    - emitir(valor, vencimento, cliente_id) -> Boleto
#    - consultar(boleto_id) -> str
#    - cancelar(boleto_id) -> bool
#
# 3. Crie a classe LegadoCobrancaAdapter implementando IServicoCobranca
#    que chama as funções *_legado e normaliza os resultados
#
# 4. Crie a classe FachadaCobranca com o método:
#    - processar_cobranca_completa(valor, vencimento, cliente_id) -> dict
#      (emite + consulta + cancela e retorna um resumo)
#
# ─────────────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    boleto = emitir_cobranca(500.0, "2026-08-15", "CLI-200")
    print(f"Boleto: id={boleto['id']}, status={boleto['status']}")
    status = verificar_cobranca(boleto["id"])
    print(f"Status: {status}")
    cancelado = estornar_cobranca(boleto["id"])
    print(f"Cancelado: {cancelado}")
