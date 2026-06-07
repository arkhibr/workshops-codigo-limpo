/**
 * EXERCÍCIO 19 — Anti-patterns Clássicos (TypeScript)
 * Tempo estimado: 15 minutos
 * Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3
 *
 * INSTRUÇÕES:
 *   O código abaixo demonstra dois anti-patterns:
 *   1. God Object: GestorFolhaPagamento faz tudo — CRUD, cálculo, relatório, email.
 *   2. Magic Strings/Numbers: if (categoria === "C"), salarioBase = 1412.
 *
 *   1. Quebre o God Object em classes com responsabilidade única.
 *   2. Substitua as strings/números mágicos por union types/const e constantes.
 *   3. Execute: npx ts-node exercicio.ts (deve rodar antes e depois)
 */

interface Funcionario {
  id:        string;
  nome:      string;
  email:     string;
  categoria: string;   // "C" = CLT, "P" = PJ, "E" = Estagiário
  salario:   number;
}

class GestorFolhaPagamento {
  buscarFuncionario(funcId: string): Funcionario {
    console.log(`  [BD] buscar funcionário ${funcId}`);
    return { id: funcId, nome: "João Silva", email: "joao@empresa.com",
             categoria: "C", salario: 3500 };
  }

  salvarFuncionario(func: Funcionario): void {
    console.log(`  [BD] salvar ${func.id}`);
  }

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

// Demo
const gestor = new GestorFolhaPagamento();
const func   = gestor.buscarFuncionario("FUNC-001");
const inss   = gestor.calcularInss(func.salario, func.categoria);
const fgts   = gestor.calcularFgts(func.salario, func.categoria);
console.log(`INSS: R$${inss.toFixed(2)}, FGTS: R$${fgts.toFixed(2)}`);
gestor.enviarContracheque(func.email, func.salario - inss);
const metodos = Object.getOwnPropertyNames(Object.getPrototypeOf(gestor))
  .filter(m => m !== "constructor");
console.log(`GestorFolhaPagamento tem ${metodos.length} métodos`);
