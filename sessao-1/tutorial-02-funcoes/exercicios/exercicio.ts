/**
 * EXERCÍCIO 02 — Funções
 * Tempo estimado: 15 minutos
 * Referência: Clean Code, Cap. 3
 *
 * INSTRUÇÕES:
 *   Refatore as funções abaixo aplicando os princípios do Clean Code:
 *   - Cada função deve fazer UMA coisa
 *   - Extraia funções auxiliares com nomes descritivos
 *   - Elimine flags booleanas (crie funções separadas)
 *   - Elimine efeitos colaterais ocultos
 *
 *   Não mude o comportamento externo — apenas a organização interna.
 *
 * Execute: npx ts-node exercicio.ts
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

// ─── Problema 1 ───────────────────────────────────────────────────────────────
// Esta função faz pelo menos 4 coisas diferentes. Quebre-a.

function gerarRelatorio(funcionarios: Funcionario[], incluirInativos: boolean, formato: string): string[] {
    const resultado: string[] = [];
    for (const f of funcionarios) {
        if (!incluirInativos && !f.ativo) continue;
        const salarioLiquido = f.salario - f.salario * 0.275;
        const bonus          = f.salario > 5000 ? f.salario * 0.10 : f.salario * 0.05;
        const total          = salarioLiquido + bonus;
        let linha: string;
        if (formato === "resumido") {
            linha = `${f.nome}: R$${total.toFixed(2)}`;
        } else {
            linha = `Nome: ${f.nome} | Salário bruto: R$${f.salario.toFixed(2)} | ` +
                    `Líquido: R$${salarioLiquido.toFixed(2)} | Bônus: R$${bonus.toFixed(2)} | ` +
                    `Total: R$${total.toFixed(2)}`;
        }
        resultado.push(linha);
    }
    return resultado;
}

// ─── Problema 2 ───────────────────────────────────────────────────────────────
// Flag booleana — crie duas funções distintas.

function enviarNotificacao(usuario: Usuario, mensagem: string, urgente: boolean): void {
    if (urgente) {
        console.log(`[URGENTE] Para: ${usuario.email} | ${mensagem}`);
    } else {
        console.log(`Para: ${usuario.email} | ${mensagem}`);
    }
}

// ─── Problema 3 ───────────────────────────────────────────────────────────────
// Efeito colateral oculto — torne o efeito explícito no retorno.

const carrinhoGlobal: Carrinho = { itens: [], total: 0 };

function adicionarProduto(nome: string, preco: number, quantidade: number): number {
    const subtotal = preco * quantidade;
    carrinhoGlobal.itens.push({ nome, preco, quantidade });
    carrinhoGlobal.total += subtotal;   // efeito colateral oculto!
    return subtotal;
}

// ─── Verificação (não altere este bloco) ──────────────────────────────────────

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
enviarNotificacao(usuario, "Reunião amanhã às 9h", false);
enviarNotificacao(usuario, "Servidor fora do ar!", true);

console.log("\n=== Carrinho ===");
adicionarProduto("Teclado", 250.0, 1);
adicionarProduto("Mouse", 80.0, 2);
console.log(`Total no carrinho: R$${carrinhoGlobal.total.toFixed(2)}`);
