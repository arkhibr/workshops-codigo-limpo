// GABARITO 25 — Dublês de Teste (Vitest)
// Seam via construtor: ServicoEntrega(apiCep, repositorio). ApiCepStub
// devolve cidade/uf fixos; RepositorioEnderecoFake guarda em memória e
// expõe foiSalvo() para inspeção. Sem delays — roda em milissegundos.
// Execute: npx vitest run gabarito.ts
import { describe, it, expect } from "vitest";

interface Endereco {
  cep: string;
  cidade: string;
  uf: string;
}

interface ApiCep {
  consultar(cep: string): Endereco;
}

interface RepositorioEndereco {
  salvar(pedidoId: string, endereco: Endereco): void;
}

class ServicoEntrega {
  constructor(
    private apiCep: ApiCep,
    private repositorio: RepositorioEndereco,
  ) {}

  confirmarEndereco(pedidoId: string, cep: string): Endereco {
    const endereco = this.apiCep.consultar(cep);
    this.repositorio.salvar(pedidoId, endereco);
    return endereco;
  }
}

// Stub: devolve resposta fixa e pré-programada, sem chamada de rede real.
class ApiCepStub implements ApiCep {
  constructor(
    private cidade: string = "São Paulo",
    private uf: string = "SP",
  ) {}

  consultar(cep: string): Endereco {
    return { cep, cidade: this.cidade, uf: this.uf };
  }
}

// Fake: implementação funcional leve, em memória — sem banco real.
class RepositorioEnderecoFake implements RepositorioEndereco {
  private enderecos = new Map<string, Endereco>();

  salvar(pedidoId: string, endereco: Endereco): void {
    this.enderecos.set(pedidoId, endereco);
  }

  foiSalvo(pedidoId: string): boolean {
    return this.enderecos.has(pedidoId);
  }
}

describe("ServicoEntrega", () => {
  it("confirma endereco retorna uf do cep consultado", () => {
    // Arrange
    const apiCep = new ApiCepStub("São Paulo", "SP");
    const repositorio = new RepositorioEnderecoFake();
    const servico = new ServicoEntrega(apiCep, repositorio);

    // Act
    const resultado = servico.confirmarEndereco("P001", "01000-000");

    // Assert
    expect(resultado.uf).toBe("SP");
  });

  it("confirma endereco salva endereco no repositorio", () => {
    const apiCep = new ApiCepStub();
    const repositorio = new RepositorioEnderecoFake();
    const servico = new ServicoEntrega(apiCep, repositorio);

    servico.confirmarEndereco("P002", "20000-000");

    expect(repositorio.foiSalvo("P002")).toBe(true);
  });

  it("confirma endereco usa cidade configurada no stub", () => {
    const apiCep = new ApiCepStub("Rio de Janeiro", "RJ");
    const repositorio = new RepositorioEnderecoFake();
    const servico = new ServicoEntrega(apiCep, repositorio);

    const resultado = servico.confirmarEndereco("P003", "20000-000");

    expect(resultado.cidade).toBe("Rio de Janeiro");
  });
});
