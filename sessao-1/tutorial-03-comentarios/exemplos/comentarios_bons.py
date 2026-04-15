"""
EXEMPLOS: Comentários que seguem os princípios do Clean Code
Referência: Clean Code, Cap. 4 — Comments
Execute: python comentarios_bons.py

Copyright (c) 2026 Arkhi Consultoria. Todos os direitos reservados.
Distribuição interna — material de treinamento.
"""

# ─── Bom 1: Comentário de intenção — explica o "porquê", não o "o quê" ────────

def calcular_total(preco: float, quantidade: int) -> float:
    return preco * quantidade
    # Sem comentário necessário — o nome já diz tudo.


PERCENTUAL_RETENCAO_ISS = 2.0

def calcular_valor_liquido(valor_bruto: float) -> float:
    # ISS é retido na fonte conforme contrato-padrão da empresa.
    # Alíquota definida na cláusula 7.3 do contrato modelo (rev. 2025).
    return valor_bruto * (1 - PERCENTUAL_RETENCAO_ISS / 100)


# ─── Bom 2: Amplificação — destaca algo não óbvio que passaria despercebido ───

PRAZO_MAXIMO_CANCELAMENTO_HORAS = 2

def pode_cancelar_pedido(pedido: dict) -> bool:
    from datetime import datetime, timezone

    criado_em = pedido["criado_em"]
    agora = datetime.now(timezone.utc)
    horas_decorridas = (agora - criado_em).total_seconds() / 3600

    # IMPORTANTE: usamos timezone UTC em ambos os lados intencionalmente.
    # O campo "criado_em" é sempre gravado em UTC no banco — nunca em
    # horário local — para evitar ambiguidade no horário de verão.
    return horas_decorridas <= PRAZO_MAXIMO_CANCELAMENTO_HORAS


# ─── Bom 3: TODO rastreável — com ticket, responsável e prazo ─────────────────

def buscar_usuario(usuario_id: str) -> dict:
    # TODO [PLAT-1847]: substituir mock por chamada real ao serviço de usuários.
    # Responsável: @ana.souza  |  Prazo: Sprint 42 (2026-05-05)
    # Contexto: o serviço ainda está em homologação; mock garante os testes passem.
    return {"id": usuario_id, "nome": "Usuário Mockado"}


# ─── Bom 4: Código autodocumentado que dispensa comentário ────────────────────

# ❌ Ruim: precisava de comentário para explicar a condição
# if u["tp"] == 1 and u["st"] != 0 and u["dt_exp"] is None:

# ✅ Bom: o código fala por si mesmo
def usuario_pode_emitir_nota(usuario: dict) -> bool:
    eh_pessoa_juridica = usuario["tipo"] == "PJ"
    esta_ativo = usuario["status"] == "ativo"
    sem_restricao_fiscal = usuario["restricao_fiscal"] is None
    return eh_pessoa_juridica and esta_ativo and sem_restricao_fiscal


DESCONTO_FIDELIDADE_PERCENTUAL = 5.0
DESCONTO_VOLUME_PERCENTUAL = 10.0
QUANTIDADE_MINIMA_PARA_DESCONTO_VOLUME = 10

def calcular_desconto(quantidade: int, eh_cliente_fidelidade: bool) -> float:
    if quantidade >= QUANTIDADE_MINIMA_PARA_DESCONTO_VOLUME:
        return DESCONTO_VOLUME_PERCENTUAL
    if eh_cliente_fidelidade:
        return DESCONTO_FIDELIDADE_PERCENTUAL
    return 0.0


# ─── Bom 5: Comentário de licença e cabeçalho de módulo ──────────────────────
# (demonstrado no docstring do módulo, no topo deste arquivo)

# ─── Bom 6: Explicando uma escolha de algoritmo não óbvia ─────────────────────

def aplicar_arredondamento_bancario(valor: float) -> float:
    # Arredondamento bancário (half-even / "round half to even"):
    # 2.5 → 2,  3.5 → 4  (arredonda para o par mais próximo).
    # Usado para neutralizar viés acumulado em grandes volumes de transações.
    # Python 3 implementa este comportamento nativamente com round().
    return round(valor, 2)


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    from datetime import datetime, timezone, timedelta

    print("=== Demonstração: Comentários Bons ===\n")

    print("calcular_total(50.0, 3):", calcular_total(50.0, 3))
    print("calcular_valor_liquido(R$1000):", calcular_valor_liquido(1000.0))

    pedido_recente = {
        "id": "P01",
        "criado_em": datetime.now(timezone.utc) - timedelta(hours=1),
    }
    pedido_antigo = {
        "id": "P02",
        "criado_em": datetime.now(timezone.utc) - timedelta(hours=3),
    }
    print("\npode_cancelar (1h atrás):", pode_cancelar_pedido(pedido_recente))
    print("pode_cancelar (3h atrás):", pode_cancelar_pedido(pedido_antigo))

    print("\nbuscar_usuario('U42'):", buscar_usuario("U42"))

    usuario_pj_ativo = {"tipo": "PJ", "status": "ativo", "restricao_fiscal": None}
    usuario_pf = {"tipo": "PF", "status": "ativo", "restricao_fiscal": None}
    print("\nusuario_pode_emitir_nota (PJ ativo):", usuario_pode_emitir_nota(usuario_pj_ativo))
    print("usuario_pode_emitir_nota (PF):", usuario_pode_emitir_nota(usuario_pf))

    print("\ncalcular_desconto(15 unidades):", calcular_desconto(15, False), "%")
    print("calcular_desconto(5 unidades, fidelidade):", calcular_desconto(5, True), "%")
    print("calcular_desconto(3 unidades, sem fidelidade):", calcular_desconto(3, False), "%")

    print("\narredondamento bancário de 2.5:", aplicar_arredondamento_bancario(2.5))
    print("arredondamento bancário de 3.5:", aplicar_arredondamento_bancario(3.5))
    print("arredondamento bancário de 2.455:", aplicar_arredondamento_bancario(2.455))
