/**
 * Saída do modelo de IA (sem spec firme) — Sistema de Reservas de Sala
 * Referência: Tutorial 10 — Spec-first: do requisito ao código verificável
 * Execute: npx ts-node reserva_gerado.ts
 *
 * ATENÇÃO: saída de IA sem spec firme — exigência implícita perdida.
 * O código é limpo, tipado e idiomático: interface com tipos explícitos,
 * Error para entradas inválidas, repositório em memória, demo com console.log.
 * Cobre o caminho principal (criar e listar reservas) sem nenhum problema aparente.
 *
 * Mas a exigência implícita crítica foi perdida: o sistema aceita silenciosamente
 * duas reservas sobrepostas na mesma sala. O prompt pediu "criar e listar reservas"
 * — e o modelo fez exatamente isso, sem inferir que sobreposição deveria ser
 * bloqueada. O defeito não aparece nos casos normais; só quando duas reservas
 * compartilham sala e horário.
 */

// ─── Entidade ─────────────────────────────────────────────────────────────────

interface Reserva {
  id:          number;
  sala:        string;
  inicio:      Date;
  fim:         Date;
  responsavel: string;
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

  // ⚠️  DEFEITO: não verifica sobreposição de horário na mesma sala.
  // A exigência implícita — "não permitir reservas sobrepostas" — foi perdida
  // porque o prompt informal não a mencionava explicitamente. O modelo gerou
  // o caminho principal (criar → salvar) sem inferir a restrição de negócio.
  const reserva: Reserva = {
    id: proximoId++,
    sala,
    inicio,
    fim,
    responsavel,
  };
  repositorio.push(reserva);
  return reserva;
}

function listarReservas(sala?: string): Reserva[] {
  if (sala === undefined) return [...repositorio];
  return repositorio.filter(r => r.sala === sala);
}

function formatarHora(data: Date): string {
  return data.toTimeString().slice(0, 5);
}

function formatarReserva(reserva: Reserva): string {
  const dia = reserva.inicio.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" });
  return (
    `  [${reserva.id}] ${reserva.sala} | ` +
    `${dia} ${formatarHora(reserva.inicio)}–${formatarHora(reserva.fim)} | ` +
    `${reserva.responsavel}`
  );
}

// ─── Execução de demonstração ─────────────────────────────────────────────────

const data = new Date(2026, 5, 10);  // 10/06/2026

function dt(hora: number, minuto: number): Date {
  return new Date(data.getFullYear(), data.getMonth(), data.getDate(), hora, minuto, 0, 0);
}

console.log("=== Reservas de Sala (saída do modelo — exigência implícita perdida) ===\n");

// Reserva normal — OK
const r1 = criarReserva("Sala A", dt(10, 0), dt(11, 0), "Ana");
console.log(`Criada: ${formatarReserva(r1)}`);

// Reserva sobreposta — deveria ser rejeitada, mas é aceita silenciosamente
const r2 = criarReserva("Sala A", dt(10, 30), dt(11, 30), "Bob");
console.log(`Criada: ${formatarReserva(r2)}  <- SOBREPOSIÇÃO ACEITA (defeito)`);

// Reserva em sala diferente — OK
const r3 = criarReserva("Sala B", dt(10, 0), dt(11, 0), "Carlos");
console.log(`Criada: ${formatarReserva(r3)}`);

console.log();
console.log("Reservas em Sala A:");
listarReservas("Sala A").forEach(r => console.log(formatarReserva(r)));

console.log();
console.log("Caso crítico — sobreposição aceita silenciosamente:");
console.log("  Sala A 10:00–11:00 (Ana) e Sala A 10:30–11:30 (Bob)");
console.log("  Ambas estão no repositório — conflito não detectado.");
console.log("  Um participante chegará à Sala A e encontrará outra reunião.");
