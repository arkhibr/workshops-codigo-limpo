/**
 * EXERCÍCIO 19 — Anti-patterns Clássicos (TypeScript)
 * Tempo estimado: 34 minutos (4 micro-passos)
 * Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3
 *
 * INSTRUÇÕES GERAIS:
 *   O código abaixo demonstra 4 anti-patterns.
 *   Siga os 4 passos em ordem — cada passo é independente e verificável.
 *   Execute: npx ts-node exercicio.ts (deve rodar sem erro antes e depois de cada passo)
 *
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 * PASSO 1 — MAGIC STRINGS/NUMBERS  (8 min)
 *   Extraia as strings e números mágicos para constantes nomeadas:
 *     const SALARIO_MINIMO_2026 = 1412.0
 *     const CATEGORIA_CLT = "C"  /  CATEGORIA_PJ = "P"  /  CATEGORIA_ESTAGIARIO = "E"
 *   Substitua todas as ocorrências nos lugares onde estão usados.
 *   Verifique que o demo ainda roda.
 *
 * PASSO 2 — FEATURE ENVY  (8 min)
 *   Mova calcularInss() de GestorFolhaPagamento para a interface/classe Funcionario.
 *   Transforme Funcionario em classe com método calcularInss(): number
 *   (sem parâmetros extras, usa this.salario/this.categoria).
 *   Atualize os chamadores.
 *   Verifique que o demo ainda roda.
 *
 * PASSO 3 — COPY-PASTE  (8 min)
 *   Extraia calcularBase() como função de módulo:
 *     function calcularBase(func: Funcionario): number { ... }
 *   Faça CalculoNormal.calcularBase() e CalculoTerceirizado.calcularBase()
 *   chamarem calcularBase().
 *   Verifique que o demo ainda roda.
 *
 * PASSO 4 — GOD OBJECT  (10 min)
 *   Separe GestorFolhaPagamento em 3 classes com responsabilidade única:
 *     RepositorioFuncionario  — buscarFuncionario, salvarFuncionario
 *     ServicoNotificacao      — enviarContracheque, notificarRh
 *     GeradorRelatorioRH      — gerarRelatorio, exportarCsv, arquivarFolha
 *   Deixe calcularFgts() em RepositorioFuncionario ou crie CalculadorFolha separado.
 *   Verifique que o demo ainda roda.
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 */

interface Funcionario {
  id:        string;
  nome:      string;
  email:     string;
  categoria: string;   // "C" = CLT, "P" = PJ, "E" = Estagiário
  salario:   number;
}

// ─── Anti-pattern 3 — Feature Envy (calcularInss fora de Funcionario) ─────────

class GestorFolhaPagamento {
  buscarFuncionario(funcId: string): Funcionario {
    console.log(`  [BD] buscar funcionário ${funcId}`);
    return { id: funcId, nome: "João Silva", email: "joao@empresa.com",
             categoria: "C", salario: 3500 };
  }

  salvarFuncionario(func: Funcionario): void {
    console.log(`  [BD] salvar ${func.id}`);
  }

  // Feature Envy: sabe mais sobre Funcionario do que sobre si mesmo
  calcularInss(salario: number, categoria: string): number {
    if (categoria === "C") {         // magic string
      if (salario <= 1412) {         // magic number — salário mínimo 2026
        return Math.round(salario * 0.075 * 100) / 100;
      } else if (salario <= 2666.68) {
        return Math.round(salario * 0.09 * 100) / 100;
      } else {
        return Math.round(salario * 0.12 * 100) / 100;
      }
    }
    if (categoria === "P") {         // magic string
      return 0;
    }
    return Math.round(salario * 0.03 * 100) / 100; // estagiário
  }

  calcularFgts(salario: number, categoria: string): number {
    if (categoria === "C") {
      return Math.round(salario * 0.08 * 100) / 100;
    }
    return 0;
  }

  enviarContracheque(email: string, valor: number): void {
    console.log(`  [Email] → ${email}: contracheque R$${valor.toFixed(2)}`);
  }

  arquivarFolha(mes: number, ano: number): void {
    console.log(`  [BD] arquivando folha ${mes}/${ano}`);
  }

  gerarRelatorio(ano: number): string {
    return `Relatório folha ${ano}`;
  }

  exportarCsv(dados: unknown[]): string {
    return "funcionario,salario\n";
  }

  reprocessarFolha(mes: number): boolean {
    console.log(`  reprocessando folha ${mes}`);
    return true;
  }

  notificarRh(msg: string): void {
    console.log(`  [RH] ${msg}`);
  }

  validarCpf(cpf: string): boolean {
    return cpf.replace(/[.\-]/g, "").length === 11;
  }

  calcularFerias(salario: number): number {
    return Math.round(salario / 3 * 100) / 100;
  }
}

// ─── Anti-pattern 4 — Copy-Paste ─────────────────────────────────────────────

class CalculoNormal {
  calcularBase(func: Funcionario): number {
    const salarioBase = 1412;          // magic number — copiado em CalculoTerceirizado
    if (func.categoria === "C") {
      return Math.max(func.salario, salarioBase);
    }
    return func.salario;
  }

  calcularLiquido(func: Funcionario): number {
    return Math.round(this.calcularBase(func) * 0.85 * 100) / 100;
  }
}

class CalculoTerceirizado {
  calcularBase(func: Funcionario): number {  // idêntico a CalculoNormal
    const salarioBase = 1412;          // magic number — copiado de CalculoNormal
    if (func.categoria === "C") {
      return Math.max(func.salario, salarioBase);
    }
    return func.salario;
  }

  calcularLiquido(func: Funcionario): number {
    return Math.round(this.calcularBase(func) * 0.80 * 100) / 100;
  }
}

// ─── Demo ─────────────────────────────────────────────────────────────────────

const gestor = new GestorFolhaPagamento();
const func   = gestor.buscarFuncionario("FUNC-001");
const inss   = gestor.calcularInss(func.salario, func.categoria);
const fgts   = gestor.calcularFgts(func.salario, func.categoria);
console.log(`INSS: R$${inss.toFixed(2)}, FGTS: R$${fgts.toFixed(2)}`);
gestor.enviarContracheque(func.email, func.salario - inss);
const metodos = Object.getOwnPropertyNames(Object.getPrototypeOf(gestor))
  .filter(m => m !== "constructor");
console.log(`GestorFolhaPagamento tem ${metodos.length} métodos`);

const normal       = new CalculoNormal();
const terceirizado = new CalculoTerceirizado();
console.log(`Líquido CLT: R$${normal.calcularLiquido(func).toFixed(2)}`);
console.log(`Líquido Terc: R$${terceirizado.calcularLiquido(func).toFixed(2)}`);

// ── Stubs de verificação — descomente após cada passo ─────────────────────────

// PASSO 1 — descomente para verificar:
// console.assert(CATEGORIA_CLT        === "C",    "CATEGORIA_CLT deve ser 'C'");
// console.assert(CATEGORIA_PJ         === "P",    "CATEGORIA_PJ deve ser 'P'");
// console.assert(CATEGORIA_ESTAGIARIO === "E",    "CATEGORIA_ESTAGIARIO deve ser 'E'");
// console.assert(SALARIO_MINIMO_2026  === 1412.0, "SALARIO_MINIMO_2026 deve ser 1412.0");
// console.log("PASSO 1 OK: constantes definidas e usadas");

// PASSO 2 — descomente para verificar (requer Passo 1 feito):
// const fClt = new Funcionario("F1", "João", "j@e.com", CATEGORIA_CLT, 3500.0);
// console.assert(Math.abs(fClt.calcularInss() - Math.round(3500 * 0.12 * 100) / 100) < 0.01);
// const fPj = new Funcionario("F2", "Ana", "a@e.com", CATEGORIA_PJ, 8000.0);
// console.assert(fPj.calcularInss() === 0);
// console.log("PASSO 2 OK: calcularInss() pertence a Funcionario");

// PASSO 3 — descomente para verificar (requer Passo 1 feito):
// const fTeste = new Funcionario("F3", "Leo", "l@e.com", CATEGORIA_CLT, 3500.0);
// const n2 = new CalculoNormal();
// const t2 = new CalculoTerceirizado();
// console.assert(Math.abs(n2.calcularLiquido(fTeste) - Math.round(3500 * 0.85 * 100) / 100) < 0.01);
// console.assert(Math.abs(t2.calcularLiquido(fTeste) - Math.round(3500 * 0.80 * 100) / 100) < 0.01);
// console.log("PASSO 3 OK: calcularBase() sem duplicação");

// PASSO 4 — descomente para verificar:
// const classes4 = [
//   ["RepositorioFuncionario", new RepositorioFuncionario()],
//   ["ServicoNotificacao",     new ServicoNotificacao()],
//   ["GeradorRelatorioRH",     new GeradorRelatorioRH()],
// ] as [string, object][];
// for (const [nome, obj] of classes4) {
//   const qtd = Object.getOwnPropertyNames(Object.getPrototypeOf(obj))
//     .filter(m => m !== "constructor").length;
//   console.assert(qtd <= 5, `${nome} ainda tem responsabilidades demais`);
// }
// console.log("PASSO 4 OK: God Object separado em 3 classes");
