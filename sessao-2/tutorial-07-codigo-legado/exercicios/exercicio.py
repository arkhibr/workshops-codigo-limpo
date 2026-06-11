# ============================================================================
# EXERCÍCIO — Tutorial 07: Código Legado
#
# Módulo de cálculo de comissões de vendedores.
# Status: em produção desde 2020, nunca teve testes, nunca foi refatorado.
#
# PASSOS (faça um de cada vez, em ordem):
#
#   PASSO 1 — TESTES DE CARACTERIZAÇÃO (10 min)
#     No bloco if __name__ == "__main__", escreva asserts para documentar
#     o comportamento atual. Rode o arquivo para ver os valores, então
#     substitua os ??? pelos valores observados.
#     Meta: cobrir pelo menos 5 casos distintos antes de tocar no código.
#     Importante: use uma instância nova de CommissionCalc por assert,
#     ou chame _cache.clear() entre testes — o cache global mascara resultados.
#
#   PASSO 2 — MAPEAR SMELLS (5 min)
#     Leia CommissionCalc e adicione um comentário # SMELL: antes de
#     cada problema encontrado.
#     Exemplos: magic number, nome obscuro, estado global, duplicação,
#     comentário desatualizado.
#
#   PASSO 3 — CONSTANTES + NOMES (8 min)
#     a) Extraia os magic numbers para constantes nomeadas acima da classe:
#        0.08, 0.05, 0.03, 0.02, 1.1, 1.2, 0.8, 5000
#     b) Renomeie os parâmetros em calc_comm:
#        s → vendedor_id   r → receita   t → tipo_meta   m → meta
#     Verifique que seus testes do Passo 1 ainda passam.
#
#   PASSO 4 — ELIMINAR DUPLICAÇÃO (10 min)
#     batch_calc duplica toda a lógica de calc_comm em vez de chamá-lo.
#     Altere batch_calc para chamar self.calc_comm em vez de repetir o cálculo.
#     Mova também _cache de variável global para self._cache no __init__,
#     para que cada instância tenha seu próprio estado.
#     Verifique que seus testes continuam passando.
#
# Para rodar: python3 exercicio.py
# ============================================================================

# Estado global modificado por método — dificulta paralelismo e testes
_cache = {}

# Tabela de vendedores (simulando banco de dados)
_vendedores = {
    "V001": {"nome": "Ana Paula",   "tipo": "SR", "regiao": "SP"},
    "V002": {"nome": "Carlos Lima", "tipo": "JR", "regiao": "RJ"},
    "V003": {"nome": "Maria Costa", "tipo": "SR", "regiao": "MG"},
}


class CommissionCalc:
    # Calcula comissao mensal — atualizado em jan/2020
    # (comentario desatualizado: a logica foi alterada em 2022 sem atualizar o comentario)

    def calc_comm(self, s, r, t, m):
        # s = vendedor id, r = receita total, t = tipo de meta, m = meta

        if s in _cache:
            return _cache[s]

        v = _vendedores.get(s)
        if not v:
            return 0

        # calcula para senior
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

        # calcula para junior — copiado e modificado do bloco acima
        else:
            if r >= m:
                c = r * 0.05
                if r > m * 1.2:
                    c = c + (r - m * 1.2) * 0.02
            else:
                if r >= m * 0.8:
                    c = r * 0.03
                else:
                    c = r * 0.03  # igual ao else acima — bug ou intencional?
            if t == "AGR":
                c = c * 1.1
            if r < 5000:
                c = 0

        _cache[s] = round(c, 2)
        return _cache[s]

    def batch_calc(self, vendas):
        resultados = {}
        for venda in vendas:
            s = venda["id"]
            r = venda["receita"]
            t = venda["tipo_meta"]
            m = venda["meta"]

            v = _vendedores.get(s)
            if not v:
                continue

            # duplica toda a logica de calc_comm ao inves de chamar o metodo
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

            resultados[s] = round(c, 2)

        return resultados


if __name__ == "__main__":
    calc = CommissionCalc()

    # -----------------------------------------------------------------------
    # PASSO 1: escreva seus testes de caracterização aqui.
    # Rode o arquivo para ver os valores, depois substitua ??? pelo resultado.
    # Use _cache.clear() entre chamadas para evitar que o cache mascare o teste.
    #
    # Exemplos de chamadas para explorar o comportamento:
    # -----------------------------------------------------------------------

    print("=== Explorando o comportamento atual ===")
    _cache.clear()
    print("SR, receita=10000, meta=8000, tipo=STD:", calc.calc_comm("V001", 10000, "STD", 8000))
    _cache.clear()
    print("SR, receita=4000,  meta=8000, tipo=STD:", calc.calc_comm("V003", 4000,  "STD", 8000))
    _cache.clear()
    print("SR, receita=7000,  meta=8000, tipo=STD:", calc.calc_comm("V003", 7000,  "STD", 8000))
    _cache.clear()
    print("JR, receita=6000,  meta=5000, tipo=STD:", calc.calc_comm("V002", 6000,  "STD", 5000))
    _cache.clear()
    print("JR, receita=6000,  meta=5000, tipo=AGR:", calc.calc_comm("V002", 6000,  "AGR", 5000))
    _cache.clear()
    print("JR, receita=4000,  meta=5000, tipo=STD:", calc.calc_comm("V002", 4000,  "STD", 5000))
    _cache.clear()
    print("Inexistente V999:", calc.calc_comm("V999", 10000, "STD", 8000))

    print()
    print("=== Batch ===")
    _cache.clear()
    vendas = [
        {"id": "V001", "receita": 10000, "tipo_meta": "STD", "meta": 8000},
        {"id": "V002", "receita": 6000,  "tipo_meta": "AGR", "meta": 5000},
    ]
    print(calc.batch_calc(vendas))

    # -----------------------------------------------------------------------
    # Substitua os ??? e descomente os asserts após anotar os valores acima:
    # -----------------------------------------------------------------------
    # _cache.clear(); assert calc.calc_comm("V001", 10000, "STD", 8000) == ???
    # _cache.clear(); assert calc.calc_comm("V003", 4000,  "STD", 8000) == ???
    # _cache.clear(); assert calc.calc_comm("V003", 7000,  "STD", 8000) == ???
    # _cache.clear(); assert calc.calc_comm("V002", 6000,  "STD", 5000) == ???
    # _cache.clear(); assert calc.calc_comm("V002", 6000,  "AGR", 5000) == ???
    # _cache.clear(); assert calc.calc_comm("V002", 4000,  "STD", 5000) == ???
    # _cache.clear(); assert calc.calc_comm("V999", 10000, "STD", 8000) == ???
    # print("[OK] testes de caracterização passando")
