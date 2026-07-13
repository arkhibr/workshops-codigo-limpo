"""
massa_bons.py — Test Data Builder, Factory com Faker e teste baseado em propriedade.
Execute: pytest massa_bons.py -v
"""
from dataclasses import dataclass, field
import factory
from faker import Faker
from hypothesis import given, strategies as st

fake = Faker("pt_BR")


@dataclass
class Pedido:
    id: str = "P000"
    itens: list = field(default_factory=lambda: [{"produto": "Item Padrão", "preco": 100.0, "quantidade": 1}])
    cupom_desconto: str = None
    status: str = "pendente"


class PedidoBuilder:
    """Test Data Builder: valores padrão sensatos, sobrescreve só o relevante."""

    def __init__(self):
        self._pedido = Pedido()

    def com_item(self, produto: str, preco: float, quantidade: int = 1) -> "PedidoBuilder":
        self._pedido.itens = [{"produto": produto, "preco": preco, "quantidade": quantidade}]
        return self

    def com_cupom(self, codigo: str) -> "PedidoBuilder":
        self._pedido.cupom_desconto = codigo
        return self

    def construir(self) -> Pedido:
        return self._pedido


def aplicar_cupom(pedido: Pedido, codigo) -> Pedido:
    if codigo == "PROMO10":
        for item in pedido.itens:
            item["preco"] = round(item["preco"] * 0.9, 2)
    return pedido


class ClienteFactory(factory.Factory):
    class Meta:
        model = dict

    nome = factory.LazyFunction(fake.name)
    email = factory.LazyFunction(fake.email)
    cpf = factory.LazyFunction(fake.cpf)


def test_cupom_aplica_10_por_cento_de_desconto():
    pedido = PedidoBuilder().com_item("Notebook", preco=3000.0).com_cupom("PROMO10").construir()
    resultado = aplicar_cupom(pedido, "PROMO10")
    assert resultado.itens[0]["preco"] == 2700.0


def test_pedido_sem_cupom_mantem_preco_original():
    pedido = PedidoBuilder().com_item("Notebook", preco=3000.0).construir()
    resultado = aplicar_cupom(pedido, None)
    assert resultado.itens[0]["preco"] == 3000.0


def test_cliente_gerado_pela_factory_tem_email_valido():
    cliente = ClienteFactory()
    assert "@" in cliente["email"]


@given(st.floats(min_value=0, max_value=100_000, allow_nan=False, allow_infinity=False))
def test_aplicar_cupom_nunca_gera_preco_negativo(preco):
    pedido = PedidoBuilder().com_item("Item", preco=preco).com_cupom("PROMO10").construir()
    resultado = aplicar_cupom(pedido, "PROMO10")
    assert resultado.itens[0]["preco"] >= 0
