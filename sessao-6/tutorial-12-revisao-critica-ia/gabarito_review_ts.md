# Gabarito — Revisão Crítica: `codigo_gerado_por_ia.ts`

> Equivalente TypeScript de `gabarito_review.md`.
> Cada comentário segue o formato: **Linha · Categoria do checklist · Problema · Por que é sutil · Como corrigir**.

---

## Defeito 1 — API/método alucinado

**Linha 193 — Categoria: Dependências/alucinação**

`(gateway as any).verificarIdempotencia(transacaoId)` chama um método que não
existe na classe `GatewaySimulado` (nem na SDK real do provedor versão 3.x). O
`as any` é um sinal de alerta — em TS estrito ele é necessário precisamente
porque o método não existe no tipo declarado.

**Por que é sutil:** o ramo está numa guarda `if (valor <= 0)` que o demo não
exercita. O TypeScript sequer reclama em tempo de compilação porque o `as any`
suprime a checagem. O erro só aparece em produção ao estornar com valor inválido.

**Como corrigir:** verificar a documentação da SDK. Se a funcionalidade existe,
usar o método correto e tipado. Se não existe, implementar localmente com um
`Set<string>` de IDs já processados.

---

## Defeito 2 — Lógica confiante-mas-errada (off-by-one)

**Linha 129 — Categoria: Correção**

```typescript
for (let i = 1; i < numParcelas; i++) {  // gera [1, 2] para numParcelas=3
```

Para 3 parcelas, `i < 3` gera índices `[1, 2]` — a terceira parcela nunca é
criada. A saída da demo já deixa visível: "2 (de 3 solicitadas)".

**Por que é sutil:** o cálculo de `valorParcela` com juros compostos está
correto; a estrutura do loop está idiomática. O `<` vs `<=` é um detalhe de
um caractere que passa facilmente em leitura rápida.

**Como corrigir:**
```typescript
for (let i = 1; i <= numParcelas; i++) {
```

---

## Defeito 3 — Segurança sutil (comparação não constant-time)

**Linha 149 — Categoria: Segurança**

```typescript
return assinaturaEsperada === assinaturaRecebida;
```

A comparação de strings com `===` em JavaScript encerra a comparação no
primeiro caractere diferente, expondo um timing side-channel. Um atacante pode
medir o tempo de resposta para adivinhar a assinatura byte a byte.

**Por que é sutil:** a função tem nome claro, parâmetros tipados e a lógica de
geração da assinatura está correta. O defeito está apenas no operador de
comparação — uma linha que parece idiomática.

**Como corrigir:** usar `crypto.timingSafeEqual()` com buffers:
```typescript
import * as crypto from "crypto";
const a = Buffer.from(assinaturaEsperada, "hex");
const b = Buffer.from(assinaturaRecebida, "hex");
return a.length === b.length && crypto.timingSafeEqual(a, b);
```

> Nota: o Tutorial 14 aprofunda segurança em código gerado por IA. Este
> defeito é a introdução ao tema.

---

## Defeito 4 — Edge case ausente (valor zero/negativo)

**Linha 173 (console.log), linha 175 (gateway.cobrar) — Categoria: Edge cases**

`cobrar()` não valida se `cobranca.valor` é positivo. Chamar com `valor: -50`
executa sem erro e registra uma transação inválida no gateway simulado.

**Por que é sutil:** a função tem tipagem completa (`number` aceita negativos),
JSDoc detalhado e log de auditoria — parece defensiva. A ausência da guarda
de valor não salta aos olhos porque tudo ao redor está bem cuidado.

**Como corrigir:**
```typescript
if (cobranca.valor <= 0) {
  throw new Error(`Valor deve ser positivo; recebido: ${cobranca.valor}`);
}
```

---

## Defeito 5 — Over-engineering (factory desnecessária)

**Linhas 15–36 (comentário + classe) — Categoria: Legibilidade/Coesão**

`GerenciadorDeProcessamento` é uma factory/strategy que não foi pedida. O
requisito original era apenas três funções: `cobrar`, `estornar`,
`consultarStatus`. A classe adiciona ~20 linhas de abstração, um `enum` extra
e um método `processar` que delega diretamente para as funções livres — sem
nenhum comportamento próprio.

**Por que é sutil:** o padrão strategy é reconhecível e "parece correto" para
múltiplos tipos de pagamento. A abstração não quebra nada; apenas acrescenta
complexidade sem valor para o pedido atual.

**Como corrigir:** remover `GerenciadorDeProcessamento` e `TipoProcessador`.
Manter apenas as funções livres `cobrar`, `estornar`, `consultarStatus`. Se
o roteamento por tipo for necessário no futuro, introduzir a abstração então.

---

## Defeito 6 — Docstring que mente

**Linha 166 (JSDoc de `cobrar`) — Categoria: Legibilidade/Coesão**

```typescript
/**
 * Valida o CPF do cliente e garante idempotência via pedidoId antes de
 * submeter ao gateway.
 */
```

O corpo da função não valida CPF nem garante idempotência. O `pedidoId` é
apenas repassado ao gateway sem nenhuma verificação de duplicidade.

**Por que é sutil:** o JSDoc está bem escrito, profissional e descreve
comportamentos desejáveis. Em uma revisão rápida, é tentador assumir que se
está documentado, está implementado.

**Como corrigir:** ou implementar a validação prometida, ou corrigir o JSDoc:
```typescript
/** Submete uma cobrança ao gateway e retorna o resultado. */
```

---

> **Total: 6 defeitos**
> Distribuição: 1 Alucinação · 1 Correção · 1 Segurança · 1 Edge case · 1 Over-engineering · 1 Docstring
