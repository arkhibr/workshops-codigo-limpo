# Tutorial 09 — Padrões de Criação
> Referência: Gamma et al., *Design Patterns: Elements of Reusable Object-Oriented Software* (GoF), Cap. 3 — Creational Patterns

## 1. Contexto e Motivação

Criar objetos parece trivial — até o construtor acumular 10 parâmetros ou a função factory acumular 15 casos no `if/elif`. Dois sintomas clássicos:

**Construtor gordo:** um único objeto carrega campos para todos os subtipos possíveis, a maioria `None`/`null`. O chamador não sabe quais campos são obrigatórios; é possível criar objetos em estado inválido.

**if/elif de instanciação:** adicionar um novo subtipo exige abrir e alterar a função factory — viola o princípio Aberto/Fechado e cresce indefinidamente.

Os padrões de criação encapsulam *como* e *quando* os objetos são construídos, protegendo o restante do código dessas decisões.

---

## 2. Conceito Central

### Factory Method

Delega a decisão de qual classe instanciar para um registro ou método especializado, em vez de codificar um `if/elif`.

**❌ Sem Factory — acrescentar TED exige alterar esta função:**
```python
def criar_documento(tipo: str, dados: dict) -> DocumentoCobranca:
    if tipo == "boleto":
        return DocumentoCobranca(tipo="boleto", valor=dados["valor"], ...)
    elif tipo == "pix":
        return DocumentoCobranca(tipo="pix", valor=dados["valor"], ...)
    elif tipo == "nota_fiscal":
        ...
    else:
        raise ValueError(f"Tipo desconhecido: {tipo}")
```

**✅ Com Factory — adicionar TED é registrar uma linha:**
```python
class FabricaDocumento:
    _registro: Dict[str, type] = {}

    @classmethod
    def registrar(cls, tipo: str, classe: type) -> None:
        cls._registro[tipo] = classe

    @classmethod
    def criar(cls, tipo: str, **dados) -> DocumentoCobranca:
        if tipo not in cls._registro:
            disponiveis = ", ".join(sorted(cls._registro.keys()))
            raise ValueError(f"Tipo '{tipo}' não registrado. Disponíveis: {disponiveis}")
        return cls._registro[tipo](**dados)

FabricaDocumento.registrar("boleto",      Boleto)
FabricaDocumento.registrar("pix",         Pix)
FabricaDocumento.registrar("nota_fiscal", NotaFiscal)
# Para adicionar TED: uma linha abaixo, zero alterações acima.
```

**Quando aplicar:**
- O tipo do objeto é determinado em runtime (configuração, input do usuário, banco de dados).
- Novos subtipos são adicionados com frequência.
- A lógica de construção de cada subtipo é suficientemente distinta.

---

### Builder

Constrói um objeto complexo passo a passo, garantindo que campos obrigatórios sejam fornecidos antes de entregar o objeto pronto.

**❌ Sem Builder — 10 parâmetros, maioria opcional, objeto pode nascer inválido:**
```python
@dataclass
class DocumentoCobranca:
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
```

**✅ Com Builder — interface fluente, objeto só existe quando está completo:**
```python
boleto = (
    ConstruirBoleto()
    .com_valor(1500.0)
    .com_vencimento("2026-07-15")
    .com_beneficiario("CLI-100")
    .construir()          # lança ValueError se algum campo obrigatório faltar
)
```

O método `construir()` é a barreira: valida todos os campos antes de instanciar. Sem ele, não há objeto.

**Quando aplicar:**
- O objeto tem mais de 4 parâmetros no construtor, especialmente com muitos opcionais.
- É preciso garantir que o objeto nunca exista em estado inválido.
- A ordem de configuração é flexível (campos independentes entre si).

---

### Quando escolher Factory vs Builder?

| Situação | Padrão |
|---|---|
| Criar diferentes tipos polimórficos | Factory Method |
| Construir um objeto com muitos parâmetros opcionais | Builder |
| Adicionar novos tipos sem alterar código existente | Factory Method |
| Garantir que um objeto não seja criado incompleto | Builder |
| O tipo é decidido em runtime (config, banco, input) | Factory Method |
| A construção tem etapas sequenciais com validação | Builder |

Os dois padrões se combinam bem: a Factory pode usar um Builder internamente para montar objetos complexos.

---

## 3. Exercício

**Domínio:** geração de contratos (serviço, locação, fornecimento).

Arquivo: `exercicios/exercicio.py` (e equivalentes `.php`, `.ts`, `.tlpp`)

O código tem um dataclass `Contrato` com 9 campos e uma função `criar_contrato()` com `if/elif`. Sua tarefa:

1. Aplique **Factory Method**: crie `FabricaContrato` com `registrar()` e `criar()`.
2. Aplique **Builder**: crie `ConstruirContratoServico` com métodos fluentes e validação em `construir()`.

Solução: `exercicios/gabarito.py`.

---

## 4. Checklist

- [ ] Adicionar um novo tipo de documento exige alterar `criar_documento()`? Se sim → Factory Method.
- [ ] O construtor tem mais de 4 parâmetros, com maioria opcional? Se sim → Builder.
- [ ] É possível criar um objeto sem campos obrigatórios? Se sim → `Builder.construir()` com validação.
- [ ] O tipo do objeto é decidido em runtime? Se sim → Factory Method com registro.
- [ ] Criar objetos inválidos gera bugs silenciosos? Se sim → Builder como barreira.

---

## 5. Referências

- Gamma, E. et al. *Design Patterns: Elements of Reusable Object-Oriented Software* (GoF). Addison-Wesley, 1994.
  - Factory Method: Cap. 3, p. 107.
  - Builder: Cap. 3, p. 97.
- Python docs: [`abc.ABC`](https://docs.python.org/3/library/abc.html), [`abc.abstractmethod`](https://docs.python.org/3/library/abc.html#abc.abstractmethod).
- PHP 8.1: [match expression](https://www.php.net/manual/en/control-structures.match.php), [readonly properties](https://www.php.net/manual/en/language.oop5.properties.php#language.oop5.properties.readonly-properties).
- TypeScript: [Abstract Classes](https://www.typescriptlang.org/docs/handbook/2/classes.html#abstract-classes-and-members), [Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map).
