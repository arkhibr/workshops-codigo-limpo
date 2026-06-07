# Gabarito — Code Review Orientado a Padrões

## Violação 1 — God Object (SRP)
**Localização:** `class GestorCobranca` (12 métodos: `validar_cpf`, `buscar_cliente`, `criar_cobranca`, `calcular_desconto`, `processar_pagamento`, `enviar_email`, `gerar_boleto`, `arquivar`, `gerar_relatorio`, `exportar_csv`, `atualizar_status`, `reprocessar_falha`, `consultar_historico`)
**Problema:** Uma classe gerencia validação de CPF, busca de cliente, criação de cobrança, cálculo de desconto, envio de email, geração de boleto, arquivamento, relatório, CSV, status, reprocessamento e histórico. Qualquer mudança em qualquer uma dessas responsabilidades toca a mesma classe.
**Padrão recomendado:** SRP — separar em `RepositorioCobranca`, `ServicoNotificacao`, `CalculadorDesconto`, `GeradorRelatorio`
**Correção (fragmento):**
```python
class RepositorioCobranca:
    def criar(self, cobranca: Cobranca) -> None: ...
    def arquivar(self, cobranca_id: str) -> None: ...
    def atualizar_status(self, cobranca_id: str, status: str) -> None: ...

class ServicoNotificacao:
    def __init__(self, notificador: INotificador) -> None: ...
    def notificar_cobranca(self, cliente: Cliente, cobranca: Cobranca) -> None: ...
```

## Violação 2 — Magic Strings
**Localização:** `cobranca.tipo == "B"`, `cliente.nivel_fidelidade == "O"`, `cliente.nivel_fidelidade == "P"`, `cobranca.tipo == "C"`
**Problema:** "B", "P", "C", "O" não têm significado sem contexto. Buscar "B" no código retorna falsos positivos.
**Padrão recomendado:** `enum TipoCobranca(str, Enum)`, `enum NivelFidelidade(str, Enum)`
**Correção:**
```python
from enum import Enum

class TipoCobranca(str, Enum):
    BOLETO  = "boleto"
    PIX     = "pix"
    CARTAO  = "cartao"

class NivelFidelidade(str, Enum):
    BRONZE = "bronze"
    PRATA  = "prata"
    OURO   = "ouro"
```

## Violação 3 — Feature Envy
**Localização:** `Cobranca.calcular_desconto_fidelidade(cliente)` acessa `cliente.nivel_fidelidade`, `cliente.pontos`, `cliente.historico_compras`
**Problema:** O método sabe mais sobre `Cliente` do que sobre `Cobranca`. Princípio: mova o método para onde os dados vivem.
**Padrão recomendado:** mover `calcular_desconto_fidelidade()` para `Cliente`
**Correção:**
```python
@dataclass
class Cliente:
    ...
    def calcular_desconto_fidelidade(self) -> float:
        if self.nivel_fidelidade == NivelFidelidade.OURO:
            return min(self.historico_compras * 0.03 + self.pontos * 0.002, 150.0)
        elif self.nivel_fidelidade == NivelFidelidade.PRATA:
            return min(self.pontos * 0.001, 50.0)
        return 0.0
```

## Violação 4 — Missing Strategy (if/elif de algoritmo)
**Localização:** `processar_pagamento()` — if/elif para "B"/"P"/"C"
**Problema:** Adicionar "TED" exige alterar `processar_pagamento()`. Viola OCP.
**Padrão recomendado:** Strategy — `Protocol EstrategiaCobranca` + `ProcessadorBoleto`, `ProcessadorPix`, `ProcessadorCartao`
**Correção (fragmento):**
```python
class EstrategiaCobranca(Protocol):
    def processar(self, cobranca: Cobranca) -> dict: ...

class ProcessadorBoleto:
    def processar(self, cobranca: Cobranca) -> dict:
        boleto = BoletoSimples(f"BOL-{cobranca.id}", cobranca.valor, "2026-07-31")
        if not boleto.validar_vencimento():
            raise ValueError("Boleto vencido")
        return {"metodo": "boleto", "codigo": boleto.numero}
```

## Violação 5 — DIP violation
**Localização:** `GestorCobranca.__init__` — `self.notificador = SmtpEmailSender()`, `self.banco = BancoDadosPostgres()`
**Problema:** `GestorCobranca` depende de implementações concretas. Impossível testar sem SMTP real e PostgreSQL real.
**Padrão recomendado:** DIP — injetar `INotificador` e `IRepositorio` no construtor
**Correção:**
```python
class GestorCobranca:
    def __init__(self, notificador: INotificador, banco: IRepositorioCobranca) -> None:
        self._notificador = notificador
        self._banco       = banco
```

## Violação 6 — Copy-paste (DRY)
**Localização:** `BoletoSimples.validar_vencimento()` e `BoletoParcelado.validar_vencimento()` — código byte-a-byte idêntico
**Problema:** Corrigir um bug de validação (ex: fuso horário) exige alterar dois lugares independentemente.
**Padrão recomendado:** extrair `_validar_data_vencimento(vencimento: str) -> bool` como função livre, ou Template Method via herança
**Correção:**
```python
def _validar_data_vencimento(vencimento: str) -> bool:
    partes = vencimento.split("-")
    if len(partes) != 3:
        return False
    ano, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
    return date(ano, mes, dia) >= date.today()

@dataclass
class BoletoSimples:
    ...
    def validar_vencimento(self) -> bool:
        return _validar_data_vencimento(self.vencimento)
```

## Pontuação
- 6/6 violações: excelente
- 4–5/6: bom
- 2–3/6: revisitar T19 (Anti-patterns) e T16–T21 (padrões)
- 0–1/6: rever o tutorial do zero
