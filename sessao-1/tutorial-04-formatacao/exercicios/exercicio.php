<?php
/**
 * EXERCÍCIO — Tutorial 04: Formatação
 * Referência: Clean Code, Cap. 5
 * Execute: php exercicio.php
 *
 * TAREFA: Formate o código abaixo seguindo PSR-12 e as convenções do Clean Code.
 * Não altere a lógica — apenas a formatação.
 *
 * O que corrigir:
 *   1. Imports (use) desorganizados — ordene por nome
 *   2. Constantes misturadas com a lógica — mova para o topo da classe
 *   3. Sem espaços entre operadores e após vírgulas
 *   4. Linhas muito longas (>120 chars) — quebre
 *   5. Métodos sem linha em branco de separação
 *   6. Chaves de abertura de método na linha errada (PSR-12: mesma linha)
 *   7. Métodos privados misturados com públicos sem separação clara
 */
use DateTime;
use InvalidArgumentException;
use stdClass;

const STATUS_APROVADO="aprovado";
const STATUS_RECUSADO="recusado";
const STATUS_PENDENTE="pendente";
const TAXA_PROCESSAMENTO=0.025;
const LIMITE_DIARIO=10000.0;
const VALOR_MINIMO_PAGAMENTO=1.0;

class ProcessadorDePagamentos
{
    private string $nomeComercianteprivate;
    private float $limitePrivateDiario;
    private float $_totalProcessadoHoje=0.0;
    private array $_historico=[];
    private ?array $_ultimaTransacao=null;
    function __construct(string $nomeComercianteprivate,float $limitePrivateDiario=LIMITE_DIARIO)
    {$this->nomeComercianteprivate=$nomeComercianteprivate;$this->limitePrivateDiario=$limitePrivateDiario;}
    public function validarPagamento(float $valor,string $metodoPagamento,?array $dadosCartao=null,?string $cpfTitular=null,string $descricao=""): array
    {$erros=[];if($valor<VALOR_MINIMO_PAGAMENTO){$erros[]="Valor mínimo é R$ ".number_format(VALOR_MINIMO_PAGAMENTO,2,',','.');}if($this->_totalProcessadoHoje+$valor>$this->limitePrivateDiario){$erros[]="Limite diário de R$ ".number_format($this->limitePrivateDiario,2,',','.')." seria excedido";}if(!in_array($metodoPagamento,["credito","debito","pix","boleto"])){$erros[]="Método de pagamento inválido: {$metodoPagamento}";}if(in_array($metodoPagamento,["credito","debito"])&&!$dadosCartao){$erros[]="Dados do cartão são obrigatórios para pagamento com cartão";}return ["valido"=>count($erros)===0,"erros"=>$erros];}
    public function processarPagamento(float $valor,string $metodoPagamento,?array $dadosCartao=null,?string $cpfTitular=null,string $descricao=""): array
    {$validacao=$this->validarPagamento($valor,$metodoPagamento,$dadosCartao,$cpfTitular,$descricao);if(!$validacao["valido"]){return ["status"=>STATUS_RECUSADO,"motivos"=>$validacao["erros"],"valor"=>$valor];}$taxa=$metodoPagamento==="credito"?$valor*TAXA_PROCESSAMENTO:0.0;$valorLiquido=$valor-$taxa;$this->_totalProcessadoHoje+=$valor;$idTransacao="TRX-".(new DateTime())->format("YmdHisu");$registro=["id"=>$idTransacao,"valor_bruto"=>$valor,"taxa"=>round($taxa,2),"valor_liquido"=>round($valorLiquido,2),"metodo"=>$metodoPagamento,"status"=>STATUS_APROVADO,"timestamp"=>(new DateTime())->format("c"),"descricao"=>$descricao];$this->_historico[]=$registro;$this->_ultimaTransacao=$registro;return ["status"=>STATUS_APROVADO,"transacao_id"=>$idTransacao,"valor_liquido"=>round($valorLiquido,2),"taxa"=>round($taxa,2)];}
    public function gerarComprovante(string $transacaoId): ?string
    {$transacao=null;foreach($this->_historico as $t){if($t["id"]===$transacaoId){$transacao=$t;break;}}if(!$transacao){return null;}$linhas=["==================================================","COMPROVANTE DE PAGAMENTO","Comerciante: {$this->nomeComercianteprivate}","==================================================","ID Transação : {$transacao['id']}","Data/Hora    : {$transacao['timestamp']}","Método       : ".strtoupper($transacao['metodo']),"Valor Bruto  : R$ ".number_format($transacao['valor_bruto'],2,',','.'),"Taxa         : R$ ".number_format($transacao['taxa'],2,',','.'),"Valor Líquido: R$ ".number_format($transacao['valor_liquido'],2,',','.'),"Status       : ".strtoupper($transacao['status']),"=================================================="];if($transacao["descricao"]){array_splice($linhas,count($linhas)-1,0,["Descrição    : {$transacao['descricao']}"]);}return implode("\n",$linhas);}
    private function _calcularTotalTaxas(): float
    {return array_sum(array_column($this->_historico,"taxa"));}
    public function obterResumoDoDia(): array
    {return ["total_processado"=>$this->_totalProcessadoHoje,"numero_transacoes"=>count($this->_historico),"total_taxas"=>$this->_calcularTotalTaxas(),"limite_disponivel"=>$this->limitePrivateDiario-$this->_totalProcessadoHoje];}
}

$proc=new ProcessadorDePagamentos("Restaurante do Zé",5000.0);
$v1=$proc->processarPagamento(150.0,"credito",["numero"=>"****1234"],null,"Almoço executivo");
echo "Transação 1: ".json_encode($v1,JSON_UNESCAPED_UNICODE)."\n";
$v2=$proc->processarPagamento(0.50,"pix",null,null,"Teste abaixo do mínimo");
echo "Transação 2 (inválida): ".json_encode($v2,JSON_UNESCAPED_UNICODE)."\n";
$v3=$proc->processarPagamento(80.0,"pix",null,null,"Sobremesa");
echo "Transação 3: ".json_encode($v3,JSON_UNESCAPED_UNICODE)."\n";
if($v1["status"]===STATUS_APROVADO){$comprovante=$proc->gerarComprovante($v1["transacao_id"]);echo "\n".$comprovante."\n";}
echo "\nResumo do dia: ".json_encode($proc->obterResumoDoDia(),JSON_UNESCAPED_UNICODE)."\n";
