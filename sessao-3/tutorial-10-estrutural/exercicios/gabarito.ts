// GABARITO 18 TypeScript — Padrões Estruturais: Adapter + Facade
// Execute: npx ts-node gabarito.ts

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


// ─── Modelo de domínio moderno ────────────────────────────────────────────────

interface Boleto {
    id:           number;
    codigoBarras: string;
    status:       string;
    valor:        number;
}


// ─── Contrato (interface) ────────────────────────────────────────────────────

interface IServicoCobranca {
    emitir(valor: number, vencimento: string, clienteId: string): Boleto;
    consultar(boletoId: number): string;
    cancelar(boletoId: number): boolean;
}


// ─── Adapter: isola a API legada do código de negócio ────────────────────────

class LegadoCobrancaAdapter implements IServicoCobranca {
    /** Traduz a API legada (nId*, cCodigo*, cStatus*) para o contrato IServicoCobranca. */

    emitir(valor: number, vencimento: string, clienteId: string): Boleto {
        const raw = gerar_boleto_legado(valor, vencimento, clienteId);
        return {
            id:           raw['nIdBoleto'] as number,
            codigoBarras: raw['cCodigoBarras'] as string,
            status:       (raw['cStatusBoleto'] as string).toLowerCase(),
            valor:        raw['nValorBoleto'] as number,
        };
    }

    consultar(boletoId: number): string {
        const statusRaw = consultar_status_legado(boletoId);
        return statusRaw.toLowerCase();
    }

    cancelar(boletoId: number): boolean {
        return cancelar_boleto_legado(boletoId, 'SOLICITACAO_CLIENTE');
    }
}


// ─── Facade: orquestra o fluxo completo de cobrança ──────────────────────────

class FachadaCobranca {
    /** Quem chama executa o fluxo completo passando apenas os dados essenciais. */
    constructor(private readonly servico: IServicoCobranca) {}

    processarCobrancaCompleta(valor: number, vencimento: string, clienteId: string): Record<string, unknown> {
        const boleto    = this.servico.emitir(valor, vencimento, clienteId);
        const status    = this.servico.consultar(boleto.id);
        const cancelado = this.servico.cancelar(boleto.id);
        return {
            boletoId:    boleto.id,
            codigo:      boleto.codigoBarras,
            statusFinal: status,
            cancelado,
        };
    }
}


// ─── Verificação ──────────────────────────────────────────────────────────────

function verificarAdapter(): void {
    const adapter = new LegadoCobrancaAdapter();

    const boleto = adapter.emitir(500.0, '2026-08-15', 'CLI-200');
    console.assert(boleto.id === 12345, `esperado 12345, obtido ${boleto.id}`);
    console.assert(boleto.status === 'ativo', `esperado 'ativo', obtido '${boleto.status}'`);
    console.assert(!('nIdBoleto' in boleto), 'campo legado nIdBoleto não deve ser exposto');
    console.log('OK: Adapter — emitir() retorna Boleto sem campos legados');

    const status = adapter.consultar(12345);
    console.assert(status === 'ativo', `esperado 'ativo', obtido '${status}'`);
    console.log('OK: Adapter — consultar() normaliza status para minúsculas');

    const cancelado = adapter.cancelar(12345);
    console.assert(cancelado === true, `esperado true, obtido ${cancelado}`);
    console.log('OK: Adapter — cancelar() passa motivo fixo ao sistema legado');
}

function verificarFacade(): void {
    const fachada   = new FachadaCobranca(new LegadoCobrancaAdapter());
    const resultado = fachada.processarCobrancaCompleta(300.0, '2026-09-01', 'CLI-300');

    console.assert(resultado['boletoId'] === 12345, `esperado 12345, obtido ${resultado['boletoId']}`);
    console.assert(resultado['statusFinal'] === 'ativo', `esperado 'ativo', obtido '${resultado['statusFinal']}'`);
    console.assert(resultado['cancelado'] === true, `esperado true, obtido ${resultado['cancelado']}`);
    console.log('OK: Facade — processarCobrancaCompleta() executa emitir + consultar + cancelar');
    console.log('OK: Facade — chamador não conhece API legada nem sequência de passos');
}

console.log('=== Gabarito 18 TypeScript — Adapter + Facade (boletos) ===\n');
verificarAdapter();
console.log('');
verificarFacade();
