/**
 * GABARITO 02 — Funções
 * Abra este arquivo apenas após tentar o exercício por conta própria.
 */

// ─── Interfaces ───────────────────────────────────────────────────────────────

interface Funcionario {
    nome:    string;
    salario: number;
    ativo:   boolean;
}

interface Usuario {
    email: string;
}

interface ItemCarrinho {
    nome:       string;
    preco:      number;
    quantidade: number;
}

interface Carrinho {
    itens: ItemCarrinho[];
    total: number;
}

// ─── Solução 1: Quebrar função grande em responsabilidades únicas ─────────────

const ALIQUOTA_INSS = 0.275;

function calcularSalarioLiquido(salarioBruto: number): number {
    return salarioBruto * (1 - ALIQUOTA_INSS);
}

function calcularBonus(salarioBruto: number): number {
    return salarioBruto > 5000 ? salarioBruto * 0.10 : salarioBruto * 0.05;
}

function calcularRemuneracaoTotal(salarioBruto: number): { liquido: number; bonus: number; total: number } {
    const liquido = calcularSalarioLiquido(salarioBruto);
    const bonus   = calcularBonus(salarioBruto);
    return { liquido, bonus, total: liquido + bonus };
}

function formatarLinhaResumida(funcionario: Funcionario, total: number): string {
    return `${funcionario.nome}: R$${total.toFixed(2)}`;
}

function formatarLinhaDetalhada(
    funcionario: Funcionario,
    salarioLiquido: number,
    bonus: number,
    total: number
): string {
    return `Nome: ${funcionario.nome} | Salário bruto: R$${funcionario.salario.toFixed(2)} | ` +
           `Líquido: R$${salarioLiquido.toFixed(2)} | Bônus: R$${bonus.toFixed(2)} | ` +
           `Total: R$${total.toFixed(2)}`;
}

function formatarLinhaFuncionario(funcionario: Funcionario, formato: string): string {
    const { liquido, bonus, total } = calcularRemuneracaoTotal(funcionario.salario);
    if (formato === "resumido") {
        return formatarLinhaResumida(funcionario, total);
    }
    return formatarLinhaDetalhada(funcionario, liquido, bonus, total);
}

function filtrarFuncionarios(funcionarios: Funcionario[], incluirInativos: boolean): Funcionario[] {
    if (incluirInativos) return funcionarios;
    return funcionarios.filter(f => f.ativo);
}

function gerarRelatorio(funcionarios: Funcionario[], incluirInativos: boolean, formato: string): string[] {
    return filtrarFuncionarios(funcionarios, incluirInativos)
        .map(f => formatarLinhaFuncionario(f, formato));
}

// ─── Solução 2: Duas funções em vez de flag booleana ─────────────────────────

function enviarNotificacaoNormal(usuario: Usuario, mensagem: string): void {
    console.log(`Para: ${usuario.email} | ${mensagem}`);
}

function enviarNotificacaoUrgente(usuario: Usuario, mensagem: string): void {
    console.log(`[URGENTE] Para: ${usuario.email} | ${mensagem}`);
}

// ─── Solução 3: Efeito colateral explícito no retorno ────────────────────────

function adicionarProdutoAoCarrinho(
    carrinho: Carrinho,
    nome: string,
    preco: number,
    quantidade: number
): Carrinho {
    const subtotal = preco * quantidade;
    return {
        itens: [...carrinho.itens, { nome, preco, quantidade }],
        total: carrinho.total + subtotal,
    };
}

// ─── Verificação ──────────────────────────────────────────────────────────────

const funcionarios: Funcionario[] = [
    { nome: "Ana",   salario: 6000.0, ativo: true  },
    { nome: "Bruno", salario: 4000.0, ativo: false },
    { nome: "Carla", salario: 3500.0, ativo: true  },
];

console.log("=== Relatório resumido (todos) ===");
for (const linha of gerarRelatorio(funcionarios, true, "resumido")) {
    console.log(linha);
}

console.log("\n=== Relatório detalhado (apenas ativos) ===");
for (const linha of gerarRelatorio(funcionarios, false, "detalhado")) {
    console.log(linha);
}

console.log("\n=== Notificações ===");
const usuario: Usuario = { email: "ana@empresa.com" };
enviarNotificacaoNormal(usuario, "Reunião amanhã às 9h");
enviarNotificacaoUrgente(usuario, "Servidor fora do ar!");

console.log("\n=== Carrinho (sem estado global) ===");
let carrinho: Carrinho = { itens: [], total: 0 };
carrinho = adicionarProdutoAoCarrinho(carrinho, "Teclado", 250.0, 1);
carrinho = adicionarProdutoAoCarrinho(carrinho, "Mouse", 80.0, 2);
console.log(`Total no carrinho: R$${carrinho.total.toFixed(2)}`);
