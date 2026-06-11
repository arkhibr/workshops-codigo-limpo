/**
 * GABARITO 19 — Anti-patterns Clássicos (TypeScript)
 * Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3
 * Execute: npx ts-node gabarito.ts
 */

// ─── Passo 1: Magic Strings/Numbers → constantes nomeadas ────────────────────

const CATEGORIA_CLT        = "C";
const CATEGORIA_PJ         = "P";
const CATEGORIA_ESTAGIARIO = "E";

const SALARIO_MINIMO_2026:      number = 1412.0;
const LIMITE_FAIXA_INSS_2:      number = 2666.68;
const ALIQUOTA_INSS_FAIXA_1:    number = 0.075;
const ALIQUOTA_INSS_FAIXA_2:    number = 0.09;
const ALIQUOTA_INSS_FAIXA_3:    number = 0.12;
const ALIQUOTA_INSS_ESTAGIARIO: number = 0.03;
const ALIQUOTA_FGTS:            number = 0.08;

// ─── Modelo de domínio ────────────────────────────────────────────────────────

// Passo 2: interface vira classe para suportar calcularInss()
class Funcionario {
  constructor(
    public id:        string,
    public nome:      string,
    public email:     string,
    public categoria: string,   // usa as constantes CATEGORIA_* acima
    public salario:   number,
  ) {}

  // Passo 2: Feature Envy → calcularInss() pertence ao dono dos dados
  calcularInss(): number {
    if (this.categoria === CATEGORIA_CLT) {
      if (this.salario <= SALARIO_MINIMO_2026) {
        return Math.round(this.salario * ALIQUOTA_INSS_FAIXA_1 * 100) / 100;
      }
      if (this.salario <= LIMITE_FAIXA_INSS_2) {
        return Math.round(this.salario * ALIQUOTA_INSS_FAIXA_2 * 100) / 100;
      }
      return Math.round(this.salario * ALIQUOTA_INSS_FAIXA_3 * 100) / 100;
    }
    if (this.categoria === CATEGORIA_PJ) {
      return 0;
    }
    return Math.round(this.salario * ALIQUOTA_INSS_ESTAGIARIO * 100) / 100;
  }
}

// ─── Passo 3: Copy-Paste → função livre compartilhada ────────────────────────

function calcularBase(func: Funcionario): number {
  if (func.categoria === CATEGORIA_CLT) {
    return Math.max(func.salario, SALARIO_MINIMO_2026);
  }
  return func.salario;
}

class CalculoNormal {
  calcularBase(func: Funcionario): number {
    return calcularBase(func);
  }

  calcularLiquido(func: Funcionario): number {
    return Math.round(this.calcularBase(func) * 0.85 * 100) / 100;
  }
}

class CalculoTerceirizado {
  calcularBase(func: Funcionario): number {
    return calcularBase(func);
  }

  calcularLiquido(func: Funcionario): number {
    return Math.round(this.calcularBase(func) * 0.80 * 100) / 100;
  }
}

// ─── Passo 4: God Object → 3 classes com responsabilidade única ──────────────

class RepositorioFuncionario {
  buscarFuncionario(funcId: string): Funcionario {
    console.log(`  [BD] buscar funcionário ${funcId}`);
    return new Funcionario(funcId, "João Silva", "joao@empresa.com",
                           CATEGORIA_CLT, 3500);
  }

  salvarFuncionario(func: Funcionario): void {
    console.log(`  [BD] salvar ${func.id}`);
  }

  calcularFgts(func: Funcionario): number {
    if (func.categoria === CATEGORIA_CLT) {
      return Math.round(func.salario * ALIQUOTA_FGTS * 100) / 100;
    }
    return 0;
  }
}

class ServicoNotificacao {
  enviarContracheque(email: string, valor: number): void {
    console.log(`  [Email] → ${email}: contracheque R$${valor.toFixed(2)}`);
  }

  notificarRh(msg: string): void {
    console.log(`  [RH] ${msg}`);
  }
}

class GeradorRelatorioRH {
  gerarRelatorio(ano: number): string {
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

console.log("=== Gabarito 19 — Anti-patterns RH (TypeScript) ===\n");

// Passo 1
console.assert(CATEGORIA_CLT        === "C",    "CATEGORIA_CLT deve ser 'C'");
console.assert(CATEGORIA_PJ         === "P",    "CATEGORIA_PJ deve ser 'P'");
console.assert(CATEGORIA_ESTAGIARIO === "E",    "CATEGORIA_ESTAGIARIO deve ser 'E'");
console.assert(SALARIO_MINIMO_2026  === 1412.0, "SALARIO_MINIMO_2026 deve ser 1412.0");
console.log("PASSO 1 OK: constantes CATEGORIA_* e SALARIO_MINIMO_2026 definidas");

// Passo 2
const fClt   = new Funcionario("F1", "João", "j@e.com", CATEGORIA_CLT,        3500);
const fPj    = new Funcionario("F2", "Ana",  "a@e.com", CATEGORIA_PJ,         8000);
const fEstag = new Funcionario("F3", "Leo",  "l@e.com", CATEGORIA_ESTAGIARIO,  900);
const inssEsperadoClt = Math.round(3500 * ALIQUOTA_INSS_FAIXA_3 * 100) / 100;
console.assert(Math.abs(fClt.calcularInss()   - inssEsperadoClt) < 0.01);
console.assert(fPj.calcularInss()    === 0);
console.assert(Math.abs(fEstag.calcularInss() - Math.round(900 * ALIQUOTA_INSS_ESTAGIARIO * 100) / 100) < 0.01);
console.log(`PASSO 2 OK: calcularInss() em Funcionario (CLT=R$${fClt.calcularInss().toFixed(2)}, PJ=R$${fPj.calcularInss().toFixed(2)})`);

// Passo 3
const n = new CalculoNormal();
const t = new CalculoTerceirizado();
console.assert(Math.abs(n.calcularLiquido(fClt) - Math.round(3500 * 0.85 * 100) / 100) < 0.01);
console.assert(Math.abs(t.calcularLiquido(fClt) - Math.round(3500 * 0.80 * 100) / 100) < 0.01);
console.log(`PASSO 3 OK: calcularBase() sem duplicação (CLT=R$${n.calcularLiquido(fClt).toFixed(2)}, Terc=R$${t.calcularLiquido(fClt).toFixed(2)})`);

// Passo 4
const classes4: [string, object][] = [
  ["RepositorioFuncionario", new RepositorioFuncionario()],
  ["ServicoNotificacao",     new ServicoNotificacao()],
  ["GeradorRelatorioRH",     new GeradorRelatorioRH()],
];
for (const [nome, obj] of classes4) {
  const qtd = Object.getOwnPropertyNames(Object.getPrototypeOf(obj))
    .filter(m => m !== "constructor").length;
  console.assert(qtd <= 5, `${nome} ainda tem responsabilidades demais`);
}
console.log("PASSO 4 OK: RepositorioFuncionario / ServicoNotificacao / GeradorRelatorioRH");

console.log("\n--- Demo completo ---");
const repo  = new RepositorioFuncionario();
const notif = new ServicoNotificacao();
const func  = repo.buscarFuncionario("FUNC-001");
const inss  = func.calcularInss();
const fgts  = repo.calcularFgts(func);
console.log(`INSS: R$${inss.toFixed(2)}, FGTS: R$${fgts.toFixed(2)}`);
notif.enviarContracheque(func.email, func.salario - inss);
