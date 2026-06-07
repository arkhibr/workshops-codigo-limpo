/**
 * Exercício — Cancelamento de Reserva (saída de IA sem spec firme)
 * Referência: Tutorial 10 — Spec-first: do requisito ao código verificável
 * Execute: npx ts-node exercicio.ts
 *
 * Contexto:
 *   Este módulo foi gerado por um modelo de fronteira com boas práticas aplicadas:
 *   interface com tipos explícitos, Error para entradas inválidas, repositório
 *   em memória, demo com console.log. O código é limpo e cobre o caminho principal.
 *
 *   Mas foi gerado sem especificação de uma exigência implícita:
 *     "o cancelamento só é permitido com antecedência mínima de 2 horas."
 *   O código cancela qualquer reserva a qualquer momento — inclusive nos últimos
 *   minutos antes do horário agendado, o que viola a política da empresa.
 *
 * Suas tarefas:
 *   (1) Execute o exercício e observe o resultado. Identifique qual caso demonstra
 *       o cancelamento que deveria ser rejeitado.
 *   (2) Escreva a spec que fixa a exigência implícita, incluindo:
 *       - A regra de antecedência mínima (2 horas)
 *       - Exemplos de contrato com entrada→saída esperada para os casos de fronteira
 *   (3) Corrija o código para respeitar a regra e compare com gabarito.ts.
 */

// ─── Exceção de domínio ───────────────────────────────────────────────────────

class ReservaNaoEncontradaError extends Error {
  constructor(mensagem: string) {
    super(mensagem);
    this.name = "ReservaNaoEncontradaError";
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

  // ⚠️  DEFEITO: cancela a qualquer momento sem verificar antecedência mínima.
  // A exigência implícita — "cancelamento apenas com 2h de antecedência" —
  // foi perdida porque o prompt informal descreveu apenas "cancelar reserva".
  // O caminho principal (cancelar reservas existentes) funciona corretamente;
  // o defeito só aparece quando o cancelamento ocorre muito próximo ao horário.
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

console.log("=== Cancelamento de Reserva (exercício — exigência implícita perdida) ===\n");

// Criar reservas para o dia
const r1 = criarReserva("Sala A", dt(14, 0), dt(15, 0), "Ana");
const r2 = criarReserva("Sala B", dt(15, 0), dt(16, 0), "Bob");
const r3 = criarReserva("Sala C", dt(16, 0), dt(17, 0), "Carlos");

console.log("Reservas criadas:");
listarReservasAtivas().forEach(r => console.log(formatarReserva(r)));
console.log();

// Cancelamento com 3 horas de antecedência — OK em qualquer política
const agoraCedo = dt(11, 0);
cancelarReserva(r1.id, agoraCedo);
console.log(`Cancelamento às ${formatarHora(agoraCedo)} (3h antes de 14:00):`);
console.log(formatarReserva(r1));

// Cancelamento exatamente no horário — deveria ser rejeitado (exigência perdida)
const agoraTarde = dt(14, 0);
cancelarReserva(r2.id, agoraTarde);
console.log(`\nCancelamento às ${formatarHora(agoraTarde)} (no horário da reserva 15:00):`);
console.log(formatarReserva(r2));
console.log("  <- ACEITO (defeito: deveria exigir 2h de antecedência)");

// Cancelamento 30 minutos antes — deveria ser rejeitado
const agoraMuitoTarde = dt(15, 30);
cancelarReserva(r3.id, agoraMuitoTarde);
console.log(`\nCancelamento às ${formatarHora(agoraMuitoTarde)} (30min antes de 16:00):`);
console.log(formatarReserva(r3));
console.log("  <- ACEITO (defeito: deveria exigir 2h de antecedência)");

console.log();
console.log("Reservas ativas após cancelamentos:");
const ativas = listarReservasAtivas();
if (ativas.length > 0) {
  ativas.forEach(r => console.log(formatarReserva(r)));
} else {
  console.log("  (nenhuma)");
}
