// equivalente.ts — Integração ponta-a-ponta API+Banco em Vitest + supertest + better-sqlite3
// Contra um handler HTTP real que persiste em SQLite :memory: injetado — a
// request percorre a stack real até o banco, e o teste verifica os DOIS
// lados: a resposta HTTP e o estado gravado (relendo via better-sqlite3
// diretamente).
// Execute: npx vitest run equivalente.ts
//
// Ilustrativo: Vitest não está instalado neste ambiente de workshop.
// O objetivo é mostrar o padrão de verificação dos dois lados, não rodar.
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import request from "supertest";
import Database from "better-sqlite3";
import { criarApp } from "./api"; // criarApp(db): recebe a conexão injetada

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

describe("API de Pedidos com persistência (integração vertical)", () => {
  let db: Database.Database;
  let app: ReturnType<typeof criarApp>;

  // ✅ banco :memory: novo por teste, e o app recebe essa mesma conexão —
  // isolamento real entre testes.
  beforeEach(() => {
    db = new Database(":memory:");
    criarSchema(db);
    app = criarApp(db);
  });

  afterEach(() => {
    db.close();
  });

  it("post pedido persiste no banco", async () => {
    const resposta = await request(app)
      .post("/pedidos")
      .send({
        cliente: "Ana",
        itens: [{ produto: "Livro", quantidade: 3, preco_unitario: 10.0 }],
      });

    expect(resposta.status).toBe(201);

    // ✅ verifica o OUTRO lado: o dado realmente foi ao banco
    const linha = db
      .prepare("SELECT cliente, total FROM pedidos WHERE id = ?")
      .get(resposta.body.id) as any;
    expect(linha.cliente).toBe("Ana");
    expect(linha.total).toBe(30.0);
  });

  it("get le pedido persistido", async () => {
    const criado = await request(app)
      .post("/pedidos")
      .send({
        cliente: "Bob",
        itens: [{ produto: "Caneta", quantidade: 2, preco_unitario: 5.0 }],
      });

    const resposta = await request(app).get(`/pedidos/${criado.body.id}`);

    expect(resposta.status).toBe(200);
    expect(resposta.body.total).toBe(10.0);
  });
});

// ❌ Contraponto (anti-padrão, não incluído na suíte acima): "integração
// vertical falsa" — mocka a própria camada de banco, então a request HTTP
// nunca chega a rodar SQL de verdade; e só confere a resposta, nunca o banco.
it("cria pedido com banco mockado (ruim)", async () => {
  // ❌ mocka o acesso a dados — nenhum INSERT roda de verdade
  const dbFalso = {
    inserirPedido: (_cliente: string, _total: number) => 1, // ❌ nunca toca o banco
  };

  const pedidoId = dbFalso.inserirPedido("Ana", 30.0);

  // ❌ só confirma o retorno simulado — nunca relê o banco para confirmar
  // que o pedido foi realmente persistido
  expect(pedidoId).toBe(1);
});
