<?php
/**
 * EQUIVALENTE PHP — Comentários
 * Referência: Clean Code, Cap. 4
 *
 * Foco: PHPDoc mal usado, código comentado, comentário redundante.
 */

// ════════════════════════════════════════════════════════════════
// PROBLEMA 1: PHPDoc redundante — repete o óbvio
// ════════════════════════════════════════════════════════════════

// ❌ Ruim: PHPDoc que não agrega nada além do que a assinatura já diz
/**
 * Calcula o total.
 *
 * @param float $preco O preço.
 * @param int $quantidade A quantidade.
 * @return float O total.
 */
function calcularTotal(float $preco, int $quantidade): float {
    return $preco * $quantidade;
}

// ✅ Bom: PHPDoc só quando agrega informação real (exceção, restrição, contexto)
/**
 * Calcula o valor líquido retendo ISS na fonte.
 *
 * A alíquota é fixada em 2% conforme contrato-padrão (cláusula 7.3, rev. 2025).
 * Não use esta função para contratos com cláusula de ISS variável.
 *
 * @throws \InvalidArgumentException se $valorBruto for negativo.
 */
function calcularValorLiquido(float $valorBruto): float {
    if ($valorBruto < 0) {
        throw new \InvalidArgumentException('Valor bruto não pode ser negativo.');
    }
    return $valorBruto * 0.98;
}


// ════════════════════════════════════════════════════════════════
// PROBLEMA 2: Código comentado sem explicação
// ════════════════════════════════════════════════════════════════

// ❌ Ruim: bloco comentado — por que está aqui? É temporário? Deve voltar?
function processarPagamento_ruim(float $valor, string $metodo): float {
    // if ($metodo === 'pix') {
    //     $taxa = 0.0;
    // } elseif ($metodo === 'debito') {
    //     $taxa = 0.005;
    // }
    // $valorFinal = $valor * (1 + $taxa);
    // enviarParaGatewayAntigo($valorFinal);

    $taxa = $metodo === 'credito' ? 0.025 : 0.0;
    return $valor * (1 + $taxa);
}

// ✅ Bom: sem código morto. Se precisar consultar o histórico, use git log.
const TAXA_CREDITO = 0.025;

function processarPagamento(float $valor, string $metodo): float {
    $taxa = $metodo === 'credito' ? TAXA_CREDITO : 0.0;
    return $valor * (1 + $taxa);
}


// ════════════════════════════════════════════════════════════════
// PROBLEMA 3: Comentário redundante que repete a assinatura
// ════════════════════════════════════════════════════════════════

// ❌ Ruim
function buscarUsuario_ruim(string $id): array {
    // busca o usuário pelo id
    return ['id' => $id, 'nome' => 'Mock'];
}

// ✅ Bom: comentário explica o "porquê" do mock, não o "o quê"
function buscarUsuario(string $id): array {
    // TODO [PLAT-1847]: substituir por chamada real ao microsserviço de usuários.
    // Serviço em homologação até Sprint 42. Responsável: @ana.souza
    return ['id' => $id, 'nome' => 'Mock'];
}
