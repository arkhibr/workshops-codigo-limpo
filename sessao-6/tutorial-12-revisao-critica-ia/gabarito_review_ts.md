# Gabarito — Revisão Crítica: `codigo_gerado_por_ia.ts`

> Equivalente TypeScript do `gabarito_review.md`. Problemas mapeados 1:1 com a versão Python.
> Cada entrada segue o formato: **Arquivo:Linha · Categoria · Problema · Como corrigir**.

---

## Problema 1 — Segurança: chave de API hardcoded

**`codigo_gerado_por_ia.ts:15`**

**Categoria do checklist:** Segurança

**Por que é problema:**
```typescript
const API_KEY = "sk-prod-2b7f3e9a4c1d0f6e8a2b5c7d9e1f3a5b";
```
Idêntico ao problema Python: a chave de produção está no código-fonte e será exposta em qualquer repositório — incluindo histórico de git e forks privados.

**Como corrigir:**
```typescript
const API_KEY = process.env.GATEWAY_API_KEY;
if (!API_KEY) throw new Error("Variável de ambiente GATEWAY_API_KEY não configurada.");
```

---

## Problema 2 — Segurança: URL montada por concatenação de string

**`codigo_gerado_por_ia.ts:93`**

**Categoria do checklist:** Segurança

**Por que é problema:**
```typescript
const url = BASE_URL + "/cobrancas?descricao=" + descricao;
```
Se `descricao` contiver caracteres especiais (`&`, `=`, `#`, `../`), a URL fica malformada ou manipulada. O TypeScript não oferece nenhuma proteção extra aqui — o comportamento é idêntico ao Python.

**Como corrigir:**
```typescript
const params = new URLSearchParams({ descricao });
const url = `${BASE_URL}/cobrancas?${params.toString()}`;
```
Ou mover `descricao` para o corpo da requisição (`payload`), onde não há risco de injeção via query string.

---

## Problema 3 — Lógica invertida na condição de aprovação

**`codigo_gerado_por_ia.ts:107`**

**Categoria do checklist:** Correção

**Por que é problema:**
```typescript
if (respostaBruta.status !== "aprovado") {   // condição invertida
  return { ok: true, ... };                   // bloco de SUCESSO
} else {
  return { ok: false, ... };                  // bloco de FALHA
}
```
Mesma inversão da versão Python: `!== "aprovado"` é verdadeiro quando o gateway recusa, mas o bloco retorna `ok: true`. A demo exibe o bug: o simulador retorna `"aprovado"` e o resultado é `{ ok: false }`.

**Como corrigir:**
```typescript
if (respostaBruta.status === "aprovado") {
  return { ok: true, codigoAutorizacao: respostaBruta.codigoAutorizacao, mensagem: respostaBruta.mensagem };
} else {
  return { ok: false, erro: `Cobrança recusada: ${respostaBruta.mensagem}` };
}
```

---

## Problema 4 — Alucinação: método inexistente

**`codigo_gerado_por_ia.ts:136`**

**Categoria do checklist:** Dependências

**Por que é problema:**
```typescript
return (clienteHttp as any).postParcelado(url, payload, montarHeaders());
```
O método `postParcelado` não existe na classe `GatewayHttpClient`. O cast `as any` é o indício: ele foi necessário exatamente porque o TypeScript apontou o erro em tempo de compilação. Em produção, qualquer chamada a `cobrarParcelado` lançaria `TypeError: clienteHttp.postParcelado is not a function`.

O cast `as any` em código de IA muitas vezes é sinal de que o modelo tentou contornar uma inconsistência que ele próprio criou.

A função não é chamada pela demo, por isso o erro não aparece na execução normal.

**Como corrigir:**
Verificar a interface real do cliente HTTP e usar o método correto. Remover o `as any` — se o TypeScript reclamar, o problema está no design, não no compilador.

---

## Problema 4b — Over-engineering: abstração não pedida

**`codigo_gerado_por_ia.ts:121`**

**Categoria do checklist:** A IA entendeu o pedido?

**Por que é problema:**
A função `cobrarParcelado` implementa um endpoint dedicado de parcelamento, mas o parâmetro `parcelas` já existe na função `cobrar()`. O prompt original (`prompt_original.md`) pediu uma função de cobrança com suporte a parcelas — não um endpoint separado de parcelamento.

A IA inventou uma abstração que o pedido não pedia: criou uma segunda superfície de API (`cobrarParcelado`) que duplica responsabilidade, exige manutenção extra e, neste caso, introduz também o método alucinado `postParcelado` (Problema 4). Over-engineering e alucinação, neste exemplo, andam juntos.

**Como corrigir:**
Remover `cobrarParcelado` e garantir que `cobrar()` lide com o parâmetro `parcelas` já existente. O endpoint de parcelamento, se necessário, deve ser uma decisão explícita do time — não uma abstração espontânea da IA.

---

## Problema 5 — Edge case ausente: valor zero ou negativo

**`codigo_gerado_por_ia.ts:71–84`** (função `cobrar`, antes de qualquer validação)

**Categoria do checklist:** Edge cases

**Por que é problema:**
A função `cobrar` não verifica se `valor > 0`. Uma chamada com `cobrar(0, ...)` ou `cobrar(-50, ...)` é processada normalmente. O tipo `number` do TypeScript não impede valores não positivos — a validação precisaria ser explícita.

Mesmo comportamento e mesmo risco da versão Python: dependendo do gateway real, valores zero ou negativos podem causar desde registros espúrios até bypasses de autorização.

**Como corrigir:**
```typescript
if (valor <= 0) {
  throw new Error(`Valor da cobrança deve ser positivo. Recebido: ${valor}`);
}
```

---

## Problema 6 — Comentário que mente sobre o que o código faz

**`codigo_gerado_por_ia.ts:51`**

**Categoria do checklist:** Legibilidade e Coesão

**Por que é problema:**
```typescript
/** Valida o CPF do titular do cartão conforme regras da Receita Federal. */
function validarCpf(cpf: string): boolean {
  const cpfLimpo = cpf.replace(/[.\-]/g, "");
  return cpfLimpo.length === 11 && /^\d+$/.test(cpfLimpo);
}
```
A JSDoc afirma validação "conforme regras da Receita Federal", mas o código apenas verifica comprimento e se são dígitos. CPFs com todos os dígitos iguais (`"11111111111"`) ou sequências simples (`"12345678901"`) passam — mas são todos inválidos pelo algoritmo real.

**Como corrigir:**
Ou implementar o algoritmo completo (módulo 11 com dois dígitos verificadores), ou ser honesto na assinatura:
```typescript
/** Verifica apenas se o CPF tem 11 dígitos. NÃO valida os dígitos verificadores. */
function cpfTemFormatoBasico(cpf: string): boolean { ... }
```

---

> **Total: 6 problemas plantados** (+ 1 entrada de aprofundamento: Problema 4b)
> Distribuição: 2 Segurança · 1 Correção (lógica) · 1 Dependências (alucinação) · 1 Edge cases · 1 Legibilidade e Coesão (comentário que mente)
> Problema 4b (over-engineering) aprofunda o Problema 4 sob a categoria "A IA entendeu o pedido?" — não é um sétimo problema plantado.
>
> Mapeamento 1:1 com `gabarito_review.md`: mesmos 6 modos de falha, mesmas categorias do checklist, linhas correspondentes na versão TypeScript.
