/**
 * VERSÃO REVISADA — agendamento de consultas após revisão de código gerado por IA
 * Referência: Clean Code, Cap. 2–3
 *
 * Problemas corrigidos em relação à versão gerada:
 *   - Nomes descritivos em português para todos os identificadores
 *   - Parâmetros soltos substituídos por interface tipada
 *   - Número mágico extraído como constante nomeada
 *   - Validação de conflito em função própria
 *   - Erro lançado como exceção com mensagem clara
 *   - Idioma consistente (sem mistura PT/EN)
 *
 * Execute: npx ts-node sessao-5/tutorial-08-clean-code-com-ia/exemplos/agendamento_revisado.ts
 */

const DURACAO_PADRAO_MIN = 30; // duração padrão de consulta em minutos

interface Consulta {
  data: string;          // formato "AAAA-MM-DD"
  horario: string;       // formato "HH:MM"
  nomePaciente: string;
  duracaoMin: number;
  status: string;
}

// repositório em memória (simula banco de dados)
const consultasAgendadas: Consulta[] = [];


function existeConflito(data: string, nomePaciente: string): boolean {
  return consultasAgendadas.some(
    (c) => c.data === data && c.nomePaciente === nomePaciente
  );
}


function agendarConsulta(data: string, horario: string, nomePaciente: string): Consulta {
  if (existeConflito(data, nomePaciente)) {
    throw new Error(
      `Paciente '${nomePaciente}' já possui consulta agendada em ${data}.`
    );
  }

  const novaConsulta: Consulta = {
    data,
    horario,
    nomePaciente,
    duracaoMin: DURACAO_PADRAO_MIN,
    status: "confirmada",
  };
  consultasAgendadas.push(novaConsulta);
  return novaConsulta;
}


function consultasDoPaciente(nomePaciente: string): Consulta[] {
  return consultasAgendadas.filter((c) => c.nomePaciente === nomePaciente);
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

const c1 = agendarConsulta("2026-07-10", "09:00", "Ana Lima");
console.log("Agendamento 1:", c1);

// tenta agendar o mesmo paciente no mesmo dia — deve lançar exceção
try {
  const c2 = agendarConsulta("2026-07-10", "14:00", "Ana Lima");
} catch (erro) {
  console.log(`Conflito detectado: ${(erro as Error).message}`);
}

// agendamento em dia diferente — deve funcionar
const c3 = agendarConsulta("2026-07-11", "10:30", "Carlos Souza");
console.log("Agendamento 3:", c3);

console.log("\nConsultas de Ana Lima:", consultasDoPaciente("Ana Lima"));
