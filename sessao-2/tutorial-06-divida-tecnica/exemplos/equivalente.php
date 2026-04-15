<?php
/**
 * EQUIVALENTE PHP — Dívida de Duplicação
 * Referência: Clean Code, Cap. 17
 *
 * Foco: como a duplicação de código cria dívida técnica em PHP
 * e como eliminá-la extraindo uma função compartilhada.
 */

// ════════════════════════════════════════════════════════════════
// ANTES — validação duplicada em dois métodos
// ════════════════════════════════════════════════════════════════

class AutenticacaoService_Ruim
{
    public function login(string $email, string $senha): array
    {
        // ❌ Duplicação: mesma validação copiada em login() e em renovarToken()
        if (empty($email) || strlen($email) < 3) {
            return ['ok' => false, 'msg' => 'e-mail inválido'];
        }
        if (!str_contains($email, '@')) {
            return ['ok' => false, 'msg' => 'e-mail inválido'];
        }
        if (empty($senha) || strlen($senha) < 8) {
            return ['ok' => false, 'msg' => 'senha fraca'];
        }
        if (ctype_digit($senha)) {
            return ['ok' => false, 'msg' => 'senha só com números'];
        }

        $hash = hash('sha256', $senha);
        $token = md5($email . $hash . time());
        return ['ok' => true, 'token' => $token];
    }

    public function renovarToken(string $email, string $senha, string $tokenAtual): array
    {
        // ❌ Duplicação: cópia idêntica da validação acima
        if (empty($email) || strlen($email) < 3) {
            return ['ok' => false, 'msg' => 'e-mail inválido'];
        }
        if (!str_contains($email, '@')) {
            return ['ok' => false, 'msg' => 'e-mail inválido'];
        }
        if (empty($senha) || strlen($senha) < 8) {
            return ['ok' => false, 'msg' => 'senha fraca'];
        }
        if (ctype_digit($senha)) {
            return ['ok' => false, 'msg' => 'senha só com números'];
        }

        if (strlen($tokenAtual) !== 32) {
            return ['ok' => false, 'msg' => 'token inválido'];
        }

        $hash = hash('sha256', $senha);
        $novoToken = md5($email . $hash . time());
        return ['ok' => true, 'token' => $novoToken];
    }
}


// ════════════════════════════════════════════════════════════════
// DEPOIS — duplicação eliminada com função extraída
// ════════════════════════════════════════════════════════════════

const TAMANHO_MINIMO_EMAIL = 3;
const TAMANHO_MINIMO_SENHA = 8;
const TAMANHO_TOKEN_MD5 = 32;

class AutenticacaoService
{
    public function login(string $email, string $senha): array
    {
        $validacao = $this->validarCredenciais($email, $senha);
        if (!$validacao['valido']) {
            return ['ok' => false, 'msg' => $validacao['erros'][0]];
        }

        $hash = hash('sha256', $senha);
        $token = md5($email . $hash . time());
        return ['ok' => true, 'token' => $token];
    }

    public function renovarToken(string $email, string $senha, string $tokenAtual): array
    {
        $validacao = $this->validarCredenciais($email, $senha);
        if (!$validacao['valido']) {
            return ['ok' => false, 'msg' => $validacao['erros'][0]];
        }

        if (strlen($tokenAtual) !== TAMANHO_TOKEN_MD5) {
            return ['ok' => false, 'msg' => 'token inválido'];
        }

        $hash = hash('sha256', $senha);
        $novoToken = md5($email . $hash . time());
        return ['ok' => true, 'token' => $novoToken];
    }

    // ── Privado ──────────────────────────────────────────────────────────

    private function validarCredenciais(string $email, string $senha): array
    {
        $erros = [];

        if (empty($email) || strlen($email) < TAMANHO_MINIMO_EMAIL) {
            $erros[] = 'e-mail muito curto';
        }

        if (!empty($email) && !str_contains($email, '@')) {
            $erros[] = 'e-mail inválido';
        }

        if (empty($senha) || strlen($senha) < TAMANHO_MINIMO_SENHA) {
            $erros[] = 'senha deve ter ao menos 8 caracteres';
        }

        if (!empty($senha) && ctype_digit($senha)) {
            $erros[] = 'senha não pode conter apenas números';
        }

        return ['valido' => empty($erros), 'erros' => $erros];
    }
}
