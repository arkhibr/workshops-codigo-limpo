# Tutorial 18 — Padrões Estruturais: Adapter e Facade

> Referência: Gamma et al., *Design Patterns: Elements of Reusable Object-Oriented Software* (GoF), Cap. 4 — Structural Patterns

## 1. Contexto e Motivação

Todo sistema de médio porte integra APIs que não controlamos: ERPs, gateways de pagamento, bibliotecas legadas. O problema não é a integração em si — é quando o código de negócio conhece os detalhes dessas APIs. Cada mudança de versão, cada renomeação de campo, cada troca de fornecedor propaga efeitos por todo o código.

Padrões estruturais organizam como classes e objetos se compõem. **Adapter** e **Facade** resolvem dois problemas distintos de integração: incompatibilidade de interfaces e complexidade de subsistemas.

## 2. Conceito Central

### Adapter — quando a API não pode mudar

O Adapter converte a interface de uma classe em outra que o cliente espera. É o "tradutor" entre dois mundos que não foram projetados para conversar.

**❌ Sem Adapter — nomenclatura ADVPL exposta no código de negócio:**

```python
def registrar_pedido(cliente_id: str, produto_id: str, quantidade: int) -> str:
    erp_buscar_cliente(cliente_id)   # chama ERP diretamente
    nro = erp_salvar_pedido({
        "cNroPedido":  "PED-TEMP",   # campo ADVPL no código de negócio
        "nCodCliente": int(cliente_id.split("-")[1]),
        "cCodProduto": produto_id,
        "nQtdPedida":  quantidade,
    })
    erp_atualizar_estoque(produto_id, -quantidade)
    return nro
```

**✅ Com Adapter — código de negócio fala o idioma do domínio:**

```python
class ERPPedidoAdapter:
    def salvar(self, cliente_id: str, produto_id: str, quantidade: int) -> str:
        return erp_salvar_pedido({        # tradução concentrada aqui
            "cNroPedido":  "PED-TEMP",
            "nCodCliente": int(cliente_id.split("-")[1]),
            "cCodProduto": produto_id,
            "nQtdPedida":  quantidade,
        })

# Código de negócio agora fala o idioma do domínio:
nro = adapter.salvar(cliente_id, produto_id, quantidade)
```

> **Caso especial ADVPL:** O Adapter é o padrão mais valioso em integrações com Protheus.
> Isolando User Functions (U_*) do restante da lógica, upgrades de versão do ERP
> (ex: P12 → P12.1.33) impactam apenas os adapters — não o código de negócio.

**Quando aplicar Adapter:**
- A API externa usa convenções de nomenclatura incompatíveis com o domínio
- Você quer proteger o código de negócio de mudanças na API externa
- A mesma lógica de tradução se repete em múltiplos pontos

### Facade — quando o subsistema é complexo

A Facade fornece uma interface simplificada para um subsistema complexo. O chamador não precisa conhecer a sequência de etapas — apenas os dados que precisa fornecer.

**❌ Sem Facade — chamador orquestra 5 etapas:**

```python
def processar_pedido_completo(cliente_id, produto_id, qtd):
    # Quem chama deve conhecer TODA a sequência:
    cliente    = buscar_dados_cliente(cliente_id)
    nro_pedido = registrar_pedido(cliente_id, produto_id, qtd)
    nf         = emitir_nota_fiscal(nro_pedido)
    enviar_email(cliente["email"], nro_pedido)
    atualizar_dashboard(nro_pedido)
```

**✅ Com Facade — uma chamada, sem conhecer os subsistemas:**

```python
class FachadaProcessamentoPedido:
    def processar(self, cliente_id, produto_id, quantidade) -> ResultadoPedido:
        cliente    = self._repo_cliente.buscar(cliente_id)
        nro_pedido = self._repo_pedido.salvar(cliente_id, produto_id, quantidade)
        self._repo_pedido.atualizar_estoque(produto_id, quantidade)
        nf = self._repo_pedido.gerar_nota_fiscal(nro_pedido)
        ...
        return ResultadoPedido(nro_pedido, nf, cliente.nome)

# Chamador não conhece ERP, adapters ou sequência:
resultado = fachada.processar("CLI-100", "PROD-001", 5)
```

**Quando aplicar Facade:**
- A mesma sequência de chamadas se repete em vários pontos do código
- Quem chama não deveria precisar conhecer os subsistemas internos
- O subsistema tem muitas classes ou passos difíceis de memorizar

### Adapter vs Facade — quando usar cada um?

| Situação | Padrão |
|---|---|
| API externa não pode ser alterada | Adapter |
| Você controla ambos os lados | Nenhum — refatore diretamente |
| Subsistema com muitos passos | Facade |
| Apenas 1-2 chamadas ao subsistema | Nenhum — chame diretamente |
| Integração com ERP/sistema legado | Adapter |
| Orquestrar múltiplos adapters | Facade + Adapter |

## 3. Exercício

**Domínio:** sistema de boletos bancários com API legada inconsistente.

As funções `gerar_boleto_legado`, `consultar_status_legado` e `cancelar_boleto_legado` usam nomenclatura inconsistente (`nIdBoleto`, `cStatusBoleto`, etc.) e o código de negócio as chama diretamente em três pontos diferentes.

**Sua tarefa:**
1. Crie um `Adapter` que isole o sistema legado: normalize os campos e encapsule os detalhes de nomenclatura.
2. Crie uma `Facade` que simplifique o fluxo completo (emitir + consultar + cancelar) em uma única chamada.

Arquivos: `exercicios/exercicio.py` (e equivalentes `.php`, `.ts`, `.tlpp`)
Solução: `exercicios/gabarito.py` (e equivalentes)

## 4. Checklist

- [ ] O código de negócio conhece a nomenclatura da API externa? (→ Adapter)
- [ ] Alterar a versão do ERP/biblioteca quebraria múltiplos pontos? (→ Adapter)
- [ ] Quem chama precisa saber a sequência de passos do subsistema? (→ Facade)
- [ ] A mesma sequência de chamadas se repete em vários lugares? (→ Facade)

## 5. Referências

- Gamma, E. et al. *Design Patterns* (GoF). Cap. 4: Adapter (p. 139), Facade (p. 185).
- Feathers, Michael. *Working Effectively with Legacy Code*. Cap. 3 — Sensing and Separation.
