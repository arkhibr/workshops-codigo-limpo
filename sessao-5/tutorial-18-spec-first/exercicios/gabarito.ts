/**
 * Gabarito — Cancelamento de Reserva (gerado a partir da spec com exigência fixada)
 * Referência: Tutorial 10 — Spec-first: do requisito ao código verificável
 * Execute: npx ts-node gabarito.ts
 *
 * Correção em relação a exercicio.ts:
 *   - Regra de antecedência mínima implementada: cancelamento só permitido com
 *     pelo menos 2 horas de antecedência em relação ao início da reserva.
 *   - Se antecedência < 2 horas, lança CancelamentoForaDoPrazoError com mensagem
 *     descritiva informando o tempo restante e o prazo exigido.
 *   - Demo exercita os casos de fronteira: exatamente 2h (OK), menos de 2h (ERRO).
 */

// ─── Constantes de domínio ────────────────────────────────────────────────────

const ANTECEDENCIA_MINIMA_MS = 2 * 60 * 60 * 1000;  // 2 horas em milissegundos

// ─── Exceções de domínio ─────────────────────────────────────────────────────

class ReservaNaoEncontradaError extends Error {
  constructor(mensagem: string) {
    super(mensagem);
    this.name = "ReservaNaoEncontradaError";
  }
}

class CancelamentoForaDoPrazoError extends Error {
  constructor(mensagem: string) {
    super(mensagem);
    this.name = "CancelamentoForaDoPrazoError";
  }
}

// ─── Entidade ─────────────────────────────────────────────────────────────────

interface Reserva {
  id:          number;
  sala:        string;
  inicio:      Date;
  fim:         Date;
  responsavel: string;
  cancelada:   boolean;
}

// ─── Repositório em memória ───────────────────────────────────────────────────

const repositorio: Reserva[] = [];
let proximoId = 1;

// ─── Operações ────────────────────────────────────────────────────────────────

function criarReserva(
  sala:        string,
  inicio:      Date,
  fim:         Date,
  responsavel: string,
): Reserva {
  if (!sala.trim()) {
    throw new Error("O campo 'sala' não pode ser vazio");
  }
  if (!responsavel.trim()) {
    throw new Error("O campo 'responsavel' não pode ser vazio");
  }
  if (fim <= inicio) {
    throw new Error(
      `Horário de fim deve ser após o início ` +
      `(início=${formatarHora(inicio)}, fim=${formatarHora(fim)})`
    );
  }

  const reserva: Reserva = {
    id: proximoId++,
    sala,
    inicio,
    fim,
    responsavel,
    cancelada: false,
  };
  repositorio.push(reserva);
  return reserva;
}

function cancelarReserva(idReserva: number, agora: Date): Reserva {
  const reserva = repositorio.find(r => r.id === idReserva && !r.cancelada);
  if (!reserva) {
    throw new ReservaNaoEncontradaError(
      `Reserva ${idReserva} não encontrada ou já cancelada`
    );
  }

  const antecedenciaMs = reserva.inicio.getTime() - agora.getTime();
  if (antecedenciaMs < ANTECEDENCIA_MINIMA_MS) {
    const horasRestantes = antecedenciaMs / (60 * 60 * 1000);
    const horasMinimas = ANTECEDENCIA_MINIMA_MS / (60 * 60 * 1000);
    throw new CancelamentoForaDoPrazoError(
      `Cancelamento não permitido: faltam ${horasRestantes.toFixed(1)}h para o início ` +
      `da reserva (mínimo exigido: ${horasMinimas}h)`
    );
  }

  reserva.cancelada = true;
  return reserva;
}

function listarReservasAtivas(): Reserva[] {
  return repositorio.filter(r => !r.cancelada);
}

function formatarHora(data: Date): string {
  return data.toTimeString().slice(0, 5);
}

function formatarReserva(reserva: Reserva): string {
  const dia = reserva.inicio.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" });
  const status = reserva.cancelada ? "cancelada" : "ativa";
  return (
    `  [${reserva.id}] ${reserva.sala} | ` +
    `${dia} ${formatarHora(reserva.inicio)}–${formatarHora(reserva.fim)} | ` +
    `${reserva.responsavel} | ${status}`
  );
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

const data = new Date(2026, 5, 10);  // 10/06/2026

function dt(hora: number, minuto: number): Date {
  return new Date(data.getFullYear(), data.getMonth(), data.getDate(), hora, minuto, 0, 0);
}

console.log("=== Cancelamento de Reserva (gabarito — exigência de antecedência fixada) ===\n");

// Criar reservas para o dia
const r1 = criarReserva("Sala A", dt(14, 0), dt(15, 0), "Ana");
const r2 = criarReserva("Sala B", dt(15, 0), dt(16, 0), "Bob");
const r3 = criarReserva("Sala C", dt(16, 0), dt(17, 0), "Carlos");
const r4 = criarReserva("Sala D", dt(17, 0), dt(18, 0), "Dana");

console.log("Reservas criadas:");
listarReservasAtivas().forEach(r => console.log(formatarReserva(r)));
console.log();

// Caso 1 — cancelamento com 3h de antecedência (OK)
let agora = dt(11, 0);
cancelarReserva(r1.id, agora);
console.log(`Caso 1 — OK: cancelamento às ${formatarHora(agora)} (3h antes de 14:00)`);
console.log(formatarReserva(r1));

// Caso 2 — cancelamento exatamente com 2h de antecedência (OK — no limite)
agora = dt(13, 0);
cancelarReserva(r2.id, agora);
console.log(`\nCaso 2 — OK: cancelamento às ${formatarHora(agora)} (exatamente 2h antes de 15:00)`);
console.log(formatarReserva(r2));

// Caso 3 — cancelamento com 1h30min de antecedência (ERRO — fora do prazo)
agora = dt(14, 30);
try {
  cancelarReserva(r3.id, agora);
  console.log(`\nCaso 3 — FALHA: deveria ter sido rejeitado`);
} catch (erro) {
  if (erro instanceof CancelamentoForaDoPrazoError) {
    console.log(`\nCaso 3 — OK: CancelamentoForaDoPrazoError: ${erro.message}`);
  } else throw erro;
}

// Caso 4 — cancelamento no próprio horário (ERRO — fora do prazo)
agora = dt(17, 0);
try {
  cancelarReserva(r4.id, agora);
  console.log(`\nCaso 4 — FALHA: deveria ter sido rejeitado`);
} catch (erro) {
  if (erro instanceof CancelamentoForaDoPrazoError) {
    console.log(`\nCaso 4 — OK: CancelamentoForaDoPrazoError: ${erro.message}`);
  } else throw erro;
}

console.log();
console.log("Reservas ativas após cancelamentos:");
const ativas = listarReservasAtivas();
if (ativas.length > 0) {
  ativas.forEach(r => console.log(formatarReserva(r)));
} else {
  console.log("  (nenhuma)");
}
