// equivalente.ts — Dublês de Teste em Vitest
// Execute: npx vitest run equivalente.ts
import { describe, it, expect, vi } from "vitest";

interface ResultadoPagamento {
  status: string;
  valor: number;
}

interface GatewayPagamento {
  cobrar(valor: number): ResultadoPagamento;
}

interface ServicoNotificacao {
  enviar(destinatario: string, mensagem: string): boolean;
}

class GatewayPagamentoReal implements GatewayPagamento {
  cobrar(valor: number): ResultadoPagamento {
    // em produção, faria uma chamada de rede real
    return { status: "aprovado", valor };
  }
}

class ProcessadorPagamento {
  constructor(
    private gateway: GatewayPagamento,
    private notificacao: ServicoNotificacao,
  ) {}

  processar(valor: number, destinatario: string): ResultadoPagamento {
    const resultado = this.gateway.cobrar(valor);
    if (resultado.status === "aprovado") {
      this.notificacao.enviar(destinatario, "Pagamento aprovado");
    }
    return resultado;
  }
}

// Fake: implementação funcional leve, em memória — sem instrumentação de chamadas.
class RepositorioPedidoFake {
  private pedidos = new Map<string, Record<string, unknown>>();

  salvar(pedidoId: string, dados: Record<string, unknown>): void {
    this.pedidos.set(pedidoId, dados);
  }

  buscar(pedidoId: string): Record<string, unknown> | undefined {
    return this.pedidos.get(pedidoId);
  }
}

// Ruim: dependência real instanciada diretamente, sem nenhum double —
// acopla o teste à implementação concreta do gateway.
it("processa pagamento sem nenhum double", () => {
  const gatewayReal = new GatewayPagamentoReal();
  const notificacaoReal: ServicoNotificacao = {
    enviar: () => true,
  };
  const processador = new ProcessadorPagamento(gatewayReal, notificacaoReal);

  const resultado = processador.processar(100, "cliente@teste.com");

  expect(resultado.status).toBe("aprovado");
});

// Bom: vi.fn() como mock simples, vi.spyOn() sobre objeto existente, e Fake em memória
describe("ProcessadorPagamento", () => {
  it("notifica o cliente quando o pagamento é aprovado", () => {
    // Arrange — mock simples com vi.fn()
    const gateway: GatewayPagamento = {
      cobrar: vi.fn().mockReturnValue({ status: "aprovado", valor: 100 }),
    };
    const notificacao: ServicoNotificacao = {
      enviar: vi.fn().mockReturnValue(true),
    };
    const processador = new ProcessadorPagamento(gateway, notificacao);

    // Act
    const resultado = processador.processar(100, "cliente@teste.com");

    // Assert — comportamento observável, não implementação interna
    expect(resultado.status).toBe("aprovado");
    expect(notificacao.enviar).toHaveBeenCalledWith("cliente@teste.com", "Pagamento aprovado");
  });

  it("nao notifica o cliente quando o pagamento e recusado", () => {
    const gateway: GatewayPagamento = {
      cobrar: vi.fn().mockReturnValue({ status: "recusado", valor: 100 }),
    };
    const notificacao: ServicoNotificacao = { enviar: vi.fn() };
    const processador = new ProcessadorPagamento(gateway, notificacao);

    processador.processar(100, "cliente@teste.com");

    expect(notificacao.enviar).not.toHaveBeenCalled();
  });

  it("dummy: notificacao nao e exercitada quando pagamento e recusado", () => {
    // Dummy: precisa satisfazer a interface ServicoNotificacao para o
    // construtor de ProcessadorPagamento, mas nunca é de fato invocado
    // neste caminho — quando o pagamento é recusado, o `if` dentro de
    // processar() pula a chamada a notificacao.enviar(...). Lança um erro
    // se for chamado, provando que o caminho testado não o exercita.
    const gateway: GatewayPagamento = {
      cobrar: vi.fn().mockReturnValue({ status: "recusado", valor: 100 }),
    };
    const notificacaoDummy: ServicoNotificacao = {
      enviar: () => {
        throw new Error("Dummy não deveria ser chamado");
      },
    };
    const processador = new ProcessadorPagamento(gateway, notificacaoDummy);

    const resultado = processador.processar(100, "cliente@teste.com");

    expect(resultado.status).toBe("recusado");
  });

  it("espiona uma chamada real via spyOn sobre o gateway real", () => {
    // Spy: vi.spyOn observa uma implementação real em execução, sem
    // substituir o comportamento — apenas registra a chamada.
    const gatewayReal = new GatewayPagamentoReal();
    const spy = vi.spyOn(gatewayReal, "cobrar");

    gatewayReal.cobrar(50);

    expect(spy).toHaveBeenCalledWith(50);
  });

  it("fake do repositorio guarda e recupera pedido", () => {
    const repositorio = new RepositorioPedidoFake();
    repositorio.salvar("P001", { total: 100 });
    expect(repositorio.buscar("P001")).toEqual({ total: 100 });
  });
});
