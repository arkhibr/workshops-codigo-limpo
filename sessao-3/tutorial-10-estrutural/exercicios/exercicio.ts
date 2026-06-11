// EXERCÍCIO 18 TypeScript — Padrões Estruturais: Adapter + Facade
// Execute: npx ts-node exercicio.ts
//
// PASSOS:
//
//   PASSO 1 — IDENTIFICAR (5 min)
//     Nas 3 funções de negócio (emitirCobranca, verificarCobranca, estornarCobranca),
//     adicione um comentário // ACOPLAMENTO: antes de cada chamada à API legada.
//     Meta: marcar os 3 acoplamentos antes de alterar código.
//
//   PASSO 2 — MODELO DE DOMÍNIO (5 min)
//     Crie a interface Boleto com propriedades:
//       id: number, codigoBarras: string, status: string, valor: number
//     (sem alterar mais nada ainda)
//
//   PASSO 3 — ADAPTER (10 min)
//     Crie a classe LegadoCobrancaAdapter com 3 métodos:
//       emitir(valor: number, vencimento: string, clienteId: string): Boleto
//       consultar(boletoId: number): string
//       cancelar(boletoId: number): boolean
//     Cada método chama uma função *_legado e normaliza os campos.
//     Verifique: adapter.emitir(500.0, '2026-08-15', 'CLI-200') retorna um Boleto.
//
//   PASSO 4 — FACADE (8 min)
//     Crie FachadaCobranca recebendo um adapter no construtor, com:
//       processarCobrancaCompleta(valor, vencimento, clienteId): Record<string, unknown>
//     Que chama emitir + consultar + cancelar e devolve resumo.
//     Verifique que o caller não precisa mais conhecer a API legada.

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


// ─── Passo 2: implemente a interface Boleto aqui ─────────────────────────────
// interface Boleto {
//     id:           number;
//     codigoBarras: string;
//     status:       string;
//     valor:        number;
// }


// ─── Passo 3: implemente LegadoCobrancaAdapter aqui ──────────────────────────
// class LegadoCobrancaAdapter {
//     emitir(valor: number, vencimento: string, clienteId: string): Boleto { ... }
//     consultar(boletoId: number): string { ... }
//     cancelar(boletoId: number): boolean { ... }
// }


// ─── Passo 4: implemente FachadaCobranca aqui ────────────────────────────────
// class FachadaCobranca {
//     constructor(private readonly adapter: LegadoCobrancaAdapter) {}
//     processarCobrancaCompleta(valor: number, vencimento: string, clienteId: string): Record<string, unknown> { ... }
// }


// Demo (código original)
// Passo 1: adicione // ACOPLAMENTO: nas linhas de chamada legada dentro das funções acima
const boleto = emitirCobranca(500.0, '2026-08-15', 'CLI-200');
console.log(`Boleto: id=${boleto['id']}, status=${boleto['status']}`);
const status = verificarCobranca(boleto['id'] as number);
console.log(`Status: ${status}`);
const cancelado = estornarCobranca(boleto['id'] as number);
console.log(`Cancelado: ${cancelado}`);

// Passo 3 — descomente para verificar o Adapter:
// const adapter = new LegadoCobrancaAdapter();
// const b = adapter.emitir(500.0, '2026-08-15', 'CLI-200');
// console.log(`[Adapter] Boleto: id=${b.id}, status=${b.status}`);

// Passo 4 — descomente para verificar a Facade:
// const fachada = new FachadaCobranca(new LegadoCobrancaAdapter());
// const resultado = fachada.processarCobrancaCompleta(500.0, '2026-08-15', 'CLI-200');
// console.log('[Facade] resultado:', resultado);
