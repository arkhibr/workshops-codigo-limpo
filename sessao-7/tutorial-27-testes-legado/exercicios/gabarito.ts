// GABARITO 27 — Testes de Unidade em Código Legado (Âncora) (Vitest)
// Seam via construtor: ProcessadorReembolso(gateway, auditoria). GatewayPagamentoStub
// devolve { status: "estornado", valor: ... }; ServicoAuditoriaFake guarda os
// eventos registrados em uma lista, para inspeção. O primeiro teste é de
// caracterização — congela o comportamento atual antes de qualquer melhoria.
// Execute: npx vitest run gabarito.ts
import { describe, it, expect } from "vitest";

interface ResultadoEstorno {
  status: string;
  valor: number;
}

interface GatewayPagamento {
  estornar(transacaoId: string, valor: number): ResultadoEstorno;
}

interface EventoAuditoria {
  evento: string;
  detalhes: Record<string, unknown>;
}

interface ServicoAuditoria {
  registrar(evento: string, detalhes: Record<string, unknown>): void;
}

class ProcessadorReembolso {
  constructor(
    private gateway: GatewayPagamento,
    private auditoria: ServicoAuditoria,
  ) {}

  processarReembolso(transacaoId: string, valor: number): ResultadoEstorno {
    const resultado = this.gateway.estornar(transacaoId, valor);
    this.auditoria.registrar("reembolso", { transacaoId, valor });
    return resultado;
  }
}

// Stub: devolve resposta fixa e pré-programada, sem chamada de rede real.
class GatewayPagamentoStub implements GatewayPagamento {
  constructor(private status: string = "estornado") {}

  estornar(_transacaoId: string, valor: number): ResultadoEstorno {
    return { status: this.status, valor };
  }
}

// Fake: guarda os eventos registrados em memória, para inspeção posterior.
class ServicoAuditoriaFake implements ServicoAuditoria {
  eventosRegistrados: EventoAuditoria[] = [];

  registrar(evento: string, detalhes: Record<string, unknown>): void {
    this.eventosRegistrados.push({ evento, detalhes });
  }
}

describe("ProcessadorReembolso", () => {
  it("caracterizacao: processa reembolso com sucesso", () => {
    // Teste de caracterização: congela o comportamento atual do
    // ProcessadorReembolso como oráculo, agora que o seam permite isolá-lo.
    const gateway = new GatewayPagamentoStub("estornado");
    const auditoria = new ServicoAuditoriaFake();
    const processador = new ProcessadorReembolso(gateway, auditoria);

    const resultado = processador.processarReembolso("TX001", 150.0);

    expect(resultado).toEqual({ status: "estornado", valor: 150.0 });
  });

  it("reembolso registra evento de auditoria", () => {
    const gateway = new GatewayPagamentoStub();
    const auditoria = new ServicoAuditoriaFake();
    const processador = new ProcessadorReembolso(gateway, auditoria);

    processador.processarReembolso("TX002", 80.0);

    expect(auditoria.eventosRegistrados).toHaveLength(1);
    expect(auditoria.eventosRegistrados[0].evento).toBe("reembolso");
    expect(auditoria.eventosRegistrados[0].detalhes).toEqual({
      transacaoId: "TX002",
      valor: 80.0,
    });
  });
});
