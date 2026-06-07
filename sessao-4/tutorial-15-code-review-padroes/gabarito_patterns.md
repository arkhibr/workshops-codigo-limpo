# Catálogo de Padrões — Referência da Equipe

> Use este documento como referência permanente durante code reviews.
> Pergunte: "Esse código seria melhor com algum desses padrões?"

## Princípios SOLID

| Princípio | Sintoma que viola | Solução | Tutorial |
|-----------|-------------------|---------|----------|
| SRP — Responsabilidade Única | Classe com mais de 1 razão para mudar | Separe em classes menores | T16, T19, T23 |
| OCP — Aberto/Fechado | `if/elif tipo == "X"` que cresce | Strategy, Factory | T17, T20 |
| LSP — Substituição de Liskov | Subclasse lança exceção que a base não lança | Não override para quebrar | T16 |
| ISP — Segregação de Interfaces | Interface com métodos que nem todos usam | Protocolos menores | T16 |
| DIP — Inversão de Dependência | `self.x = ConcreteClass()` no constructor | Injetar por Protocol/interface | T16, T23 |

## Padrões de Criação (GoF Cap. 3)

| Padrão | Quando usar | Quando NÃO usar | Exemplo workshop | ADVPL? |
|--------|-------------|-----------------|------------------|--------|
| Factory Method | Tipo de objeto determinado em runtime; extensível sem alterar fábrica | Apenas 1 tipo concreto fixo | `FabricaDocumento` (T17) | Sim — `Do Case` em função `FabricarX()` |
| Builder | Objeto com muitos campos opcionais; construção em etapas | Objeto simples com 2–3 campos | `ConstruirBoleto` (T17) | Parcialmente — função `MontarX()` com validação |

## Padrões Estruturais (GoF Cap. 4)

| Padrão | Quando usar | Quando NÃO usar | Exemplo workshop | ADVPL? |
|--------|-------------|-----------------|------------------|--------|
| Adapter | API legada com nomenclatura incompatível; biblioteca externa | Código sob seu controle | `ERPClienteAdapter` (T18) | Sim — **especialmente valioso** para isolar User Functions do Protheus |
| Facade | Subsistema complexo com 5+ etapas que o chamador não deve conhecer | Poucas etapas simples | `FachadaProcessamentoPedido` (T18) | Sim — função orquestradora |

## Padrões Comportamentais (GoF Cap. 5)

| Padrão | Quando usar | Quando NÃO usar | Exemplo workshop | ADVPL? |
|--------|-------------|-----------------|------------------|--------|
| Strategy | Algoritmo que varia por contexto; `if/elif` que cresce | Apenas 1 algoritmo fixo | `EstrategiaImposto`, `EstrategiaFrete` (T20) | Sim — `Do Case` em função paramétrica |
| Template Method | Esqueleto fixo com variações em passos específicos | Variações em todos os passos | `RelatorioBase._montar_saida()` (T20) | Parcialmente — codeblocks |
| Observer | Evento com N consumidores desacoplados | 1 consumidor fixo e estável | `GerenciadorPedido + observadores` (T21) | Sim — array de codeblocks |
| Command | Operação que precisa de undo/redo; histórico | Operação simples sem reversão | `ComandoCancelamento + HistoricoComandos` (T21) | Parcialmente — struct com estado anterior |

## Anti-patterns a Evitar (T19, T23)

| Anti-pattern | Sintoma | Correção | Tutorial |
|--------------|---------|----------|----------|
| God Object | Classe com 8+ métodos cobrindo domínios diferentes | SRP — divide em classes por responsabilidade | T19, T23 |
| Magic Strings/Numbers | `if status == "A"`, `valor > 1412` sem contexto | `enum`, constantes nomeadas | T19, T23 |
| Feature Envy | Método acessa mais dados de outra classe do que da própria | Mover método para a classe dos dados | T19, T23 |
| Copy-paste | Dois blocos idênticos em lugares diferentes | Extrair função/método; Template Method | T19, T23 |

## Idioms por Linguagem (T22)

| Idiom | Python | PHP 8.1+ | TypeScript | ADVPL |
|-------|--------|----------|------------|-------|
| Struct com validação | `@dataclass + __post_init__` | `readonly class + __construct` | `interface + class` | Função `CriarX()` + validação |
| Cleanup garantido | `with` (context manager) | — | — | `Begin Sequence / End Sequence` |
| Lazy iteration | `yield` (generator) | `yield` (generator) | `function*` | Loop inline |
| Cross-cutting concern | `@decorator` | — | — | Sem equivalente |
| Tipo nomeado | `enum` | `enum` | discriminated union | `#define` |

## Checklist de Code Review

Para cada PR/módulo, pergunte:
- [ ] Alguma classe tem mais de 2 responsabilidades? → SRP
- [ ] Há `if/elif tipo == "X"` que pode crescer? → Strategy
- [ ] Algum método acessa mais dados de outro objeto do que do próprio? → Feature Envy
- [ ] Algum bloco de código aparece em 2+ lugares? → DRY / Template Method
- [ ] O constructor instancia dependências concretas? → DIP
- [ ] Há strings ou números "misteriosos" sem contexto? → Magic Strings/Numbers
