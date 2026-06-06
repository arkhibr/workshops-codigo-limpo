# Prompt sem Contexto vs. Prompt com Contexto de Manutenibilidade

> Dar contexto ao agente não é apenas educação — é a única forma de impedir que ele crie deriva.

---

## Prompt sem contexto de padrão

```
adiciona uma função que calcula o desconto baseado nas vendas do mês
```

**O que a IA não sabe** e vai inventar: quais funções já existem no módulo, qual é o estilo de nomes adotado, se já existe alguma lógica de desconto que deve ser reutilizada, quais dependências estão disponíveis, e qual é o idioma dos identificadores.

**Resultado típico no diff:**
- Nova função com nome em inglês ou camelCase enquanto o restante do módulo usa snake_case PT.
- Lógica de cálculo que duplica parcialmente uma função já existente.
- Importação de uma biblioteca nova para algo que `round()` ou `sum()` já resolve.
- Formatação divergente (espaçamento, docstring ou ausência deles) em relação ao restante.

> Arquivo de exemplo: `relatorio_gerado.py` / `relatorio_gerado.ts` — observe os quatro sinais de deriva.

---

## Prompt com contexto de manutenibilidade

```
No módulo relatorio_vendas.py:
- Todos os identificadores estão em português, snake_case.
- O estilo de funções segue o padrão: def nome_funcao(parametro: tipo) -> tipo:
  com docstring curta descrevendo o que a função retorna.
- Formatação: linha em branco entre funções, sem linhas extras no corpo.
- Sem dependências externas — usa apenas a stdlib do Python.

Adiciona a função calcular_desconto_fidelidade(total_vendas: float) -> float
que:
1. Retorna 0.10 se total_vendas >= LIMITE_DESCONTO_FIDELIDADE (constante nomeada = 5000.0).
2. Retorna 0.05 se total_vendas >= LIMITE_DESCONTO_BASICO (constante nomeada = 2000.0).
3. Retorna 0.0 caso contrário.
4. Deve reutilizar calcular_total_vendas() para obter o total se necessário.
5. Sem duplicar lógica já existente no módulo.
```

**O que muda no diff:**
- A nova função segue o mesmo estilo snake_case PT das vizinhas.
- As constantes nomeadas mantêm o padrão das constantes já existentes no módulo.
- Nenhuma dependência nova aparece no diff.
- O revisor vê uma função que parece ter sido escrita pelo mesmo time.

> Arquivo de exemplo: `relatorio_revisado.py` / `relatorio_revisado.ts` — versão consolidada com estilo uniforme.

---

## O que revisar no diff após cada contribuição de agente

| Sinal de deriva               | Como detectar no diff                                      |
|-------------------------------|------------------------------------------------------------|
| Estilo de nome divergente     | `calcTotal` ou `get_total` ao lado de `calcular_total_vendas` |
| Duplicação de lógica          | Duas funções com corpos quase idênticos adicionadas        |
| Dependência desnecessária     | Nova linha em `import` que usa algo que a stdlib fornece   |
| Formatação divergente         | Espaçamentos e docstrings inconsistentes com o entorno     |

**Conclusão:** dar contexto eleva o ponto de partida do agente, mas não elimina a revisão do diff. O contexto reduz a deriva; a revisão do diff detecta o que ficou apesar do contexto.
