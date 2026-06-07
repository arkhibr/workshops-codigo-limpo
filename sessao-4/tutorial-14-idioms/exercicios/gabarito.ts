/**
 * gabarito.ts — Solução do Exercício 22: Idiom Patterns em TypeScript
 * Execute: npx ts-node gabarito.ts
 */

// ─── Idiom 1: Discriminated Union (Result type) ───────────────────────────────
interface Funcionario {
    id:           string;
    nome:         string;
    departamento: string;
    salario:      number;
    contato?:     { email?: { principal?: string } };
}

type ResultadoBusca =
    | { ok: true;  dados: Funcionario }
    | { ok: false; erro: string };

// ─── Idiom 2: função retornando discriminated union ───────────────────────────
function buscarFuncionario(id: string): ResultadoBusca {
    const base: Funcionario[] = [
        { id: "F001", nome: "Ana Silva",  departamento: "TI", salario: 5000.0,
          contato: { email: { principal: "ana@empresa.com" } } },
        { id: "F002", nome: "João Costa", departamento: "RH", salario: 3500.0 },
        { id: "F003", nome: "Maria Lima", departamento: "TI", salario: 6000.0 },
    ];
    const encontrado = base.find(f => f.id === id);
    if (!encontrado) {
        return { ok: false, erro: `Funcionário não encontrado: ${id}` };
    }
    return { ok: true, dados: encontrado };
}

function processarBusca(id: string): string {
    const resultado = buscarFuncionario(id);
    // narrowing seguro — TypeScript sabe o tipo exato em cada branch
    if (!resultado.ok) return `Erro: ${resultado.erro}`;
    return `${resultado.dados.nome} — ${resultado.dados.departamento}: R$${resultado.dados.salario.toFixed(2)}`;
}

// ─── Idiom 3: optional chaining e nullish coalescing ─────────────────────────
function obterEmailFuncionario(func: Funcionario): string {
    return func.contato?.email?.principal ?? 'nao-informado';
}

// ─── Idiom 4: async/await com Promise<ResultadoBusca> ────────────────────────
async function buscarFuncionarioAsync(id: string): Promise<ResultadoBusca> {
    // simula I/O assíncrono
    return buscarFuncionario(id);
}

// ─── Verificação ──────────────────────────────────────────────────────────────
console.log("=== Gabarito 22 TypeScript — Idiom Patterns: Folha de Pagamento ===\n");

// Discriminated Union — sucesso
const r1 = buscarFuncionario("F001");
console.assert(r1.ok === true, "buscarFuncionario F001 deveria ser ok");
console.log(`OK: Discriminated Union — ${processarBusca("F001")}`);

// Discriminated Union — erro
const r2 = buscarFuncionario("F999");
console.assert(r2.ok === false, "buscarFuncionario F999 deveria ser erro");
console.log(`OK: Discriminated Union — erro tratado: ${r2.ok ? '' : r2.erro}`);

// Optional chaining com email presente
const funcComEmail: Funcionario = {
    id: "F001", nome: "Ana Silva", departamento: "TI", salario: 5000.0,
    contato: { email: { principal: "ana@empresa.com" } }
};
const emailAna = obterEmailFuncionario(funcComEmail);
console.assert(emailAna === "ana@empresa.com");
console.log(`OK: Optional chaining — email presente: '${emailAna}'`);

// Nullish coalescing com email ausente
const funcSemEmail: Funcionario = {
    id: "F002", nome: "João Costa", departamento: "RH", salario: 3500.0
};
const emailJoao = obterEmailFuncionario(funcSemEmail);
console.assert(emailJoao === "nao-informado");
console.log(`OK: Nullish coalescing — email ausente retorna '${emailJoao}'`);

// async/await
buscarFuncionarioAsync("F001").then(r => {
    console.assert(r.ok === true);
    console.log(`OK: async/await — buscarFuncionarioAsync resolvido: ${r.ok ? r.dados.nome : ''}`);
});

buscarFuncionarioAsync("F999").then(r => {
    console.assert(r.ok === false);
    console.log(`OK: async/await — buscarFuncionarioAsync erro: ${r.ok ? '' : r.erro}`);
});
