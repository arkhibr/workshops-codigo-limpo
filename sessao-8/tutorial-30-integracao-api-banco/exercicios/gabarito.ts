// GABARITO 30 — Integração ponta-a-ponta API+Banco (Vitest + supertest + better-sqlite3)
// Suíte refatorada: além de conferir a resposta HTTP, relê o pedido
// diretamente via better-sqlite3 para confirmar que o status "pago" foi
// realmente persistido — verificando os DOIS lados, não só o contrato HTTP.
// Execute: npx vitest run gabarito.ts
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import request from "supertest";
import Database from "better-sqlite3";
import { criarApp } from "./api";

function criarSchema(db: Database.Database): void {
  db.exec(`
    CREATE TABLE IF NOT EXISTS pedidos (
      id      INTEGER PRIMARY KEY AUTOINCREMENT,
      cliente TEXT    NOT NULL,
      total   REAL    NOT NULL CHECK (total >= 0),
      status  TEXT    NOT NULL DEFAULT 'aberto'
    );
  `);
}

describe("Gabarito 30", () => {
  let db: Database.Database;
  let app: ReturnType<typeof criarApp>;

  beforeEach(() => {
    db = new Database(":memory:");
    criarSchema(db);
    app = criarApp(db);
  });

  afterEach(() => {
    db.close();
  });

  async function criaPedidoAberto() {
    return request(app)
      .post("/pedidos")
      .send({
        cliente: "Ana",
        itens: [{ produto: "Livro", quantidade: 1, preco_unitario: 10.0 }],
      });
  }

  it("paga pedido persiste status pago no banco", async () => {
    const criado = await criaPedidoAberto();

    const resposta = await request(app).post(`/pedidos/${criado.body.id}/pagar`);

    expect(resposta.status).toBe(200);
    expect(resposta.body.status).toBe("pago");

    // ✅ verifica o OUTRO lado: o status "pago" foi realmente gravado
    const linha = db
      .prepare("SELECT status FROM pedidos WHERE id = ?")
      .get(criado.body.id) as any;
    expect(linha.status).toBe("pago");
  });

  it("paga pedido inexistente retorna 404", async () => {
    const resposta = await request(app).post("/pedidos/999/pagar");
    expect(resposta.status).toBe(404);
  });

  it("paga pedido ja pago retorna 409 e nao altera banco", async () => {
    const criado = await criaPedidoAberto();
    await request(app).post(`/pedidos/${criado.body.id}/pagar`);

    const resposta = await request(app).post(`/pedidos/${criado.body.id}/pagar`);

    expect(resposta.status).toBe(409);
    // ✅ confirma que o banco continua com status "pago" (não foi
    // corrompido pela segunda tentativa de pagamento)
    const linha = db
      .prepare("SELECT status FROM pedidos WHERE id = ?")
      .get(criado.body.id) as any;
    expect(linha.status).toBe("pago");
  });
});
