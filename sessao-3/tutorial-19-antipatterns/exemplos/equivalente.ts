/**
 * equivalente.ts — Anti-patterns Clássicos em TypeScript
 * Referência: Clean Code Cap. 17 + Fowler Refactoring Cap. 3
 * Execute: npx ts-node equivalente.ts
 */

// ============================================================================
// ❌ RUIM — God Object + Magic Strings + Feature Envy
// ============================================================================

interface ClienteRuim {
  id: string;
  nome: string;
  email: string;
  nivelFidelidade: string;
  historicoCompras: number;
  pontosAcumulados: number;
  dataCadastro: string;
}

interface ItemPedidoRuim {
  produtoId: string;
  preco: number;
  quantidade: number;
}

/** God Object: CRUD, cálculo, notificação, relatório — tudo em uma classe. */
class GestorPedidosRuim {
  buscarCliente(clienteId: string): ClienteRuim {
    console.log(`  [BD] buscar cliente ${clienteId}`);
    return { id: clienteId, nome: "Empresa X", email: "x@x.com",
             nivelFidelidade: "ouro", historicoCompras: 5000, pontosAcumulados: 200,
             dataCadastro: "2020-01-01" };
  }

  salvarCliente(cliente: ClienteRuim): void {
    console.log(`  [BD] salvar cliente ${cliente.id}`);
  }

  validarCpf(cpf: string): boolean {
    return cpf.replace(/[.\-]/g, "").length === 11;
  }

  calcularTotal(itens: ItemPedidoRuim[]): number {
    return itens.reduce((acc, i) => acc + i.preco * i.quantidade, 0);
  }

  aplicarDesconto(total: number, percentual: number): number {
    return Math.round(total * (1 - percentual) * 100) / 100;
  }

  enviarEmail(email: string, assunto: string): void {
    console.log(`  [Email] → ${email}: ${assunto}`);
  }

  gerarBoleto(valor: number, vencimento: string): string {
    return `BOL-${Math.floor(valor)}-${vencimento}`;
  }

  atualizarEstoque(produtoId: string, quantidade: number): void {
    console.log(`  [Estoque] ${produtoId}: -${quantidade}`);
  }

  gerarRelatorio(clienteId: string): string {
    return `Relatório do cliente ${clienteId}`;
  }

  exportarCsv(dados: unknown[]): string {
    return "id,valor\n" + dados.map(String).join("\n");
  }
}

/** Magic Strings: "A", "P" sem contexto. Magic Numbers: 1500, 30. */
function processarPorStatusRuim(
  status: string,
  tipo: string,
  valor: number,
  prazo: number,
): Record<string, unknown> {
  const resultado: Record<string, unknown> = {};
  if (status === "A") {          // "A" = Ativo? Aprovado?
    resultado["ativo"] = true;
    if (tipo === "P") {          // "P" = Premium? Parcial?
      if (valor > 1500) {        // por que 1500?
        prazo = 30;              // 30 dias? horas?
      }
      resultado["taxaExtra"] = valor * 0.02;
    } else {
      resultado["taxaExtra"] = 0;
    }
  } else {
    resultado["ativo"] = false;
  }
  resultado["prazo"] = prazo;
  resultado["tipo"]  = tipo;
  return resultado;
}

/** Feature Envy: PedidoRuim sabe mais sobre Cliente do que sobre si mesmo. */
class PedidoRuim {
  calcularDescontoFidelidade(cliente: ClienteRuim): number {
    if (cliente.nivelFidelidade === "ouro") {
      const base  = cliente.historicoCompras * 0.05;
      const bonus = cliente.pontosAcumulados * 0.001;
      const anos  = 2026 - parseInt(cliente.dataCadastro.slice(0, 4));
      return Math.min(base + bonus + anos * 2.0, 200);
    }
    if (cliente.nivelFidelidade === "prata") {
      return Math.min(cliente.pontosAcumulados * 0.001, 50);
    }
    return 0;
  }
}

// ============================================================================
// ✅ BOM — Responsabilidade única + Union types + Constantes + Method moved
// ============================================================================

type NivelFidelidade = "bronze" | "prata" | "ouro";
type StatusPedido    = "ativo"  | "inativo";
type TipoPedido      = "premium" | "normal";

const LIMITE_FRETE_GRATIS  = 1500.0;
const PRAZO_PAGAMENTO_DIAS = 30;
const TAXA_PREMIUM         = 0.02;

interface ItemPedido {
  produtoId: string;
  preco: number;
  quantidade: number;
}

/** Feature Envy corrigido: método vive onde os dados vivem. */
class Cliente {
  constructor(
    public readonly id:               string,
    public readonly nome:             string,
    public readonly email:            string,
    public readonly nivelFidelidade:  NivelFidelidade,
    public readonly historicoCompras: number = 0,
    public readonly pontosAcumulados: number = 0,
    public readonly dataCadastro:     string = "2020-01-01",
  ) {}

  calcularDescontoFidelidade(): number {
    if (this.nivelFidelidade === "ouro") {
      const base  = this.historicoCompras * 0.05;
      const bonus = this.pontosAcumulados * 0.001;
      const anos  = 2026 - parseInt(this.dataCadastro.slice(0, 4));
      return Math.min(base + bonus + anos * 2.0, 200);
    }
    if (this.nivelFidelidade === "prata") {
      return Math.min(this.pontosAcumulados * 0.001, 50);
    }
    return 0;
  }
}

class RepositorioCliente {
  buscar(clienteId: string): Cliente {
    console.log(`  [BD] buscar cliente ${clienteId}`);
    return new Cliente(clienteId, "Empresa X", "x@x.com", "ouro", 5000, 200);
  }
  salvar(cliente: Cliente): void {
    console.log(`  [BD] salvar cliente ${cliente.id}`);
  }
}

class ValidadorDocumento {
  validarCpf(cpf: string): boolean {
    return cpf.replace(/[.\-]/g, "").length === 11;
  }
}

class ServicoNotificacao {
  enviarEmail(email: string, assunto: string): void {
    console.log(`  [Email] → ${email}: ${assunto}`);
  }
}

class ServicoCobranca {
  gerarBoleto(valor: number, vencimento: string): string {
    return `BOL-${Math.floor(valor)}-${vencimento}`;
  }
}

class GeradorRelatorio {
  gerar(clienteId: string): string {
    return `Relatório do cliente ${clienteId}`;
  }
  exportarCsv(dados: unknown[]): string {
    return "id,valor\n" + dados.map(String).join("\n");
  }
}

function processarPorStatusBom(
  status: StatusPedido,
  tipo:   TipoPedido,
  valor:  number,
  prazo:  number,
): Record<string, unknown> {
  const resultado: Record<string, unknown> = {};
  if (status === "ativo") {
    resultado["ativo"] = true;
    if (tipo === "premium" && valor > LIMITE_FRETE_GRATIS) {
      prazo = PRAZO_PAGAMENTO_DIAS;
      resultado["taxaExtra"] = Math.round(valor * TAXA_PREMIUM * 100) / 100;
    } else {
      resultado["taxaExtra"] = 0;
    }
  } else {
    resultado["ativo"] = false;
  }
  resultado["prazo"] = prazo;
  resultado["tipo"]  = tipo;
  return resultado;
}

// ============================================================================
// Demo
// ============================================================================

console.log("=== Anti-patterns — TypeScript ===\n");

console.log("❌ God Object:");
const gestorRuim = new GestorPedidosRuim();
const metodosRuim = Object.getOwnPropertyNames(Object.getPrototypeOf(gestorRuim))
  .filter(m => m !== "constructor");
console.log(`  GestorPedidosRuim tem ${metodosRuim.length} métodos públicos`);

console.log("\n✅ God Object corrigido:");
for (const [nome, cls] of [
  ["RepositorioCliente", RepositorioCliente],
  ["ValidadorDocumento", ValidadorDocumento],
  ["ServicoNotificacao", ServicoNotificacao],
  ["ServicoCobranca",    ServicoCobranca],
  ["GeradorRelatorio",   GeradorRelatorio],
] as const) {
  const obj = new (cls as new () => object)();
  const qtd = Object.getOwnPropertyNames(Object.getPrototypeOf(obj))
    .filter(m => m !== "constructor").length;
  console.log(`  ${nome}: ${qtd} método(s)`);
}

console.log("\n❌ Magic Strings/Numbers:");
const rRuim = processarPorStatusRuim("A", "P", 2000, 15);
console.log(`  status='A', tipo='P' → prazo=${rRuim["prazo"]}, taxaExtra=${rRuim["taxaExtra"]}`);

console.log("\n✅ Union types e constantes:");
const rBom = processarPorStatusBom("ativo", "premium", 2000, 15);
console.log(`  status='ativo', tipo='premium' → prazo=${rBom["prazo"]}, taxaExtra=${rBom["taxaExtra"]}`);

console.log("\n❌ Feature Envy:");
const pedidoRuim = new PedidoRuim();
const clienteRuim = gestorRuim.buscarCliente("CLI-100");
const descontoRuim = pedidoRuim.calcularDescontoFidelidade(clienteRuim);
console.log(`  PedidoRuim.calcularDescontoFidelidade(cliente) → R$${descontoRuim.toFixed(2)}`);

console.log("\n✅ Feature Envy corrigido:");
const cliente = new Cliente("CLI-100", "X", "x@x.com", "ouro", 5000, 200);
const desconto = cliente.calcularDescontoFidelidade();
console.log(`  Cliente.calcularDescontoFidelidade() → R$${desconto.toFixed(2)}`);
