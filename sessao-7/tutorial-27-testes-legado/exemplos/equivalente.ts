// equivalente.ts — Testes de Unidade em Código Legado em Vitest
// Execute: npx vitest run equivalente.ts
import { describe, it, expect } from "vitest";

class ConexaoBancoReal {
  buscarEstoque(_produtoId: string): number {
    throw new Error("Não há banco de dados real disponível neste ambiente");
  }

  atualizarEstoque(_produtoId: string, _quantidade: number, _valorTotal: number): void {
    throw new Error("Não há banco de dados real disponível neste ambiente");
  }
}

class ServicoPrecoExternoReal {
  consultar(_produtoId: string): number {
    throw new Error("Não há serviço de preço real disponível neste ambiente");
  }
}

// Sem seam: GerenciadorEstoqueLegado instancia as dependências reais
// diretamente no construtor — impossível testar em isolamento.
class GerenciadorEstoqueLegado {
  private banco = new ConexaoBancoReal();
  private servicoPrecos = new ServicoPrecoExternoReal();

  recalcularEstoque(produtoId: string, quantidadeVendida: number): number {
    const preco = this.servicoPrecos.consultar(produtoId);
    const estoqueAtual = this.banco.buscarEstoque(produtoId);
    const novoEstoque = estoqueAtual - quantidadeVendida;
    const valorTotal = novoEstoque * preco;
    this.banco.atualizarEstoque(produtoId, novoEstoque, valorTotal);
    return novoEstoque;
  }
}

// Ruim: o único teste possível sem seam documenta a impossibilidade de
// testar em isolamento — falha por falta de infraestrutura real, não por
// um bug de lógica.
it("e impossivel testar sem infraestrutura real", () => {
  expect(() => {
    const gerenciador = new GerenciadorEstoqueLegado();
    gerenciador.recalcularEstoque("PROD1", 10);
  }).toThrow("Não há serviço de preço real disponível neste ambiente");
});

interface ConexaoBanco {
  buscarEstoque(produtoId: string): number;
  atualizarEstoque(produtoId: string, quantidade: number, valorTotal: number): void;
}

interface ServicoPreco {
  consultar(produtoId: string): number;
}

// Bom: seam via injeção de construtor.
class GerenciadorEstoque {
  private cachePrecos: Map<string, number>;

  constructor(
    private banco: ConexaoBanco,
    private servicoPrecos: ServicoPreco,
    cachePrecos?: Map<string, number>,
  ) {
    this.cachePrecos = cachePrecos ?? new Map();
  }

  recalcularEstoque(produtoId: string, quantidadeVendida: number): number {
    let preco = this.cachePrecos.get(produtoId);
    if (preco === undefined) {
      preco = this.servicoPrecos.consultar(produtoId);
      this.cachePrecos.set(produtoId, preco);
    }
    const estoqueAtual = this.banco.buscarEstoque(produtoId);
    const novoEstoque = estoqueAtual - quantidadeVendida;
    const valorTotal = novoEstoque * preco;
    this.banco.atualizarEstoque(produtoId, novoEstoque, valorTotal);
    return novoEstoque;
  }
}

// Fake em memória — também atua como builder do estado inicial (comEstoque).
class BancoEstoqueFake implements ConexaoBanco {
  private estoques = new Map<string, number>();
  ultimoValorTotal: number | null = null;

  comEstoque(produtoId: string, quantidade: number): this {
    this.estoques.set(produtoId, quantidade);
    return this;
  }

  buscarEstoque(produtoId: string): number {
    return this.estoques.get(produtoId) ?? 0;
  }

  atualizarEstoque(produtoId: string, quantidade: number, valorTotal: number): void {
    this.estoques.set(produtoId, quantidade);
    this.ultimoValorTotal = valorTotal;
  }
}

class ServicoPrecoStub implements ServicoPreco {
  chamadas = 0;

  constructor(private preco: number) {}

  consultar(_produtoId: string): number {
    this.chamadas++;
    return this.preco;
  }
}

describe("GerenciadorEstoque", () => {
  it("caracterizacao: recalculo com estoque suficiente", () => {
    // Teste de caracterização: congela o comportamento atual do legado
    // como oráculo, sem julgar se a regra de negócio está correta.
    const banco = new BancoEstoqueFake().comEstoque("PROD1", 100);
    const precos = new ServicoPrecoStub(10.0);
    const gerenciador = new GerenciadorEstoque(banco, precos);

    const novoEstoque = gerenciador.recalcularEstoque("PROD1", 30);

    expect(novoEstoque).toBe(70);
    expect(banco.ultimoValorTotal).toBe(700.0);
  });

  it("recalculo com venda maior que estoque gera saldo negativo", () => {
    // Caso de borda descoberto durante a caracterização: o legado não
    // valida estoque insuficiente. Documentamos o comportamento atual;
    // decidir se corrige é uma decisão de produto, não deste teste.
    const banco = new BancoEstoqueFake().comEstoque("PROD1", 10);
    const precos = new ServicoPrecoStub(5.0);
    const gerenciador = new GerenciadorEstoque(banco, precos);

    const novoEstoque = gerenciador.recalcularEstoque("PROD1", 30);

    expect(novoEstoque).toBe(-20);
  });

  it("recalculo reaproveita preco em cache na segunda chamada", () => {
    const banco = new BancoEstoqueFake().comEstoque("PROD1", 100);
    const precos = new ServicoPrecoStub(10.0);
    const gerenciador = new GerenciadorEstoque(banco, precos);

    gerenciador.recalcularEstoque("PROD1", 10);
    gerenciador.recalcularEstoque("PROD1", 5);

    expect(precos.chamadas).toBe(1);
  });
});
