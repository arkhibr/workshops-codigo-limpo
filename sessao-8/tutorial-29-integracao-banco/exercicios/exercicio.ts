// EXERCÍCIO 29 — Testes de Integração de Banco de Dados (Vitest + better-sqlite3)
// Tempo estimado: 20 minutos
//
// INSTRUÇÕES:
//   A suíte abaixo testa totalGastoPeloCliente(db, clienteId) mas tem os
//   mesmos 3 problemas estruturais de exemplos/equivalente.ts:
//     1. Mocka o próprio acesso a dados — nenhum SQL roda de verdade.
//     2. Depende de um banco em arquivo (teste.db), persistente e nunca
//        limpo entre execuções.
//     3. Sem schema isolado por teste — assume que a tabela e os dados já
//        existem (deixados por uma execução anterior).
//
//   Refatore aplicando os padrões de exemplos/equivalente.ts: beforeEach
//   cria um Database(":memory:") novo por teste, chama criarSchema, e
//   verifica a soma real (e o isolamento entre clientes).
//   Execute: npx vitest run exercicio.ts
//
// Ilustrativo: Vitest não está instalado neste ambiente de workshop.
//
// NOTA DE AUTOCONTENÇÃO: as funções de repositório abaixo são uma cópia
// local do SUT (idênticas a exemplos/equivalente.ts) — o repositório não
// permite que um arquivo importe de outro diretório.
import { it, expect } from "vitest";
import Database from "better-sqlite3";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";

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

function totalGastoPeloClienteRuim(db: Database.Database, clienteId: number): number {
  const pedidos = listarPedidosDoCliente(db, clienteId);
  return pedidos.reduce((soma, p) => soma + p.total, 0);
}

// ❌ 2. Banco em arquivo persistente compartilhado — sem limpeza entre
// execuções. Os dados de uma rodada anterior continuam lá na próxima.
const CAMINHO_BANCO_COMPARTILHADO = path.join(os.tmpdir(), "exercicio_29_teste.db");

it("total gasto soma os pedidos do cliente (mockado)", () => {
  // ❌ 1. Mocka o próprio acesso a dados — nenhum SQL roda. O teste "passa"
  // porque o stub devolve exatamente os dados programados, não porque a
  // query de listarPedidosDoCliente está correta.
  const repositorioFalso = {
    listarPedidosDoCliente: () => [
      { id: 1, cliente_id: 1, total: 30.0, status: "aberto" },
      { id: 2, cliente_id: 1, total: 20.0, status: "aberto" },
    ],
  };

  const total = repositorioFalso
    .listarPedidosDoCliente()
    .reduce((soma, p) => soma + p.total, 0);

  expect(total).toBe(50.0);
});

it("total gasto no banco compartilhado", () => {
  // ❌ 3. Sem schema isolado — assume que a tabela `pedidos` já existe
  // (criada por uma execução anterior deste mesmo teste).
  const db = new Database(CAMINHO_BANCO_COMPARTILHADO);
  db.exec(`
    CREATE TABLE IF NOT EXISTS pedidos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      cliente_id INTEGER NOT NULL,
      total REAL NOT NULL,
      status TEXT NOT NULL DEFAULT 'aberto'
    );
  `);
  inserirPedido(db, 1, 15.0);

  const total = totalGastoPeloClienteRuim(db, 1);

  // ❌ Esse assert só funciona por acaso: o total cresce a cada execução
  // da suíte — não é repetível nem independente.
  expect(total).toBeGreaterThanOrEqual(15.0);
  db.close();
});
