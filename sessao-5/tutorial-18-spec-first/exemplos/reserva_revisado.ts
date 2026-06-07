/**
 * Revisão corrigida — Sistema de Reservas de Sala (gerado a partir da spec.md)
 * Referência: Tutorial 10 — Spec-first: do requisito ao código verificável
 * Execute: npx ts-node reserva_revisado.ts
 *
 * Correção em relação a reserva_gerado.ts:
 *   - Regra R1 implementada: sobreposição de horário na mesma sala é detectada e
 *     rejeitada com ReservaSobrepostaError antes de salvar a reserva.
 *   - Fórmula de sobreposição: inicio_nova < fim_existente AND fim_nova > inicio_existente
 *   - Reservas adjacentes (fim === início) não são consideradas sobrepostas.
 *   - Reservas em salas diferentes são independentes.
 *   - Demo exercita todos os 6 casos do contrato definido em spec.md.
 */

// ─── Exceção de domínio ───────────────────────────────────────────────────────

class ReservaSobrepostaError extends Error {
  constructor(mensagem: string) {
    super(mensagem);
    this.name = "ReservaSobrepostaError";
  }
}

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

// ─── Lógica de sobreposição ───────────────────────────────────────────────────

function reservasSobrepostas(existente: Reserva, inicio: Date, fim: Date): boolean {
  /**
   * Retorna true se o intervalo [inicio, fim] se sobrepõe ao intervalo da reserva.
   *
   * Fórmula: inicio_nova < fim_existente AND fim_nova > inicio_existente
   * Reservas adjacentes não se sobrepõem.
   */
  return inicio < existente.fim && fim > existente.inicio;
}

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

  // Regra R1: verificar sobreposição de horário na mesma sala
  for (const reserva of repositorio) {
    if (reserva.sala === sala && reservasSobrepostas(reserva, inicio, fim)) {
      throw new ReservaSobrepostaError(
        `${sala} já está reservada das ${formatarHora(reserva.inicio)} ` +
        `às ${formatarHora(reserva.fim)} por ${reserva.responsavel}`
      );
    }
  }

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

console.log("=== Reservas de Sala (revisado — spec completa, sobreposição detectada) ===\n");

// Caso 1 — criação normal (OK)
const r1 = criarReserva("Sala A", dt(10, 0), dt(11, 0), "Ana");
console.log(`Caso 1 — OK:    ${formatarReserva(r1)}`);

// Caso 2 — sobreposição total (ERRO esperado)
try {
  criarReserva("Sala A", dt(10, 30), dt(11, 30), "Bob");
  console.log("Caso 2 — FALHA: sobreposição deveria ter sido detectada");
} catch (erro) {
  if (erro instanceof ReservaSobrepostaError) {
    console.log(`Caso 2 — OK:    ReservaSobrepostaError: ${erro.message}`);
  } else throw erro;
}

// Caso 3 — sobreposição parcial no fim (ERRO esperado)
try {
  criarReserva("Sala A", dt(9, 30), dt(10, 30), "Carlos");
  console.log("Caso 3 — FALHA: sobreposição deveria ter sido detectada");
} catch (erro) {
  if (erro instanceof ReservaSobrepostaError) {
    console.log(`Caso 3 — OK:    ReservaSobrepostaError: ${erro.message}`);
  } else throw erro;
}

// Caso 4 — reserva adjacente após (OK — não sobrepõe)
const r4 = criarReserva("Sala A", dt(11, 0), dt(12, 0), "Dana");
console.log(`Caso 4 — OK:    ${formatarReserva(r4)}  (adjacente, não sobrepõe)`);

// Caso 5 — sala diferente no mesmo horário (OK)
const r5 = criarReserva("Sala B", dt(10, 0), dt(11, 0), "Eva");
console.log(`Caso 5 — OK:    ${formatarReserva(r5)}  (sala diferente)`);

// Caso 6 — fim antes do início (ERRO esperado)
try {
  criarReserva("Sala A", dt(14, 0), dt(13, 0), "Felipe");
  console.log("Caso 6 — FALHA: Error deveria ter sido lançado");
} catch (erro) {
  if (erro instanceof Error && !(erro instanceof ReservaSobrepostaError)) {
    console.log(`Caso 6 — OK:    Error: ${erro.message}`);
  } else throw erro;
}

console.log();
console.log("Reservas confirmadas:");
listarReservas().forEach(r => console.log(formatarReserva(r)));
