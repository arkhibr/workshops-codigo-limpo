/**
 * busca_revisado.ts — Endpoint de busca de pedidos (versão endurecida).
 *
 * Corrige três brechas presentes em busca_gerado.ts:
 *   1. ORDER BY interpolado → validação via allow-list antes de qualquer uso.
 *   2. Regex com bypass (/^[\w\s]+$/) → padrão restrito sem underscore nem wildcards.
 *   3. LIKE por concatenação → filter com includes() parametrizado (não concatenado).
 *
 * Qualquer campo de ordenação ou termo fora dos critérios aceitos é rejeitado
 * com Error antes de chegar à lógica de busca.
 *
 * Execute: npx ts-node busca_revisado.ts
 */

// ---------------------------------------------------------------------------
// Constantes de domínio
// ---------------------------------------------------------------------------

const STATUS_VALIDOS = new Set(["pendente", "processando", "concluido", "cancelado"]);

const CAMPOS_ORDENACAO_PERMITIDOS = new Set([
  "dataCriacao",
  "valorTotal",
  "numeroPedido",
]);

// Padrão restrito: apenas letras (incluindo acentuadas), dígitos e espaço,
// com comprimento máximo explícito. Fecha os caracteres que tornariam um LIKE
// perigoso se concatenado (%, _, ;, aspas, parênteses, underscore via \w).
const PADRAO_TERMO_SEGURO = /^[a-zA-ZÀ-ÿ0-9 ]{1,50}$/;

// ---------------------------------------------------------------------------
// Modelos de dados
// ---------------------------------------------------------------------------

interface FiltroBusca {
  status:    string;
  clienteId: string;
  termo:     string;
}

interface Pedido {
  id:           number;
  numeroPedido: string;
  clienteId:    string;
  status:       string;
  valorTotal:   number;
  dataCriacao:  string;
  descricao:    string;
}

function validarFiltros(filtros: FiltroBusca): void {
  if (!STATUS_VALIDOS.has(filtros.status)) {
    throw new Error(`Status inválido: '${filtros.status}'`);
  }
  if (!filtros.clienteId.trim()) {
    throw new Error("clienteId não pode ser vazio");
  }
  if (filtros.termo && !PADRAO_TERMO_SEGURO.test(filtros.termo)) {
    throw new Error(
      `Termo de busca inválido: '${filtros.termo}'. ` +
      "Use apenas letras e espaços (máx. 50 caracteres).",
    );
  }
}

// ---------------------------------------------------------------------------
// Banco de dados simulado em memória
// ---------------------------------------------------------------------------

const BANCO_PEDIDOS: Pedido[] = [
  { id: 1, numeroPedido: "PED-2026-0001", clienteId: "CLI-100", status: "concluido",   valorTotal:  450.00, dataCriacao: "2026-05-10", descricao: "webcam full hd 1080p" },
  { id: 2, numeroPedido: "PED-2026-0002", clienteId: "CLI-100", status: "concluido",   valorTotal:  980.50, dataCriacao: "2026-05-22", descricao: "adaptador usb thunderbolt" },
  { id: 3, numeroPedido: "PED-2026-0003", clienteId: "CLI-100", status: "processando", valorTotal:  275.00, dataCriacao: "2026-06-01", descricao: "teclado mecânico compacto" },
  { id: 4, numeroPedido: "PED-2026-0004", clienteId: "CLI-200", status: "concluido",   valorTotal: 1200.00, dataCriacao: "2026-05-15", descricao: "notebook premium 15 polegadas" },
  { id: 5, numeroPedido: "PED-2026-0005", clienteId: "CLI-200", status: "pendente",    valorTotal:  330.75, dataCriacao: "2026-06-04", descricao: "mouse ergonômico sem fio" },
];

// ---------------------------------------------------------------------------
// Validação de segurança
// ---------------------------------------------------------------------------

/**
 * Valida que o campo de ordenação pertence ao allow-list.
 *
 * Em query builders e ORMs, ORDER BY frequentemente não aceita parâmetro
 * posicional — a coluna precisa ser interpolada. Esta função garante que
 * apenas campos conhecidos sejam usados na ordenação.
 * Qualquer outro valor é rejeitado antes de chegar à lógica de busca.
 */
function campoOrdenacaoSeguro(ordenacao: string): keyof Pedido {
  const campo = ordenacao.trim();
  if (!CAMPOS_ORDENACAO_PERMITIDOS.has(campo)) {
    throw new Error(
      `Campo de ordenação inválido: '${ordenacao}'. ` +
      `Permitidos: ${[...CAMPOS_ORDENACAO_PERMITIDOS].sort().join(", ")}`,
    );
  }
  return campo as keyof Pedido;
}

/**
 * Executa a busca simulada com filtros validados e ordenação via allow-list.
 * O termo vai como valor ao filter/includes — nunca concatenado na query.
 */
function executarQuery(filtros: FiltroBusca, campo: keyof Pedido): Pedido[] {
  const termo = filtros.termo.toLowerCase();
  const filtrados = BANCO_PEDIDOS.filter(
    (p) =>
      p.status === filtros.status &&
      p.clienteId === filtros.clienteId &&
      (termo === "" || p.descricao.toLowerCase().includes(termo)),
  );
  return [...filtrados].sort((a, b) => {
    const va = a[campo];
    const vb = b[campo];
    if (typeof va === "number" && typeof vb === "number") return va - vb;
    return String(va ?? "").localeCompare(String(vb ?? ""));
  });
}

// ---------------------------------------------------------------------------
// Lógica de busca
// ---------------------------------------------------------------------------

/**
 * Busca pedidos aplicando os filtros fornecidos e ordenando pelo campo indicado.
 *
 * WHERE parametrizado: status e clienteId validados antes do filtro.
 * ORDER BY: campo validado por allow-list antes de qualquer uso na ordenação.
 * Termo: validado por regex restrita; passado como valor (não concatenado).
 * Levanta Error para qualquer entrada fora dos critérios aceitos.
 */
function buscarPedidos(filtros: FiltroBusca, ordenacao: string = "dataCriacao"): Pedido[] {
  validarFiltros(filtros);
  const campo = campoOrdenacaoSeguro(ordenacao);
  return executarQuery(filtros, campo);
}

// ---------------------------------------------------------------------------
// Demo
// ---------------------------------------------------------------------------

function demonstrarBuscaNormal(): void {
  const filtros: FiltroBusca = { status: "concluido", clienteId: "CLI-100", termo: "" };
  const resultados = buscarPedidos(filtros, "valorTotal");

  console.log("Busca normal (status=concluido, cliente=CLI-100, ordem=valorTotal):");
  console.log("  " + "Número".padEnd(16) + "Valor".padStart(10) + "  " + "Data");
  console.log("  " + "-".repeat(44));
  for (const p of resultados) {
    console.log("  " + p.numeroPedido.padEnd(16) + ("R$" + p.valorTotal.toFixed(2)).padStart(10) + "  " + p.dataCriacao);
  }
  console.log();
}

function demonstrarRejeicaoOrdenacaoMaliciosa(): void {
  const filtros: FiltroBusca = { status: "concluido", clienteId: "CLI-100", termo: "" };
  const ordenacaoMaliciosa = "valorTotal DESC, (SELECT 1)";

  console.log("Tentativa com ordenacao maliciosa:");
  console.log("  ordenacao recebida: " + JSON.stringify(ordenacaoMaliciosa));
  try {
    buscarPedidos(filtros, ordenacaoMaliciosa);
    console.log("  FALHOU: a busca executou sem erro — allow-list não funcionou.");
  } catch (erro) {
    console.log("  Bloqueado antes da query: " + (erro as Error).message);
  }
  console.log();
}

function demonstrarRejeicaoCaracteresEspeciais(): void {
  const casos: Array<[string, string]> = [
    ["notebook",       "termo legítimo"],
    ["monitor 34",     "termo com espaço — legítimo"],
    ["x'; DROP TABLE", "payload com aspas e ponto-vírgula"],
    ["%_wildcard",     "wildcards LIKE — rejeitados"],
    ["a".repeat(51),   "termo muito longo — rejeitado"],
  ];

  console.log("Tentativas com termos suspeitos (validação de entrada):");
  console.log("  " + "Termo".padEnd(20) + "Resultado");
  console.log("  " + "-".repeat(56));
  for (const [termo, descricao] of casos) {
    try {
      const filtros: FiltroBusca = { status: "concluido", clienteId: "CLI-100", termo };
      validarFiltros(filtros);
      console.log("  " + JSON.stringify(termo.slice(0, 16)).padEnd(20) + "Aceito (" + descricao + ")");
    } catch {
      console.log("  " + JSON.stringify(termo.slice(0, 16)).padEnd(20) + "Rejeitado (" + descricao + ")");
    }
  }
  console.log();
  console.log("  Mesmo que um termo passe a regex, ele vai como valor ao filter/includes");
  console.log("  — nunca concatenado na string da query.");
  console.log();
}

// ─── Execução ────────────────────────────────────────────────────────────────

console.log("=== Busca de Pedidos — versão endurecida ===\n");

demonstrarBuscaNormal();
demonstrarRejeicaoOrdenacaoMaliciosa();
demonstrarRejeicaoCaracteresEspeciais();
