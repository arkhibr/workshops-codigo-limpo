// GABARITO 29 — Testes de Integração de Banco de Dados (Vitest + better-sqlite3)
// Suíte refatorada: beforeEach cria um Database(":memory:") novo por teste,
// schema isolado, e verificação da soma real (SQL de verdade) — sem mock,
// sem arquivo compartilhado.
// Execute: npx vitest run gabarito.ts
import { describe, it, expect, beforeEach } from "vitest";
import Database from "better-sqlite3";

function criarSchema(db: Database.Database): void {
  db.pragma("foreign_keys = ON");
  db.exec(`
    CREATE TABLE clientes (
      id   INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT    NOT NULL,
      vip  INTEGER NOT NULL DEFAULT 0
    );
    CREATE TABLE pedidos (
      id         INTEGER PRIMARY KEY AUTOINCREMENT,
      cliente_id INTEGER NOT NULL REFERENCES clientes(id),
      total      REAL    NOT NULL CHECK (total >= 0),
      status     TEXT    NOT NULL DEFAULT 'aberto'
    );
  `);
}

function inserirCliente(db: Database.Database, nome: string, vip = false): number {
  const info = db
    .prepare("INSERT INTO clientes (nome, vip) VALUES (?, ?)")
    .run(nome, vip ? 1 : 0);
  return Number(info.lastInsertRowid);
}

function inserirPedido(db: Database.Database, clienteId: number, total: number): number {
  const info = db
    .prepare("INSERT INTO pedidos (cliente_id, total) VALUES (?, ?)")
    .run(clienteId, total);
  return Number(info.lastInsertRowid);
}

function listarPedidosDoCliente(db: Database.Database, clienteId: number): any[] {
  return db
    .prepare("SELECT id, cliente_id, total, status FROM pedidos WHERE cliente_id = ?")
    .all(clienteId);
}

function totalGastoPeloCliente(db: Database.Database, clienteId: number): number {
  const pedidos = listarPedidosDoCliente(db, clienteId);
  return pedidos.reduce((soma, p) => soma + p.total, 0);
}

describe("totalGastoPeloCliente (integração com SQLite real)", () => {
  let db: Database.Database;

  // ✅ beforeEach roda antes de CADA teste — banco :memory: novo, sem
  // estado vazado entre testes.
  beforeEach(() => {
    db = new Database(":memory:");
    criarSchema(db);
  });

  it("soma os pedidos do cliente", () => {
    const clienteId = inserirCliente(db, "Ana");
    inserirPedido(db, clienteId, 30.0);
    inserirPedido(db, clienteId, 20.0);

    const total = totalGastoPeloCliente(db, clienteId);

    expect(total).toBe(50.0);
  });

  it("e zero para cliente sem pedidos", () => {
    const clienteId = inserirCliente(db, "Ana");

    const total = totalGastoPeloCliente(db, clienteId);

    expect(total).toBe(0.0);
  });

  it("nao soma pedidos de outro cliente", () => {
    const ana = inserirCliente(db, "Ana");
    const bob = inserirCliente(db, "Bob");
    inserirPedido(db, ana, 30.0);
    inserirPedido(db, bob, 100.0);

    const totalAna = totalGastoPeloCliente(db, ana);

    expect(totalAna).toBe(30.0);
  });
});
