/**
 * EXERCÍCIO — Tutorial 04: Formatação
 * Referência: Clean Code, Cap. 5
 * Execute: npx ts-node exercicio.ts
 *
 * TAREFA: Formate o código abaixo seguindo as convenções do Clean Code e ESLint/Prettier.
 * Não altere a lógica — apenas a formatação.
 *
 * O que corrigir:
 *   1. Tipos "any" onde deveriam ser interfaces tipadas
 *   2. Sem espaços entre operadores e após vírgulas
 *   3. Métodos sem linha em branco de separação
 *   4. Linhas muito longas (>100 chars) — quebre
 *   5. Constantes misturadas com a lógica — mova para o topo do arquivo
 *   6. Métodos privados sem separação clara dos públicos
 */

const STATUS_APROVADO="aprovado";const STATUS_RECUSADO="recusado";const STATUS_PENDENTE="pendente";const TAXA_PROCESSAMENTO=0.025;const LIMITE_DIARIO=10000;const VALOR_MINIMO_PAGAMENTO=1;

class ProcessadorDePagamentos {
    private nomeComercianteprivate:string;private limitePrivateDiario:number;private _totalProcessadoHoje:number=0;private _historico:any[]=[];private _ultimaTransacao:any=null;
    constructor(nomeComercianteprivate:string,limitePrivateDiario:number=LIMITE_DIARIO){this.nomeComercianteprivate=nomeComercianteprivate;this.limitePrivateDiario=limitePrivateDiario;}
    validarPagamento(valor:number,metodoPagamento:string,dadosCartao:any=null,cpfTitular:any=null,descricao:string=""):any{const erros:string[]=[];if(valor<VALOR_MINIMO_PAGAMENTO){erros.push(`Valor mínimo é R$ ${VALOR_MINIMO_PAGAMENTO.toFixed(2)}`);}if(this._totalProcessadoHoje+valor>this.limitePrivateDiario){erros.push(`Limite diário de R$ ${this.limitePrivateDiario.toFixed(2)} seria excedido`);}if(!["credito","debito","pix","boleto"].includes(metodoPagamento)){erros.push(`Método de pagamento inválido: ${metodoPagamento}`);}if(["credito","debito"].includes(metodoPagamento)&&!dadosCartao){erros.push("Dados do cartão são obrigatórios para pagamento com cartão");}return {valido:erros.length===0,erros};}
    processarPagamento(valor:number,metodoPagamento:string,dadosCartao:any=null,cpfTitular:any=null,descricao:string=""):any{const validacao=this.validarPagamento(valor,metodoPagamento,dadosCartao,cpfTitular,descricao);if(!validacao.valido){return {status:STATUS_RECUSADO,motivos:validacao.erros,valor};}const taxa=metodoPagamento==="credito"?valor*TAXA_PROCESSAMENTO:0;const valorLiquido=valor-taxa;this._totalProcessadoHoje+=valor;const idTransacao=`TRX-${new Date().toISOString().replace(/[-:.TZ]/g,"")}`;const registro={id:idTransacao,valor_bruto:valor,taxa:Math.round(taxa*100)/100,valor_liquido:Math.round(valorLiquido*100)/100,metodo:metodoPagamento,status:STATUS_APROVADO,timestamp:new Date().toISOString(),descricao};this._historico.push(registro);this._ultimaTransacao=registro;return {status:STATUS_APROVADO,transacao_id:idTransacao,valor_liquido:Math.round(valorLiquido*100)/100,taxa:Math.round(taxa*100)/100};}
    gerarComprovante(transacaoId:string):string|null{const transacao=this._historico.find((t:any)=>t.id===transacaoId)??null;if(!transacao){return null;}const linhas=["=".repeat(50),"COMPROVANTE DE PAGAMENTO",`Comerciante: ${this.nomeComercianteprivate}`,"=".repeat(50),`ID Transação : ${transacao.id}`,`Data/Hora    : ${transacao.timestamp}`,`Método       : ${transacao.metodo.toUpperCase()}`,`Valor Bruto  : R$ ${transacao.valor_bruto.toFixed(2)}`,`Taxa         : R$ ${transacao.taxa.toFixed(2)}`,`Valor Líquido: R$ ${transacao.valor_liquido.toFixed(2)}`,`Status       : ${transacao.status.toUpperCase()}`,"=".repeat(50)];if(transacao.descricao){linhas.splice(linhas.length-1,0,`Descrição    : ${transacao.descricao}`);}return linhas.join("\n");}
    private _calcularTotalTaxas():number{return this._historico.reduce((acc:number,t:any)=>acc+t.taxa,0);}
    obterResumoDoDia():any{return {total_processado:this._totalProcessadoHoje,numero_transacoes:this._historico.length,total_taxas:this._calcularTotalTaxas(),limite_disponivel:this.limitePrivateDiario-this._totalProcessadoHoje};}
}

const proc=new ProcessadorDePagamentos("Restaurante do Zé",5000);
const v1=proc.processarPagamento(150,"credito",{numero:"****1234"},null,"Almoço executivo");
console.log("Transação 1:",v1);
const v2=proc.processarPagamento(0.50,"pix",null,null,"Teste abaixo do mínimo");
console.log("Transação 2 (inválida):",v2);
const v3=proc.processarPagamento(80,"pix",null,null,"Sobremesa");
console.log("Transação 3:",v3);
if(v1.status===STATUS_APROVADO){const comprovante=proc.gerarComprovante(v1.transacao_id);console.log("\n"+comprovante);}
console.log("\nResumo do dia:",proc.obterResumoDoDia());
