// GABARITO 24 — Fundamentos de Testes de Unidade (Vitest)
// Suíte refatorada: AAA explícito, nomes comportamentais, sem estado
// compartilhado, sem dependência do relógio real.
// Execute: npx vitest run gabarito.ts
import { describe, it, expect } from "vitest";

function calcularComissao(valorVenda: number, metaBatida: boolean): number {
  return metaBatida ? valorVenda * 0.08 : valorVenda * 0.03;
}

describe("calcularComissao", () => {
  it("paga 8% quando bate a meta", () => {
    // Arrange
    const valorVenda = 1000;
    // Act
    const resultado = calcularComissao(valorVenda, true);
    // Assert
    expect(resultado).toBe(80);
  });

  it("paga 3% quando nao bate a meta", () => {
    const resultado = calcularComissao(1000, false);
    expect(resultado).toBe(30);
  });

  it.each([
    [0, true, 0],
    [0, false, 0],
    [500, true, 40],
    [500, false, 15],
    [10_000, true, 800],
  ])("calcula comissao para valor=%i meta=%s", (valorVenda, metaBatida, esperado) => {
    expect(calcularComissao(valorVenda, metaBatida as unknown as boolean)).toBe(esperado);
  });
});
