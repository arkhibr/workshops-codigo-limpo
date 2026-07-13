// EXERCÍCIO 26 — Massa de Dados para Testes (Vitest)
// Tempo estimado: 15 minutos
//
// INSTRUÇÕES:
//   Os testes abaixo duplicam um literal gigante de NotaFiscal em cada teste,
//   mudando só um campo por vez. Extraia uma NotaFiscalFactory (fishery) com
//   valores padrão sensatos e reduza cada teste ao que é relevante.
//   Execute: npx vitest run exercicio.ts
import { it, expect } from "vitest";

interface ItemNota {
  descricao: string;
  valor: number;
}

interface NotaFiscal {
  numero: string;
  emitente: { cnpj: string; razaoSocial: string };
  destinatario: { cpf: string; nome: string };
  itens: ItemNota[];
  aliquota: number;
  chaveAcesso: string;
}

function calcularImposto(notaFiscal: NotaFiscal): number {
  const totalItens = notaFiscal.itens.reduce((soma, item) => soma + item.valor, 0);
  return totalItens * notaFiscal.aliquota;
}

it("calcula imposto com aliquota padrao", () => {
  const nota: NotaFiscal = {
    numero: "NF-001",
    emitente: { cnpj: "11.111.111/0001-11", razaoSocial: "Empresa A" },
    destinatario: { cpf: "111.111.111-11", nome: "Cliente A" },
    itens: [{ descricao: "Produto X", valor: 1000.0 }],
    aliquota: 0.18,
    chaveAcesso: "35260100000000000000000000000000000000000000",
  };
  expect(calcularImposto(nota)).toBe(180.0);
});

it("calcula imposto com aliquota reduzida", () => {
  const nota: NotaFiscal = {
    numero: "NF-002",
    emitente: { cnpj: "11.111.111/0001-11", razaoSocial: "Empresa A" },
    destinatario: { cpf: "111.111.111-11", nome: "Cliente A" },
    itens: [{ descricao: "Produto X", valor: 1000.0 }],
    aliquota: 0.12,
    chaveAcesso: "35260100000000000000000000000000000000000001",
  };
  expect(calcularImposto(nota)).toBe(120.0);
});
