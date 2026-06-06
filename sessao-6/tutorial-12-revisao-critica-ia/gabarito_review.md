# Gabarito — Revisão Crítica: `codigo_gerado_por_ia.py`

> Simulação de comentários de code review esperados para código gerado por IA.
> Cada entrada segue o formato: **Arquivo:Linha · Categoria · Problema · Como corrigir**.

---

## Problema 1 — Segurança: chave de API hardcoded

**`codigo_gerado_por_ia.py:21`**

**Categoria do checklist:** Segurança

**Por que é problema:**
A constante `API_KEY = "sk-prod-2b7f3e9a4c1d0f6e8a2b5c7d9e1f3a5b"` está diretamente no código-fonte. Qualquer pessoa com acesso ao repositório — incluindo histórico de git — possui a chave de produção. Um `git log` ou `git show` antigo pode expor a chave mesmo depois de removida do HEAD.

IAs tendem a hardcodar segredos porque o prompt não especificou o contrário, e o modelo "sabe" que a função precisa de uma chave — então coloca uma. É o caminho de menor resistência.

**Como corrigir:**
```python
import os
API_KEY = os.environ["GATEWAY_API_KEY"]  # falha explicitamente se não configurada
```
Nunca commitar segredos. Usar `.env` local + biblioteca `python-dotenv` em desenvolvimento; variável de ambiente injetada pelo orquestrador (Kubernetes Secret, AWS Secrets Manager) em produção.

---

## Problema 2 — Segurança: URL montada por concatenação de string

**`codigo_gerado_por_ia.py:86`**

**Categoria do checklist:** Segurança

**Por que é problema:**
```python
url = BASE_URL + "/cobrancas?descricao=" + descricao
```
Se `descricao` for `"../admin"` ou `"foo&outro_param=valor"`, a URL resultante fica malformada ou manipulada. Em APIs que refletem parâmetros de query (logs, analytics), isso pode vazar dados ou modificar o comportamento da requisição sem que o chamador perceba.

Além disso, caracteres como espaço, `#`, `&` e `=` em `descricao` quebram a URL silenciosamente.

**Como corrigir:**
```python
from urllib.parse import urlencode

params = urlencode({"descricao": descricao})
url = f"{BASE_URL}/cobrancas?{params}"
```
Ou, melhor ainda, passar `descricao` no corpo do payload em vez de na query string.

---

## Problema 3 — Lógica invertida na condição de aprovação

**`codigo_gerado_por_ia.py:100`**

**Categoria do checklist:** Correção

**Por que é problema:**
```python
if resposta_bruta.get("status") != "aprovado":   # condição invertida
    return {"ok": True, ...}                       # bloco de SUCESSO
else:
    return {"ok": False, ...}                      # bloco de FALHA
```
A condição `!= "aprovado"` é verdadeira quando o gateway recusa. Porém o bloco `if` retorna `ok=True` e o bloco `else` retorna `ok=False` — exatamente ao contrário. Uma transação aprovada retorna `ok=False`; uma recusada retorna `ok=True`.

A demo exibe esse bug diretamente: o gateway simulado retorna `"aprovado"` e o resultado é `{"ok": false, "erro": "Cobrança recusada: Transação aprovada"}`.

Este é o modo de falha mais silencioso: o código compila, não lança exceção, e o sistema inteiro passa a aceitar cobranças negadas enquanto rejeita aprovadas.

**Como corrigir:**
```python
if resposta_bruta.get("status") == "aprovado":
    return {"ok": True, "codigo_autorizacao": ..., "mensagem": ...}
else:
    return {"ok": False, "erro": f"Cobrança recusada: {resposta_bruta.get('mensagem')}"}
```

---

## Problema 4 — Alucinação: método inexistente

**`codigo_gerado_por_ia.py:124`**

**Categoria do checklist:** Dependências

**Por que é problema:**
```python
return _cliente_http.post_parcelado(url, payload, _montar_headers())
```
O método `post_parcelado` não existe na classe `_GatewayHttpClient`. A IA gerou um nome plausível para uma operação de parcelamento, mas simplesmente inventou o método sem verificar a interface disponível.

Em runtime, isso lança `AttributeError: '_GatewayHttpClient' object has no attribute 'post_parcelado'`. O bug não aparece na demo porque `_cobrar_parcelado` nunca é chamada — mas qualquer integração que tente usar parcelamento quebraria imediatamente.

IAs cometem esse erro com frequência ao trabalhar com SDKs, clientes HTTP e ORMs: o nome gerado é coerente com o padrão da lib, mas o método específico não existe.

**Como corrigir:**
Verificar a documentação/interface do cliente real e usar o método correto. Neste caso, provavelmente seria `_cliente_http.post(url, payload, ...)` com o endpoint de parcelamento já embutido na URL.

---

## Problema 4b — Over-engineering: abstração não pedida

**`codigo_gerado_por_ia.py:113`**

**Categoria do checklist:** A IA entendeu o pedido?

**Por que é problema:**
A função `_cobrar_parcelado` implementa um endpoint dedicado de parcelamento, mas o parâmetro `parcelas` já existe na função `cobrar()`. O prompt original (`prompt_original.md`) pediu uma função de cobrança com suporte a parcelas — não um endpoint separado de parcelamento.

A IA inventou uma abstração que o pedido não pedia: criou uma segunda superfície de API (`_cobrar_parcelado`) que duplica responsabilidade, exige manutenção extra e, neste caso, introduz também o método alucinado `post_parcelado` (Problema 4). Over-engineering e alucinação, neste exemplo, andam juntos.

**Como corrigir:**
Remover `_cobrar_parcelado` e garantir que `cobrar()` lide com o parâmetro `parcelas` já existente. O endpoint de parcelamento, se necessário, deve ser uma decisão explícita do time — não uma abstração espontânea da IA.

---

## Problema 5 — Edge case ausente: valor zero ou negativo

**`codigo_gerado_por_ia.py:65–78`** (função `cobrar`, antes de qualquer validação)

**Categoria do checklist:** Edge cases

**Por que é problema:**
A função `cobrar` não valida se `valor > 0`. Uma chamada com `cobrar(0, ...)` ou `cobrar(-50, ...)` é processada normalmente e enviada ao gateway. Dependendo do gateway real:
- Alguns aceitam valores zero e registram uma "transação de R$ 0,00" que ocupa espaço nos logs e relatórios.
- Alguns aceitam valores negativos, interpretando como estorno automático — bypass na lógica de autorização.
- Outros rejeitam na API e o código recebe um erro que não foi mapeado.

IAs raramente pensam em edge cases não mencionados no prompt — e o prompt original (`prompt_original.md`) não os especificou.

**Como corrigir:**
```python
if valor <= 0:
    raise ValueError(f"Valor da cobrança deve ser positivo. Recebido: {valor}")
```

---

## Problema 6 — Comentário que mente sobre o que o código faz

**`codigo_gerado_por_ia.py:53`**

**Categoria do checklist:** Legibilidade e Coesão

**Por que é problema:**
```python
def _validar_cpf(cpf: str) -> bool:
    """Valida o CPF do titular do cartão conforme regras da Receita Federal."""
    cpf_limpo = cpf.replace(".", "").replace("-", "")
    return len(cpf_limpo) == 11 and cpf_limpo.isdigit()
```
A docstring afirma validação "conforme regras da Receita Federal", mas o código apenas verifica se a string tem exatamente 11 dígitos. CPFs como `"00000000000"`, `"11111111111"` e `"12345678901"` passam na validação — mas são todos inválidos pelo algoritmo real (módulo 11 com dois dígitos verificadores).

O nome `_validar_cpf` também indica um comportamento mais completo do que é entregue.

Este é o modo de falha mais insidioso: a confiança no código é maior do que deveria. Qualquer chamador assume que um CPF que passou em `_validar_cpf` é juridicamente válido — o que é falso.

**Como corrigir:**
Ou implementar o algoritmo completo da Receita Federal, ou ser honesto no nome e na docstring:
```python
def _cpf_tem_formato_basico(cpf: str) -> bool:
    """Verifica apenas se o CPF tem 11 dígitos. NÃO valida os dígitos verificadores."""
    cpf_limpo = cpf.replace(".", "").replace("-", "")
    return len(cpf_limpo) == 11 and cpf_limpo.isdigit()
```

---

> **Total: 6 problemas plantados** (+ 1 entrada de aprofundamento: Problema 4b)
> Distribuição: 2 Segurança · 1 Correção (lógica) · 1 Dependências (alucinação) · 1 Edge cases · 1 Legibilidade e Coesão (comentário que mente)
> Problema 4b (over-engineering) aprofunda o Problema 4 sob a categoria "A IA entendeu o pedido?" — não é um sétimo problema plantado.
>
> Referência cruzada com `checklist_revisao_ia.md`: todos os 6 problemas têm categoria mapeada no checklist.
