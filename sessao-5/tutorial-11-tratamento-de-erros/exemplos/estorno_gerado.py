"""
SAÍDA TÍPICA DE IA — processamento de estornos (a partir de prompt sem requisitos de erro)
Referência: Clean Code, Cap. 7 (Error Handling)

⚠️  Este arquivo é INTENCIONALMENTE IMPERFEITO.
    Note o tratamento de erro silencioso: erros são engolidos com
    except Exception: pass e a função retorna None em falha.
    O caminho feliz funciona, mas um estorno inválido some sem aviso.

Execute: python3 sessao-5/tutorial-11-tratamento-de-erros/exemplos/estorno_gerado.py
"""

# Prompt usado: "cria uma função que processa um estorno e retorna o resultado"


def processar_estorno(estorno):  # sem type hints, sem contrato claro
    try:
        valor = estorno["valor"]
        valor_original = estorno["valor_original"]
        if valor <= 0:
            return None  # falha silenciosa — quem chamou não sabe o que houve
        if valor > valor_original:
            return None  # regra de negócio violada, mas sem aviso
        resultado = {
            "id": estorno.get("id", "sem-id"),
            "status": "aprovado",
            "valor": valor,
        }
        return resultado
    except Exception:
        pass  # engole qualquer erro — KeyError, TypeError, o que vier


# ─── Execução de demonstração ─────────────────────────────────────────────────

if __name__ == "__main__":
    estorno_valido = {
        "id": "EST-001",
        "valor": 150.00,
        "valor_original": 300.00,
    }

    estorno_sem_campo = {
        "id": "EST-002",
        "valor": 80.00,
        # 'valor_original' ausente — KeyError engolido pelo except
    }

    estorno_excedido = {
        "id": "EST-003",
        "valor": 500.00,
        "valor_original": 300.00,
        # valor excede o original — retorna None sem aviso
    }

    print("=== Demonstração: estorno_gerado.py ===")
    print()

    resultado = processar_estorno(estorno_valido)
    print(f"EST-001 (válido): {resultado}")

    resultado = processar_estorno(estorno_sem_campo)
    print(f"EST-002 (campo ausente): {resultado}")   # imprime None — falha invisível

    resultado = processar_estorno(estorno_excedido)
    print(f"EST-003 (valor excedido): {resultado}")  # imprime None — falha invisível

    print()
    print("⚠ EST-002 e EST-003 falharam, mas nenhum erro foi levantado.")
    print("  O sistema continua rodando como se tudo estivesse bem.")
