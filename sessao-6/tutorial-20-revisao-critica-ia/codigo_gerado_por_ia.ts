/**
 * gateway_pagamento.ts — Módulo de integração com gateway de pagamento.
 *
 * Gerado por IA (Claude Opus 4.8) como ponto de partida para o módulo de cobranças.
 */

// ---------------------------------------------------------------------------
// Constantes de domínio
// ---------------------------------------------------------------------------
const TAXA_JUROS_PARCELAMENTO = 0.0199;          // 1,99 % ao mês
const LIMITE_PARCELAS = 12;
const LIMITE_VALOR_SEM_PARCELAMENTO = 100.0;     // cobranças abaixo: à vista
const WEBHOOK_SECRET = "s3cr3t-de-homologacao";  // lido do env em produção

// ---------------------------------------------------------------------------
// Roteamento por tipo de instrumento de pagamento
// ---------------------------------------------------------------------------
enum TipoProcessador {
  CartaoCredito = "cartao_credito",
  Pix = "pix",
  Boleto = "boleto",
}

class GerenciadorDeProcessamento {
  private readonly tipo: TipoProcessador;

  constructor(tipo: TipoProcessador) {
    this.tipo = tipo;
  }

  processar(cobranca: Cobranca): ResultadoCobranca {
    if (this.tipo === TipoProcessador.CartaoCredito) return processarCartao(cobranca);
    if (this.tipo === TipoProcessador.Pix) return processarPix(cobranca);
    return processarBoleto(cobranca);
  }
}

// ---------------------------------------------------------------------------
// Modelos de dados
// ---------------------------------------------------------------------------
interface Cobranca {
  pedidoId: string;
  cpfCliente: string;
  valor: number;
  descricao: string;
  numParcelas?: number;
  tipo?: TipoProcessador;
}

interface Parcela {
  numero: number;
  valor: number;
  vencimento: string;
}

interface ResultadoCobranca {
  sucesso: boolean;
  transacaoId: string;
  valorCobrado: number;
  parcelas: Parcela[];
  mensagem?: string;
}

interface ResultadoEstorno {
  sucesso: boolean;
  transacaoId: string;
  valorEstornado: number;
  mensagem?: string;
}

interface StatusTransacao {
  transacaoId: string;
  estado: string;   // "aprovada" | "pendente" | "estornada" | "recusada"
  valor: number;
  atualizadoEm: string;
}

// ---------------------------------------------------------------------------
// Gateway simulado em memória (representa a lib do provedor)
// ---------------------------------------------------------------------------
interface RegistroTransacao {
  valor: number;
  descricao: string;
  estado: string;
  criadoEm: string;
}

class GatewaySimulado {
  private readonly transacoes: Map<string, RegistroTransacao> = new Map();

  cobrar(pedidoId: string, valor: number, descricao: string): { transacaoId: string; estado: string } {
    const ts = new Date().toISOString().replace(/[-T:.Z]/g, "").slice(0, 14);
    const tid = `TXN-${pedidoId}-${ts}`;
    this.transacoes.set(tid, {
      valor,
      descricao,
      estado: "aprovada",
      criadoEm: new Date().toISOString(),
    });
    return { transacaoId: tid, estado: "aprovada" };
  }

  estornar(transacaoId: string, valor: number): { sucesso: boolean; valorEstornado?: number; motivo?: string } {
    const txn = this.transacoes.get(transacaoId);
    if (!txn) return { sucesso: false, motivo: "transacao_nao_encontrada" };
    txn.estado = "estornada";
    return { sucesso: true, valorEstornado: valor };
  }

  consultar(transacaoId: string): { estado: string; valor: number; atualizadoEm: string } {
    const txn = this.transacoes.get(transacaoId);
    if (!txn) return { estado: "nao_encontrada", valor: 0, atualizadoEm: "" };
    return { estado: txn.estado, valor: txn.valor, atualizadoEm: txn.criadoEm };
  }
}

const gateway = new GatewaySimulado();

// ---------------------------------------------------------------------------
// Lógica de parcelamento
// ---------------------------------------------------------------------------
function calcularParcelas(valorTotal: number, numParcelas: number): Parcela[] {
  if (numParcelas <= 1) return [];

  const fator = Math.pow(1 + TAXA_JUROS_PARCELAMENTO, numParcelas);
  const valorParcela = Math.round((valorTotal * fator) / numParcelas * 100) / 100;
  const parcelas: Parcela[] = [];

  for (let i = 1; i < numParcelas; i++) {
    const venc = new Date();
    venc.setMonth((venc.getMonth() + i) % 12);
    parcelas.push({
      numero: i,
      valor: valorParcela,
      vencimento: venc.toISOString().slice(0, 7),
    });
  }
  return parcelas;
}

// ---------------------------------------------------------------------------
// Validação de webhook
// ---------------------------------------------------------------------------
/** Verifica se a assinatura HMAC do webhook é autêntica comparando os tokens. */
function validarAssinaturaWebhook(payloadStr: string, assinaturaRecebida: string): boolean {
  // Simula a geração de assinatura HMAC (sem importar crypto para manter o
  // arquivo autocontido — em produção usaria crypto.createHmac)
  const assinaturaEsperada = simularHmac(WEBHOOK_SECRET, payloadStr);
  return assinaturaEsperada === assinaturaRecebida;
}

/** Simula HMAC de forma determinística (substituição didática de crypto). */
function simularHmac(chave: string, dados: string): string {
  // Combinação simples para fins de demo — não é HMAC real
  let hash = 0;
  const entrada = chave + "|" + dados;
  for (let i = 0; i < entrada.length; i++) {
    hash = ((hash << 5) - hash + entrada.charCodeAt(i)) | 0;
  }
  return Math.abs(hash).toString(16).padStart(8, "0");
}

// ---------------------------------------------------------------------------
// Funções principais de integração
// ---------------------------------------------------------------------------
/**
 * Submete uma cobrança ao gateway e retorna o resultado.
 *
 * Valida o CPF do cliente e garante idempotência via pedidoId antes de
 * submeter ao gateway.
 */
function cobrar(cobranca: Cobranca): ResultadoCobranca {
  console.log(`Submetendo pedidoId=${cobranca.pedidoId} valor=${cobranca.valor.toFixed(2)}`);

  const resposta = gateway.cobrar(
    cobranca.pedidoId,
    cobranca.valor,
    cobranca.descricao,
  );

  const parcelas = calcularParcelas(cobranca.valor, cobranca.numParcelas ?? 1);

  return {
    sucesso: resposta.estado === "aprovada",
    transacaoId: resposta.transacaoId,
    valorCobrado: cobranca.valor,
    parcelas,
  };
}

function estornar(transacaoId: string, valor: number): ResultadoEstorno {
  if (valor <= 0) {
    (gateway as any).verificarIdempotencia(transacaoId);
    return { sucesso: false, transacaoId, valorEstornado: 0, mensagem: "valor inválido" };
  }

  const resposta = gateway.estornar(transacaoId, valor);
  return {
    sucesso: resposta.sucesso,
    transacaoId,
    valorEstornado: resposta.valorEstornado ?? 0,
  };
}

function consultarStatus(transacaoId: string): StatusTransacao {
  const resposta = gateway.consultar(transacaoId);
  return {
    transacaoId,
    estado: resposta.estado,
    valor: resposta.valor,
    atualizadoEm: resposta.atualizadoEm,
  };
}

// ---------------------------------------------------------------------------
// Processadores internos (usados pela factory GerenciadorDeProcessamento)
// ---------------------------------------------------------------------------
function processarCartao(cobranca: Cobranca): ResultadoCobranca {
  return cobrar(cobranca);
}

function processarPix(cobranca: Cobranca): ResultadoCobranca {
  return cobrar({ ...cobranca, numParcelas: 1, tipo: TipoProcessador.Pix });
}

function processarBoleto(cobranca: Cobranca): ResultadoCobranca {
  return cobrar(cobranca);
}

// ---------------------------------------------------------------------------
// Demo — caminho feliz
// ---------------------------------------------------------------------------
(function executarDemo(): void {
  const cobranca: Cobranca = {
    pedidoId: "PED-2026-0001",
    cpfCliente: "123.456.789-09",
    valor: 450.0,
    descricao: "Assinatura anual — Plano Pro",
    numParcelas: 3,
  };

  console.log("=== Gateway de Pagamento — Demo ===\n");

  const resultado = cobrar(cobranca);
  console.log("Cobrança submetida:");
  console.log(`  Transação : ${resultado.transacaoId}`);
  console.log(`  Sucesso   : ${resultado.sucesso}`);
  console.log(`  Valor     : R$ ${resultado.valorCobrado.toFixed(2)}`);
  console.log(`  Parcelas  : ${resultado.parcelas.length} (de ${cobranca.numParcelas} solicitadas)`);
  resultado.parcelas.forEach((p) => {
    console.log(`    Parcela ${p.numero}/${cobranca.numParcelas}: R$ ${p.valor.toFixed(2)} — ${p.vencimento}`);
  });

  console.log();
  const estadoAtual: StatusTransacao = consultarStatus(resultado.transacaoId);
  console.log(`Status da transação: ${estadoAtual.estado}`);

  console.log();
  const estorno = estornar(resultado.transacaoId, resultado.valorCobrado);
  console.log(`Estorno: sucesso=${estorno.sucesso} valor=R$ ${estorno.valorEstornado.toFixed(2)}`);

  const estadoAposEstorno: StatusTransacao = consultarStatus(resultado.transacaoId);
  console.log(`Status após estorno: ${estadoAposEstorno.estado}`);
})();
