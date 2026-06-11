"""
EXERCÍCIO 18 — Padrões Estruturais: Adapter + Facade
Tempo estimado: 28 minutos (4 micro-passos)
Referência: Design Patterns (GoF), Cap. 4

PASSOS:

  PASSO 1 — IDENTIFICAR (5 min)
    Nas 3 funções de negócio (emitir_cobranca, verificar_cobranca, estornar_cobranca),
    adicione um comentário # ACOPLAMENTO: antes de cada chamada à API legada.
    Meta: marcar os 3 acoplamentos antes de alterar código.

  PASSO 2 — MODELO DE DOMÍNIO (5 min)
    Crie o dataclass Boleto com campos:
      id: int, codigo_barras: str, status: str, valor: float
    (sem alterar mais nada ainda)

  PASSO 3 — ADAPTER (10 min)
    Crie a classe LegadoCobrancaAdapter com 3 métodos:
      emitir(valor, vencimento, cliente_id) -> Boleto
      consultar(boleto_id) -> str
      cancelar(boleto_id) -> bool
    Cada método chama uma função *_legado e normaliza os campos.
    Verifique: adapter.emitir(500.0, "2026-08-15", "CLI-200") retorna um Boleto.

  PASSO 4 — FACADE (8 min)
    Crie FachadaCobranca recebendo um adapter no construtor, com:
      processar_cobranca_completa(valor, vencimento, cliente_id) -> dict
    Que chama emitir + consultar + cancelar e devolve resumo.
    Verifique que o caller não precisa mais conhecer a API legada.

  Execute: python3 exercicio.py (deve rodar antes e depois de cada passo)
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


# ─── Passo 2: implemente o dataclass Boleto aqui ─────────────────────────────
# @dataclass
# class Boleto:
#     ...


# ─── Passo 3: implemente LegadoCobrancaAdapter aqui ──────────────────────────
# class LegadoCobrancaAdapter:
#     def emitir(self, valor, vencimento, cliente_id) -> Boleto: ...
#     def consultar(self, boleto_id) -> str: ...
#     def cancelar(self, boleto_id) -> bool: ...


# ─── Passo 4: implemente FachadaCobranca aqui ────────────────────────────────
# class FachadaCobranca:
#     def __init__(self, adapter): ...
#     def processar_cobranca_completa(self, valor, vencimento, cliente_id) -> dict: ...


if __name__ == "__main__":
    # Código original (Passo 1: adicione # ACOPLAMENTO: nas linhas de chamada legada)
    boleto = emitir_cobranca(500.0, "2026-08-15", "CLI-200")
    print(f"Boleto: id={boleto['id']}, status={boleto['status']}")
    status = verificar_cobranca(boleto["id"])
    print(f"Status: {status}")
    cancelado = estornar_cobranca(boleto["id"])
    print(f"Cancelado: {cancelado}")

    # Passo 3 — descomente para verificar o Adapter:
    # adapter = LegadoCobrancaAdapter()
    # b = adapter.emitir(500.0, "2026-08-15", "CLI-200")
    # print(f"[Adapter] Boleto: id={b.id}, status={b.status}")

    # Passo 4 — descomente para verificar a Facade:
    # fachada = FachadaCobranca(LegadoCobrancaAdapter())
    # resultado = fachada.processar_cobranca_completa(500.0, "2026-08-15", "CLI-200")
    # print(f"[Facade] resultado={resultado}")
