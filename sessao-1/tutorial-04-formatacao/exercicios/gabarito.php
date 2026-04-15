<?php
/**
 * GABARITO — Tutorial 04: Formatação
 * Referência: Clean Code, Cap. 5
 * Execute: php gabarito.php
 *
 * Formatação: PSR-12 / phpcs --standard=PSR12
 * Lógica: idêntica ao exercicio.php — apenas formatação alterada.
 */

// ── Imports ───────────────────────────────────────────────────────────────────
use DateTime;
use InvalidArgumentException;
use stdClass;

// ── Constantes ────────────────────────────────────────────────────────────────

const STATUS_APROVADO          = 'aprovado';
const STATUS_RECUSADO          = 'recusado';
const STATUS_PENDENTE          = 'pendente';

const TAXA_PROCESSAMENTO       = 0.025;
const LIMITE_DIARIO            = 10000.0;
const VALOR_MINIMO_PAGAMENTO   = 1.0;

// ── Classes ───────────────────────────────────────────────────────────────────

class ProcessadorDePagamentos
{
    private string  $nomeComercianteprivate;
    private float   $limitePrivateDiario;
    private float   $_totalProcessadoHoje = 0.0;
    private array   $_historico           = [];
    private ?array  $_ultimaTransacao     = null;

    public function __construct(
        string $nomeComercianteprivate,
        float $limitePrivateDiario = LIMITE_DIARIO
    ) {
        $this->nomeComercianteprivate = $nomeComercianteprivate;
        $this->limitePrivateDiario    = $limitePrivateDiario;
    }

    // ── Operações públicas ─────────────────────────────────────────────────

    public function validarPagamento(
        float $valor,
        string $metodoPagamento,
        ?array $dadosCartao = null,
        ?string $cpfTitular = null,
        string $descricao = ''
    ): array {
        $erros = [];

        if ($valor < VALOR_MINIMO_PAGAMENTO) {
            $erros[] = 'Valor mínimo é R$ ' . number_format(VALOR_MINIMO_PAGAMENTO, 2, ',', '.');
        }

        if ($this->_totalProcessadoHoje + $valor > $this->limitePrivateDiario) {
            $erros[] = 'Limite diário de R$ '
                . number_format($this->limitePrivateDiario, 2, ',', '.')
                . ' seria excedido';
        }

        if (!in_array($metodoPagamento, ['credito', 'debito', 'pix', 'boleto'])) {
            $erros[] = "Método de pagamento inválido: {$metodoPagamento}";
        }

        if (in_array($metodoPagamento, ['credito', 'debito']) && !$dadosCartao) {
            $erros[] = 'Dados do cartão são obrigatórios para pagamento com cartão';
        }

        return ['valido' => count($erros) === 0, 'erros' => $erros];
    }

    public function processarPagamento(
        float $valor,
        string $metodoPagamento,
        ?array $dadosCartao = null,
        ?string $cpfTitular = null,
        string $descricao = ''
    ): array {
        $validacao = $this->validarPagamento(
            $valor,
            $metodoPagamento,
            $dadosCartao,
            $cpfTitular,
            $descricao
        );

        if (!$validacao['valido']) {
            return [
                'status'  => STATUS_RECUSADO,
                'motivos' => $validacao['erros'],
                'valor'   => $valor,
            ];
        }

        $taxa        = $metodoPagamento === 'credito' ? $valor * TAXA_PROCESSAMENTO : 0.0;
        $valorLiquido = $valor - $taxa;

        $this->_totalProcessadoHoje += $valor;
        $idTransacao = 'TRX-' . (new DateTime())->format('YmdHisu');

        $registro = [
            'id'           => $idTransacao,
            'valor_bruto'  => $valor,
            'taxa'         => round($taxa, 2),
            'valor_liquido'=> round($valorLiquido, 2),
            'metodo'       => $metodoPagamento,
            'status'       => STATUS_APROVADO,
            'timestamp'    => (new DateTime())->format('c'),
            'descricao'    => $descricao,
        ];

        $this->_historico[]      = $registro;
        $this->_ultimaTransacao  = $registro;

        return [
            'status'       => STATUS_APROVADO,
            'transacao_id' => $idTransacao,
            'valor_liquido'=> round($valorLiquido, 2),
            'taxa'         => round($taxa, 2),
        ];
    }

    public function gerarComprovante(string $transacaoId): ?string
    {
        $transacao = null;
        foreach ($this->_historico as $t) {
            if ($t['id'] === $transacaoId) {
                $transacao = $t;
                break;
            }
        }

        if (!$transacao) {
            return null;
        }

        $linhas = [
            str_repeat('=', 50),
            'COMPROVANTE DE PAGAMENTO',
            "Comerciante: {$this->nomeComercianteprivate}",
            str_repeat('=', 50),
            "ID Transação : {$transacao['id']}",
            "Data/Hora    : {$transacao['timestamp']}",
            'Método       : ' . strtoupper($transacao['metodo']),
            'Valor Bruto  : R$ ' . number_format($transacao['valor_bruto'], 2, ',', '.'),
            'Taxa         : R$ ' . number_format($transacao['taxa'], 2, ',', '.'),
            'Valor Líquido: R$ ' . number_format($transacao['valor_liquido'], 2, ',', '.'),
            'Status       : ' . strtoupper($transacao['status']),
            str_repeat('=', 50),
        ];

        if ($transacao['descricao']) {
            array_splice($linhas, count($linhas) - 1, 0, ["Descrição    : {$transacao['descricao']}"]);
        }

        return implode("\n", $linhas);
    }

    public function obterResumoDoDia(): array
    {
        return [
            'total_processado'   => $this->_totalProcessadoHoje,
            'numero_transacoes'  => count($this->_historico),
            'total_taxas'        => $this->_calcularTotalTaxas(),
            'limite_disponivel'  => $this->limitePrivateDiario - $this->_totalProcessadoHoje,
        ];
    }

    // ── Operações privadas ─────────────────────────────────────────────────

    private function _calcularTotalTaxas(): float
    {
        return array_sum(array_column($this->_historico, 'taxa'));
    }
}

// ── Execução de demonstração ──────────────────────────────────────────────────

$processador = new ProcessadorDePagamentos('Restaurante do Zé', 5000.0);

$resultado1 = $processador->processarPagamento(
    150.0,
    'credito',
    ['numero' => '****1234'],
    null,
    'Almoço executivo'
);
echo 'Transação 1: ' . json_encode($resultado1, JSON_UNESCAPED_UNICODE) . "\n";

$resultado2 = $processador->processarPagamento(0.50, 'pix', null, null, 'Teste abaixo do mínimo');
echo 'Transação 2 (inválida): ' . json_encode($resultado2, JSON_UNESCAPED_UNICODE) . "\n";

$resultado3 = $processador->processarPagamento(80.0, 'pix', null, null, 'Sobremesa');
echo 'Transação 3: ' . json_encode($resultado3, JSON_UNESCAPED_UNICODE) . "\n";

if ($resultado1['status'] === STATUS_APROVADO) {
    $comprovante = $processador->gerarComprovante($resultado1['transacao_id']);
    echo "\n" . $comprovante . "\n";
}

echo "\nResumo do dia: " . json_encode($processador->obterResumoDoDia(), JSON_UNESCAPED_UNICODE) . "\n";
