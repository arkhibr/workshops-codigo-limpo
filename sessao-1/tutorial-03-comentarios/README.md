# Tutorial 03 — Comentários

> Referência: *Clean Code*, Capítulo 4 — Comments

---

## 1. Contexto e Motivação

O capítulo 4 do Clean Code abre com a frase mais forte do livro sobre o tema:

> *"The proper use of comments is to compensate for our failure to express ourselves in code."*
> — Robert C. Martin, Clean Code, p. 54

Cada comentário é uma admissão de falha na expressividade do código — não necessariamente uma falha grave, mas um ponto onde o código não conseguiu se explicar sozinho. Martin não diz que comentários são sempre ruins; diz que eles deveriam ser raros, porque código bem escrito raramente precisa deles.

O problema real é a **defasagem temporal**. Comentários envelhecem. O código muda, o comentário não acompanha. Em pouco tempo, o comentário deixa de descrever o presente e começa a descrever um passado que já não existe — ou pior, descreve algo errado. Quando isso acontece, o comentário não é apenas inútil: ele é ativamente prejudicial, porque engana o leitor com informação falsa que parece confiável.

---

## 2. Conceito Central

O Clean Code categoriza comentários em dois grupos: os que agregam valor e os que não agregam.

### Comentários que têm valor

**Legal** — cabeçalho de licença ou copyright. Obrigação contratual ou legal, não uma escolha.
```python
# Copyright (c) 2026 Arkhi Business Agility Ltda. Licença MIT — veja LICENSE.txt
```

**Informativo** — explica o formato de um retorno que o tipo não consegue expressar sozinho.
```python
# Retorna string no formato "YYYY-MM-DDTHH:MM:SSZ" (ISO 8601 UTC)
def timestamp_atual() -> str: ...
```

**Intenção** — explica o *porquê* de uma decisão, não o *o quê* do código. Regras de negócio, restrições externas, trade-offs conscientes.
```python
# Ordenamos por data DESC aqui porque o cliente lê apenas os 10 primeiros
# e a query com índice DESC é 40x mais rápida nesse volume (benchmark Sprint 38).
pedidos = repo.listar(ordem="data_desc", limite=10)
```

**Clarificação** — traduz algo obscuro que não pode ser renomeado (e.g., API externa com nomes fixos, expressão matemática com nome canônico).
```python
# Fórmula de Haversine: distância entre dois pontos na superfície esférica da Terra
a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
```

**Aviso de consequências** — alerta sobre efeito colateral relevante que o leitor poderia ignorar.
```python
# ATENÇÃO: este método abre uma transação e NÃO faz commit.
# O chamador é responsável por chamar db.commit() ou db.rollback().
def iniciar_transferencia(origem, destino, valor): ...
```

**TODO rastreável** — promessa com número de ticket, responsável e prazo. Sem esses dados, não é TODO: é ruído.
```python
# TODO [PLAT-1847]: substituir mock por chamada real ao serviço de usuários.
# Responsável: @ana.souza  |  Prazo: Sprint 42 (2026-05-05)
```

**Amplificação** — destaca algo que parece trivial mas tem impacto não óbvio.
```python
# IMPORTANTE: trim() aqui é intencional — o campo chega com espaços do legado.
# Remover este trim() quebra a validação de duplicatas no passo seguinte.
codigo = dados["codigo"].strip()
```

---

### Comentários que não têm valor

**Redundante** — repete exatamente o que o código já diz com clareza. O leitor lê o código duas vezes sem ganhar nada.
```python
# multiplica o preço pela quantidade
total = preco * quantidade
```

**Enganoso** — informação desatualizada ou imprecisa. Pior que nenhum comentário: cria falsa confiança.
```python
# retorna True se o produto NÃO estiver disponível
return produto["estoque"] > 0   # na verdade retorna True quando ESTÁ disponível
```

**Mandatório** — comentário exigido por uma regra burocrática ("toda função deve ter docstring") sem nenhum conteúdo real.
```python
def calcular_total(preco, quantidade):
    """Calcula o total."""         # mandatório: zero informação acrescentada
    return preco * quantidade
```

**Diário de bordo (Journal/Changelog)** — histórico de alterações inline. O git existe exatamente para isso.
```python
# 12/03/2023 - João alterou a alíquota de 12% para 15%
# 05/07/2023 - Maria reverteu para 12%
aliquota = 0.13
```

**Ruído** — comentários óbvios que declaram o que qualquer desenvolvedor vê imediatamente.
```python
# incrementa o contador
contador += 1

# construtor padrão
def __init__(self): ...
```

**Código comentado** — código morto sem explicação do motivo. Cria dúvida: foi removido? vai voltar? está correto?
```python
# if metodo == "pix":
#     taxa = 0.0
# enviar_para_gateway_antigo(valor)
```

**Nonlocal Information** — o comentário descreve o comportamento de outra parte do sistema, longe de onde está.
```python
def calcular_frete(cep_destino):
    # O serviço de CEP opera das 6h às 23h conforme SLA do contrato com os Correios
    # (configurado em config/integracao.yaml linha 47)
    return servico_cep.consultar(cep_destino)
```

---

### A Tensão Fundamental

Há uma tensão real que o Clean Code reconhece: docstrings em APIs públicas (Javadoc, JSDoc, docstrings de módulo Python), quando consumidas por outros times ou geradas como documentação, são valiosas e **recomendadas**. São o contrato da API — descrevem parâmetros, exceções e comportamentos que o código sozinho não deixa explícito.

O problema são os **comentários inline** que explicam código interno confuso. Se o código interno precisa de comentário para ser entendido, a solução correta é reescrever o código — não adicionar o comentário.

**Regra de ouro:**
- **Se o comentário explica *o quê* o código faz** → o código deve ser reescrito. Renomear variáveis e funções quase sempre resolve.
- **Se o comentário explica *por quê* uma decisão foi tomada** → o comentário tem valor genuíno.

```python
# ❌ Explica o "o quê" — o código deveria se explicar
# multiplica o preço pela quantidade e soma ao total
total += item["preco"] * item["quantidade"]

# ✅ Explica o "por quê" — isso não está no código e tem valor
# ISS retido na fonte conforme contrato-padrão (cláusula 7.3, rev. 2025).
# Alíquota de 2% fixada em contrato; não alterar sem validação jurídica.
return valor_bruto * (1 - ALIQUOTA_ISS)
```

> **👉 ATIVIDADE:** Encontre um comentário no código da equipe que poderia ser eliminado com uma renomeação de função ou variável. Traga o exemplo para discussão.

---

## 3. O Problema na Prática

```python
# ❌ Comentário redundante
def calcular_total(preco, quantidade):
    # multiplica preço pela quantidade
    total = preco * quantidade
    # retorna o total
    return total

# ❌ Comentário enganoso
def esta_disponivel(produto):
    # retorna True se o produto NÃO estiver disponível
    return produto["estoque"] > 0  # na verdade retorna True quando ESTÁ disponível

# ❌ Código comentado sem contexto
def processar_pagamento(valor, metodo):
    # if metodo == "pix":
    #     taxa = 0.0
    # enviar_para_gateway_antigo(valor)
    ...

# ❌ TODO sem rastreabilidade
def buscar_usuario(usuario_id):
    # TODO: adicionar cache
    # TODO: melhorar isso depois
    ...

# ❌ Diário de bordo
def calcular_imposto(valor_bruto):
    # 12/03/2023 - João alterou a alíquota de 12% para 15%
    # 05/07/2023 - Maria reverteu para 12%
    aliquota = 0.13
    ...
```

> Arquivo completo: [`exemplos/comentarios_ruins.py`](exemplos/comentarios_ruins.py)

---

## 4. A Solução

```python
# ✅ Sem comentário: o nome já diz tudo
def calcular_total(preco: float, quantidade: int) -> float:
    return preco * quantidade

# ✅ Comentário de intenção: explica a REGRA DE NEGÓCIO
PERCENTUAL_RETENCAO_ISS = 2.0

def calcular_valor_liquido(valor_bruto: float) -> float:
    # ISS retido na fonte conforme contrato-padrão (cláusula 7.3, rev. 2025).
    return valor_bruto * (1 - PERCENTUAL_RETENCAO_ISS / 100)

# ✅ TODO rastreável
def buscar_usuario(usuario_id: str) -> dict:
    # TODO [PLAT-1847]: substituir mock por chamada real ao serviço de usuários.
    # Responsável: @ana.souza  |  Prazo: Sprint 42 (2026-05-05)
    return {"id": usuario_id, "nome": "Usuário Mockado"}

# ✅ Amplificação: destaca algo que passaria despercebido
def pode_cancelar_pedido(pedido: dict) -> bool:
    # IMPORTANTE: usamos timezone UTC em ambos os lados intencionalmente.
    # O campo "criado_em" é sempre gravado em UTC no banco para evitar
    # ambiguidade no horário de verão.
    ...
```

> Arquivo completo: [`exemplos/comentarios_bons.py`](exemplos/comentarios_bons.py)

---

## 5. Equivalentes em Outras Linguagens

### PHP

```php
// ❌ PHPDoc redundante
/**
 * Calcula o total.
 * @param float $preco O preço.
 * @param int $quantidade A quantidade.
 * @return float O total.
 */
function calcularTotal(float $preco, int $quantidade): float {
    return $preco * $quantidade;
}

// ✅ PHPDoc que agrega: documenta exceção e restrição de uso
/**
 * Calcula o valor líquido retendo ISS na fonte.
 * Alíquota fixada em 2% conforme contrato-padrão (cláusula 7.3, rev. 2025).
 * Não use para contratos com ISS variável.
 *
 * @throws \InvalidArgumentException se $valorBruto for negativo.
 */
function calcularValorLiquido(float $valorBruto): float { ... }
```

### TypeScript

```typescript
// ❌ JSDoc desnecessário: TypeScript já documenta os tipos
/**
 * @param preco - O preço do produto.
 * @param quantidade - A quantidade.
 * @returns O total calculado.
 */
function calcularTotal(preco: number, quantidade: number): number {
  return preco * quantidade;
}

// ✅ JSDoc útil: explica o comportamento do arredondamento bancário
/**
 * Aplica arredondamento bancário (half-even) ao valor.
 * 2.5 → 2, 3.5 → 4. Neutraliza viés acumulado em grandes volumes.
 */
function aplicarArredondamentoBancario(valor: number): number { ... }
```

### ADVPL/TLPP

```advpl
// ✅ Cabeçalho Protheus.doc (padrão do ecossistema TDS)
/*/{Protheus.doc} CalcularValorLiquido
    Calcula o valor líquido retendo ISS na fonte conforme contrato-padrão.
    A alíquota de 2% está fixada na cláusula 7.3 do contrato modelo (rev. 2025).

    @author  ana.souza
    @since   14/04/2026
    @param   nValorBruto  Numeric  Valor bruto antes da retenção
    @return  Numeric  Valor após dedução do ISS
/*/
Function CalcularValorLiquido( nValorBruto )
    Local nAliquotaISS := 0.02
Return nValorBruto * ( 1 - nAliquotaISS )
```

> **Nota ADVPL/TLPP:** O cabeçalho `{Protheus.doc}` é gerado pelo TDS e deve ser mantido em funções públicas de negócio. Para funções auxiliares, um comentário de intenção simples é suficiente.

> Arquivos completos: [`exemplos/equivalente.php`](exemplos/equivalente.php) · [`exemplos/equivalente.ts`](exemplos/equivalente.ts) · [`exemplos/equivalente.tlpp`](exemplos/equivalente.tlpp)

---

## 6. Regras de Ouro

- **Comentário bom explica o "porquê"** — não o "o quê" nem o "como"; esses devem estar no próprio código
- **Código comentado vai para o lixo** — o histórico está no git; use `git log` ou `git blame`
- **TODO sem ticket é promessa vazia** — inclua sempre o número do ticket, responsável e prazo
- **Comentário enganoso é pior que nenhum** — quando o comentário mente, o leitor perde a confiança em todos os outros
- **Nomes melhores eliminam comentários** — antes de escrever um comentário, pergunte: "posso refatorar o código para dispensá-lo?"
- **APIs públicas merecem documentação** — docstrings e JSDoc em código exposto a outros times têm valor; em código interno, raramente

---

## 7. Exercício

**Problema 1 (remover/reescrever):** O arquivo de exercício contém funções com comentários redundantes, enganosos e código comentado. Remova o ruído, reescreva os TODOs com rastreabilidade e, quando necessário, renomeie funções e variáveis para tornar o código autodocumentado.

**Problema 2 (adicionar):** O mesmo arquivo contém uma função de cálculo de parcela de financiamento sem nenhum comentário. A fórmula usada tem nome e contexto específicos que o código não consegue expressar. Adicione o comentário correto.

```bash
# Rode o exercício para ver o output esperado:
python exercicios/exercicio.py

# Quando terminar, compare com o gabarito:
python exercicios/gabarito.py
```

> Arquivo: [`exercicios/exercicio.py`](exercicios/exercicio.py)
> Gabarito: [`exercicios/gabarito.py`](exercicios/gabarito.py)

---

## 8. Para se Aprofundar

- **Clean Code**, Robert C. Martin — Capítulo 4: *Comments* (p. 53–74)
- **The Art of Readable Code**, Boswell & Foucher — Capítulo 5: *Knowing What to Comment*
- Ferramenta: [`flake8`](https://flake8.pycqa.org/) com plugin `flake8-bugbear` detecta comentários `# noqa` excessivos e blocos de código comentado
- Conceito: `git blame` e `git log -p -- <arquivo>` substituem completamente os diários de bordo inline

---

> **Próximo tutorial:** [Tutorial 04 — Formatação](../tutorial-04-formatacao/README.md)
