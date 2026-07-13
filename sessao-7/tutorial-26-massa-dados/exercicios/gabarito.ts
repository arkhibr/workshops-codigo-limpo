// GABARITO 26 — Massa de Dados para Testes (Vitest)
// NotaFiscalFactory (fishery) centraliza valores padrão sensatos (emitente,
// destinatario, item e aliquota fixos) e cada teste sobrescreve só o campo
// que varia — a alíquota.
// Execute: npx vitest run gabarito.ts
import { describe, it, expect } from "vitest";
import { Factory } from "fishery";

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

const notaFiscalFactory = Factory.define<NotaFiscal>(() => ({
  numero: "NF-000",
  emitente: { cnpj: "11.111.111/0001-11", razaoSocial: "Empresa A" },
  destinatario: { cpf: "111.111.111-11", nome: "Cliente A" },
  itens: [{ descricao: "Produto X", valor: 1000.0 }],
  aliquota: 0.18,
  chaveAcesso: "35260100000000000000000000000000000000000000",
}));

describe("calcularImposto", () => {
  it("calcula imposto com aliquota padrao", () => {
    const nota = notaFiscalFactory.build();
    expect(calcularImposto(nota)).toBe(180.0);
  });

  it("calcula imposto com aliquota reduzida", () => {
    const nota = notaFiscalFactory.build({ aliquota: 0.12 });
    expect(calcularImposto(nota)).toBe(120.0);
  });
});
