// EXERCÍCIO 18 TypeScript — Padrões Estruturais: Adapter + Facade
// Execute: npx ts-node exercicio.ts
//
// INSTRUÇÕES:
//   O sistema de boletos bancários abaixo tem uma API legada com nomes e
//   estruturas de dados inconsistentes. O código de negócio chama essas
//   funções diretamente em 3 lugares diferentes.
//
//   1. Crie um Adapter que isole o sistema legado do código de negócio.
//   2. Crie uma Facade que simplifique o fluxo completo (emitir + consultar + cancelar).

// ─── API legada (não pode ser alterada) ───────────────────────────────────────

function gerar_boleto_legado(nValor: number, cVencimento: string, cPagador: string): Record<string, unknown> {
    console.log(`  [Legado] gerarBoleto(${cPagador}, R$${nValor.toFixed(2)})`);
    return {
        nIdBoleto:     12345,
        cCodigoBarras: '9999.99999 99999.999999',
        cStatusBoleto: 'ATIVO',
        nValorBoleto:  nValor,
    };
}

function consultar_status_legado(nIdBoleto: number): string {
    console.log(`  [Legado] consultarStatus(${nIdBoleto})`);
    return 'ATIVO';
}

function cancelar_boleto_legado(nIdBoleto: number, cMotivo: string): boolean {
    console.log(`  [Legado] cancelarBoleto(${nIdBoleto}, ${cMotivo})`);
    return true;
}


// ─── Código de negócio — chama legado diretamente ────────────────────────────

function emitirCobranca(valor: number, vencimento: string, clienteId: string): Record<string, unknown> {
    const raw = gerar_boleto_legado(valor, vencimento, clienteId);   // acoplamento direto
    return {
        id:     raw['nIdBoleto'],
        codigo: raw['cCodigoBarras'],
        status: (raw['cStatusBoleto'] as string).toLowerCase(),
        valor:  raw['nValorBoleto'],
    };
}

function verificarCobranca(boletoId: number): string {
    const statusRaw = consultar_status_legado(boletoId);             // acoplamento direto
    return statusRaw.toLowerCase();
}

function estornarCobranca(boletoId: number): boolean {
    return cancelar_boleto_legado(boletoId, 'SOLICITACAO_CLIENTE');  // acoplamento direto
}


// ─── TODO: Implemente aqui ────────────────────────────────────────────────────
//
// 1. Crie uma interface Boleto com propriedades:
//    id, codigoBarras, status, valor
//
// 2. Crie uma interface IServicoCobranca com os métodos:
//    - emitir(valor: number, vencimento: string, clienteId: string): Boleto
//    - consultar(boletoId: number): string
//    - cancelar(boletoId: number): boolean
//
// 3. Crie a classe LegadoCobrancaAdapter implements IServicoCobranca
//    que chama as funções *_legado e normaliza os resultados
//
// 4. Crie a classe FachadaCobranca com o método:
//    - processarCobrancaCompleta(valor, vencimento, clienteId): Record<string, unknown>
//      (emite + consulta + cancela e retorna um resumo)
//
// ─────────────────────────────────────────────────────────────────────────────


// Demo
const boleto = emitirCobranca(500.0, '2026-08-15', 'CLI-200');
console.log(`Boleto: id=${boleto['id']}, status=${boleto['status']}`);
const status = verificarCobranca(boleto['id'] as number);
console.log(`Status: ${status}`);
const cancelado = estornarCobranca(boleto['id'] as number);
console.log(`Cancelado: ${cancelado}`);
