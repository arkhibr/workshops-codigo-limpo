"""
solid_bons.py — Os 5 princípios SOLID aplicados ao módulo de pedidos.
Cada seção demonstra um princípio com implementação completa e executável.
Execute: python3 solid_bons.py
"""
from typing import List, Optional, Protocol, runtime_checkable
from dataclasses import dataclass, field


# ──────────────────────────────────────────────
# DOMÍNIO COMPARTILHADO
# ──────────────────────────────────────────────

@dataclass
class ItemPedido:
    produto_id: str
    descricao:  str
    preco:      float
    quantidade: int

@dataclass
class Pedido:
    id:         str
    cliente_id: str
    itens:      List[ItemPedido]
    status:     str = "pendente"

    def confirmar(self) -> None:
        self.status = "confirmado"


# ══════════════════════════════════════════════
# S — SRP: UMA CLASSE, UMA RESPONSABILIDADE
# Cada classe tem exatamente um motivo para mudar.
# ══════════════════════════════════════════════

class ValidadorPedido:
    """Responsável apenas por regras de validação de negócio."""

    def validar(self, pedido: Pedido) -> bool:
        if not pedido.itens:
            print(f"  [Validação] Pedido {pedido.id}: sem itens")
            return False
        if not pedido.cliente_id:
            print(f"  [Validação] Pedido {pedido.id}: cliente ausente")
            return False
        if any(i.preco <= 0 for i in pedido.itens):
            print(f"  [Validação] Pedido {pedido.id}: item com preço inválido")
            return False
        if any(i.quantidade <= 0 for i in pedido.itens):
            print(f"  [Validação] Pedido {pedido.id}: item com quantidade inválida")
            return False
        return True


class CalculadorTotal:
    """Responsável apenas por cálculo financeiro."""

    TAXA_IMPOSTO = 0.10

    def calcular(self, pedido: Pedido) -> float:
        subtotal = sum(i.preco * i.quantidade for i in pedido.itens)
        return round(subtotal * (1 + self.TAXA_IMPOSTO), 2)

    def calcular_imposto(self, pedido: Pedido) -> float:
        subtotal = sum(i.preco * i.quantidade for i in pedido.itens)
        return round(subtotal * self.TAXA_IMPOSTO, 2)

    def calcular_subtotal(self, pedido: Pedido) -> float:
        return round(sum(i.preco * i.quantidade for i in pedido.itens), 2)


class RepositorioPedido:
    """Responsável apenas por persistência."""

    def __init__(self) -> None:
        self._dados: dict = {}

    def salvar(self, pedido: Pedido) -> None:
        self._dados[pedido.id] = {
            "id":      pedido.id,
            "status":  pedido.status,
            "cliente": pedido.cliente_id,
            "itens":   len(pedido.itens),
        }
        print(f"  [BD] salvo: {pedido.id} → {pedido.status}")

    def buscar(self, pedido_id: str) -> Optional[dict]:
        return self._dados.get(pedido_id)

    def listar_por_status(self, status: str) -> list:
        return [d for d in self._dados.values() if d["status"] == status]


class NotificadorEmail:
    """Responsável apenas por envio de e-mail."""

    def notificar(self, destinatario: str, mensagem: str) -> None:
        print(f"  [Email] → {destinatario}: {mensagem}")


# ══════════════════════════════════════════════
# O — OCP: ABERTO PARA EXTENSÃO, FECHADO PARA MODIFICAÇÃO
# Novos formatadores são adicionados sem alterar GeradorRelatorio.
# ══════════════════════════════════════════════

@runtime_checkable
class Formatador(Protocol):
    def formatar(self, pedido: "Pedido", total: float) -> str: ...


class FormatadorVendas:
    def formatar(self, pedido: Pedido, total: float) -> str:
        itens_str = ", ".join(
            f"{i.descricao} x{i.quantidade}" for i in pedido.itens
        )
        return (
            f"[Vendas] Pedido {pedido.id} | Cliente: {pedido.cliente_id} | "
            f"Itens: {itens_str} | Total: R${total:.2f}"
        )


class FormatadorFinanceiro:
    def formatar(self, pedido: Pedido, total: float) -> str:
        calc = CalculadorTotal()
        subtotal = calc.calcular_subtotal(pedido)
        imposto  = calc.calcular_imposto(pedido)
        return (
            f"[Financeiro] Pedido {pedido.id} | "
            f"Subtotal: R${subtotal:.2f} | Imposto: R${imposto:.2f} | Total: R${total:.2f}"
        )


class FormatadorEstoque:
    # Adicionado sem nenhuma alteração em GeradorRelatorio — OCP respeitado
    def formatar(self, pedido: Pedido, total: float) -> str:
        linhas = [f"  • {i.descricao} (ref: {i.produto_id}): {i.quantidade} un" for i in pedido.itens]
        return f"[Estoque] Pedido {pedido.id} — movimentação:\n" + "\n".join(linhas)


class FormatadorNFe:
    # Segundo tipo adicionado — ainda sem alterar GeradorRelatorio
    def formatar(self, pedido: Pedido, total: float) -> str:
        return (
            f"[NF-e] DANFE | Emitente: Loja XYZ | Destinatário: {pedido.cliente_id} | "
            f"Nr. Pedido: {pedido.id} | Valor: R${total:.2f} | Chave: 0000-0000-{pedido.id}"
        )


# ══════════════════════════════════════════════
# L — LSP: SUBCLASSES HONRAM O CONTRATO DA BASE
# Qualquer subtipo pode substituir Pedido sem surpresas em runtime.
# ══════════════════════════════════════════════

class PedidoAmostra(Pedido):
    """Amostra: confirma normalmente (contrato mantido) + comportamento próprio."""

    def calcular_total_especial(self) -> float:
        return 0.0  # amostras têm custo zero para o cliente

    # confirmar() herdado sem alteração — pós-condição da base garantida


class PedidoPrioritario(Pedido):
    """Pedido prioritário: honra confirmar() e adiciona lógica de fila."""

    def __init__(self, *args, prioridade: int = 1, **kwargs):
        super().__init__(*args, **kwargs)
        self.prioridade = prioridade

    def confirmar(self) -> None:
        super().confirmar()   # honra o contrato: self.status = "confirmado"
        print(f"  [Fila] Pedido {self.id} inserido na fila com prioridade {self.prioridade}")


def confirmar_e_exibir(pedido: Pedido) -> None:
    """Aceita qualquer subtipo de Pedido — funciona com todos."""
    pedido.confirmar()
    assert pedido.status == "confirmado", "Contrato violado: status deve ser 'confirmado'"
    print(f"  {pedido.__class__.__name__} {pedido.id} → status: {pedido.status}")


# ══════════════════════════════════════════════
# I — ISP: INTERFACES PEQUENAS E COESAS
# Clientes implementam apenas o que precisam — sem métodos mortos.
# ══════════════════════════════════════════════

@runtime_checkable
class Validavel(Protocol):
    def validar(self) -> bool: ...

@runtime_checkable
class Calculavel(Protocol):
    def calcular(self) -> float: ...

@runtime_checkable
class Arquivavel(Protocol):
    def arquivar(self) -> None: ...
    def exportar_csv(self) -> str: ...

@runtime_checkable
class ExportavelEmPDF(Protocol):
    def exportar_pdf(self) -> bytes: ...


class ProcessadorSimples:
    """Só precisa de validar e calcular — implementa Validavel e Calculavel.
    Sem métodos mortos, sem exportar_csv/pdf que nunca serão chamados."""

    def __init__(self, pedido: Pedido) -> None:
        self._pedido = pedido

    def validar(self) -> bool:
        return bool(self._pedido.itens) and bool(self._pedido.cliente_id)

    def calcular(self) -> float:
        return round(sum(i.preco * i.quantidade for i in self._pedido.itens), 2)


class ProcessadorCompleto:
    """Exportador completo — implementa todas as interfaces necessárias."""

    def __init__(self, pedido: Pedido) -> None:
        self._pedido = pedido

    def validar(self) -> bool:
        return bool(self._pedido.itens) and bool(self._pedido.cliente_id)

    def calcular(self) -> float:
        return round(sum(i.preco * i.quantidade for i in self._pedido.itens), 2)

    def arquivar(self) -> None:
        print(f"  [Arquivo] Pedido {self._pedido.id} arquivado em storage frio")

    def exportar_csv(self) -> str:
        linhas = ["produto_id,descricao,preco,quantidade"]
        for i in self._pedido.itens:
            linhas.append(f"{i.produto_id},{i.descricao},{i.preco},{i.quantidade}")
        return "\n".join(linhas)

    def exportar_pdf(self) -> bytes:
        conteudo = (
            f"PEDIDO {self._pedido.id}\n"
            f"Cliente: {self._pedido.cliente_id}\n"
            f"Status: {self._pedido.status}\n"
            + "\n".join(
                f"  {i.descricao}: {i.quantidade} x R${i.preco:.2f}"
                for i in self._pedido.itens
            )
        )
        return conteudo.encode("utf-8")


# ══════════════════════════════════════════════
# D — DIP: DEPENDER DE ABSTRAÇÕES, NÃO DE CONCRETOS
# GeradorRelatorio recebe todas as dependências via construtor.
# Trocar Email por Log não exige alterar GeradorRelatorio.
# ══════════════════════════════════════════════

@runtime_checkable
class RepositorioDePedido(Protocol):
    def salvar(self, pedido: "Pedido") -> None: ...
    def buscar(self, pedido_id: str) -> Optional[dict]: ...

@runtime_checkable
class Notificador(Protocol):
    def notificar(self, destinatario: str, mensagem: str) -> None: ...


class NotificadorLog:
    """Alternativa a NotificadorEmail — mesma interface, sem SMTP."""

    def notificar(self, destinatario: str, mensagem: str) -> None:
        print(f"  [Log] {destinatario}: {mensagem}")


class RepositorioEmMemoria:
    """Implementação de teste — sem banco de dados real."""

    def __init__(self) -> None:
        self._dados: dict = {}

    def salvar(self, pedido: Pedido) -> None:
        self._dados[pedido.id] = {"id": pedido.id, "status": pedido.status}
        print(f"  [Mem] salvo: {pedido.id} → {pedido.status}")

    def buscar(self, pedido_id: str) -> Optional[dict]:
        return self._dados.get(pedido_id)


class GeradorRelatorio:
    """Módulo de alto nível — depende apenas de abstrações injetadas no construtor.
    Para adicionar suporte a SMS, basta criar NotificadorSms sem tocar aqui."""

    def __init__(
        self,
        repo:        RepositorioDePedido,
        notificador: Notificador,
        formatador:  Formatador,
        calculador:  CalculadorTotal,
    ) -> None:
        self._repo        = repo
        self._notificador = notificador
        self._formatador  = formatador
        self._calculador  = calculador

    def processar(self, pedido: Pedido) -> str:
        total = self._calculador.calcular(pedido)
        self._repo.salvar(pedido)
        self._notificador.notificar(
            pedido.cliente_id,
            f"Pedido {pedido.id} processado. Total: R${total:.2f}"
        )
        return self._formatador.formatar(pedido, total)


# ──────────────────────────────────────────────
# DEMONSTRAÇÃO
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=== SOLID _bons — 5 princípios aplicados ===\n")

    itens  = [
        ItemPedido("P001", "Webcam HD",  299.90, 1),
        ItemPedido("P002", "Cabo USB-C",  49.90, 2),
    ]
    pedido = Pedido("PED-001", "CLI-100", itens)

    # ── S — SRP ──────────────────────────────────────────────────
    print("── S — SRP: cada classe tem uma responsabilidade ──────")
    validador  = ValidadorPedido()
    calculador = CalculadorTotal()
    repo_real  = RepositorioPedido()
    notif_email = NotificadorEmail()

    print(f"  Válido: {validador.validar(pedido)}")
    print(f"  Subtotal: R${calculador.calcular_subtotal(pedido):.2f}")
    print(f"  Imposto:  R${calculador.calcular_imposto(pedido):.2f}")
    print(f"  Total:    R${calculador.calcular(pedido):.2f}")
    repo_real.salvar(pedido)
    notif_email.notificar(pedido.cliente_id, f"Pedido {pedido.id} registrado")
    buscado = repo_real.buscar(pedido.id)
    print(f"  Busca por ID: {buscado}")

    # ── O — OCP ──────────────────────────────────────────────────
    print("\n── O — OCP: novos formatadores sem alterar GeradorRelatorio ──")
    repo_mem = RepositorioEmMemoria()
    notif_log = NotificadorLog()
    calc = CalculadorTotal()
    for fmt_cls, nome in [
        (FormatadorVendas,     "vendas"),
        (FormatadorFinanceiro, "financeiro"),
        (FormatadorEstoque,    "estoque"),
        (FormatadorNFe,        "nfe"),
    ]:
        gerador = GeradorRelatorio(repo_mem, notif_log, fmt_cls(), calc)
        print(f"\n  [{nome}] {gerador.processar(pedido)}")

    # ── L — LSP ──────────────────────────────────────────────────
    print("\n── L — LSP: todos os subtipos honram o contrato de Pedido ──")
    casos = [
        Pedido("PED-002", "CLI-200", itens),
        PedidoAmostra("PED-003", "CLI-300", itens),
        PedidoPrioritario("PED-004", "CLI-400", itens, prioridade=3),
    ]
    for p in casos:
        confirmar_e_exibir(p)

    # ── I — ISP ──────────────────────────────────────────────────
    print("\n── I — ISP: ProcessadorSimples usa 2 interfaces, sem métodos mortos ──")
    simples = ProcessadorSimples(pedido)
    print(f"  validar={simples.validar()}, calcular=R${simples.calcular():.2f}")
    assert isinstance(simples, Validavel)
    assert isinstance(simples, Calculavel)
    # simples não implementa Arquivavel nem ExportavelEmPDF — zero código morto

    completo = ProcessadorCompleto(pedido)
    completo.arquivar()
    print(f"  CSV:\n{completo.exportar_csv()}")
    print(f"  PDF ({len(completo.exportar_pdf())}B): {completo.exportar_pdf()[:40]}...")

    # ── D — DIP ──────────────────────────────────────────────────
    print("\n── D — DIP: trocar Email por Log sem alterar GeradorRelatorio ──")
    gerador_prod  = GeradorRelatorio(repo_real,            notif_email, FormatadorVendas(), calc)
    gerador_teste = GeradorRelatorio(RepositorioEmMemoria(), NotificadorLog(), FormatadorVendas(), calc)

    print("  [Produção]:")
    print(f"    {gerador_prod.processar(pedido)}")
    print("  [Teste com mocks]:")
    print(f"    {gerador_teste.processar(pedido)}")
