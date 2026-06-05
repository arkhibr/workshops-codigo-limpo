/**
 * GABARITO — Lista de espera da clínica (versão refatorada)
 * Referência: Clean Code, Cap. 2–3 aplicados a código assistido por IA
 *
 * Problemas corrigidos em relação ao exercício:
 *   - Nomes descritivos em português para todos os identificadores
 *   - Interface tipada em vez de any[] com chaves vagas
 *   - Constante nomeada para posição inicial
 *   - Violação de CQS corrigida: adicionar não retorna o ID
 *   - Remoção de paciente inexistente lança exceção com mensagem clara
 *   - Responsabilidade de "chamar próximo" separada em função coesa
 *
 * Execute: npx ts-node sessao-5/tutorial-08-clean-code-com-ia/exercicios/gabarito.ts
 */

const POSICAO_INICIAL = 1; // posição inicial do contador de entradas na fila

interface EntradaFila {
  posicao: number;
  nomePaciente: string;
  tipoAtendimento: string;
  registradoEm: string;
  atendido: boolean;
}

// repositório em memória
const listaDeEspera: EntradaFila[] = [];
let proximoNumero = POSICAO_INICIAL;


function adicionarNaFila(nomePaciente: string, tipoAtendimento: string): void {
  const entrada: EntradaFila = {
    posicao: proximoNumero,
    nomePaciente,
    tipoAtendimento,
    registradoEm: new Date().toISOString(),
    atendido: false,
  };
  listaDeEspera.push(entrada);
  proximoNumero += 1;
}


function removerDaFila(posicao: number): void {
  const indice = listaDeEspera.findIndex((e) => e.posicao === posicao);
  if (indice === -1) {
    throw new Error(`Nenhum paciente encontrado na posição ${posicao}.`);
  }
  listaDeEspera.splice(indice, 1);
}


function exibirListaDeEspera(): void {
  for (const entrada of listaDeEspera) {
    const marcador = entrada.atendido ? "✓" : "·";
    console.log(
      `[${marcador}] #${entrada.posicao} ${entrada.nomePaciente} (${entrada.tipoAtendimento})`
    );
  }
}


function proximaEntradaPendente(): EntradaFila | undefined {
  return listaDeEspera.find((e) => !e.atendido);
}


function chamarProximoPaciente(): EntradaFila {
  const entrada = proximaEntradaPendente();
  if (!entrada) {
    throw new Error("Não há pacientes aguardando na fila de espera.");
  }
  entrada.atendido = true;
  return entrada;
}


// ─── Execução de demonstração ─────────────────────────────────────────────────

adicionarNaFila("Maria Oliveira", "retorno");
adicionarNaFila("João Costa", "primeira consulta");
adicionarNaFila("Beatriz Ferreira", "exame");

console.log("=== Lista de espera ===");
exibirListaDeEspera();

console.log("\nChamando próximo paciente...");
const proximo = chamarProximoPaciente();
console.log(`Chamado: ${proximo.nomePaciente} (${proximo.tipoAtendimento})`);

console.log("\n=== Lista atualizada ===");
exibirListaDeEspera();

// remove um paciente da fila
removerDaFila(2);
console.log("\n=== Após remover posição 2 ===");
exibirListaDeEspera();

// tenta remover posição inexistente — deve lançar exceção
try {
  removerDaFila(99);
} catch (erro) {
  console.log(`\nErro esperado: ${(erro as Error).message}`);
}
