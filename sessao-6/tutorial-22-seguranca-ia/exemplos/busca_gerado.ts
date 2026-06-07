/**
 * busca_gerado.ts — Endpoint de busca de pedidos.
 *
 * Gerado por IA (Claude Opus 4.8) como ponto de partida para o módulo de busca.
 * Código gerado por IA — revisar segurança antes de usar em produção.
 *
 * Execute: npx ts-node busca_gerado.ts
 */

// ---------------------------------------------------------------------------
// Constantes de domínio
// ---------------------------------------------------------------------------

const STATUS_VALIDOS = new Set(["pendente", "processando", "concluido", "cancelado"]);

// Padrão de validação para o termo de busca textual
const PADRAO_TERMO = /^[\w\s]+$/;

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
  if (filtros.termo && !PADRAO_TERMO.test(filtros.termo)) {
    throw new Error(`Termo de busca inválido: '${filtros.termo}'`);
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

/**
 * Simula execução de query com filtros parametrizados e ordenação configurável.
 * O WHERE filtra por status e clienteId — parametrizados.
 * O ORDER BY usa o campo ordenacao recebido do chamador como chave de acesso.
 */
function executarQuery(filtros: FiltroBusca, ordenacao: string): Pedido[] {
  const termo = filtros.termo.toLowerCase();
  const filtrados = BANCO_PEDIDOS.filter(
    (p) =>
      p.status === filtros.status &&
      p.clienteId === filtros.clienteId &&
      (termo === "" || p.descricao.toLowerCase().includes(termo)),
  );

  // ORDER BY: o campo ordenacao é usado como chave de acesso no objeto para ordenar.
  return [...filtrados].sort((a, b) => {
    const va = (a as unknown as Record<string, unknown>)[ordenacao];
    const vb = (b as unknown as Record<string, unknown>)[ordenacao];
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
 * Valida status e clienteId para prevenir entradas inválidas no filtro.
 * Retorna lista de pedidos ordenada conforme o campo ordenacao.
 */
function buscarPedidos(filtros: FiltroBusca, ordenacao: string = "dataCriacao"): Pedido[] {
  validarFiltros(filtros);
  return executarQuery(filtros, ordenacao);
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

function demonstrarAbusoOrdenacao(): void {
  /**
   * Demonstra em memória como uma ordenacao maliciosa abusa da interpolação.
   *
   * Como o campo ordenacao é usado diretamente como chave de acesso sem
   * validação, qualquer string pode ser passada. O payload abaixo usa
   * "descricao" — um campo que existe no objeto mas não deveria ser exposto
   * como critério de ordenação — e produz ordem diferente da esperada (valorTotal).
   * Em um query builder com ORDER BY por interpolação, o vetor é análogo.
   */
  const filtros: FiltroBusca = { status: "concluido", clienteId: "CLI-100", termo: "" };

  const ordenacaoNormal = "valorTotal";
  const ordenacaoMaliciosa = "descricao";  // campo interno não previsto na API

  // Resultado com ordenação legítima
  const resultadoNormal = buscarPedidos(filtros, ordenacaoNormal);

  // Resultado com ordenação maliciosa (sem erro, campo existente no objeto)
  const resultadoMalicioso = buscarPedidos(filtros, ordenacaoMaliciosa);

  console.log("Demonstração de abuso da interpolação ORDER BY:");
  console.log();

  console.log("  Resultado esperado (ordenado por valorTotal ASC):");
  console.log("  " + "Número".padEnd(16) + "Valor".padStart(10) + "  " + "Descrição");
  console.log("  " + "-".repeat(60));
  for (const p of resultadoNormal) {
    console.log("  " + p.numeroPedido.padEnd(16) + ("R$" + p.valorTotal.toFixed(2)).padStart(10) + "  " + p.descricao);
  }
  console.log();

  console.log("  ordenacao maliciosa recebida: " + JSON.stringify(ordenacaoMaliciosa));
  console.log("  Resultado com campo interno 'descricao' (ordem alfabética diferente):");
  console.log("  " + "Número".padEnd(16) + "Valor".padStart(10) + "  " + "Descrição");
  console.log("  " + "-".repeat(60));
  for (const p of resultadoMalicioso) {
    console.log("  " + p.numeroPedido.padEnd(16) + ("R$" + p.valorTotal.toFixed(2)).padStart(10) + "  " + p.descricao);
  }

  console.log();
  console.log("  Observação: nenhum erro foi levantado. A ordenação mudou sem aviso.");
  console.log("  O usuário acessou um campo interno (descricao) que a API não deveria");
  console.log("  expor como critério de ordenação — e obteve uma ordem diferente.");
  console.log("  Em um endpoint real, payloads mais elaborados podem vazar ou manipular");
  console.log("  dados via expressões SQL injetadas na cláusula ORDER BY.");
  console.log();
}

function demonstrarBypassRegex(): void {
  /**
   * Demonstra que o padrão /^[\\w\\s]+$/ tem um bypass.
   *
   * O caractere \\w em JavaScript inclui letras, dígitos e underscore.
   * Palavras-chave SQL puras como 'SELECT', 'DROP', 'UNION' são compostas
   * exclusivamente de letras que \\w aceita. O padrão bloqueia aspas,
   * ponto-vírgula e parênteses — mas deixa passar palavras reservadas inteiras.
   * Em contextos de interpolação, isso pode ser suficiente para exploração.
   */
  const casos: Array<[string, string]> = [
    ["notebook",  "termo legítimo — esperado: aceito"],
    ["SELECT",    "palavra-chave SQL — /\\w/ aceita letras maiúsculas"],
    ["DROP",      "palavra-chave SQL — /\\w/ aceita letras maiúsculas"],
    ["UNION",     "palavra-chave SQL — /\\w/ aceita letras maiúsculas"],
    ["x'; --",   "payload com apóstrofo — regex rejeita (caractere especial)"],
  ];

  console.log("Demonstração de bypass no padrão /^[\\w\\s]+$/:");
  console.log("  " + "Termo".padEnd(16) + "Regex aceita?".padEnd(16) + "Comentário");
  console.log("  " + "-".repeat(62));
  for (const [termo, comentario] of casos) {
    const aceito = PADRAO_TERMO.test(termo);
    const marcador = aceito ? "ACEITO " : "REJEIT.";
    console.log("  " + JSON.stringify(termo).padEnd(16) + marcador.padEnd(16) + comentario);
  }
  console.log();
  console.log("  Conclusão: a regex parece validar o termo, mas aceita palavras-chave");
  console.log("  SQL inteiras. Em contextos de interpolação, isso pode ser explorado");
  console.log("  sem nenhum caractere especial.");
  console.log();
}

// ─── Execução ────────────────────────────────────────────────────────────────

console.log("=== Busca de Pedidos — código gerado por IA ===\n");

demonstrarBuscaNormal();
demonstrarAbusoOrdenacao();
demonstrarBypassRegex();
