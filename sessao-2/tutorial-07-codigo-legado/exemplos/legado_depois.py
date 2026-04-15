# Módulo de processamento de faturas — versão refatorada
# Mesma lógica de negócio do legado_antes.py, com responsabilidades separadas.

from dataclasses import dataclass, field
from typing import List, Optional

# ---------------------------------------------------------------------------
# Constantes nomeadas — sem magic numbers espalhados pelo código
# ---------------------------------------------------------------------------
ALIQUOTA_PJ_ALTA = 0.12       # ISS sobre serviços PJ acima do limiar
ALIQUOTA_PJ_BAIXA = 0.065     # ISS sobre serviços PJ abaixo do limiar
LIMIAR_PJ = 5000.0            # Valor que define faixa de alíquota PJ

ALIQUOTA_PF_ALTA = 0.075      # IR retido para PF acima do limiar
ALIQUOTA_PF_BAIXA = 0.03      # IR retido para PF abaixo do limiar
LIMIAR_PF = 2000.0            # Valor que define faixa de alíquota PF

# Taxa administrativa fixa cobrada em faturas de pessoa física.
# Origem: contrato com câmara de compensação (revisão: dez/2022).
TAXA_FIXA_PF = 150.0

ADICIONAL_MUITOS_ITENS = 1.15  # Acréscimo quando fatura PJ tem mais de 10 itens
LIMITE_MUITOS_ITENS = 10

PERCENTUAL_DESCONTO_ALTO_VALOR = 0.05   # Desconto progressivo para valores altos
LIMIAR_DESCONTO = 10000.0


# ---------------------------------------------------------------------------
# Objetos de domínio
# ---------------------------------------------------------------------------
@dataclass
class Cliente:
    id: str
    nome: str
    email: str
    tipo: str  # "PF" ou "PJ"


@dataclass
class ItemFatura:
    descricao: str


@dataclass
class Fatura:
    id: str
    cliente: Cliente
    valor_bruto: float
    imposto: float
    desconto: float
    valor_total: float
    itens: List[str]
    status: str = "EMITIDA"

    @property
    def valor_liquido(self) -> float:
        return self.valor_bruto + self.imposto - self.desconto


# ---------------------------------------------------------------------------
# ValidadorDeFatura — responsabilidade única: verificar integridade dos dados
# ---------------------------------------------------------------------------
class ValidadorDeFatura:
    def validar(self, dados: dict) -> Optional[str]:
        """Retorna mensagem de erro ou None se válido."""
        if not dados:
            return "dados ausentes"
        for campo in ("cli", "val", "it"):
            if campo not in dados:
                return f"campo obrigatório ausente: {campo}"
        if dados["val"] <= 0:
            return "valor deve ser positivo"
        return None


# ---------------------------------------------------------------------------
# CalculadorDeImpostos — responsabilidade única: regras fiscais
# ---------------------------------------------------------------------------
class CalculadorDeImpostos:
    def calcular(self, valor: float, tipo_cliente: str, quantidade_itens: int) -> float:
        if tipo_cliente == "PJ":
            return self._imposto_pj(valor, quantidade_itens)
        return self._imposto_pf(valor)

    def _imposto_pj(self, valor: float, quantidade_itens: int) -> float:
        aliquota = ALIQUOTA_PJ_ALTA if valor > LIMIAR_PJ else ALIQUOTA_PJ_BAIXA
        imposto = valor * aliquota
        # Acréscimo por volume de itens — regra interna aprovada em 2021
        if quantidade_itens > LIMITE_MUITOS_ITENS:
            imposto *= ADICIONAL_MUITOS_ITENS
        return imposto

    def _imposto_pf(self, valor: float) -> float:
        aliquota = ALIQUOTA_PF_ALTA if valor > LIMIAR_PF else ALIQUOTA_PF_BAIXA
        return valor * aliquota + TAXA_FIXA_PF

    def calcular_desconto(self, valor: float) -> float:
        if valor > LIMIAR_DESCONTO:
            return valor * PERCENTUAL_DESCONTO_ALTO_VALOR
        return 0.0


# ---------------------------------------------------------------------------
# RepositorioDeFaturas — responsabilidade única: persistência
# ---------------------------------------------------------------------------
class RepositorioDeFaturas:
    def __init__(self):
        self._faturas: dict = {}

    def salvar(self, fatura: Fatura) -> None:
        self._faturas[fatura.id] = fatura

    def buscar(self, fatura_id: str) -> Optional[Fatura]:
        return self._faturas.get(fatura_id)

    def proximo_id(self) -> str:
        return "F" + str(len(self._faturas) + 1).zfill(4)


# ---------------------------------------------------------------------------
# NotificadorDeFaturas — responsabilidade única: comunicação com cliente
# ---------------------------------------------------------------------------
class NotificadorDeFaturas:
    def notificar_emissao(self, fatura: Fatura) -> None:
        print(
            f"EMAIL -> {fatura.cliente.email}: "
            f"Fatura {fatura.id} no valor de R$ {fatura.valor_total:.2f} emitida."
        )

    def notificar_atualizacao(self, fatura: Fatura) -> None:
        print(
            f"EMAIL -> {fatura.cliente.email}: "
            f"Fatura {fatura.id} atualizada para R$ {fatura.valor_total:.2f}."
        )


# ---------------------------------------------------------------------------
# ProcessadorDeFaturas — orquestra as demais classes
# ---------------------------------------------------------------------------
class ProcessadorDeFaturas:
    def __init__(
        self,
        clientes: dict,
        repositorio: RepositorioDeFaturas,
        calculador: CalculadorDeImpostos,
        validador: ValidadorDeFatura,
        notificador: NotificadorDeFaturas,
    ):
        self._clientes = clientes
        self._repositorio = repositorio
        self._calculador = calculador
        self._validador = validador
        self._notificador = notificador

    def processar(self, dados: dict) -> Optional[Fatura]:
        erro = self._validador.validar(dados)
        if erro:
            print(f"[ERRO] {erro}")
            return None

        cliente = self._clientes.get(dados["cli"])
        if cliente is None:
            print("[ERRO] cliente não encontrado")
            return None

        valor_bruto = dados["val"]
        itens = dados["it"]
        imposto = self._calculador.calcular(valor_bruto, cliente.tipo, len(itens))
        desconto = self._calculador.calcular_desconto(valor_bruto)
        valor_total = valor_bruto + imposto - desconto

        fatura = Fatura(
            id=self._repositorio.proximo_id(),
            cliente=cliente,
            valor_bruto=valor_bruto,
            imposto=round(imposto, 2),
            desconto=round(desconto, 2),
            valor_total=round(valor_total, 2),
            itens=itens,
        )

        self._repositorio.salvar(fatura)
        self._notificador.notificar_emissao(fatura)
        print(f"[OK] Fatura {fatura.id} criada para {cliente.nome}")
        return fatura

    def reprocessar(self, fatura_id: str) -> Optional[Fatura]:
        fatura = self._repositorio.buscar(fatura_id)
        if fatura is None:
            print(f"[ERRO] Fatura {fatura_id} não encontrada")
            return None

        imposto = self._calculador.calcular(
            fatura.valor_bruto, fatura.cliente.tipo, len(fatura.itens)
        )
        desconto = self._calculador.calcular_desconto(fatura.valor_bruto)

        fatura.imposto = round(imposto, 2)
        fatura.desconto = round(desconto, 2)
        fatura.valor_total = round(fatura.valor_bruto + imposto - desconto, 2)
        fatura.status = "REPROCESSADA"

        self._repositorio.salvar(fatura)
        self._notificador.notificar_atualizacao(fatura)
        print(f"[OK] Fatura {fatura_id} reprocessada")
        return fatura


# ---------------------------------------------------------------------------
# Bootstrap — montagem das dependências
# ---------------------------------------------------------------------------
def criar_processador(clientes_raw: dict) -> ProcessadorDeFaturas:
    clientes = {
        cid: Cliente(id=cid, nome=c["nome"], email=c["email"], tipo=c["tipo"])
        for cid, c in clientes_raw.items()
    }
    return ProcessadorDeFaturas(
        clientes=clientes,
        repositorio=RepositorioDeFaturas(),
        calculador=CalculadorDeImpostos(),
        validador=ValidadorDeFatura(),
        notificador=NotificadorDeFaturas(),
    )


if __name__ == "__main__":
    clientes_bd = {
        "C001": {"nome": "Acme Corp", "email": "faturamento@acme.com", "tipo": "PJ"},
        "C002": {"nome": "João Silva", "email": "joao@email.com", "tipo": "PF"},
    }

    processador = criar_processador(clientes_bd)

    print("=== Teste 1: fatura PJ acima de 5000 ===")
    fatura1 = processador.processar({
        "cli": "C001",
        "val": 8000,
        "it": ["Consultoria", "Suporte"]
    })
    print(f"Resultado: id={fatura1.id}, total=R$ {fatura1.valor_total:.2f}, status={fatura1.status}")
    print()

    print("=== Teste 2: fatura PF abaixo de 2000 ===")
    fatura2 = processador.processar({
        "cli": "C002",
        "val": 1500,
        "it": ["Produto A"]
    })
    print(f"Resultado: id={fatura2.id}, total=R$ {fatura2.valor_total:.2f}, status={fatura2.status}")
    print()

    print("=== Teste 3: reprocessar fatura ===")
    if fatura1:
        reprocessada = processador.reprocessar(fatura1.id)
        print(f"Reprocessado: id={reprocessada.id}, total=R$ {reprocessada.valor_total:.2f}, status={reprocessada.status}")
    print()
