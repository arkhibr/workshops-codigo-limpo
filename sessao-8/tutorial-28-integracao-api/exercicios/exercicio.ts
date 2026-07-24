// EXERCÍCIO 28 — Testes de Integração de API (Vitest + supertest)
// Tempo estimado: 20 minutos
//
// INSTRUÇÕES:
//   A suíte abaixo testa POST /pedidos/{id}/pagar mas tem 3 problemas
//   estruturais (os mesmos de exemplos/equivalente.ts):
//     1. App compartilhado no escopo do módulo (estado vaza).
//     2. Só verifica resposta.status — nunca olha o corpo da resposta.
//     3. Ordem importa — um teste assume que o pedido criado por outro
//        teste ainda existe, com o id que ele espera.
//
//   Refatore aplicando os padrões de exemplos/equivalente.ts: beforeEach
//   cria um app novo por teste, nomes comportamentais, e asserções sobre
//   o contrato completo (status + corpo).
//   Execute: npx vitest run exercicio.ts (deve passar antes e depois da refatoração)
//
// Ilustrativo: Vitest não está instalado neste ambiente de workshop.
import { it, expect } from "vitest";
import request from "supertest";
import { criarApp } from "./api";

// ❌ 1. App compartilhado — o mesmo servidor e os mesmos pedidos são
// reaproveitados por todos os testes do módulo.
const app = criarApp();

it("cria pedido para pagar depois", async () => {
  // ❌ 2. Só checa o status — não confirma id, total ou status "aberto".
  const resposta = await request(app)
    .post("/pedidos")
    .send({
      cliente: "Bruno",
      itens: [{ produto: "Caneta", quantidade: 3, preco_unitario: 5.0 }],
    });
  expect(resposta.status).toBe(201);
});

it("paga pedido", async () => {
  // ❌ 3. Ordem importa: assume que o pedido id=1, criado pelo teste
  // anterior via `app` compartilhado, ainda existe e está "aberto".
  const resposta = await request(app).post("/pedidos/1/pagar");
  expect(resposta.status).toBe(200);
});

it("pagar pedido novamente falha", async () => {
  // ❌ 3 (de novo): depende do teste anterior já ter pago o pedido id=1.
  const resposta = await request(app).post("/pedidos/1/pagar");
  expect(resposta.status).toBe(409);
});
