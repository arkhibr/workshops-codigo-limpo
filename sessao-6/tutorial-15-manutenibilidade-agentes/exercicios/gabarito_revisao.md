# Gabarito de Revisão — Dashboard com Deriva de IA

> Este documento lista cada sinal de deriva encontrado no `exercicio.py` / `exercicio.ts`
> e como cada um foi consolidado.

---

## Sinais de deriva identificados e consolidados

### 1. Duplicação de lógica de cálculo de total

**Problema:** três funções fazem essencialmente a mesma operação (somar `v["valor"]` de cada item), com nomes e estilos diferentes:

| Função original          | Estilo              | Problema adicional          |
|--------------------------|---------------------|-----------------------------|
| `calcular_total_periodo` | snake_case PT       | Função original — correta   |
| `getTotal`               | camelCase EN / `any`| Duplicata em inglês sem tipo |
| `calcular_soma_vendas`   | snake_case PT       | Terceiro nome para a mesma coisa |

**Consolidação:** `getTotal` e `calcular_soma_vendas` foram removidas. `calcular_total_periodo` é a única função de cálculo de total — reutilizada em `exibir_dashboard`.

---

### 2. Estilo de nome divergente

**Problema:** o módulo misturava dois estilos:
- `calcular_total_periodo` (snake_case PT — estilo original)
- `getTotal` (camelCase EN — contribuição sem contexto)
- `calcular_soma_vendas` (snake_case PT, mas terceiro nome idêntico)

**Consolidação:** todos os nomes unificados em snake_case português com type hints explícitos (Python) / camelCase português com tipagem explícita (TypeScript).

---

### 3. Dependência desnecessária (`UtilPercentual`)

**Problema:** a IA adicionou `UtilPercentual.formatar(valor)` para formatar um percentual — uma biblioteca simulada que poderia ser qualquer pacote externo. A stdlib Python (`f"{valor * 100:.1f}%"`) e o runtime TypeScript (`toFixed`) resolvem o problema sem dependência alguma.

**Impacto de uma dependência real:** entrada no `requirements.txt` / `package.json`, risco de vulnerabilidade de segurança futura, custo de atualização.

**Consolidação:** `UtilPercentual` removido. `formatar_percentual()` / `formatarPercentual()` usa f-string nativa / `toFixed`. A classe `UtilPercentual` não existe mais no módulo.

---

### 4. Formatação e assinatura divergentes em `exibir_dashboard`

**Problema:** a contribuição 4 adicionou `exibir_dashboard` com:
- Sem espaços em torno do `=` nos parâmetros padrão (`periodo="Período Atual"`)
- Sem type hints nos parâmetros e sem tipo de retorno declarado
- Uso de `getTotal` (duplicata) em vez de `calcular_total_periodo`
- Formatação de moeda inline com cadeia de `replace` duplicada dentro da função
- Mistura de concatenação de string (`"Meta atingida: " + ...`) e f-strings

**Consolidação:**
- Assinatura com espaços, type hints e `: None` explícito
- `exibir_dashboard` usa `calcular_total_periodo` e `calcular_percentual_meta`
- Formatação de moeda extraída para `formatar_reais()` — chamada uma vez, reutilizável
- Todas as saídas usam f-strings uniformemente

---

## O que NÃO foi alterado (comportamento preservado)

| Saída observável                         | exercicio | gabarito |
|------------------------------------------|-----------|----------|
| Total de vendas calculado                | 9050.00   | 9050.00  |
| Percentual de meta                       | 90.5%     | 90.5%    |
| Status (meta não atingida)               | sim       | sim      |
| Quanto falta para a meta                 | 950.00    | 950.00   |

A consolidação eliminou a deriva sem alterar nenhuma saída observável.

---

## Prompt forte que teria prevenido a deriva

```
No módulo dashboard_vendas.py:
- Todos os identificadores em português, snake_case, com type hints.
- Funções de cálculo de total já existem: calcular_total_periodo().
  Não duplique — reutilize.
- Formatação de moeda: f-string com :,.2f + replace de separadores.
- Sem dependências externas — apenas stdlib.

Adiciona a função exibir_dashboard(vendas, periodo) → None que:
1. Usa calcular_total_periodo() para obter o total.
2. Usa calcular_percentual_meta() para o percentual.
3. Exibe total, percentual e status de meta.
4. Segue a formatação das funções existentes.
```
