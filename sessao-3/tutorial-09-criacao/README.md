# Tutorial 09 — Padrões de Criação

> Referência: Gamma et al., *Design Patterns: Elements of Reusable Object-Oriented Software* (GoF), Cap. 3 — Creational Patterns

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/52200c2e-a677-471a-9bb9-bc1dfed92a7e" />

---

## 1. Contexto e Motivação

Criar objetos parece trivial — até o construtor acumular 10 parâmetros ou a função factory acumular 15 casos no `if/elif`. Dois sintomas clássicos indicam que a criação de objetos precisa de estrutura:

**Construtor gordo:** um único tipo carrega campos para todos os subtipos possíveis, a maioria `None`/`null`. O chamador não sabe quais campos são obrigatórios para qual subtipo; é possível criar objetos em estado inválido sem nenhuma mensagem de erro.

**`if/elif` de instanciação:** adicionar um novo subtipo exige abrir e alterar a função factory existente — viola o OCP (tutorial-08) e cresce indefinidamente a cada nova demanda.

Os padrões de criação encapsulam *como* e *quando* os objetos são construídos, protegendo o restante do código dessas decisões e mantendo a compatibilidade com SOLID.

> **Conexão com o tutorial-08:** Factory Method resolve a violação de OCP na instanciação. Builder resolve a violação de SRP quando um construtor acumula lógica de validação de múltiplos subtipos.

---

## 2. Factory Method — extensão sem modificação

### O problema

```python
def criar_documento(tipo: str, dados: dict) -> DocumentoCobranca:
    if tipo == "boleto":
        return DocumentoCobranca(tipo="boleto", valor=dados["valor"],
                                  codigo_barras=dados.get("codigo_barras", "..."))
    elif tipo == "pix":
        return DocumentoCobranca(tipo="pix", valor=dados["valor"],
                                  chave_pix=dados.get("chave_pix", "..."))
    elif tipo == "nota_fiscal":
        return DocumentoCobranca(tipo="nota_fiscal", valor=dados["valor"],
                                  numero_nf=dados.get("numero_nf", "..."), cfop=...)
    # próxima demanda (TED, débito automático): abrir esta função novamente
    else:
        raise ValueError(f"Tipo desconhecido: {tipo}")
```

Cada nova forma de pagamento exige reabrir a função. Com 10 tipos, esse bloco se torna um ponto de mudança permanente.

### A solução

```python
from abc import ABC, abstractmethod

class DocumentoCobranca(ABC):
    def __init__(self, valor: float, vencimento: str, beneficiario: str) -> None:
        if valor <= 0:
            raise ValueError(f"Valor deve ser positivo: {valor}")
        self.valor        = valor
        self.vencimento   = vencimento
        self.beneficiario = beneficiario

    @abstractmethod
    def descricao(self) -> str: ...


class Boleto(DocumentoCobranca):
    def __init__(self, valor: float, vencimento: str, beneficiario: str,
                 codigo_barras: str) -> None:
        super().__init__(valor, vencimento, beneficiario)
        self.codigo_barras = codigo_barras

    def descricao(self) -> str:
        return f"Boleto R${self.valor:.2f} venc {self.vencimento} | {self.codigo_barras}"


class Pix(DocumentoCobranca):
    def __init__(self, valor: float, vencimento: str, beneficiario: str,
                 chave_pix: str) -> None:
        super().__init__(valor, vencimento, beneficiario)
        self.chave_pix = chave_pix

    def descricao(self) -> str:
        return f"Pix R${self.valor:.2f} venc {self.vencimento} → {self.chave_pix}"


class FabricaDocumento:
    _registro: dict[str, type] = {}

    @classmethod
    def registrar(cls, tipo: str, classe: type) -> None:
        cls._registro[tipo] = classe       # extensão: registrar uma linha

    @classmethod
    def criar(cls, tipo: str, **dados) -> DocumentoCobranca:
        if tipo not in cls._registro:
            disponiveis = ", ".join(sorted(cls._registro.keys()))
            raise ValueError(f"Tipo '{tipo}' não registrado. Disponíveis: {disponiveis}")
        return cls._registro[tipo](**dados)


FabricaDocumento.registrar("boleto",      Boleto)
FabricaDocumento.registrar("pix",         Pix)
FabricaDocumento.registrar("nota_fiscal", NotaFiscal)
# TED: FabricaDocumento.registrar("ted", Ted) — uma linha, zero alterações acima
```

**Por que funciona:** o `if/elif` é substituído por um dicionário. Adicionar um tipo é escrever uma linha de `registrar()`, não abrir e modificar a lógica existente.

### Quando aplicar

- O tipo do objeto é determinado em runtime (configuração, input do usuário, banco de dados)
- Novos subtipos são adicionados com frequência
- A lógica de construção de cada subtipo é suficientemente distinta

---

> **📝 Reflita:** No seu código atual, existe alguma função factory com `if/elif` por tipo? Quantas vezes por mês alguém a abre para adicionar um novo caso? Com quantos `elif` ela termina o ano?

---

## 3. Builder — objeto só existe quando está completo

### O problema

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

O chamador pode criar um `DocumentoCobranca` com `tipo="boleto"` sem fornecer `codigo_barras`, ou um `tipo="pix"` sem `chave_pix` — e o código compila sem aviso. O objeto nasce inválido e o bug só aparece quando alguém tenta usá-lo.

### A solução

```python
class ConstruirBoleto:
    def __init__(self) -> None:
        self._valor:         Optional[float] = None
        self._vencimento:    Optional[str]   = None
        self._beneficiario:  Optional[str]   = None
        self._codigo_barras: str             = "0000.00000 00000.000000"

    def com_valor(self, valor: float) -> "ConstruirBoleto":
        self._valor = valor
        return self                          # retorna self para encadeamento fluente

    def com_vencimento(self, vencimento: str) -> "ConstruirBoleto":
        self._vencimento = vencimento
        return self

    def com_beneficiario(self, beneficiario: str) -> "ConstruirBoleto":
        self._beneficiario = beneficiario
        return self

    def com_codigo_barras(self, codigo: str) -> "ConstruirBoleto":
        self._codigo_barras = codigo
        return self

    def construir(self) -> Boleto:
        """Barreira: valida campos obrigatórios antes de criar o objeto."""
        if self._valor is None:
            raise ValueError("valor é obrigatório")
        if self._vencimento is None:
            raise ValueError("vencimento é obrigatório")
        if self._beneficiario is None:
            raise ValueError("beneficiario é obrigatório")
        return Boleto(self._valor, self._vencimento, self._beneficiario,
                      self._codigo_barras)
```

Uso com encadeamento fluente:

```python
boleto = (
    ConstruirBoleto()
    .com_valor(1500.0)
    .com_vencimento("2026-07-15")
    .com_beneficiario("CLI-100")
    .com_codigo_barras("1234.56789 00000.000000")
    .construir()              # lança ValueError se algum campo obrigatório faltar
)
```

Sem chamar `.construir()`, o objeto não existe. Não há como criar um `Boleto` incompleto.

### Builder por tipo

O padrão se replica para cada tipo de documento com seus próprios campos obrigatórios:

```python
class ConstruirPix:
    def com_valor(self, valor: float) -> "ConstruirPix": ...
    def com_vencimento(self, v: str) -> "ConstruirPix": ...
    def com_beneficiario(self, b: str) -> "ConstruirPix": ...
    def com_chave_pix(self, chave: str) -> "ConstruirPix": ...

    def construir(self) -> Pix:
        if self._chave_pix is None:
            raise ValueError("chave_pix é obrigatória")
        ...
```

### Quando aplicar

- O objeto tem mais de 4 parâmetros no construtor, especialmente com muitos opcionais
- Campos obrigatórios variam por subtipo
- A ordem de configuração é flexível (campos independentes entre si)
- Objetos inválidos causam bugs silenciosos em runtime

### Factory vs. Builder

| Situação | Padrão |
|---|---|
| Criar diferentes tipos polimórficos | Factory Method |
| Construir um objeto com muitos parâmetros opcionais | Builder |
| Adicionar novos tipos sem alterar código existente | Factory Method |
| Garantir que o objeto nunca exista em estado inválido | Builder |
| O tipo é decidido em runtime (config, banco, input) | Factory Method |
| A construção tem etapas sequenciais com validação | Builder |

Os dois padrões se combinam: a Factory pode usar um Builder internamente para montar objetos complexos — cada `FabricaDocumento.criar("boleto", ...)` poderia chamar `ConstruirBoleto().com_valor(...).construir()`.

---

> **📝 Reflita:** Existe algum dataclass ou struct no seu código com mais de 4 campos `Optional`? Algum desses campos tem semântica diferente dependendo do valor de outro campo (como `cfop` que só faz sentido quando `tipo == "nota_fiscal"`)?

---

## 4. Singleton — instância única, com ou sem SOLID

### O padrão

Singleton garante que uma classe tenha apenas uma instância durante o ciclo de vida da aplicação. O caso de uso mais claro: registros centrais, configurações globais, conexões de banco com pool gerenciado.

```python
class RegistroDocumentos:
    _instancia: Optional["RegistroDocumentos"] = None

    def __new__(cls) -> "RegistroDocumentos":
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._registro = {}
        return cls._instancia

    def registrar(self, tipo: str, classe: type) -> None:
        self._registro[tipo] = classe

    def criar(self, tipo: str, **dados) -> DocumentoCobranca:
        if tipo not in self._registro:
            raise ValueError(f"Tipo '{tipo}' não registrado")
        return self._registro[tipo](**dados)
```

```python
reg1 = RegistroDocumentos()
reg2 = RegistroDocumentos()
assert reg1 is reg2   # sempre True — mesma instância
```

### Singleton e SOLID: a tensão

O Singleton é o padrão GoF com a pior reputação em contextos de testes — não pelo Singleton em si, mas pela forma como é *consumido*. Há duas formas:

**Forma anti-SOLID — dependência oculta:**

```python
class ProcessadorDocumento:
    def processar(self, tipo: str, **dados) -> str:
        registro = RegistroDocumentos()   # acessa o Singleton diretamente
        doc = registro.criar(tipo, **dados)
        return doc.descricao()
        # Para testar, é preciso que o Singleton global esteja configurado.
        # Não há como injetar um registro diferente sem modificar o código.
```

O Singleton age como uma variável global disfarçada. `ProcessadorDocumento` tem uma dependência oculta que não aparece no construtor — viola DIP.

**Forma SOLID — injeção via construtor:**

```python
class ProcessadorDocumento:
    def __init__(self, registro: RegistroDocumentos) -> None:
        self._registro = registro   # DIP: recebe a dependência injetada

    def processar(self, tipo: str, **dados) -> str:
        doc = self._registro.criar(tipo, **dados)
        return doc.descricao()
        # Para testar: passa um RegistroDocumentos() limpo, sem tipos registrados.
        # ProcessadorDocumento não sabe — e não precisa saber — que é um Singleton.
```

```python
# No startup da aplicação (uma vez):
registro = RegistroDocumentos()
registro.registrar("boleto",      Boleto)
registro.registrar("pix",         Pix)
registro.registrar("nota_fiscal", NotaFiscal)

# Injetado onde precisar:
processador_a = ProcessadorDocumento(registro)
processador_b = ProcessadorDocumento(registro)   # mesma instância, injetada
```

### A distinção fundamental

> Singleton controla **quantas** instâncias existem. SOLID controla **o quê** cada classe faz e como se relaciona com outras. Eles operam em eixos diferentes — e são compatíveis quando o Singleton é consumido via DIP.

| | Anti-SOLID | SOLID-friendly |
|---|---|---|
| **Acesso** | `RegistroDocumentos()` chamado dentro de métodos | `RegistroDocumentos()` criado no startup, injetado via construtor |
| **Testabilidade** | Exige que o Singleton global esteja configurado | Passa qualquer instância no construtor — inclusive uma limpa para testes |
| **Visibilidade da dependência** | Oculta — não aparece no construtor | Explícita — aparece como parâmetro do construtor |
| **DIP** | Violado | Respeitado |

### Quando aplicar Singleton

- Um único ponto de registro garante consistência: todos os processos da aplicação veem os mesmos tipos registrados
- Conexão de banco com pool: o pool não deve ser recriado a cada chamada
- Configurações globais: lidas do arquivo uma vez, disponíveis em toda a aplicação
- Logger de sistema: uma instância gerencia o destino dos logs

### Quando NÃO usar Singleton

- A "razão" para usar é evitar passar o parâmetro pelo código — isso é conveniência, não necessidade
- O objeto tem estado mutável compartilhado entre threads — Singleton + estado mutable = condição de corrida
- O teste do objeto requer estado diferente do Singleton global — sinal de que o design precisa de DIP

---

> **📝 Reflita:** No seu sistema, existe alguma classe que é instanciada com `new MinhaClasse()` em dezenas de lugares diferentes, mas que deveria ser única? Quantas dessas instâncias são accessadas diretamente dentro de métodos em vez de recebidas pelo construtor?

---

## 5. Os Três Padrões em Conjunto

Os padrões de criação se complementam naturalmente:

```
Startup da aplicação:
  registro = RegistroDocumentos()      ← Singleton: instância única
  registro.registrar("boleto", Boleto)
  registro.registrar("pix", Pix)

Quando o negócio pede um novo tipo:
  registro.registrar("ted", Ted)       ← Factory: extensão sem modificação (OCP)

Quando a criação tem muitos campos:
  ted = ConstruirTed()                 ← Builder: objeto só existe completo
      .com_valor(1000.0)
      .com_banco_destino("001")
      .com_agencia("1234")
      .construir()

Processamento:
  processador = ProcessadorDocumento(registro)   ← DIP: injetado
  processador.processar("ted", ...)
```

Cada padrão resolve um problema diferente na mesma pipeline:
- Singleton: há um único registro por aplicação
- Factory: adicionar TED não abre `FabricaDocumento`
- Builder: criar um TED sem banco_destino é um erro, não silêncio

---

## 6. Regras de Ouro

- **Factory Method:** quando o `if/elif` por tipo aparecer pela segunda vez, considere substituir por registro
- **Builder:** mais de 4 parâmetros no construtor com opcionais que variam por subtipo → extraia um Builder
- **Singleton:** crie no startup, injete via construtor — nunca acesse dentro de métodos
- **Singleton + DIP:** o consumidor do Singleton não precisa saber que é Singleton — para ele, é só uma dependência recebida no construtor
- **Factory + Builder:** combinam bem — a Factory cria, o Builder garante que o que foi criado está completo
- **Nomeação:** `FabricaDocumento`, `ConstruirBoleto`, `RegistroDocumentos` — padrão no nome comunica a intenção

---

## 7. Checklist

- [ ] Adicionar um novo tipo de documento exige alterar `criar_documento()`? → Factory Method
- [ ] O construtor tem mais de 4 parâmetros, com maioria opcional? → Builder
- [ ] É possível criar o objeto sem fornecer campos obrigatórios? → `construir()` com validação
- [ ] O tipo do objeto é decidido em runtime? → Factory Method com registro
- [ ] O Singleton é acessado com `.getInstance()` dentro de métodos? → extraia para construtor (DIP)
- [ ] O código de teste precisa do Singleton global configurado? → sinal de DIP violado

---

## 8. Exercício

**Domínio:** geração de contratos (serviço, locação, fornecimento).

Arquivo: `exercicios/exercicio.py` (equivalentes: `.php`, `.ts`, `.tlpp`)

O código tem um dataclass `Contrato` com 9 campos e uma função `criar_contrato()` com `if/elif`. Sua tarefa:

1. Aplique **Factory Method**: crie `FabricaContrato` com `registrar()` e `criar()`.
2. Aplique **Builder**: crie `ConstruirContratoServico` com métodos fluentes e validação em `construir()`.
3. Aplique **Singleton**: crie `RegistroContratos` como Singleton e injete-o em `ProcessadorContrato` via construtor (DIP).

```bash
python3 exercicios/exercicio.py   # estado inicial com violações
python3 exercicios/gabarito.py    # solução com Factory + Builder + Singleton
```

Gabarito: `exercicios/gabarito.py`

---

## 9. Equivalentes em Outras Linguagens

| Linguagem | Factory | Builder | Singleton |
|---|---|---|---|
| **Python** | Dicionário de classes + `registrar()` | Métodos fluentes, `construir()` como barreira | `__new__` com atributo de classe `_instancia` |
| **PHP 8.1+** | `array` de callables + `registrar()` | Métodos fluentes, tipagem nativa `static` | `private __construct()` + `static getInstance()` |
| **TypeScript** | `Map<string, FabricaFn>` | Métodos fluentes, `?: type` para campos opcionais | `private constructor()` + `static instancia` |
| **ADVPL/TLPP** | Array de `{cTipo, codeblock}` + loop de busca | Função validadora antes do `Return` | `Static Variable` de módulo persistindo entre chamadas |

> Arquivos: `exemplos/criacao_ruins.py` · `exemplos/criacao_bons.py` · `exemplos/equivalente.php` · `exemplos/equivalente.ts` · `exemplos/equivalente.tlpp`

---

## 10. Para se Aprofundar

- **Design Patterns**, GoF — Cap. 3: Factory Method (p. 107), Builder (p. 97), Singleton (p. 127)
- **Effective Java**, Joshua Bloch — Item 3 (*Enforce the Singleton property*), Item 2 (*Builder*)
- **Refactoring**, Martin Fowler — *Replace Constructor with Factory Method*, *Replace Magic Number with Symbolic Constant*
- Crítica ao Singleton: Miško Hevery, *"Singletons are Pathological Liars"* (Google Testing Blog, 2008) — explica por que Singleton com acesso global viola testabilidade
- **Clean Code**, Martin — Cap. 10 (*Classes*): contexto de SRP aplicado ao design de classes

---

> **Próximo tutorial:** [Tutorial 10 — Padrões Estruturais](../tutorial-10-estrutural/README.md)
