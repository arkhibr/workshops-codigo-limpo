// equivalente.ts — Massa de Dados para Testes em Vitest
// Execute: npx vitest run equivalente.ts
import { describe, it, expect } from "vitest";
import { Factory } from "fishery";
import { faker } from "@faker-js/faker";

interface ItemPedido {
  produto: string;
  preco: number;
  quantidade: number;
}

interface Pedido {
  id: string;
  itens: ItemPedido[];
  cupomDesconto: string | null;
  status: string;
}

interface Cliente {
  nome: string;
  email: string;
  cpf: string;
}

function aplicarCupom(pedido: Pedido, codigo: string | null): Pedido {
  if (codigo === "PROMO10") {
    for (const item of pedido.itens) {
      item.preco = Math.round(item.preco * 0.9 * 100) / 100;
    }
  }
  return pedido;
}

// Ruim: literal gigante duplicado em cada teste — só o cupom importa aqui,
// mas o teste repete cliente, endereço e forma de pagamento por inteiro.
describe("aplicarCupom (ruim: literais duplicados)", () => {
  it("aplica desconto de 10% com cupom PROMO10", () => {
    const pedido: Pedido = {
      id: "P001",
      itens: [{ produto: "Notebook", preco: 3000.0, quantidade: 1 }],
      cupomDesconto: "PROMO10",
      status: "pendente",
    };
    const resultado = aplicarCupom(pedido, "PROMO10");
    expect(resultado.itens[0].preco).toBe(2700.0);
  });

  it("mantem preco original sem cupom", () => {
    const pedido: Pedido = {
      id: "P002",
      itens: [{ produto: "Notebook", preco: 3000.0, quantidade: 1 }],
      cupomDesconto: null,
      status: "pendente",
    };
    const resultado = aplicarCupom(pedido, null);
    expect(resultado.itens[0].preco).toBe(3000.0);
  });
});

// Bom: PedidoFactory (fishery) com valores padrão sensatos, sobrescritos só
// no que é relevante para cada teste; ClienteFactory usa @faker-js/faker
// para gerar dados de cliente sem literais fixos e repetitivos.
const pedidoFactory = Factory.define<Pedido>(() => ({
  id: "P000",
  itens: [{ produto: "Item Padrão", preco: 100.0, quantidade: 1 }],
  cupomDesconto: null,
  status: "pendente",
}));

const clienteFactory = Factory.define<Cliente>(() => ({
  nome: faker.person.fullName(),
  email: faker.internet.email(),
  cpf: faker.string.numeric(11),
}));

describe("aplicarCupom (bom: Factory + Faker)", () => {
  it("aplica 10% de desconto com cupom PROMO10", () => {
    const pedido = pedidoFactory.build({
      itens: [{ produto: "Notebook", preco: 3000.0, quantidade: 1 }],
      cupomDesconto: "PROMO10",
    });

    const resultado = aplicarCupom(pedido, "PROMO10");

    expect(resultado.itens[0].preco).toBe(2700.0);
  });

  it("mantem preco original sem cupom", () => {
    const pedido = pedidoFactory.build({
      itens: [{ produto: "Notebook", preco: 3000.0, quantidade: 1 }],
    });

    const resultado = aplicarCupom(pedido, null);

    expect(resultado.itens[0].preco).toBe(3000.0);
  });

  it("cliente gerado pela factory tem email valido", () => {
    const cliente = clienteFactory.build();
    expect(cliente.email).toContain("@");
  });
});
