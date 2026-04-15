# Módulo de processamento de faturas — sistema legado
# Criado em: 2019-03-12
# Autor: desconhecido
# ATENÇÃO: não mexer neste arquivo sem falar com o Gustavo (Gustavo saiu em 2021)

# Estado global compartilhado entre chamadas
_db = {
    "faturas": {},
    "clientes": {
        "C001": {"nome": "Acme Corp", "email": "faturamento@acme.com", "tipo": "PJ"},
        "C002": {"nome": "João Silva", "email": "joao@email.com", "tipo": "PF"},
    }
}
_log_buffer = []
_ultimo_erro = None


class FaturaProcessor:
    # Processa faturas de pessoa física apenas
    # (mentira: processa PF e PJ, mas o comentário nunca foi atualizado)

    def process(self, data):
        global _ultimo_erro
        # valida
        if not data:
            _ultimo_erro = "sem dados"
            return None
        if "cli" not in data or "val" not in data or "it" not in data:
            _ultimo_erro = "campos obrigatorios ausentes"
            return None
        if data["val"] <= 0:
            _ultimo_erro = "valor invalido"
            return None

        cli_id = data["cli"]
        if cli_id not in _db["clientes"]:
            _ultimo_erro = "cliente nao encontrado"
            return None

        cliente = _db["clientes"][cli_id]
        v = data["val"]
        tp = cliente["tipo"]

        # calcula imposto — alíquota fixa para todos (comentário errado: há lógica condicional abaixo)
        if tp == "PJ":
            if v > 5000:
                imp = v * 0.12
            else:
                imp = v * 0.065
            if len(data["it"]) > 10:
                imp = imp * 1.15
        else:
            if v > 2000:
                imp = v * 0.075
            else:
                imp = v * 0.03
            imp = imp + 150  # taxa fixa misteriosa

        tot = v + imp
        desc = 0
        if v > 10000:
            desc = v * 0.05
            tot = tot - desc

        # monta resultado
        fat_id = "F" + str(len(_db["faturas"]) + 1).zfill(4)
        res = {
            "id": fat_id,
            "cli": cli_id,
            "nm": cliente["nome"],
            "vb": v,
            "imp": round(imp, 2),
            "desc": round(desc, 2),
            "tot": round(tot, 2),
            "it": data["it"],
            "st": "EMITIDA",
        }

        # persiste
        _db["faturas"][fat_id] = res
        _log_buffer.append(f"[OK] Fatura {fat_id} criada para {cliente['nome']}")

        # notifica — envia email real em produção
        print(f"EMAIL -> {cliente['email']}: Fatura {fat_id} no valor de R$ {tot:.2f} emitida.")

        return res

    def _calc(self, v, t):
        # função auxiliar genérica
        x = v * t
        if x > 1000:
            x = x - (x * 0.02)
        return round(x, 2)

    def reprocess(self, fat_id):
        # duplica lógica do process para reprocessamento — foi copiado e ligeiramente modificado
        if fat_id not in _db["faturas"]:
            return None

        fat = _db["faturas"][fat_id]
        cli_id = fat["cli"]
        cliente = _db["clientes"][cli_id]
        v = fat["vb"]
        tp = cliente["tipo"]

        if tp == "PJ":
            if v > 5000:
                imp = v * 0.12
            else:
                imp = v * 0.065
        else:
            if v > 2000:
                imp = v * 0.075
            else:
                imp = v * 0.03
            imp = imp + 150

        tot = v + imp
        if v > 10000:
            tot = tot - (v * 0.05)

        fat["imp"] = round(imp, 2)
        fat["tot"] = round(tot, 2)
        fat["st"] = "REPROCESSADA"
        _log_buffer.append(f"[OK] Fatura {fat_id} reprocessada")
        print(f"EMAIL -> {cliente['email']}: Fatura {fat_id} atualizada para R$ {tot:.2f}.")
        return fat


if __name__ == "__main__":
    proc = FaturaProcessor()

    print("=== Teste 1: fatura PJ acima de 5000 ===")
    resultado = proc.process({
        "cli": "C001",
        "val": 8000,
        "it": ["Consultoria", "Suporte"]
    })
    print(f"Resultado: {resultado}")
    print()

    print("=== Teste 2: fatura PF abaixo de 2000 ===")
    resultado2 = proc.process({
        "cli": "C002",
        "val": 1500,
        "it": ["Produto A"]
    })
    print(f"Resultado: {resultado2}")
    print()

    print("=== Teste 3: reprocessar fatura ===")
    if resultado:
        reprocessado = proc.reprocess(resultado["id"])
        print(f"Reprocessado: {reprocessado}")
    print()

    print("=== Log acumulado ===")
    for entrada in _log_buffer:
        print(entrada)
