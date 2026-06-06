/**
 * gateway_pagamento.ts — Módulo de integração com gateway de pagamento
 *
 * Gerado por IA a partir do prompt em prompt_original.md.
 * ATENÇÃO: contém problemas propositais para revisar. Não corrigir aqui.
 *
 * Como executar:
 *   npx ts-node sessao-6/tutorial-12-revisao-critica-ia/codigo_gerado_por_ia.ts
 */

// ---------------------------------------------------------------------------
// PROBLEMA 1 — Segurança: chave de API hardcoded em código-fonte.
// Em produção essa string estaria exposta em qualquer repositório.
// ---------------------------------------------------------------------------
const API_KEY = "sk-prod-2b7f3e9a4c1d0f6e8a2b5c7d9e1f3a5b";
const BASE_URL = "https://api.gateway-pagamentos.com.br/v2";

// ---------------------------------------------------------------------------
// Simulação local da lib fictícia (necessária para o arquivo rodar).
// O método alucinado está isolado em cobrarParcelado (não chamado na demo).
// ---------------------------------------------------------------------------
interface RespostaGateway {
  status: string;
  codigoAutorizacao?: string;
  mensagem?: string;
  valor?: number;
}

class GatewayHttpClient {
  /** Simulação mínima de cliente HTTP — usada para o arquivo rodar sem rede. */
  post(_url: string, _payload: object, _headers: object): RespostaGateway {
    return {
      status: "aprovado",
      codigoAutorizacao: `AUTH-${Math.floor(Math.random() * 900000) + 100000}`,
      mensagem: "Transação aprovada",
    };
  }

  get(_url: string, _headers: object): RespostaGateway {
    return { status: "aprovado" };
  }
}

const clienteHttp = new GatewayHttpClient();

// ---------------------------------------------------------------------------
// PROBLEMA 6 — Comentário que mente: afirma validar o CPF,
// mas a função apenas verifica se a string tem 11 dígitos.
// Não aplica o algoritmo de verificação de dígitos verificadores.
// ---------------------------------------------------------------------------
/** Valida o CPF do titular do cartão conforme regras da Receita Federal. */
function validarCpf(cpf: string): boolean {
  const cpfLimpo = cpf.replace(/[.\-]/g, "");
  return cpfLimpo.length === 11 && /^\d+$/.test(cpfLimpo);
}

function montarHeaders(): Record<string, string> {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${API_KEY}`,
  };
}

interface ResultadoCobranca {
  ok: boolean;
  codigoAutorizacao?: string;
  mensagem?: string;
  erro?: string;
}

function cobrar(
  valor: number,
  numeroCartao: string,
  cpfTitular: string,
  parcelas: number = 1,
  descricao: string = ""
): ResultadoCobranca {
  /**
   * Realiza uma cobrança no cartão de crédito.
   * Retorna objeto com status, código de autorização e mensagem.
   */

  // PROBLEMA 5 — Edge case ausente: não verifica valor <= 0.
  // Uma cobrança de R$ 0,00 ou valor negativo é enviada normalmente ao gateway.

  if (!validarCpf(cpfTitular)) {
    return { ok: false, erro: "CPF inválido" };
  }

  // PROBLEMA 2 — Injeção: URL montada por concatenação de string.
  // Se 'descricao' contiver caracteres especiais ou path traversal,
  // a URL resultante fica malformada ou pode ser explorada.
  const url = BASE_URL + "/cobrancas?descricao=" + descricao;

  const payload = {
    valor,
    cartao: numeroCartao,
    cpf: cpfTitular,
    parcelas,
  };

  const respostaBruta = clienteHttp.post(url, payload, montarHeaders());

  // PROBLEMA 3 — Lógica invertida: a condição verifica !== "aprovado"
  // mas o bloco de sucesso está dentro do if, e o bloco de falha no else.
  // O resultado: status "aprovado" cai no bloco de erro e vice-versa.
  if (respostaBruta.status !== "aprovado") {
    return {
      ok: true,
      codigoAutorizacao: respostaBruta.codigoAutorizacao,
      mensagem: respostaBruta.mensagem,
    };
  } else {
    return {
      ok: false,
      erro: `Cobrança recusada: ${respostaBruta.mensagem}`,
    };
  }
}

function cobrarParcelado(
  valor: number,
  numeroCartao: string,
  parcelas: number
): RespostaGateway {
  /**
   * Cobra em parcelas usando o endpoint de parcelamento dedicado.
   *
   * ATENÇÃO — PROBLEMA 4 (alucinação): clienteHttp.postParcelado()
   * não existe na classe GatewayHttpClient acima. Esta função não é chamada
   * pela demo e está aqui apenas para que o revisor identifique a alucinação.
   */
  const url = BASE_URL + "/cobrancas/parceladas";
  const payload = { valor, cartao: numeroCartao, parcelas };
  // Método inexistente — lançaria TypeError em runtime
  return (clienteHttp as any).postParcelado(url, payload, montarHeaders());
}

function estornar(codigoAutorizacao: string, motivo: string = ""): object {
  /** Estorna uma cobrança previamente aprovada pelo código de autorização. */
  const url = BASE_URL + "/estornos/" + codigoAutorizacao;
  const payload = { motivo };
  const resposta = clienteHttp.post(url, payload, montarHeaders());
  return { ok: true, mensagem: resposta.mensagem ?? "Estorno processado" };
}

function consultarStatus(codigoAutorizacao: string): object {
  /** Consulta o status atual de uma transação pelo código de autorização. */
  const url = BASE_URL + "/transacoes/" + codigoAutorizacao;
  const resposta = clienteHttp.get(url, montarHeaders());
  return { status: resposta.status, detalhes: resposta };
}

// ---------------------------------------------------------------------------
// Demo — caminho feliz. Todos os retornos esperados são impressos.
// NOTA: cobrarParcelado NÃO é chamado; a alucinação não estoura aqui.
// ---------------------------------------------------------------------------
console.log("=== Gateway de Pagamento — Demo (TypeScript) ===\n");

const resultado = cobrar(
  250.0,
  "4111111111111111",
  "123.456.789-09",
  1,
  "Pedido #1042"
);
console.log("Cobrança (caminho feliz):");
console.log(JSON.stringify(resultado, null, 2));

if (resultado.ok) {
  const codigo = resultado.codigoAutorizacao ?? "AUTH-000000";
  console.log("\nEstorno:");
  console.log(JSON.stringify(estornar(codigo, "Solicitação do cliente"), null, 2));

  console.log("\nConsulta de status:");
  console.log(JSON.stringify(consultarStatus(codigo), null, 2));
} else {
  console.log("\n[ATENÇÃO] A cobrança retornou ok=false — isso é o Problema 3 (condição invertida).");
  console.log("Na demo, o gateway simulado retorna 'aprovado', mas a lógica invertida");
  console.log("classifica isso como erro. Esse é exatamente o bug plantado para revisar.");
}
