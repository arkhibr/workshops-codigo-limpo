/**
 * EXERCÍCIO 22 — Idiom Patterns em TypeScript
 * Tempo estimado: 20 minutos
 *
 * INSTRUÇÕES:
 *   O código abaixo é funcional mas não usa os idioms do TypeScript.
 *   1. ResultadoBusca retorna null quando não encontrado — crie um
 *      Discriminated Union { ok: true; dados: Funcionario } | { ok: false; erro: string }.
 *   2. obterEmailFuncionario() usa encadeamento de && manuais
 *      — substitua por optional chaining ?. e nullish coalescing ??.
 *   3. buscarFuncionarioAsync() está implementado com callback
 *      — converta para async/await com Promise<ResultadoBusca>.
 *   Execute: npx ts-node exercicio.ts (deve rodar antes e depois)
 */

// ─── Interface simples sem discriminante ──────────────────────────────────────
interface Funcionario {
    id:           string;
    nome:         string;
    departamento: string;
    salario:      number;
    contato?:     { email?: { principal?: string } };
}

// ─── Retorna null em vez de discriminated union ───────────────────────────────
function buscarFuncionario(id: string): Funcionario | null {
    const base: Funcionario[] = [
        { id: "F001", nome: "Ana Silva",  departamento: "TI", salario: 5000.0,
          contato: { email: { principal: "ana@empresa.com" } } },
        { id: "F002", nome: "João Costa", departamento: "RH", salario: 3500.0 },
    ];
    for (const f of base) {
        if (f.id === id) return f;
    }
    return null;
}

function processarBusca(id: string): string {
    const resultado = buscarFuncionario(id);
    // sem narrowing de tipo: verificação manual com null
    if (resultado === null) {
        return `Erro: Funcionário não encontrado: ${id}`;
    }
    return `${resultado.nome} — ${resultado.departamento}: R$${resultado.salario.toFixed(2)}`;
}

// ─── Encadeamento manual de && sem optional chaining ─────────────────────────
function obterEmailFuncionario(func: Funcionario): string {
    // ruim: encadeamento manual de &&
    return (func.contato && func.contato.email && func.contato.email.principal)
        ? func.contato.email.principal
        : 'nao-informado';
}

// ─── Callback em vez de async/await ──────────────────────────────────────────
function buscarFuncionarioAsync(id: string, callback: (resultado: Funcionario | null) => void): void {
    // simula I/O assíncrono com setTimeout
    setTimeout(() => {
        callback(buscarFuncionario(id));
    }, 0);
}

// ─── Demo ─────────────────────────────────────────────────────────────────────
console.log("=== Exercício 22 TypeScript — antes dos idioms ===\n");

console.log(processarBusca("F001"));
console.log(processarBusca("F999"));

const funcComEmail: Funcionario = {
    id: "F001", nome: "Ana Silva", departamento: "TI", salario: 5000.0,
    contato: { email: { principal: "ana@empresa.com" } }
};
const funcSemEmail: Funcionario = {
    id: "F002", nome: "João Costa", departamento: "RH", salario: 3500.0
};

console.log(`Email Ana: ${obterEmailFuncionario(funcComEmail)}`);
console.log(`Email João: ${obterEmailFuncionario(funcSemEmail)}`);

buscarFuncionarioAsync("F001", (r) => {
    console.log(`Callback: ${r ? r.nome : 'não encontrado'}`);
});
