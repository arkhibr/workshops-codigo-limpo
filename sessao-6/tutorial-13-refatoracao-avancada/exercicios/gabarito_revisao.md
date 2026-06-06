# Gabarito de Revisão — Refatoração de IA com regressão de borda

## O caso de borda quebrado

| Caso | Original (`if/elif`) | Refatoração gerada (`>`) | Resultado |
|---|---|---|---|
| atingimento = 80% | `>= 0.80` → **10%** | `> 0.80` → **0%** | REGRESSÃO |
| atingimento = 100% | `>= 1.00` → **20%** | `> 1.00` → **10%** | REGRESSÃO |
| atingimento = 120% | `>= 1.20` → **30%** | `> 1.20` → **20%** | REGRESSÃO |
| atingimento = 90% | `>= 0.80` → 10% | `> 0.80` → 10% | OK |
| atingimento = 110% | `>= 1.00` → 20% | `> 1.00` → 20% | OK |
| atingimento = 130% | `>= 1.20` → 30% | `> 1.20` → 30% | OK |

**O defeito:** a IA gerou `>` em vez de `>=` na comparação da tabela.
Em todos os casos no *interior* das faixas, `>` e `>=` produzem o mesmo
resultado — por isso a verificação fraca (só interior) passa sem detectar.
Nos valores exatos dos limites, `>` faz o valor cair para a faixa abaixo.

**Impacto real:** um vendedor que atingiu exatamente 100% da meta recebe
bônus de 10% em vez de 20% — metade do valor esperado, sem qualquer
mensagem de erro ou aviso.

---

## Por que a verificação fraca não detecta

```python
# Verificação fraca — casos no interior das faixas
casos = [
    MetaVendedor("V01", salario, 0.60),   # 60% → 0    (OK: > e >= coincidem)
    MetaVendedor("V02", salario, 0.90),   # 90% → 10%  (OK: > e >= coincidem)
    MetaVendedor("V03", salario, 1.10),   # 110% → 20% (OK: > e >= coincidem)
    MetaVendedor("V04", salario, 1.30),   # 130% → 30% (OK: > e >= coincidem)
]
# Todos passam — a regressão de borda é invisível.
```

```python
# Verificação completa — inclui os limites exatos
casos += [
    MetaVendedor("limite-faixa1", salario, 0.80),   # 80% → original=10%, gerado=0 → FALHOU
    MetaVendedor("limite-faixa2", salario, 1.00),   # 100% → original=20%, gerado=10% → FALHOU
    MetaVendedor("limite-faixa3", salario, 1.20),   # 120% → original=30%, gerado=20% → FALHOU
]
# FALHOU revela a regressão imediatamente.
```

---

## Como a verificação de equivalência revela a regressão

Ao rodar `verificar_equivalencia` completa contra a versão com `>`:

```
FALHOU: limite-faixa1      atingimento= 80.0%  esperado=500.00  obtido=0.00
FALHOU: limite-faixa2      atingimento=100.0%  esperado=1000.00  obtido=500.00
FALHOU: limite-faixa3      atingimento=120.0%  esperado=1500.00  obtido=1000.00
```

Ao rodar contra a versão corrigida (com `>=`):

```
OK: limite-faixa1      atingimento= 80.0%  bônus=   500.00
OK: limite-faixa2      atingimento=100.0%  bônus=  1000.00
OK: limite-faixa3      atingimento=120.0%  bônus=  1500.00
```

A diferença entre `>` e `>=` é um único caractere no código — mas representa
a diferença entre preservar e quebrar o contrato de cada limite de faixa.

---

## Sequência de passos da refatoração segura

```
1. Declara a estratégia antes do código
   → Pergunte ao modelo: "qual operador vai usar: > ou >=?"
   → Resposta esperada: ">= (mesmo que o if/elif original)"
   → Se responder ">": corrija antes de prosseguir

2. Gera a tabela de faixas com o operador declarado
   → diff deve mostrar apenas a estrutura nova; semântica idêntica

3. Gera verificar_equivalencia com bordas incluídas
   → Interior das faixas: confirma casos comuns
   → Limites exatos: confirma que >= foi implementado
   → Logo abaixo: confirma que a faixa inferior está correta

4. Roda a verificação
   → Qualquer FALHOU → voltar ao passo 1 (não ao passo 2)
   → O operador é o único ponto crítico; o resto da estrutura é mecânico

5. Integra apenas quando todos os casos passam
```

---

## A lição do tutorial

Uma refatoração de if/elif para tabela parece trivial — é puramente estrutural,
não altera a lógica. Por isso é tentador não verificar. O defeito é sutil porque:

- O código refatorado é idiomático, limpo e legível.
- Os casos comuns (interior das faixas) passam em ambas as versões.
- O operador `>` é o mais intuitivo em buscas de tabela ("primeiro que supera").
- Só os valores exatos nos limites revelam a divergência.

**A verificação de equivalência com bordas é o único controle que captura
esta classe de regressão.** Sem ela, a refatoração parece correta e vai para
produção — onde o impacto é silencioso e financeiro.
