/**
 * GABARITO — cancelamento de assinatura com erros tratados explicitamente
 * Referência: Clean Code, Cap. 7 (Error Handling)
 *
 * Problemas corrigidos em relação ao exercício:
 *   - AssinaturaNaoEncontradaError: ID inexistente levanta exceção específica
 *   - AssinaturaJaCanceladaError: estado inválido levanta exceção específica
 *   - MotivoAusenteError: motivo obrigatório validado explicitamente
 *   - Responsabilidades separadas: buscar / validar / calcular / persistir / cancelar
 *   - Falhas agora são visíveis — o chamador coleta e reporta cada uma
 *
 * Execute: npx ts-node sessao-5/tutorial-11-tratamento-de-erros/exercicios/gabarito.ts
 */

// ─── Exceções específicas ──────────────────────────────────────────────────────

class AssinaturaNaoEncontradaError extends Error {
  constructor(mensagem: string) {
    super(mensagem);
    this.name = "AssinaturaNaoEncontradaError";
  }
}

class AssinaturaJaCanceladaError extends Error {
  constructor(mensagem: string) {
    super(mensagem);
    this.name = "AssinaturaJaCanceladaError";
  }
}

class MotivoAusenteError extends Error {
  constructor(mensagem: string) {
    super(mensagem);
    this.name = "MotivoAusenteError";
  }
}

// ─── Interfaces ───────────────────────────────────────────────────────────────

interface DadosAssinatura {
  plano: string;
  valor: number;
  diasRestantes: number;
  ativa: boolean;
}

interface ResultadoCancelamento {
  id: string;
  reembolso: number;
  status: string;
}

// ─── Dados em memória ─────────────────────────────────────────────────────────

const DIAS_MES = 30;
const DIAS_ANO = 365;

const bancoAssinaturas: Record<string, DadosAssinatura> = {
  "ASS-001": { plano: "mensal", valor: 49.90, diasRestantes: 18, ativa: true },
  "ASS-002": { plano: "anual",  valor: 499.00, diasRestantes: 0,  ativa: false },
  "ASS-003": { plano: "mensal", valor: 29.90, diasRestantes: 10, ativa: true },
};

const cancelamentosRegistrados: { id: string; motivo: string; reembolso: number }[] = [];


// ─── Funções com responsabilidade única ───────────────────────────────────────

function buscarAssinatura(idAssinatura: string): DadosAssinatura {
  const dados = bancoAssinaturas[idAssinatura];
  if (!dados) {
    throw new AssinaturaNaoEncontradaError(
      `Assinatura '${idAssinatura}' não encontrada.`
    );
  }
  return dados;
}

function validarCancelamento(
  idAssinatura: string,
  dados: DadosAssinatura,
  motivo: string | null | undefined
): void {
  if (!dados.ativa) {
    throw new AssinaturaJaCanceladaError(
      `Assinatura '${idAssinatura}' já foi cancelada anteriormente.`
    );
  }
  if (!motivo || !motivo.trim()) {
    throw new MotivoAusenteError(
      "O motivo do cancelamento é obrigatório e não pode ser vazio."
    );
  }
}

function calcularReembolso(dados: DadosAssinatura): number {
  if (dados.diasRestantes <= 0) {
    return 0;
  }
  const totalDias = dados.plano === "mensal" ? DIAS_MES : DIAS_ANO;
  return Math.round(dados.valor * (dados.diasRestantes / totalDias) * 100) / 100;
}

function registrarCancelamento(idAssinatura: string, motivo: string, reembolso: number): void {
  bancoAssinaturas[idAssinatura].ativa = false;
  cancelamentosRegistrados.push({ id: idAssinatura, motivo, reembolso });
}

function cancelarAssinatura(
  idAssinatura: string,
  motivo: string | null | undefined
): ResultadoCancelamento {
  const dados = buscarAssinatura(idAssinatura);
  validarCancelamento(idAssinatura, dados, motivo);
  const reembolso = calcularReembolso(dados);
  registrarCancelamento(idAssinatura, motivo as string, reembolso);
  return { id: idAssinatura, reembolso, status: "cancelado" };
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

const tentativas: [string, string | null][] = [
  ["ASS-001", "cliente solicitou"],
  ["ASS-002", "cliente solicitou"],  // já cancelada
  ["ASS-999", "cliente solicitou"],  // não existe
  ["ASS-003", null],                 // motivo ausente
];

console.log("=== Demonstração: gabarito.ts (cancelamento de assinatura) ===");
console.log();

const sucessos: ResultadoCancelamento[] = [];
const falhas: { id: string; tipo: string; erro: string }[] = [];

for (const [idAssinatura, motivo] of tentativas) {
  try {
    const resultado = cancelarAssinatura(idAssinatura, motivo);
    sucessos.push(resultado);
  } catch (erro) {
    if (
      erro instanceof AssinaturaNaoEncontradaError ||
      erro instanceof AssinaturaJaCanceladaError ||
      erro instanceof MotivoAusenteError
    ) {
      falhas.push({ id: idAssinatura, tipo: erro.name, erro: erro.message });
    } else {
      throw erro;
    }
  }
}

console.log(`Cancelamentos aprovados: ${sucessos.length}`);
for (const s of sucessos) {
  console.log(`  [${s.id}] reembolso R$ ${s.reembolso.toFixed(2)} — ${s.status}`);
}

console.log();
console.log(`Cancelamentos com falha: ${falhas.length}`);
for (const f of falhas) {
  console.log(`  [${f.id}] ${f.tipo}: ${f.erro}`);
}

console.log();
console.log("Cada falha agora é visível com tipo específico e mensagem descritiva.");
