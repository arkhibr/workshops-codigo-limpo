# Gabarito de Revisão — Lista de Espera

> Este documento lista os problemas do `exercicio.py` / `exercicio.ts` e o prompt forte sugerido.

---

## Problemas identificados no código gerado

### 1. Nomes sem significado

| Identificador original | Problema                                 | Solução              |
|------------------------|------------------------------------------|----------------------|
| `queue`                | Nome em inglês; não diz o que a lista representa | `lista_de_espera`    |
| `_id`                  | Sem contexto: ID de quê?                 | `_proximo_numero`    |
| `n`                    | Parâmetro sem nome: nome? número?        | `nome_paciente`      |
| `t`                    | Parâmetro sem nome: tipo? tempo? turno?  | `tipo_atendimento`   |
| `ts`                   | Abreviação ambígua                       | `registrado_em`      |
| `done`                 | Inglês em contexto PT; impreciso         | `atendido`           |
| `entry`                | Genérico; não diz o que representa       | `EntradaFila`        |

### 2. Mistura de idiomas

O código alterna entre português e inglês nos identificadores: `queue`, `done`, `ts`, `next_p`, `show`, `add`, `remove`. Em um projeto com domínio em português, essa inconsistência dificulta a leitura e viola o princípio de linguagem ubíqua.

### 3. Violação de CQS (Command-Query Separation)

A função `add` / `adicionar_na_fila` retorna o ID recém-gerado enquanto também modifica a lista. Isso mistura comando (modificar estado) com consulta (retornar valor), forçando o chamador a depender de um efeito colateral para obter informação.

**Correção:** `adicionar_na_fila` retorna `None`. Quem precisar do número de posição consulta o campo `posicao` da entrada retornada ou consulta a lista separadamente.

### 4. Nomes de função genéricos ou em inglês

| Função original | Problema                                    | Solução                        |
|-----------------|---------------------------------------------|--------------------------------|
| `add`           | Em inglês; não diz o domínio               | `adicionar_na_fila`            |
| `remove`        | Em inglês; não diz o domínio               | `remover_da_fila`              |
| `show`          | Vago: mostrar o quê?                        | `exibir_lista_de_espera`       |
| `next_p`        | Mistura PT/EN; abreviação obscura           | `chamar_proximo_paciente`      |

### 5. Código de retorno em vez de exceção

`remove` retorna `False` quando o paciente não é encontrado, obrigando o chamador a checar o retorno antes de confiar que a operação ocorreu. Exceção com mensagem descritiva é mais honesta: o chamador sabe imediatamente o que deu errado.

### 6. Ausência de estrutura de dados tipada

Usar `dict` com chaves abreviadas (`"n"`, `"t"`, `"ts"`) em vez de `@dataclass EntradaFila` / `interface EntradaFila` torna o código frágil: erros de digitação na chave só aparecem em tempo de execução, não em tempo de desenvolvimento.

### 7. Sombreamento de built-in (Python)

A função `remove(id)` usa `id` como nome de parâmetro, sobrescrevendo o built-in `id()` do Python dentro do escopo da função. Renomear para `posicao` corrige o problema e ainda torna o parâmetro mais descritivo.

> Nota: este problema é específico de Python; no TypeScript `id` não é um built-in.

---

## Prompt forte sugerido

```
Contexto: sistema de gestão de clínica médica. Todos os identificadores
devem estar em português brasileiro — sem mistura de idiomas.

Implemente um módulo de lista de espera com as seguintes funções:

1. `adicionar_na_fila(nome_paciente, tipo_atendimento)` → None
   - Gera um número de posição sequencial (constante nomeada para o valor inicial).
   - Cria uma EntradaFila (dataclass) com: posicao, nome_paciente,
     tipo_atendimento, registrado_em (datetime atual), atendido=False.
   - Armazena na lista em memória. Não retorna valor (CQS: é um comando).

2. `remover_da_fila(posicao)` → None
   - Remove a entrada com a posição informada.
   - Lança ValueError com mensagem descritiva se não encontrada.

3. `exibir_lista_de_espera()` → None
   - Exibe cada entrada com marcador visual para atendido/pendente.

4. `chamar_proximo_paciente()` → EntradaFila
   - Marca o primeiro paciente pendente como atendido e o retorna.
   - Lança RuntimeError se a fila estiver vazia.

Restrições de Clean Code:
- Sem números mágicos — use constantes nomeadas.
- Sem mistura de idiomas nos nomes.
- Cada função tem uma única responsabilidade.
- Erros tratados com exceções, não com códigos de retorno.

Linguagem: Python 3.10+. Sem frameworks externos.
```

---

## Por que o prompt forte produz código melhor

O prompt fraco ("cria um módulo de lista de espera pra clínica") não especifica o domínio, os contratos, as restrições de idioma nem as expectativas de qualidade. A IA preenche as lacunas com defaults genéricos — normalmente inglês, nomes curtos, dicts soltos.

O prompt forte embute a especificação de Clean Code diretamente: a IA sabe que precisa usar nomes em português, constantes nomeadas, exceções e separação de responsabilidades. O resultado ainda precisa ser revisado, mas o ponto de partida é muito mais próximo do código de produção.
