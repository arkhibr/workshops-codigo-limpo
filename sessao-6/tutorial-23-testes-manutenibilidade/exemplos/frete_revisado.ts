/**
 * frete_revisado.ts — Cálculo de frete com faixas de peso (corrigido).
 *
 * Suite completa de caracterização com valores de borda exatos.
 * A fronteira de 10 kg é testada explicitamente — o que revelaria a regressão
 * introduzida em frete_gerado.ts (< 10 em vez de <= 10).
 *
 * Execute: npx ts-node frete_revisado.ts
 */

// ---------------------------------------------------------------------------
// Constantes de domínio
// ---------------------------------------------------------------------------

const TARIFA_DISTANCIA_POR_KM = 0.08;   // R$/km adicional
const FATOR_REGIONAL = 1.15;            // multiplicador para destinos regionais

const TARIFA_LEVE   = 8.00;    // envios até 2 kg — taxa mínima fixa
const TARIFA_PADRAO = 25.00;   // envios de 2 kg até 10 kg — faixa padrão (inclui 10 kg)
const TARIFA_MEDIA  = 45.00;   // envios acima de 10 kg até 20 kg — faixa intermediária
const TARIFA_PESADA = 80.00;   // envios acima de 20 kg — carga pesada

// ---------------------------------------------------------------------------
// Lógica de cálculo (fronteira correta: <= 10)
// ---------------------------------------------------------------------------

/**
 * Calcula o frete com base no peso e na distância.
 *
 * Faixas de peso:
 *   - até 2 kg: tarifa leve (R$ 8,00 base)
 *   - 2 kg < peso <= 10 kg: tarifa padrão (R$ 25,00 base)
 *   - 10 kg < peso <= 20 kg: tarifa intermediária (R$ 45,00 base)
 *   - acima de 20 kg: tarifa de carga pesada (R$ 80,00 base)
 *
 * A componente de distância é somada à tarifa base.
 * Destinos regionais recebem multiplicador adicional.
 */
function calcularFrete(pesoKg: number, distanciaKm: number,
                       regional: boolean = false): number {
  if (pesoKg <= 0) {
    throw new Error(`Peso inválido: ${pesoKg} kg. Deve ser maior que zero.`);
  }
  if (distanciaKm <= 0) {
    throw new Error(`Distância inválida: ${distanciaKm} km. Deve ser maior que zero.`);
  }

  let tarifaBase: number;
  if (pesoKg <= 2.0) {
    tarifaBase = TARIFA_LEVE;
  } else if (pesoKg <= 10.0) {    // ← fronteira correta: inclui exatamente 10 kg na faixa padrão
    tarifaBase = TARIFA_PADRAO;
  } else if (pesoKg <= 20.0) {
    tarifaBase = TARIFA_MEDIA;
  } else {
    tarifaBase = TARIFA_PESADA;
  }

  const componenteDistancia = distanciaKm * TARIFA_DISTANCIA_POR_KM;
  let freteCalculado = tarifaBase + componenteDistancia;

  if (regional) {
    freteCalculado *= FATOR_REGIONAL;
  }

  return Math.round(freteCalculado * 100) / 100;
}

function descricaoFaixa(pesoKg: number): string {
  if (pesoKg <= 0)     return "peso inválido";
  if (pesoKg <= 2.0)   return "leve (até 2 kg)";
  if (pesoKg <= 10.0)  return "padrão (2 kg a 10 kg)";
  if (pesoKg <= 20.0)  return "intermediária (10 kg a 20 kg)";
  return "carga pesada (acima de 20 kg)";
}

// ---------------------------------------------------------------------------
// Suite COMPLETA de caracterização (inclui bordas exatas)
// ---------------------------------------------------------------------------

function verificarFaixaLeve(): void {
  const casos: Array<[number, number, boolean, number, string]> = [
    [0.5,  50, false, 12.00, "0.5 kg, 50 km — faixa leve"],
    [1.0,  50, false, 12.00, "1 kg, 50 km — faixa leve mid-band"],
    [2.0,  50, false, 12.00, "2 kg, 50 km — borda superior faixa leve"],
  ];
  for (const [peso, distancia, regional, esperado, descricao] of casos) {
    const obtido = calcularFrete(peso, distancia, regional);
    if (Math.abs(obtido - esperado) < 0.001) {
      console.log(`OK: ${descricao}`);
    } else {
      console.log(`FALHOU: ${descricao} (esperado ${esperado.toFixed(2)}, obtido ${obtido.toFixed(2)})`);
    }
  }
}

function verificarFaixaPadrao(): void {
  /**
   * Faixa padrão: acima de 2 kg até 10 kg inclusive.
   *
   * O caso de 10 kg é a fronteira crítica — frete_gerado.ts a classifica
   * erroneamente como intermediária (usa < 10 em vez de <= 10).
   */
  const casos: Array<[number, number, boolean, number, string]> = [
    [2.1,  100, false, 33.00, "2.1 kg, 100 km — borda inferior faixa padrão"],
    [5.0,  100, false, 33.00, "5 kg, 100 km — faixa padrão mid-band"],
    [8.0,  100, false, 33.00, "8 kg, 100 km — faixa padrão mid-band"],
    [10.0, 100, false, 33.00, "10 kg, 100 km — borda SUPERIOR faixa padrão (fronteira crítica)"],
  ];
  for (const [peso, distancia, regional, esperado, descricao] of casos) {
    const obtido = calcularFrete(peso, distancia, regional);
    if (Math.abs(obtido - esperado) < 0.001) {
      console.log(`OK: ${descricao}`);
    } else {
      console.log(`FALHOU: ${descricao} (esperado ${esperado.toFixed(2)}, obtido ${obtido.toFixed(2)})`);
    }
  }
}

function verificarFaixaIntermediaria(): void {
  const casos: Array<[number, number, boolean, number, string]> = [
    [10.1, 100, false, 53.00, "10.1 kg, 100 km — borda inferior faixa intermediária"],
    [15.0, 100, false, 53.00, "15 kg, 100 km — faixa intermediária mid-band"],
    [20.0, 100, false, 53.00, "20 kg, 100 km — borda superior faixa intermediária"],
  ];
  for (const [peso, distancia, regional, esperado, descricao] of casos) {
    const obtido = calcularFrete(peso, distancia, regional);
    if (Math.abs(obtido - esperado) < 0.001) {
      console.log(`OK: ${descricao}`);
    } else {
      console.log(`FALHOU: ${descricao} (esperado ${esperado.toFixed(2)}, obtido ${obtido.toFixed(2)})`);
    }
  }
}

function verificarFaixaPesada(): void {
  const casos: Array<[number, number, boolean, number, string]> = [
    [20.1, 100, false, 88.00, "20.1 kg, 100 km — borda inferior carga pesada"],
    [25.0, 100, false, 88.00, "25 kg, 100 km — carga pesada mid-band"],
    [50.0, 100, false, 88.00, "50 kg, 100 km — carga pesada extremo"],
  ];
  for (const [peso, distancia, regional, esperado, descricao] of casos) {
    const obtido = calcularFrete(peso, distancia, regional);
    if (Math.abs(obtido - esperado) < 0.001) {
      console.log(`OK: ${descricao}`);
    } else {
      console.log(`FALHOU: ${descricao} (esperado ${esperado.toFixed(2)}, obtido ${obtido.toFixed(2)})`);
    }
  }
}

function verificarComponenteRegional(): void {
  const casos: Array<[number, number, boolean, number, string]> = [
    [5.0,  100, true, 37.95, "5 kg, 100 km — regional (padrão × 1.15)"],
    [15.0, 100, true, 60.95, "15 kg, 100 km — regional (intermediária × 1.15)"],
  ];
  for (const [peso, distancia, regional, esperado, descricao] of casos) {
    const obtido = calcularFrete(peso, distancia, regional);
    if (Math.abs(obtido - esperado) < 0.001) {
      console.log(`OK: ${descricao}`);
    } else {
      console.log(`FALHOU: ${descricao} (esperado ${esperado.toFixed(2)}, obtido ${obtido.toFixed(2)})`);
    }
  }
}

function verificarEntradasInvalidas(): void {
  const casosInvalidos: Array<[number, number, string]> = [
    [0.0,   100, "peso zero"],
    [-1.0,  100, "peso negativo"],
    [5.0,   0.0, "distância zero"],
    [5.0,  -50,  "distância negativa"],
  ];
  for (const [peso, distancia, descricao] of casosInvalidos) {
    try {
      calcularFrete(peso, distancia);
      console.log(`FALHOU: ${descricao} — deveria lançar Error, mas não lançou`);
    } catch (_e) {
      console.log(`OK: ${descricao} — Error lançado corretamente`);
    }
  }
}

// ---------------------------------------------------------------------------
// Demo comparativo
// ---------------------------------------------------------------------------

function demonstrarDiferencaFronteira(): void {
  const frete10kg = calcularFrete(10.0, 100);
  console.log(`Frete para 10 kg, 100 km (nesta versão): R$ ${frete10kg.toFixed(2)}`);
  console.log(`  Faixa: ${descricaoFaixa(10.0)}`);
  console.log(`  Esperado (faixa padrão): R$ 33,00`);
  if (Math.abs(frete10kg - 33.00) < 0.001) {
    console.log("  Fronteira correta: 10 kg está na faixa padrão.");
  } else {
    console.log("  REGRESSÃO: 10 kg caiu na faixa errada.");
  }
  console.log();
}

// ─── Execução ────────────────────────────────────────────────────────────────

console.log("=== Cálculo de Frete — versão revisada com suite completa ===\n");

demonstrarDiferencaFronteira();

console.log("--- Verificações completas (incluindo bordas) ---");
verificarFaixaLeve();
verificarFaixaPadrao();
verificarFaixaIntermediaria();
verificarFaixaPesada();
verificarComponenteRegional();
verificarEntradasInvalidas();
