"""
criacao_ruins.py — Construtor gordo e if/elif de instanciação.
Execute: python3 criacao_ruins.py
"""
from typing import Optional
from dataclasses import dataclass


# ─── Problema 1: Construtor gordo ─────────────────────────────────────────────

@dataclass
class DocumentoCobranca:
    """10 parâmetros — maioria opcional, fácil chamar errado, sem garantias."""
    tipo:           str
    valor:          float
    vencimento:     str
    beneficiario:   str
    codigo_barras:  Optional[str] = None   # só boleto
    chave_pix:      Optional[str] = None   # só pix
    numero_nf:      Optional[str] = None   # só nota fiscal
    cfop:           Optional[str] = None   # só nota fiscal
    descricao:      Optional[str] = None
    observacoes:    Optional[str] = None


# ─── Problema 2: if/elif de instanciação ──────────────────────────────────────

def criar_documento(tipo: str, dados: dict) -> DocumentoCobranca:
    """Adicionar 'TED' exige alterar esta função."""
    if tipo == "boleto":
        return DocumentoCobranca(
            tipo="boleto",
            valor=dados["valor"],
            vencimento=dados["vencimento"],
            beneficiario=dados["beneficiario"],
            codigo_barras=dados.get("codigo_barras", "9999.99999 99999.999999"),
        )
    elif tipo == "pix":
        return DocumentoCobranca(
            tipo="pix",
            valor=dados["valor"],
            vencimento=dados["vencimento"],
            beneficiario=dados["beneficiario"],
            chave_pix=dados.get("chave_pix", "chave@exemplo.com.br"),
        )
    elif tipo == "nota_fiscal":
        return DocumentoCobranca(
            tipo="nota_fiscal",
            valor=dados["valor"],
            vencimento=dados["vencimento"],
            beneficiario=dados["beneficiario"],
            numero_nf=dados.get("numero_nf", "NF-000001"),
            cfop=dados.get("cfop", "5102"),
        )
    else:
        raise ValueError(f"Tipo desconhecido: {tipo}")


if __name__ == "__main__":
    print("=== Criação _ruins — construtor gordo e if/elif ===\n")

    boleto = criar_documento("boleto", {
        "valor": 1500.00, "vencimento": "2026-07-15", "beneficiario": "CLI-100"
    })
    print(f"Boleto: R${boleto.valor:.2f}, venc {boleto.vencimento}")
    print(f"  campos não usados: chave_pix={boleto.chave_pix}, numero_nf={boleto.numero_nf}")

    pix = criar_documento("pix", {
        "valor": 250.00, "vencimento": "2026-07-10", "beneficiario": "CLI-200"
    })
    print(f"Pix: R${pix.valor:.2f}, chave={pix.chave_pix}")

    nf = criar_documento("nota_fiscal", {
        "valor": 890.00, "vencimento": "2026-07-30", "beneficiario": "CLI-300"
    })
    print(f"NF: R${nf.valor:.2f}, CFOP={nf.cfop}")
