// EXERCÍCIO 30 — Integração ponta-a-ponta API+Banco (Vitest + supertest + better-sqlite3)
// Tempo estimado: 25 minutos
//
// INSTRUÇÕES:
//   A suíte abaixo testa a rota POST /pedidos/:id/pagar mas tem o mesmo
//   problema estrutural de exemplos/equivalente.ts (anti-padrão 2 do
//   tutorial): só verifica a resposta HTTP — nunca confere o banco. O teste
//   "prova" que a API respondeu com status "pago", mas não prova que o
//   status foi realmente persistido.
//
//   Refatore aplicando o padrão de exemplos/equivalente.ts: depois de
//   chamar a rota, releia o pedido diretamente via better-sqlite3 e confirme
//   que o status "pago" está lá — não só na resposta HTTP.
//   Execute: npx vitest run exercicio.ts
//
// Ilustrativo: Vitest não está instalado neste ambiente de workshop.
//
// NOTA DE AUTOCONTENÇÃO: o schema/rota de pagamento abaixo são uma cópia
// local do SUT (idênticos a exemplos/equivalente.ts, com a rota adicional
// POST /pedidos/:id/pagar) — o repositório não permite que um arquivo
// importe de outro diretório.
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

describe("Exercício 30 (ruim)", () => {
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

  it("paga pedido muda status para pago", async () => {
    const criado = await request(app)
      .post("/pedidos")
      .send({
        cliente: "Ana",
        itens: [{ produto: "Livro", quantidade: 1, preco_unitario: 10.0 }],
      });

    const resposta = await request(app).post(`/pedidos/${criado.body.id}/pagar`);

    // ❌ Só confere a resposta HTTP — nunca relê o banco para confirmar que
    // o status "pago" foi de fato persistido em `pedidos`.
    expect(resposta.status).toBe(200);
    expect(resposta.body.status).toBe("pago");
  });
});
