// equivalente.ts — Testes de Integração de Banco de Dados em Vitest + better-sqlite3
// Cria um banco SQLite em memória (:memory:) por teste — SQL, constraints
// (FK, CHECK) e transações reais são exercitados, não simulados.
// Execute: npx vitest run equivalente.ts
//
// Ilustrativo: Vitest não está instalado neste ambiente de workshop.
// O objetivo é mostrar o padrão de isolamento (beforeEach cria uma conexão
// nova por teste) e a verificação de efeitos colaterais reais no banco, não rodar.
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

function buscarPedido(db: Database.Database, pedidoId: number) {
  return db
    .prepare("SELECT id, cliente_id, total, status FROM pedidos WHERE id = ?")
    .get(pedidoId);
}

describe("Repositório de Pedidos (integração com SQLite real)", () => {
  let db: Database.Database;

  // ✅ beforeEach roda antes de CADA teste — banco :memory: novo, sem
  // estado vazado entre testes (isolamento real).
  beforeEach(() => {
    db = new Database(":memory:");
    criarSchema(db);
  });

  it("insere e recupera pedido do cliente", () => {
    const clienteId = inserirCliente(db, "Ana", true);
    const pedidoId = inserirPedido(db, clienteId, 90.0);

    const pedido = buscarPedido(db, pedidoId) as any;

    expect(pedido.cliente_id).toBe(clienteId);
    expect(pedido.total).toBe(90.0);
    expect(pedido.status).toBe("aberto");
  });

  it("rejeita pedido com cliente inexistente", () => {
    expect(() => inserirPedido(db, 999, 10.0)).toThrow();
  });

  it("rejeita pedido com total negativo", () => {
    const clienteId = inserirCliente(db, "Ana");
    expect(() => inserirPedido(db, clienteId, -5.0)).toThrow();
  });
});

// ❌ Contraponto (anti-padrão, não incluído na suíte acima): mocka o próprio
// acesso a dados — nenhum SQL roda, então uma constraint violada nunca
// seria detectada.
const repositorioFalso = {
  inserirPedido: (_clienteId: number, _total: number) => 1, // ❌ nunca toca o banco
};

it("insere pedido (ruim, mockado)", () => {
  const pedidoId = repositorioFalso.inserirPedido(999, -50.0);
  expect(pedidoId).toBe(1); // ❌ não prova que o banco aceitaria isso
});
