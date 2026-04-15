/**
 * EQUIVALENTE TypeScript — Nomes Significativos
 * Referência: Clean Code, Cap. 2
 */

// ❌ Ruim
let d = 0;
const get = (l: any[], s: string) => l.filter(i => i[0] === s);

// ✅ Bom
let diasDesdemCriacao = 0;
const filtrarPedidosPorStatus = (pedidos: Pedido[], status: string): Pedido[] =>
  pedidos.filter(pedido => pedido.status === status);

// ❌ Tipos usados como prefixo (antipadrão em TS — o tipo já está na assinatura)
const strNome: string  = "João";
const numIdade: number = 30;
const arrItens: any[]  = [];

// ✅ Sem prefixos redundantes
const nome: string  = "João";
const idade: number = 30;
const itens: Item[] = [];

// ❌ Interface com nomes obscuros
interface UsrRcrd {
  nm: string;
  ag: number;
  actv: boolean;
}

// ✅ Interface expressiva
interface Usuario {
  nome: string;
  idade: number;
  ativo: boolean;
}

// ─── Tipos auxiliares usados acima ────────────────────────────────────────────
interface Pedido { status: string; descricao: string; }
interface Item   { id: number; nome: string; }
