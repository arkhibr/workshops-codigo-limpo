# ============================================================================
# EXERCÍCIO — Tutorial 07: Gestão de Código Legado
#
# Módulo de cálculo de comissões de vendedores
# Status: em produção desde 2020, nunca teve testes, nunca foi refatorado.
#
# INSTRUÇÕES:
#   1. Escreva "testes de caracterização" para a função calc_comm abaixo:
#      testes que documentam o comportamento ATUAL antes de qualquer mudança.
#      Use asserts simples no bloco if __name__ == "__main__".
#      Dica: passe valores conhecidos e verifique o retorno. Se o resultado
#      parecer errado, documente-o assim mesmo — o objetivo é capturar o
#      comportamento existente, não corrigi-lo ainda.
#
#   2. Identifique e anote com "# SMELL:" cada problema que você encontrar
#      no código. Exemplos de smells: magic number, nome obscuro, estado
#      global modificado, lógica duplicada, comentário que mente.
#
#   3. Refatore o código aplicando as técnicas do tutorial:
#      - Constantes nomeadas para os magic numbers
#      - Classes com responsabilidade única
#      - Eliminar modificação de estado global dentro de método
#      - Nomes descritivos para parâmetros e variáveis
#      - Eliminar lógica duplicada
#
#   4. Execute seus testes de caracterização na versão refatorada.
#      Se algum assert falhar, você mudou o comportamento — investigue.
#
# Para rodar: python3 exercicio.py
# ============================================================================

# Estado global modificado por método — dificulta paralelismo e testes
_cache = {}

# Tabela de vendedores (simulando banco de dados)
_vendedores = {
    "V001": {"nome": "Ana Paula", "tipo": "SR", "regiao": "SP"},
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
    # ETAPA 1: Escreva aqui seus testes de caracterização
    # Documente o comportamento atual ANTES de refatorar.
    # Exemplo de estrutura (substitua pelos valores corretos):
    #
    #   resultado = calc.calc_comm("V001", 10000, "STD", 8000)
    #   assert resultado == ???, f"Esperado ???, obtido {resultado}"
    #
    # Rode o arquivo, veja o que retorna, e use esse valor no assert.
    # -----------------------------------------------------------------------

    print("=== Testes de caracterização ===")
    print("(implemente seus asserts aqui antes de refatorar)")
    print()

    # Exemplos de chamadas para explorar o comportamento:
    print("SR, receita=10000, meta=8000, tipo=STD:", calc.calc_comm("V001", 10000, "STD", 8000))
    print("SR, receita=4000,  meta=8000, tipo=STD:", calc.calc_comm("V003", 4000, "STD", 8000))
    print("JR, receita=6000,  meta=5000, tipo=AGR:", calc.calc_comm("V002", 6000, "AGR", 5000))
    print()

    print("=== Batch ===")
    vendas = [
        {"id": "V001", "receita": 10000, "tipo_meta": "STD", "meta": 8000},
        {"id": "V002", "receita": 6000,  "tipo_meta": "AGR", "meta": 5000},
    ]
    print(calc.batch_calc(vendas))
