# Prompt Fraco vs. Prompt Forte — Agendamento de Consulta

> O prompt é uma especificação informal. Qualidade da especificação → qualidade do código.

---

## Prompt Fraco

```
faz uma função de agendar consulta
```

**O que a IA não sabe** e vai inventar: o domínio (clínica? academia? reunião?), os campos obrigatórios, o formato de data, se há validação de conflito, qual é o tipo de retorno esperado, como tratar erros, e em que idioma nomear os identificadores.

**Resultado típico:** nomes genéricos (`processar`, `d`, `p`, `h`), mistura de idiomas (`date`, `get_consultas`), número mágico (`dur: 30`), código de erro em vez de exceção (`return -1`).

> Arquivo de exemplo: `agendamento_gerado.py` / `agendamento_gerado.ts`

---

## Prompt Forte

```
Contexto: sistema de agendamento de uma clínica médica. Todos os
identificadores devem estar em português brasileiro.

Implemente a função `agendar_consulta(data, horario, nome_paciente)`
que:
1. Recebe data no formato "AAAA-MM-DD", horário "HH:MM" e nome do paciente.
2. Verifica se o paciente já tem consulta agendada nessa data; se tiver,
   lança ValueError com mensagem descritiva.
3. Cria um objeto Consulta (dataclass) com os campos: data, horario,
   nome_paciente, duracao_min (padrão definido como constante nomeada) e
   status="confirmada".
4. Armazena a consulta em uma lista em memória e a retorna.
5. Cada responsabilidade deve estar em sua própria função.
6. Sem números mágicos — extraia constantes nomeadas.
7. Sem mistura de idiomas nos nomes — tudo em português.

Linguagem: Python 3.10+. Sem frameworks externos.
```

**O que muda:** o domínio está definido, o contrato de cada parâmetro é explícito, o tratamento de erro é especificado, a estrutura de dados é pedida, e as restrições de Clean Code estão embutidas na especificação.

**Resultado típico:** nomes descritivos, `@dataclass Consulta`, constante `DURACAO_PADRAO_MIN`, função `_existe_conflito` extraída, exceção com mensagem clara.

> Arquivo de exemplo: `agendamento_revisado.py` / `agendamento_revisado.ts`

---

## O que muda na prática

| Dimensão              | Prompt fraco                   | Prompt forte                        |
|-----------------------|--------------------------------|-------------------------------------|
| Nomes                 | `d`, `p`, `h`, `processar`     | `data`, `nome_paciente`, `agendar_consulta` |
| Idioma                | Misturado (PT + EN)            | Consistente (PT)                    |
| Tratamento de erro    | `return -1`                    | `raise ValueError("...")`           |
| Números mágicos       | `dur: 30`                      | `DURACAO_PADRAO_MIN = 30`           |
| Coesão                | Tudo numa função               | Validação extraída em função própria |
| Estrutura de dados    | Dict solto com chaves vagas    | `@dataclass Consulta` tipado        |

**Conclusão:** mesmo um prompt forte não elimina a revisão — ele apenas eleva o ponto de partida. O desenvolvedor ainda precisa ler o código gerado e aplicar o checklist de Clean Code.
