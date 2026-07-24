// GABARITO 28 — Testes de Integração de API (Vitest + supertest)
// Suíte refatorada: beforeEach cria um app novo por teste, nomes
// comportamentais, contrato completo verificado (status + corpo), sem
// dependência de ordem.
// Execute: npx vitest run gabarito.ts
import { describe, it, expect, beforeEach } from "vitest";
import request from "supertest";
import { criarApp } from "./api";

describe("POST /pedidos/:id/pagar", () => {
  let app: ReturnType<typeof criarApp>;

  // ✅ beforeEach roda antes de CADA teste — app novo, sem estado vazado.
  beforeEach(() => {
    app = criarApp();
  });

  async function criaPedidoAberto() {
    const resposta = await request(app)
      .post("/pedidos")
      .send({
        cliente: "Bruno",
        itens: [{ produto: "Caneta", quantidade: 3, preco_unitario: 5.0 }],
      });
    return resposta.body;
  }

  it("cria pedido retorna 201 com status aberto", async () => {
    const resposta = await request(app)
      .post("/pedidos")
      .send({
        cliente: "Bruno",
        itens: [{ produto: "Caneta", quantidade: 3, preco_unitario: 5.0 }],
      });

    expect(resposta.status).toBe(201);
    expect(resposta.body.total).toBe(15.0);
    expect(resposta.body.status).toBe("aberto");
  });

  it("paga pedido aberto muda status para pago", async () => {
    const pedido = await criaPedidoAberto();

    const resposta = await request(app).post(`/pedidos/${pedido.id}/pagar`);

    expect(resposta.status).toBe(200);
    expect(resposta.body.status).toBe("pago");
  });

  it("pagar pedido ja pago retorna 409", async () => {
    const pedido = await criaPedidoAberto();
    await request(app).post(`/pedidos/${pedido.id}/pagar`);

    const resposta = await request(app).post(`/pedidos/${pedido.id}/pagar`);

    expect(resposta.status).toBe(409);
  });

  it("pagar pedido inexistente retorna 404", async () => {
    const resposta = await request(app).post("/pedidos/999/pagar");

    expect(resposta.status).toBe(404);
  });
});
