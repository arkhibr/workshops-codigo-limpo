// equivalente.ts — Testes de Integração de API em Vitest + supertest
// Contra um handler HTTP real (Express/Fastify), não um mock de camada
// de aplicação — supertest sobe o servidor em memória e fala HTTP de fato.
// Execute: npx vitest run equivalente.ts
//
// Ilustrativo: Vitest não está instalado neste ambiente de workshop.
// O objetivo é mostrar o padrão de asserção de contrato completo e
// isolamento de estado (beforeEach cria um app novo por teste), não rodar.
import { describe, it, expect, beforeEach } from "vitest";
import request from "supertest";
import { criarApp } from "./api"; // criarApp(): retorna uma instância nova do servidor

describe("API de Pedidos", () => {
  let app: ReturnType<typeof criarApp>;

  // ✅ beforeEach roda antes de CADA teste — app novo, sem estado vazado.
  beforeEach(() => {
    app = criarApp();
  });

  it("cria pedido retorna 201 com total calculado", async () => {
    const resposta = await request(app)
      .post("/pedidos")
      .send({
        cliente: "Ana",
        itens: [{ produto: "Livro", quantidade: 2, preco_unitario: 30.0 }],
      });

    // ✅ Contrato completo: status + corpo, não só o status.
    expect(resposta.status).toBe(201);
    expect(resposta.body.total).toBe(60.0);
    expect(resposta.body.status).toBe("aberto");
  });

  it("busca pedido inexistente retorna 404", async () => {
    const resposta = await request(app).get("/pedidos/999");

    expect(resposta.status).toBe(404);
    expect(resposta.body.detail).toBe("pedido não encontrado");
  });

  it("paga pedido aberto muda status para pago", async () => {
    const criado = await request(app)
      .post("/pedidos")
      .send({
        cliente: "Ana",
        itens: [{ produto: "Livro", quantidade: 1, preco_unitario: 10.0 }],
      });

    const resposta = await request(app).post(`/pedidos/${criado.body.id}/pagar`);

    expect(resposta.status).toBe(200);
    expect(resposta.body.status).toBe("pago");
  });

  it("pagar pedido ja pago retorna 409", async () => {
    const criado = await request(app)
      .post("/pedidos")
      .send({
        cliente: "Ana",
        itens: [{ produto: "Livro", quantidade: 1, preco_unitario: 10.0 }],
      });
    await request(app).post(`/pedidos/${criado.body.id}/pagar`);

    const resposta = await request(app).post(`/pedidos/${criado.body.id}/pagar`);

    expect(resposta.status).toBe(409);
  });
});

// ❌ Contraponto (anti-padrão, não incluído na suíte acima): app compartilhado
// no escopo do módulo, e asserção só de status.
const appCompartilhado = criarApp(); // ❌ vaza estado entre testes

it("cria pedido (ruim)", async () => {
  const resposta = await request(appCompartilhado)
    .post("/pedidos")
    .send({ cliente: "Ana", itens: [{ produto: "Livro", quantidade: 1, preco_unitario: 10.0 }] });
  expect(resposta.status).toBe(201); // ❌ nunca olha o corpo
});
