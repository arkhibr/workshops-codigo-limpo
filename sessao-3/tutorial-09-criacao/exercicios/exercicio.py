"""
EXERCÍCIO 17 — Padrões de Criação
Referência: Design Patterns (GoF), Cap. 3

PASSOS (31 min no total):

  PASSO 1 — IDENTIFICAR (5 min)
    Leia o código abaixo e adicione comentários marcando os dois problemas:
      # PROBLEMA: construtor gordo (9 parâmetros, maioria None)
      # PROBLEMA: if/elif rígido — adicionar tipo exige alterar criar_contrato()
    Meta: encontrar os 2 problemas e anotar onde estão antes de alterar código.

  PASSO 2 — FACTORY COM DICT (8 min)
    Substitua o if/elif de criar_contrato() por um dict:
      _FABRICA = {"servico": ..., "locacao": ..., "fornecimento": ...}
    criar_contrato() consulta o dict e chama a entrada correspondente.
    Verifique que o demo ainda roda.

  PASSO 3 — FACTORY REGISTRÁVEL (8 min)
    Transforme _FABRICA em FabricaContrato com:
      FabricaContrato.registrar(tipo, funcao_criadora)
      FabricaContrato.criar(tipo, dados)
    Registre os 3 tipos existentes externamente.
    Verifique que o demo ainda roda e que um novo tipo pode ser registrado
    sem alterar FabricaContrato.

  PASSO 4 — BUILDER (10 min)
    Crie ConstruirContratoServico com métodos fluentes:
      com_valor_mensal(v) -> self
      com_vigencia(m) -> self
      com_contratante(c) -> self
      construir() -> Contrato  (lança ValueError se campos obrigatórios faltarem)
    Verifique que o demo roda com a nova sintaxe fluente.

Execute: python3 exercicio.py (deve rodar antes e depois de cada passo)
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

    # --- Stub Passo 3: registrar novo tipo sem alterar FabricaContrato ---
    # Após implementar FabricaContrato, descomente e verifique:
    # FabricaContrato.registrar("obras_civil", lambda d: Contrato(
    #     tipo="obras_civil",
    #     valor_mensal=d["valor_mensal"],
    #     vigencia_meses=d["vigencia_meses"],
    #     contratante=d["contratante"],
    # ))
    # obras = FabricaContrato.criar("obras_civil", {
    #     "valor_mensal": 25000.0, "vigencia_meses": 8, "contratante": "EMP-004"
    # })
    # print(f"Novo tipo: {obras.tipo} R${obras.valor_mensal:.2f}/mês")

    # --- Stub Passo 4: sintaxe fluente do Builder ---
    # Após implementar ConstruirContratoServico, descomente e verifique:
    # c2 = (
    #     ConstruirContratoServico()
    #     .com_valor_mensal(5000.0)
    #     .com_vigencia(12)
    #     .com_contratante("EMP-001")
    #     .construir()
    # )
    # print(f"Builder: {c2.tipo} R${c2.valor_mensal:.2f}/mês × {c2.vigencia_meses} meses")
