// EXERCÍCIO 27 — Testes de Unidade em Código Legado (Âncora) (Vitest)
// Tempo estimado: 10 minutos
//
// INSTRUÇÕES:
//   ProcessadorReembolso abaixo não tem seams nem testes: instancia
//   GatewayPagamentoReal e ServicoAuditoriaReal diretamente.
//
//   1. Introduza seams (injeção via construtor).
//   2. Escreva um teste de CARACTERIZAÇÃO para o comportamento atual.
//   3. Use doubles (Stub para o gateway, Fake para a auditoria).
//   Execute: npx vitest run exercicio.ts

interface ResultadoEstorno {
  status: string;
  valor: number;
}

class GatewayPagamentoReal {
  estornar(_transacaoId: string, _valor: number): ResultadoEstorno {
    throw new Error("Gateway real não disponível neste ambiente");
  }
}

class ServicoAuditoriaReal {
  registrar(_evento: string, _detalhes: Record<string, unknown>): void {
    throw new Error("Serviço de auditoria real não disponível neste ambiente");
  }
}

class ProcessadorReembolso {
  private gateway = new GatewayPagamentoReal();
  private auditoria = new ServicoAuditoriaReal();

  processarReembolso(transacaoId: string, valor: number): ResultadoEstorno {
    const resultado = this.gateway.estornar(transacaoId, valor);
    this.auditoria.registrar("reembolso", { transacaoId, valor });
    return resultado;
  }
}
