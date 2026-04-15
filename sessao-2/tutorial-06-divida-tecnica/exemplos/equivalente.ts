/**
 * EQUIVALENTE TypeScript — Dívida de Magic Numbers
 * Referência: Clean Code, Cap. 17
 *
 * Foco: como magic numbers criam dívida técnica em TypeScript
 * e como eliminá-los com constantes nomeadas.
 */

// ════════════════════════════════════════════════════════════════
// ANTES — magic numbers espalhados pelo código
// ════════════════════════════════════════════════════════════════

// ❌ O que significa 3600? E 900? E 86400? E 8? E 32?
function autenticarUsuario_ruim(email: string, senha: string, tipo: string) {
  if (!email || email.length < 3) {
    return { ok: false, msg: "e-mail inválido" };
  }

  if (!senha || senha.length < 8) {
    return { ok: false, msg: "senha fraca" };
  }

  let expiracao: number;
  if (tipo === "admin") {
    expiracao = Math.floor(Date.now() / 1000) + 900;
  } else if (tipo === "permanente") {
    expiracao = Math.floor(Date.now() / 1000) + 86400;
  } else {
    expiracao = Math.floor(Date.now() / 1000) + 3600;
  }

  return { ok: true, expiracao };
}

function renovarToken_ruim(token: string): boolean {
  // O que significa 32 aqui?
  return token.length === 32;
}

function calcularTentativasRestantes_ruim(tentativas: number): number {
  // Por que 5? Qual é a política?
  return 5 - tentativas;
}


// ════════════════════════════════════════════════════════════════
// DEPOIS — constantes nomeadas que explicam o negócio
// ════════════════════════════════════════════════════════════════

// ── Constantes de autenticação ────────────────────────────────────────────────

const TAMANHO_MINIMO_EMAIL = 3;
const TAMANHO_MINIMO_SENHA = 8;

const EXPIRACAO_TOKEN_BASICO_SEGUNDOS = 3_600;   // 1 hora
const EXPIRACAO_TOKEN_ADMIN_SEGUNDOS = 900;       // 15 minutos — sessão privilegiada expira rápido
const EXPIRACAO_TOKEN_PERMANENTE_SEGUNDOS = 86_400; // 24 horas

const TAMANHO_TOKEN_MD5 = 32;

// Política de bloqueio: 5 tentativas antes de bloquear a conta
const MAX_TENTATIVAS_LOGIN = 5;

// ── Funções ───────────────────────────────────────────────────────────────────

function autenticarUsuario(
  email: string,
  senha: string,
  tipoPerfil: string = "basico",
) {
  if (!email || email.length < TAMANHO_MINIMO_EMAIL) {
    return { ok: false, msg: "e-mail inválido" };
  }

  if (!senha || senha.length < TAMANHO_MINIMO_SENHA) {
    return { ok: false, msg: "senha deve ter ao menos 8 caracteres" };
  }

  const expiracao = calcularExpiracaoToken(tipoPerfil);
  return { ok: true, expiracao, tipoPerfil };
}

function calcularExpiracaoToken(tipoPerfil: string): number {
  const agora = Math.floor(Date.now() / 1000);

  if (tipoPerfil === "admin") {
    return agora + EXPIRACAO_TOKEN_ADMIN_SEGUNDOS;
  }

  if (tipoPerfil === "permanente") {
    return agora + EXPIRACAO_TOKEN_PERMANENTE_SEGUNDOS;
  }

  return agora + EXPIRACAO_TOKEN_BASICO_SEGUNDOS;
}

function tokenEhValido(token: string): boolean {
  return token.length === TAMANHO_TOKEN_MD5;
}

function calcularTentativasRestantes(tentativasRealizadas: number): number {
  return MAX_TENTATIVAS_LOGIN - tentativasRealizadas;
}

function contaEstaBloqueada(tentativasRealizadas: number): boolean {
  return tentativasRealizadas >= MAX_TENTATIVAS_LOGIN;
}
