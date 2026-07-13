// EXERCÍCIO 24 — Fundamentos de Testes de Unidade (Vitest)
// Tempo estimado: 15 minutos
//
// INSTRUÇÕES:
//   A suíte abaixo testa calcularComissao() mas tem 4 problemas:
//     1. Nomes que não dizem o que é testado (test1, test2, testComissao)
//     2. Um teste verificando comportamentos não relacionados
//     3. Estado compartilhado (módulo) entre testes (ordem importa)
//     4. Dependência do relógio real (não-determinístico)
//
//   Refatore aplicando AAA, FIRST e nomes comportamentais. Use
//   it.each para as variações de valor/meta.
//   Execute: npx vitest run exercicio.ts (deve passar antes e depois da refatoração)
import { it, expect } from "vitest";

let ultimaComissao: number | null = null; // estado compartilhado entre testes

function calcularComissao(valorVenda: number, metaBatida: boolean): number {
  return metaBatida ? valorVenda * 0.08 : valorVenda * 0.03;
}

it("test1", () => {
  // dois comportamentos não relacionados no mesmo teste
  expect(calcularComissao(1000, true)).toBe(80);
  expect(calcularComissao(1000, false)).toBe(30);
});

it("test2", () => {
  // depende de estado deixado por outro teste — ordem de execução importa
  ultimaComissao = calcularComissao(500, true);
  expect(ultimaComissao).toBe(40);
});

it("testComissao", () => {
  // nome genérico; não-determinístico: depende do dia real da execução
  const hoje = new Date();
  const metaBatida = hoje.getDay() === 1; // segunda-feira
  const resultado = calcularComissao(1000, metaBatida);
  expect(resultado).toBeGreaterThanOrEqual(0);
});
