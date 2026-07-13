// EXERCÍCIO 25 — Dublês de Teste (Vitest)
// Tempo estimado: 15 minutos
//
// INSTRUÇÕES:
//   ServicoEntrega abaixo depende de ApiCepReal (chamada de rede real, lenta,
//   simulada aqui com um pequeno delay) e RepositorioEnderecoReal (banco real).
//   O teste fornecido não usa nenhum double.
//
//   1. Crie um Stub para a API de CEP (resposta fixa) com vi.fn() ou um objeto literal.
//   2. Crie uma classe Fake para o repositório de endereço (em memória).
//   3. Reescreva o teste para não depender de infraestrutura real / delays.
//   Execute: npx vitest run exercicio.ts
import { it, expect } from "vitest";

interface Endereco {
  cep: string;
  cidade: string;
  uf: string;
}

function esperar(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

class ApiCepReal {
  async consultar(cep: string): Promise<Endereco> {
    await esperar(300); // simula latência de rede real
    return { cep, cidade: "São Paulo", uf: "SP" };
  }
}

class RepositorioEnderecoReal {
  async salvar(_pedidoId: string, _endereco: Endereco): Promise<void> {
    await esperar(200);
  }
}

class ServicoEntrega {
  private apiCep = new ApiCepReal();
  private repositorio = new RepositorioEnderecoReal();

  async confirmarEndereco(pedidoId: string, cep: string): Promise<Endereco> {
    const endereco = await this.apiCep.consultar(cep);
    await this.repositorio.salvar(pedidoId, endereco);
    return endereco;
  }
}

it("confirma endereco sem nenhum double", async () => {
  // lento: ~0.5s de delay simulando chamadas reais
  const servico = new ServicoEntrega();
  const resultado = await servico.confirmarEndereco("P001", "01000-000");
  expect(resultado.uf).toBe("SP");
});
