# Gabarito de Revisão — Cupom de Desconto Progressivo

> Este documento lista os problemas do `exercicio.py` / `exercicio.ts`, o prompt estruturado sugerido e um template reutilizável para a equipe.

---

## Problemas identificados no código gerado

### 1. Nomes sem significado

| Identificador original | Problema                                   | Solução                     |
|------------------------|--------------------------------------------|-----------------------------|
| `cupons`               | Nome vago; não diz o que a estrutura guarda | `cupomsCadastrados`         |
| `c`                    | Variável temporária sem contexto           | `cupom`                     |
| `val`                  | Abreviação: valor do quê?                  | `valorCompra`               |
| `tp`                   | Abreviação obscura                         | `tipo`                      |
| `amt`                  | Inglês; valor? montante? quantidade?       | `valor`                     |
| `d`                    | Uma letra sem contexto                     | `desconto`                  |

### 2. Funções com nomes em inglês ou genéricos

| Função original | Problema                                    | Solução                      |
|-----------------|---------------------------------------------|------------------------------|
| `apply`         | Inglês; aplica o quê?                       | `aplicarCupom`               |
| `add`           | Inglês e genérico                           | `cadastrarCupom`             |
| `rm`            | Sigla de comando Unix, não de domínio       | `removerCupom`               |
| `show_all`      | Mistura de inglês; mostra o quê?            | `exibirCuponsCadastrados`    |

### 3. Números mágicos sem nome

- `1.5` — multiplicador do desconto progressivo. Deveria ser `MULTIPLICADOR_PROGRESSIVO = 1.5`.
- `200` — limiar de valor para ativar o desconto progressivo. Deveria ser `LIMIAR_DESCONTO_PROGRESSIVO = 200.0`.

### 4. Falha silenciosa em vez de exceção

`apply("INVALIDO", 100.0)` retorna o valor sem desconto sem nenhum aviso. O chamador não sabe se o cupom foi aplicado ou não. A versão correta lança `ValueError` / `Error` com mensagem descritiva.

### 5. Estrutura de dados frágil (dict/Record solto)

`{"type": tp, "amt": amt}` usa chaves abreviadas e sem tipo. Erros de digitação (`"aamt"`) só aparecem em tempo de execução. A versão correta usa `@dataclass Cupom` / `interface Cupom` com tipos explícitos.

---

## Prompt estruturado sugerido

```
Contexto: módulo de cupons de desconto de um sistema de e-commerce.
Todos os identificadores devem estar em português brasileiro —
sem mistura de idiomas.

Implemente um módulo de cupons com as seguintes funções:

1. `cadastrar_cupom(codigo, tipo, valor)` → None
   - `tipo` é um TipoCupom (enum): PERCENTUAL ou VALOR_FIXO.
   - `valor` é o percentual (0–1) ou o valor fixo em reais.
   - Armazena em repositório em memória.

2. `aplicar_cupom(codigo, valor_compra)` → float
   - Lança ValueError com mensagem descritiva se o cupom não existir.
   - Para TipoCupom.PERCENTUAL: aplica o percentual; se valor_compra >=
     LIMIAR_DESCONTO_PROGRESSIVO (constante nomeada), multiplica o desconto
     por MULTIPLICADOR_PROGRESSIVO (constante nomeada).
   - Para TipoCupom.VALOR_FIXO: subtrai o valor fixo, mínimo PRECO_MINIMO (0).
   - Cada regra em sua própria função privada. Retorna float arredondado em 2 casas.

3. `remover_cupom(codigo)` → None
   - Lança ValueError se o cupom não existir.

4. `exibir_cupons_cadastrados()` → None
   - Exibe cada cupom com código, tipo e valor formatado.

Restrições:
- Sem bibliotecas externas.
- Sem números mágicos — todos os valores em constantes nomeadas.
- Sem mistura de idiomas nos identificadores.
- Cada função tem uma única responsabilidade.
- Erros tratados com exceções, não com retornos silenciosos.

Linguagem: Python 3.10+. Sem frameworks externos.
```

---

## Template de prompt da equipe

Use este template como ponto de partida para qualquer pedido de geração de código no projeto:

```
## Contexto
[Descreva o domínio de negócio, o módulo em que o código se insere e
o que ele faz no sistema. Ex.: "módulo de cupons de um e-commerce".]

## Domínio
[Liste os termos do negócio que a IA deve usar — não sinônimos genéricos.
Ex.: "use 'valorCompra', não 'price' ou 'val'; 'TipoCupom', não 'Type'".]
Idioma dos identificadores: português brasileiro — sem mistura de idiomas.

## Restrições
- [Liste o que a IA NÃO deve fazer. Ex.: "sem bibliotecas externas".]
- Sem números mágicos — extraia constantes nomeadas.
- Cada função com uma única responsabilidade.
- Erros tratados com exceções e mensagens descritivas.

## Exemplo do padrão desejado (few-shot)
[Cole um trecho do código existente que mostre o estilo da equipe.
Ex.: a interface ou dataclass já usada no projeto.]

## Formato de saída
[Especifique o contrato de retorno. Ex.: "retorna float arredondado em 2
casas decimais; lança ValueError se <condição>".]

Linguagem: [Python 3.10+ / TypeScript 5+]. Sem frameworks externos.
```

---

## Por que o prompt estruturado produz código melhor

O prompt fraco ("cria um módulo de cupom de desconto pra loja") não especifica o domínio, os contratos, o idioma, as restrições nem o padrão de código. A IA preenche as lacunas com defaults genéricos — nomes em inglês, dicts soltos, retornos silenciosos.

O prompt estruturado embute as expectativas de Clean Code diretamente na especificação: a IA sabe que precisa usar nomes em português, constantes nomeadas, exceções e separação de responsabilidades. O resultado ainda precisa ser revisado — mas o ponto de partida é muito mais próximo do código de produção.
