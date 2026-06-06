/**
 * frete_gerado.ts — Cálculo de frete com faixas de peso.
 *
 * Saída de IA após mudança assistida — a suite fraca mascara uma regressão.
 * Um agente adicionou a faixa "carga pesada" (> 20 kg) a pedido do negócio,
 * mas deslocou silenciosamente a fronteira entre duas faixas existentes.
 *
 * Execute: npx ts-node frete_gerado.ts
 */

// ---------------------------------------------------------------------------
// Constantes de domínio
// ---------------------------------------------------------------------------

const TARIFA_DISTANCIA_POR_KM = 0.08;   // R$/km adicional
const FATOR_REGIONAL = 1.15;            // multiplicador para destinos regionais

const TARIFA_LEVE   = 8.00;    // envios até 2 kg — taxa mínima fixa
const TARIFA_PADRAO = 25.00;   // envios de 2 kg até 10 kg — faixa padrão (base)
const TARIFA_MEDIA  = 45.00;   // envios de 10 kg até 20 kg — faixa intermediária
const TARIFA_PESADA = 80.00;   // envios acima de 20 kg — carga pesada (adicionado pelo agente)

// ---------------------------------------------------------------------------
// Lógica de cálculo
// ---------------------------------------------------------------------------

/**
 * Calcula o frete com base no peso e na distância.
 *
 * Faixas de peso:
 *   - até 2 kg: tarifa leve (R$ 8,00 base)
 *   - 2 kg < peso < 10 kg: tarifa padrão (R$ 25,00 base)
 *   - 10 kg a 20 kg: tarifa intermediária (R$ 45,00 base)
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
  } else if (pesoKg < 10.0) {      // ← fronteira deslocada: era <= 10, passou a < 10
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
  if (pesoKg <= 0)    return "peso inválido";
  if (pesoKg <= 2.0)  return "leve (até 2 kg)";
  if (pesoKg < 10.0)  return "padrão (2 kg a 10 kg)";
  if (pesoKg <= 20.0) return "intermediária (10 kg a 20 kg)";
  return "carga pesada (acima de 20 kg)";
}

// ---------------------------------------------------------------------------
// Suite fraca de verificação (mid-band apenas — mascara a regressão)
// ---------------------------------------------------------------------------

function verificarFaixaLeve(): void {
  const casos: Array<[number, number, boolean, number, string]> = [
    [1.0,  50, false, 12.00, "1 kg, 50 km — faixa leve"],
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

function verificarFaixasMidBand(): void {
  /**
   * Verifica valores no meio de cada faixa de peso.
   *
   * Cobre 5 kg, 8 kg, 15 kg e 25 kg — todos no interior das faixas.
   * Não testa valores de borda, então o deslocamento de <= 10 para < 10
   * não é detectado aqui. Todos os casos imprimem OK.
   */
  const casos: Array<[number, number, boolean, number, string]> = [
    [5.0,  100, false, 33.00, "5 kg, 100 km — faixa padrão mid-band"],
    [8.0,  100, false, 33.00, "8 kg, 100 km — faixa padrão mid-band"],
    [15.0, 100, false, 53.00, "15 kg, 100 km — faixa intermediária mid-band"],
    [25.0, 100, false, 88.00, "25 kg, 100 km — carga pesada mid-band"],
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

// ---------------------------------------------------------------------------
// Demo
// ---------------------------------------------------------------------------

function demonstrarCotacoes(): void {
  const envios: Array<[number, number, boolean, string]> = [
    [1.5,   80, false, "pacote leve"],
    [5.0,  150, false, "pacote padrão"],
    [8.0,  200, false, "pacote padrão maior"],
    [15.0, 300, false, "carga intermediária"],
    [25.0, 400, false, "carga pesada"],
    [5.0,  150, true,  "pacote padrão — regional"],
  ];

  console.log("Cotações de frete:");
  console.log("  " + "Peso".padStart(8) + "  " + "Distância".padStart(10) + "  " +
              "Regional".padStart(8) + "  " + "Faixa".padEnd(28) + "  " + "Frete".padStart(10));
  console.log("  " + "-".repeat(76));
  for (const [peso, distancia, regional, _rotulo] of envios) {
    const frete = calcularFrete(peso, distancia, regional);
    const faixa = descricaoFaixa(peso);
    const regStr = regional ? "sim" : "não";
    console.log("  " + `${peso.toFixed(1)}kg`.padStart(8) + "  " +
                `${distancia}km`.padStart(10) + "  " + regStr.padStart(8) + "  " +
                faixa.padEnd(28) + "  " + `R$${frete.toFixed(2)}`.padStart(10));
  }
  console.log();
}

// ─── Execução ────────────────────────────────────────────────────────────────

console.log("=== Cálculo de Frete — código gerado por IA (mudança assistida) ===\n");

demonstrarCotacoes();

console.log("--- Verificações (suite fraca) ---");
verificarFaixaLeve();
verificarFaixasMidBand();
console.log();
console.log("Todas as verificações passaram — mas a suite não testa 10 kg exato.");
console.log("O deslocamento de <= 10 para < 10 é invisível com estes casos.");
