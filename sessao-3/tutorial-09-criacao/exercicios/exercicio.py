"""
EXERCÍCIO 17 — Padrões de Criação
Tempo estimado: 15 minutos
Referência: Design Patterns (GoF), Cap. 3

INSTRUÇÕES:
  O código abaixo tem dois problemas:
  1. Construtor gordo: Contrato tem 9 parâmetros, maioria opcional.
  2. Função criar_contrato() com if/elif — adicionar novo tipo exige alterá-la.

  Aplique:
  1. Factory Method: crie uma FabricaContrato registrável.
  2. Builder: crie ConstruirContratoServico com métodos fluentes.

  Execute: python3 exercicio.py (deve rodar antes e depois)
"""
from typing import Optional
from dataclasses import dataclass


@dataclass
class Contrato:
    tipo:           str
    valor_mensal:   float
    vigencia_meses: int
    contratante:    str
    objeto:         Optional[str] = None       # serviço ou bem locado
    endereco:       Optional[str] = None       # para locação
    fornecedor_id:  Optional[str] = None       # para fornecimento
    prazo_entrega:  Optional[int] = None       # dias, para fornecimento
    observacoes:    Optional[str] = None


def criar_contrato(tipo: str, dados: dict) -> Contrato:
    """Adicionar ContratoObrasCivil exige alterar esta função."""
    if tipo == "servico":
        return Contrato(
            tipo="servico",
            valor_mensal=dados["valor_mensal"],
            vigencia_meses=dados["vigencia_meses"],
            contratante=dados["contratante"],
            objeto=dados.get("objeto", "Serviços gerais"),
        )
    elif tipo == "locacao":
        return Contrato(
            tipo="locacao",
            valor_mensal=dados["valor_mensal"],
            vigencia_meses=dados["vigencia_meses"],
            contratante=dados["contratante"],
            objeto=dados.get("objeto"),
            endereco=dados.get("endereco"),
        )
    elif tipo == "fornecimento":
        return Contrato(
            tipo="fornecimento",
            valor_mensal=dados["valor_mensal"],
            vigencia_meses=dados["vigencia_meses"],
            contratante=dados["contratante"],
            fornecedor_id=dados.get("fornecedor_id"),
            prazo_entrega=dados.get("prazo_entrega"),
        )
    else:
        raise ValueError(f"Tipo desconhecido: {tipo}")


if __name__ == "__main__":
    c1 = criar_contrato("servico", {
        "valor_mensal": 5000.0, "vigencia_meses": 12, "contratante": "EMP-001"
    })
    print(f"Contrato: {c1.tipo} R${c1.valor_mensal:.2f}/mês × {c1.vigencia_meses} meses")
    print(f"  campos não usados: endereco={c1.endereco}, fornecedor_id={c1.fornecedor_id}")
