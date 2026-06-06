/**
 * GABARITO 19 — Anti-patterns Clássicos (TypeScript)
 * Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3
 * Execute: npx ts-node gabarito.ts
 */

// ─── Correção: Magic Strings → union types + constantes nomeadas ──────────────

type CategoriaCargo = "clt" | "pj" | "estagiario";

const SALARIO_MINIMO_2026:      number = 1412.0;
const LIMITE_FAIXA_INSS_1:      number = 2666.68;
const ALIQUOTA_INSS_FAIXA_1:    number = 0.075;
const ALIQUOTA_INSS_FAIXA_2:    number = 0.09;
const ALIQUOTA_INSS_FAIXA_3:    number = 0.12;
const ALIQUOTA_INSS_ESTAGIARIO: number = 0.03;
const ALIQUOTA_FGTS:            number = 0.08;

// ─── Modelo de domínio ────────────────────────────────────────────────────────

interface Funcionario {
  id:        string;
  nome:      string;
  email:     string;
  categoria: CategoriaCargo;
  salario:   number;
}

// ─── Correção: God Object → classes com responsabilidade única ────────────────

class RepositorioFuncionario {
  buscar(funcId: string): Funcionario {
    console.log(`  [BD] buscar funcionário ${funcId}`);
    return { id: funcId, nome: "João Silva", email: "joao@empresa.com",
             categoria: "clt", salario: 3500 };
  }

  salvar(func: Funcionario): void {
    console.log(`  [BD] salvar ${func.id}`);
  }
}

class CalculadorInss {
  calcular(salario: number, categoria: CategoriaCargo): number {
    if (categoria === "clt") {
      if (salario <= SALARIO_MINIMO_2026) {
        return Math.round(salario * ALIQUOTA_INSS_FAIXA_1 * 100) / 100;
      }
      if (salario <= LIMITE_FAIXA_INSS_1) {
        return Math.round(salario * ALIQUOTA_INSS_FAIXA_2 * 100) / 100;
      }
      return Math.round(salario * ALIQUOTA_INSS_FAIXA_3 * 100) / 100;
    }
    if (categoria === "pj") {
      return 0;
    }
    return Math.round(salario * ALIQUOTA_INSS_ESTAGIARIO * 100) / 100;
  }
}

class CalculadorFgts {
  calcular(salario: number, categoria: CategoriaCargo): number {
    if (categoria === "clt") {
      return Math.round(salario * ALIQUOTA_FGTS * 100) / 100;
    }
    return 0;
  }
}

class ServicoNotificacaoRH {
  enviarContracheque(email: string, valor: number): void {
    console.log(`  [Email] → ${email}: contracheque R$${valor.toFixed(2)}`);
  }

  notificarRh(msg: string): void {
    console.log(`  [RH] ${msg}`);
  }
}

class GeradorRelatorioRH {
  gerar(ano: number): string {
    return `Relatório folha ${ano}`;
  }

  exportarCsv(dados: unknown[]): string {
    return "funcionario,salario\n" + dados.map(String).join("\n");
  }

  arquivarFolha(mes: number, ano: number): void {
    console.log(`  [BD] arquivando folha ${mes}/${ano}`);
  }
}

// ─── Verificação ──────────────────────────────────────────────────────────────

function verificarAntipatterns(): void {
  // God Object corrigido
  const classes: [string, object][] = [
    ["RepositorioFuncionario", new RepositorioFuncionario()],
    ["CalculadorInss",         new CalculadorInss()],
    ["CalculadorFgts",         new CalculadorFgts()],
    ["ServicoNotificacaoRH",   new ServicoNotificacaoRH()],
    ["GeradorRelatorioRH",     new GeradorRelatorioRH()],
  ];

  for (const [nome, obj] of classes) {
    const metodos = Object.getOwnPropertyNames(Object.getPrototypeOf(obj))
      .filter(m => m !== "constructor");
    if (metodos.length <= 5) {
      console.log(`OK: ${nome} tem ${metodos.length} método(s) — responsabilidade única`);
    } else {
      console.log(`FALHOU: ${nome} tem ${metodos.length} métodos — ainda muito grande`);
    }
  }

  // Enums/types e constantes
  const calcInss = new CalculadorInss();
  const inssClT  = calcInss.calcular(3500, "clt");
  const esperado = Math.round(3500 * ALIQUOTA_INSS_FAIXA_3 * 100) / 100;
  if (Math.abs(inssClT - esperado) < 0.01) {
    console.log("OK: CalculadorInss — alíquota CLT correta para R$3500");
  } else {
    console.log(`FALHOU: CalculadorInss — esperado R$${esperado}, obtido R$${inssClT}`);
  }

  const inssPJ = calcInss.calcular(5000, "pj");
  if (inssPJ === 0) {
    console.log("OK: CalculadorInss — PJ retorna zero");
  } else {
    console.log(`FALHOU: CalculadorInss — PJ esperado 0, obtido ${inssPJ}`);
  }

  console.log(`OK: CategoriaCargo union type — "clt" | "pj" | "estagiario"`);
  console.log(`OK: SALARIO_MINIMO_2026 = ${SALARIO_MINIMO_2026}`);
}

// ─── Demo ─────────────────────────────────────────────────────────────────────

console.log("=== Gabarito 19 — Anti-patterns RH (TypeScript) ===\n");
verificarAntipatterns();

console.log("\n--- Demo completo ---");
const repo        = new RepositorioFuncionario();
const calcInss    = new CalculadorInss();
const calcFgts    = new CalculadorFgts();
const notificacao = new ServicoNotificacaoRH();

const func = repo.buscar("FUNC-001");
const inss = calcInss.calcular(func.salario, func.categoria);
const fgts = calcFgts.calcular(func.salario, func.categoria);
console.log(`INSS: R$${inss.toFixed(2)}, FGTS: R$${fgts.toFixed(2)}`);
notificacao.enviarContracheque(func.email, func.salario - inss);
