# ============================================================================
# GABARITO — Tutorial 07: Gestão de Código Legado
# ============================================================================

# ============================================================================
# ETAPA 1: Testes de Caracterização
#
# Executados ANTES de qualquer refatoração para documentar o comportamento
# existente. São a "rede de segurança" — se falharem após a refatoração,
# o comportamento foi alterado acidentalmente.
# ============================================================================

# Tabela de vendedores (igual ao exercício — necessária para ambas as versões)
_vendedores_raw = {
    "V001": {"nome": "Ana Paula",   "tipo": "SR", "regiao": "SP"},
    "V002": {"nome": "Carlos Lima", "tipo": "JR", "regiao": "RJ"},
    "V003": {"nome": "Maria Costa", "tipo": "SR", "regiao": "MG"},
}


class CommissionCalcOriginal:
    """Versão original preservada apenas para referência dos testes."""

    def __init__(self):
        self._cache = {}

    def calc_comm(self, s, r, t, m):
        if s in self._cache:
            return self._cache[s]

        v = _vendedores_raw.get(s)
        if not v:
            return 0

        if v["tipo"] == "SR":
            if r >= m:
                c = r * 0.08
                if r > m * 1.2:
                    c = c + (r - m * 1.2) * 0.03
            else:
                if r >= m * 0.8:
                    c = r * 0.05
                else:
                    c = r * 0.03
            if t == "AGR":
                c = c * 1.1
            if r < 5000:
                c = 0
        else:
            if r >= m:
                c = r * 0.05
                if r > m * 1.2:
                    c = c + (r - m * 1.2) * 0.02
            else:
                if r >= m * 0.8:
                    c = r * 0.03
                else:
                    c = r * 0.03
            if t == "AGR":
                c = c * 1.1
            if r < 5000:
                c = 0

        self._cache[s] = round(c, 2)
        return self._cache[s]


def executar_testes_de_caracterizacao():
    """
    Testes de caracterização: documentam o comportamento atual.
    NÃO testam se o comportamento é correto — testam que não mudou.
    """
    original = CommissionCalcOriginal()

    # SR, receita acima da meta E acima de 120% (10000 > 8000*1.2=9600) — bônus de excedente
    # 10000 * 0.08 = 800 + (10000 - 9600) * 0.03 = 800 + 12 = 812
    assert original.calc_comm("V001", 10000, "STD", 8000) == 812.0, \
        "SR, receita=10000, meta=8000, tipo=STD"

    # SR, mesmo cenário com outro vendedor
    assert original.calc_comm("V003", 10000, "STD", 8000) == 812.0, \
        "SR, receita=10000 (>120% da meta=8000)"

    # SR, receita abaixo do mínimo (< R$ 5000) — comissão zerada
    # Nota: cada caso usa instância nova para evitar que o cache mascare o comportamento
    orig_min = CommissionCalcOriginal()
    assert orig_min.calc_comm("V001", 4000, "STD", 8000) == 0, \
        "SR, receita < 5000 deve zerar comissão"

    # SR, receita entre 80% e 100% da meta — alíquota 5%: 7000 * 0.05 = 350
    orig2 = CommissionCalcOriginal()
    assert orig2.calc_comm("V003", 7000, "STD", 8000) == 350.0, \
        "SR, receita entre 80% e 100% da meta"

    # JR, receita acima da meta — alíquota 5%
    orig3 = CommissionCalcOriginal()
    assert orig3.calc_comm("V002", 6000, "STD", 5000) == 300.0, \
        "JR, receita=6000, meta=5000, tipo=STD"

    # JR com meta agrícola (AGR) — acréscimo de 10%
    orig4 = CommissionCalcOriginal()
    # 6000 * 0.05 = 300 * 1.1 = 330
    assert orig4.calc_comm("V002", 6000, "AGR", 5000) == 330.0, \
        "JR, tipo=AGR deve acrescentar 10%"

    # JR, receita abaixo do mínimo
    orig5 = CommissionCalcOriginal()
    assert orig5.calc_comm("V002", 4000, "STD", 5000) == 0, \
        "JR, receita < 5000 deve zerar comissão"

    # Vendedor inexistente
    orig6 = CommissionCalcOriginal()
    assert orig6.calc_comm("V999", 10000, "STD", 8000) == 0, \
        "Vendedor inexistente deve retornar 0"

    print("[OK] Todos os testes de caracterização passaram.")


# ============================================================================
# ETAPA 2: Smells identificados no código original
#
# SMELL identificado: variável global `_cache` modificada dentro de método
#   → viola isolamento; duas chamadas com o mesmo vendedor retornam o valor
#     da primeira, ignorando receita e meta diferentes.
#
# SMELL identificado: parâmetros obscuros s, r, t, m
#   → impossível entender a assinatura sem ler o corpo inteiro.
#
# SMELL identificado: magic numbers 0.08, 0.05, 0.03, 0.02, 1.1, 5000, 1.2
#   → sem contexto, cada alteração exige entender a regra de negócio do zero.
#
# SMELL identificado: lógica duplicada entre calc_comm e batch_calc
#   → qualquer mudança na regra precisa ser feita em dois lugares;
#     uma das cópias inevitavelmente fica desatualizada.
#
# SMELL identificado: comentário desatualizado
#   → "# calcula para junior — copiado e modificado do bloco acima"
#     indica que a duplicação foi reconhecida mas nunca resolvida.
#
# SMELL identificado: bloco else/else com alíquotas idênticas para JR
#   → `if r >= m * 0.8: c = r * 0.03 else: c = r * 0.03`
#     as duas ramificações são iguais — bug ou intenção? sem teste, impossível saber.
# ============================================================================


# ============================================================================
# ETAPA 3: Versão Refatorada
# ============================================================================

# ---------------------------------------------------------------------------
# Constantes nomeadas — cada número tem contexto e pode ser alterado com segurança
# ---------------------------------------------------------------------------
ALIQUOTA_SR_META_ATINGIDA = 0.08
ALIQUOTA_SR_BONUS_EXCEDENTE = 0.03
ALIQUOTA_SR_PARCIAL = 0.05
ALIQUOTA_SR_ABAIXO = 0.03

ALIQUOTA_JR_META_ATINGIDA = 0.05
ALIQUOTA_JR_BONUS_EXCEDENTE = 0.02
ALIQUOTA_JR_ABAIXO = 0.03

MULTIPLICADOR_META_BONUS = 1.2    # Acima de 120% da meta, entra o bônus de excedente
MULTIPLICADOR_META_PARCIAL = 0.8  # Acima de 80% da meta, alíquota intermediária
MULTIPLICADOR_META_AGRICOLA = 1.1 # Acréscimo para metas do tipo AGR
RECEITA_MINIMA_COMISSAO = 5000.0  # Abaixo disso, comissão é zerada


from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Vendedor:
    id: str
    nome: str
    tipo: str      # "SR" ou "JR"
    regiao: str


@dataclass(frozen=True)
class EntradaComissao:
    vendedor_id: str
    receita: float
    tipo_meta: str  # "STD" ou "AGR"
    meta: float


class RepositorioDeVendedores:
    def __init__(self, dados: dict):
        self._vendedores: Dict[str, Vendedor] = {
            vid: Vendedor(id=vid, nome=d["nome"], tipo=d["tipo"], regiao=d["regiao"])
            for vid, d in dados.items()
        }

    def buscar(self, vendedor_id: str) -> Optional[Vendedor]:
        return self._vendedores.get(vendedor_id)


class CalculadorDeComissao:
    """Calcula comissão a partir de dados de receita e meta. Sem estado interno."""

    def calcular(self, entrada: EntradaComissao, vendedor: Vendedor) -> float:
        if entrada.receita < RECEITA_MINIMA_COMISSAO:
            return 0.0

        if vendedor.tipo == "SR":
            comissao = self._comissao_senior(entrada.receita, entrada.meta)
        else:
            comissao = self._comissao_junior(entrada.receita, entrada.meta)

        if entrada.tipo_meta == "AGR":
            comissao *= MULTIPLICADOR_META_AGRICOLA

        return round(comissao, 2)

    def _comissao_senior(self, receita: float, meta: float) -> float:
        if receita >= meta:
            comissao = receita * ALIQUOTA_SR_META_ATINGIDA
            if receita > meta * MULTIPLICADOR_META_BONUS:
                comissao += (receita - meta * MULTIPLICADOR_META_BONUS) * ALIQUOTA_SR_BONUS_EXCEDENTE
        elif receita >= meta * MULTIPLICADOR_META_PARCIAL:
            comissao = receita * ALIQUOTA_SR_PARCIAL
        else:
            comissao = receita * ALIQUOTA_SR_ABAIXO
        return comissao

    def _comissao_junior(self, receita: float, meta: float) -> float:
        if receita >= meta:
            comissao = receita * ALIQUOTA_JR_META_ATINGIDA
            if receita > meta * MULTIPLICADOR_META_BONUS:
                comissao += (receita - meta * MULTIPLICADOR_META_BONUS) * ALIQUOTA_JR_BONUS_EXCEDENTE
        else:
            # Nota: no código original, as duas ramificações (parcial e abaixo)
            # usavam a mesma alíquota para JR. Comportamento preservado.
            comissao = receita * ALIQUOTA_JR_ABAIXO
        return comissao


class ProcessadorDeComissoes:
    """Orquestra cálculo para um ou múltiplos vendedores. Sem estado global."""

    def __init__(self, repositorio: RepositorioDeVendedores, calculador: CalculadorDeComissao):
        self._repositorio = repositorio
        self._calculador = calculador

    def calcular_individual(self, entrada: EntradaComissao) -> float:
        vendedor = self._repositorio.buscar(entrada.vendedor_id)
        if vendedor is None:
            return 0.0
        return self._calculador.calcular(entrada, vendedor)

    def calcular_lote(self, entradas: List[EntradaComissao]) -> Dict[str, float]:
        return {
            entrada.vendedor_id: self.calcular_individual(entrada)
            for entrada in entradas
        }


# ============================================================================
# ETAPA 4: Verificação — os testes de caracterização devem passar na versão nova
# ============================================================================

def executar_testes_na_versao_refatorada():
    repositorio = RepositorioDeVendedores(_vendedores_raw)
    calculador = CalculadorDeComissao()
    processador = ProcessadorDeComissoes(repositorio, calculador)

    def calcular(vid, receita, tipo_meta, meta):
        return processador.calcular_individual(
            EntradaComissao(vendedor_id=vid, receita=receita, tipo_meta=tipo_meta, meta=meta)
        )

    assert calcular("V001", 10000, "STD", 8000) == 812.0
    assert calcular("V003", 10000, "STD", 8000) == 812.0
    assert calcular("V001", 4000,  "STD", 8000) == 0
    assert calcular("V003", 7000,  "STD", 8000) == 350.0
    assert calcular("V002", 6000,  "STD", 5000) == 300.0
    assert calcular("V002", 6000,  "AGR", 5000) == 330.0
    assert calcular("V002", 4000,  "STD", 5000) == 0
    assert calcular("V999", 10000, "STD", 8000) == 0

    print("[OK] Todos os testes de caracterização passaram na versão refatorada.")


if __name__ == "__main__":
    print("=== Etapa 1: Testes de Caracterização (versão original) ===")
    executar_testes_de_caracterizacao()
    print()

    print("=== Etapa 4: Verificação (versão refatorada) ===")
    executar_testes_na_versao_refatorada()
    print()

    print("=== Demonstração da versão refatorada ===")
    repositorio = RepositorioDeVendedores(_vendedores_raw)
    processador = ProcessadorDeComissoes(repositorio, CalculadorDeComissao())

    entrada1 = EntradaComissao(vendedor_id="V001", receita=10000, tipo_meta="STD", meta=8000)
    print(f"Ana Paula (SR): R$ {processador.calcular_individual(entrada1):.2f}")

    entrada2 = EntradaComissao(vendedor_id="V002", receita=6000, tipo_meta="AGR", meta=5000)
    print(f"Carlos Lima (JR, AGR): R$ {processador.calcular_individual(entrada2):.2f}")

    print()
    print("=== Cálculo em lote ===")
    lote = [
        EntradaComissao("V001", 10000, "STD", 8000),
        EntradaComissao("V002", 6000,  "AGR", 5000),
        EntradaComissao("V003", 7000,  "STD", 8000),
    ]
    resultados = processador.calcular_lote(lote)
    for vid, comissao in resultados.items():
        vendedor = repositorio.buscar(vid)
        print(f"  {vendedor.nome}: R$ {comissao:.2f}")
