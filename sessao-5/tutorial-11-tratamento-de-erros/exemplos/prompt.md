# Comparação de Prompts — Tratamento de Erros

Este documento mostra dois prompts para a mesma tarefa e analisa o efeito de cada um no código gerado.

---

## Prompt fraco — sem menção a erros

```
Cria uma função em Python que processa um estorno.
A função recebe um dicionário com os dados do estorno e retorna
o resultado do processamento.
```

**Saída típica:**

```python
def processar_estorno(estorno):
    try:
        valor = estorno["valor"]
        if valor > 0:
            return {"status": "aprovado", "valor": valor}
        return {"status": "rejeitado"}
    except Exception:
        pass
```

**Por que isso acontece:**

O prompt pede apenas que a função "funcione" e "retorne". A IA adiciona um `try/except` por reflexo defensivo — mas sem nenhuma instrução sobre o que fazer em caso de erro, escolhe a saída mais segura do ponto de vista do fluxo: silenciar. O `pass` garante que a função não vai "travar" o sistema, mas também garante que nenhuma informação sobre a falha chega ao chamador.

---

## Prompt forte — com tratamento de erro explícito

```
Cria uma função em Python chamada processar_estorno que recebe um
dicionário com os campos 'valor' (float) e 'valor_original' (float).

Requisitos de tratamento de erro (obrigatórios):
- Se o campo 'valor' ou 'valor_original' estiver ausente, levante
  EstornoInvalidoError com mensagem descritiva.
- Se o valor do estorno exceder o valor original, levante
  ValorEstornoExcedidoError com os dois valores na mensagem.
- Não use except genérico (except Exception) nem silencie falhas
  com pass ou retorno de None em caso de erro.
- Defina EstornoInvalidoError e ValorEstornoExcedidoError como
  classes próprias que herdam de Exception.

Todos os identificadores devem estar em português brasileiro.
```

**Saída típica:**

```python
class EstornoInvalidoError(Exception):
    """Levantada quando os dados do estorno estão incompletos."""

class ValorEstornoExcedidoError(Exception):
    """Levantada quando o valor do estorno excede o original."""

def processar_estorno(estorno: dict) -> dict:
    if "valor" not in estorno or "valor_original" not in estorno:
        raise EstornoInvalidoError(
            "Campos obrigatórios ausentes: 'valor' e 'valor_original' são necessários."
        )
    if estorno["valor"] > estorno["valor_original"]:
        raise ValorEstornoExcedidoError(
            f"Estorno de R$ {estorno['valor']:.2f} excede o valor original "
            f"de R$ {estorno['valor_original']:.2f}."
        )
    return {"status": "aprovado", "valor": estorno["valor"]}
```

**Por que isso funciona:**

O prompt especificou **o que fazer em caso de erro** — não apenas o caminho feliz. Ao nomear as exceções e proibir explicitamente o `pass`, o prompt remove a ambiguidade que leva a IA a silenciar falhas.

---

## Resumo do efeito

| Aspecto                         | Prompt fraco                   | Prompt forte                       |
|---------------------------------|--------------------------------|------------------------------------|
| Tratamento de erro              | `except Exception: pass`       | Exceções específicas nomeadas      |
| Informação em caso de falha     | Nenhuma (retorna `None`)       | Mensagem com valores e contexto    |
| Detectabilidade em produção     | Falha invisível                | Falha aparece no log imediatamente |
| Capacidade de depuração         | Mínima                         | Alta                               |
| Esforço no prompt               | 2 linhas                       | 12 linhas (ainda muito menor que o bug que evita) |
