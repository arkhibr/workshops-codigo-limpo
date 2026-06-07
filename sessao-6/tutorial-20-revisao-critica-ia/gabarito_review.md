# Gabarito — Revisão Crítica: `codigo_gerado_por_ia.py`

> Simulação de comentários de revisão esperados para código gerado por modelo de fronteira.
> Cada comentário segue o formato: **Linha · Categoria do checklist · Problema · Por que é sutil · Como corrigir**.

---

## Defeito 1 — API/método alucinado

**Linha 202 — Categoria: Dependências/alucinação**

`_gateway.verificar_idempotencia(transacao_id)` chama um método que não existe
na classe `GatewaySimulado` (nem na SDK real do provedor versão 3.x). O modelo
gerou um nome plausível e bem formado, que se encaixa naturalmente na sequência
do código.

**Por que é sutil:** o método está em um ramo de guarda (`if valor <= 0`) que o
demo não exercita — o código roda sem erro. O defeito só aparece em produção,
quando alguém tenta estornar com valor inválido.

**Como corrigir:** verificar a documentação da SDK. Se a funcionalidade de
idempotência existe, usar o método correto. Se não existe na versão usada,
implementar a lógica localmente com um `set` de IDs já processados.

---

## Defeito 2 — Lógica confiante-mas-errada (off-by-one)

**Linha 148 — Categoria: Correção**

```python
for numero in range(1, num_parcelas):   # gera [1, 2] para num_parcelas=3
```

Para 3 parcelas, `range(1, 3)` gera `[1, 2]` — a terceira parcela nunca é
criada. A saída da demo já deixa visível: "2 (de 3 solicitadas)".

**Por que é sutil:** o código está bem estruturado, com constantes nomeadas,
tipos corretos e lógica de juros composta correta. O `range` errado é um
detalhe de um caractere (`num_parcelas` vs `num_parcelas + 1`) que passa
facilmente em leitura rápida.

**Como corrigir:**
```python
for numero in range(1, num_parcelas + 1):
```

---

## Defeito 3 — Segurança sutil (comparação não constant-time)

**Linha 168 — Categoria: Segurança**

```python
return assinatura_esperada == assinatura_recebida
```

A comparação de strings com `==` em Python encerra a comparação no primeiro
byte diferente. Isso expõe um timing side-channel: um atacante pode medir o
tempo de resposta para adivinhar a assinatura byte a byte, sem precisar da
chave secreta.

**Por que é sutil:** a lógica de geração da assinatura está correta
(`hmac.new` com SHA-256). O defeito está apenas no operador de comparação
— uma linha que parece idiomática e inofensiva.

**Como corrigir:**
```python
return hmac.compare_digest(assinatura_esperada, assinatura_recebida)
```

> Nota: o Tutorial 14 aprofunda segurança em código gerado por IA. Este
> defeito é a introdução ao tema.

---

## Defeito 4 — Edge case ausente (valor zero/negativo)

**Linha 181 (logger.info), linha 183 (gateway.cobrar) — Categoria: Edge cases**

`cobrar()` não valida se `cobranca.valor` é positivo. Chamar com `valor=-50.0`
executa sem erro e registra uma transação inválida no gateway simulado.

**Por que é sutil:** a função tem tipagem completa, docstring detalhada e log
de auditoria — parece defensiva. A ausência da guarda de valor não salta aos
olhos porque tudo ao redor está bem cuidado.

**Como corrigir:**
```python
if cobranca.valor <= 0:
    raise ValueError(f"Valor deve ser positivo; recebido: {cobranca.valor}")
```

---

## Defeito 5 — Over-engineering (factory desnecessária)

**Linhas 28–48 (comentário + classe) — Categoria: Legibilidade/Coesão**

`ProcessadorDePagamento` é uma factory/strategy que não foi pedida. O requisito
original era apenas três funções: `cobrar`, `estornar`, `consultar_status`. A
classe adiciona ~20 linhas de abstração, um `enum` extra e um método `processar`
que delega diretamente para as funções livres — sem nenhum comportamento próprio.

**Por que é sutil:** o padrão strategy é reconhecível e "parece correto" para
múltiplos tipos de pagamento. A abstração não quebra nada; apenas acrescenta
complexidade sem valor para o pedido atual.

**Como corrigir:** remover `ProcessadorDePagamento` e `TipoProcessador`. Manter
apenas as funções livres `cobrar`, `estornar`, `consultar_status`. Se no futuro
o roteamento por tipo for necessário, introduzir a abstração então.

---

## Defeito 6 — Docstring que mente

**Linha 175 (docstring de `cobrar`) — Categoria: Legibilidade/Coesão**

```python
"""
Submete uma cobrança ao gateway e retorna o resultado.

Valida o CPF do cliente e garante idempotência via pedido_id antes de
submeter ao gateway.
"""
```

O corpo da função não valida CPF nem garante idempotência. O `pedido_id` é
apenas repassado ao gateway sem nenhuma verificação de duplicidade.

**Por que é sutil:** a docstring está bem escrita, profissional e descreve
comportamentos desejáveis. Em um code review rápido, é tentador assumir que
se está documentado, está implementado.

**Como corrigir:** ou implementar a validação prometida, ou corrigir a docstring
para descrever o que a função realmente faz:
```python
"""Submete uma cobrança ao gateway e retorna o resultado."""
```

---

> **Total: 6 defeitos**
> Distribuição: 1 Alucinação · 1 Correção · 1 Segurança · 1 Edge case · 1 Over-engineering · 1 Docstring
