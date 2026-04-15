/**
 * EQUIVALENTE TypeScript — Funções
 * Referência: Clean Code, Cap. 3
 */

interface Item    { preco: number; quantidade: number; }
interface Endereco { rua: string; numero: string; cidade: string; uf: string; }

// ─── ✅ Uma responsabilidade por função ────────────────────────────────────────

const CUPONS: Record<string, number> = {
  DESCONTO10: 0.90,
  DESCONTO20: 0.80,
};

function calcularTotalItens(itens: Item[]): number {
  return itens.reduce((acc, item) => acc + item.preco * item.quantidade, 0);
}

function aplicarCupom(total: number, cupom: string | null): number {
  return total * (CUPONS[cupom ?? ''] ?? 1.0);
}

function formatarEndereco(endereco: Endereco): string {
  return `${endereco.rua}, ${endereco.numero} - ${endereco.cidade}/${endereco.uf}`;
}

// ─── ❌ Flag booleana ──────────────────────────────────────────────────────────

function formatarNome(nome: string, formal: boolean): string {
  return formal ? `Sr(a). ${nome}` : nome;
}

// ─── ✅ Duas funções ou overload ───────────────────────────────────────────────

const formatarNomeInformal = (nome: string): string => nome;
const formatarNomeFormal   = (nome: string): string => `Sr(a). ${nome}`;

// ─── ✅ Objeto em vez de lista longa de parâmetros ────────────────────────────

interface DadosUsuario {
  nome: string;
  email: string;
  perfil: string;
  ativo: boolean;
}

function criarUsuario(dados: DadosUsuario): DadosUsuario {
  return { ...dados };
}
