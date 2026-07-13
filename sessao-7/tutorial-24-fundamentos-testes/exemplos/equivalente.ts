// equivalente.ts — Fundamentos de Testes de Unidade em Vitest
// Execute: npx vitest run equivalente.ts
import { describe, it, expect } from "vitest";

function calcularDesconto(valor: number, clienteVip: boolean): number {
  return clienteVip ? valor * 0.9 : valor;
}

function calcularFrete(valor: number): number {
  return valor > 200 ? 0 : 25;
}

// Ruim: nome genérico, duas asserções não relacionadas
it("test1", () => {
  expect(calcularDesconto(100, true)).toBe(90);
  expect(calcularFrete(100)).toBe(25);
});

// Bom: describe/it aninhados, nomes comportamentais, it.each para parametrização
describe("calcularDesconto", () => {
  it("aplica 10% de desconto para cliente vip", () => {
    // Arrange
    const valor = 100;
    // Act
    const resultado = calcularDesconto(valor, true);
    // Assert
    expect(resultado).toBe(90);
  });

  it.each([
    [0, true, 0],
    [100, false, 100],
    [200, true, 180],
  ])("calcula desconto para valor=%i vip=%s", (valor, vip, esperado) => {
    expect(calcularDesconto(valor, vip as unknown as boolean)).toBe(esperado);
  });
});
