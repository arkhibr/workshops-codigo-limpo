> Tutorial âncora do tema — acumula as Sessões 1–2 e os tutoriais 08–11 aplicados a código de IA

# Tutorial 12 — Revisão Crítica de Código Gerado por IA

---

## 1. Contexto e Motivação

Este é o exercício âncora do Tema 3 (IA). O papel que o Tutorial 05 desempenhou na Sessão 2 — integrar nomes, funções, comentários e formatação em uma única revisão — este tutorial desempenha no contexto de código gerado por assistente de IA.

Código de IA tem uma propriedade traiçoeira: ele é **confiante e plausível**. Compila, passa nos testes superficiais, e os nomes parecem razoáveis. Exatamente por isso a revisão crítica é mais difícil do que revisar código escrito por um colega — com um colega, você sabe que ele pode ter se distraído; com a IA, você tende a assumir que ela verificou o que afirmou ter verificado.

O tutorial parte de um prompt razoável (veja `prompt_original.md`) e do código que uma IA típica geraria a partir dele. O prompt não especificou restrições de segurança, edge cases nem como obter a chave de API. Essas omissões se traduzem diretamente nos seis problemas plantados no código — um por modo de falha característico de IA.

> **Conexão com tutoriais anteriores:** o Tutorial 09 mostrou como escrever prompts fortes para reduzir esses problemas na origem. O Tutorial 10 mostrou como refatorar o código depois de recebê-lo. Este tutorial fecha o ciclo: dado um prompt apenas razoável, como identificar sistematicamente o que ficou errado antes de commitar?

---

## 2. Conceito Central — Os Seis Modos de Falha de Código de IA

### Modo 1 — API/método alucinado

A IA inventa um nome de método coerente com o padrão da biblioteca, mas que não existe. O código compila (às vezes), mas quebra em runtime na primeira chamada ao caminho afetado.

```python
# Método post_parcelado não existe na classe _GatewayHttpClient
return _cliente_http.post_parcelado(url, payload, _montar_headers())
```

O sinal de alerta em TypeScript é o cast `as any` — ele frequentemente aparece porque o compilador apontou o erro e a IA o silenciou em vez de corrigir a causa raiz.

### Modo 2 — Lógica plausível-mas-errada (condição invertida)

A estrutura do código está correta, mas a condição booleana está invertida. O código funciona no caminho feliz apenas se os dados de entrada nunca acionarem a condição — que é exatamente o que acontece em uma demo sem rede real.

```python
# Condição invertida: != "aprovado" é verdadeiro quando o gateway RECUSA
# mas o bloco if retorna ok=True (sucesso). Uma transação aprovada retorna ok=False.
if resposta_bruta.get("status") != "aprovado":
    return {"ok": True, "codigo_autorizacao": ...}
else:
    return {"ok": False, "erro": ...}
```

### Modo 3 — Segurança (segredo hardcoded, concatenação de string)

A IA preenche lacunas do prompt com o caminho de menor resistência: hardcoda a chave de API porque o prompt não disse como obtê-la, e concatena parâmetros na URL porque é a forma mais simples de construir a query string.

```python
# Segredo exposto em qualquer repositório — incluindo histórico de git
API_KEY = "sk-prod-2b7f3e9a4c1d0f6e8a2b5c7d9e1f3a5b"

# Injeção via query string: descricao="../admin" ou "foo&outro_param=valor"
url = BASE_URL + "/cobrancas?descricao=" + descricao
```

> O **Tutorial 13** aprofunda segurança em código de IA. Este tutorial introduz os dois padrões mais frequentes.

### Modo 4 — Edge cases faltando (valor zero, lista vazia, timeout)

O prompt descreve o caso feliz. A IA implementa o caso feliz. Valores fora do intervalo esperado — zero, negativos, strings vazias, timeouts — simplesmente não entram no raciocínio do modelo se o prompt não os mencionar.

```python
# Nenhuma guarda para valor <= 0.
# cobrar(0, ...) ou cobrar(-50, ...) é enviado normalmente ao gateway.
def cobrar(valor: float, numero_cartao: str, cpf_titular: str, ...):
    if not _validar_cpf(cpf_titular):
        return {"ok": False, "erro": "CPF inválido"}
    # valor nunca é verificado antes de seguir
```

### Modo 5 — Over-engineering

A IA tende a interpretar prompts de forma mais ampla do que o necessário, adicionando abstrações, classes e generics que não foram pedidos. O resultado é código correto mas mais complexo do que o problema exige — aumentando a superfície de manutenção sem benefício proporcional.

```python
# Função auxiliar _cobrar_parcelado criada sem ter sido pedida,
# com interface própria e endpoint separado — tudo isso para uma funcionalidade
# que deveria ser apenas um parâmetro `parcelas` na função principal cobrar().
def _cobrar_parcelado(valor: float, numero_cartao: str, parcelas: int) -> dict:
    url = BASE_URL + "/cobrancas/parceladas"
    ...
```

### Modo 6 — Confiança enganosa (comentário que mente sobre o código)

A IA escreve docstrings e comentários com a mesma confiança com que escreve código. Se o código não faz o que o comentário afirma, o leitor — que tende a confiar no comentário — passa a ter uma expectativa incorreta sobre a robustez do sistema.

```python
def _validar_cpf(cpf: str) -> bool:
    """Valida o CPF do titular do cartão conforme regras da Receita Federal."""
    # Na prática: apenas verifica se a string tem 11 dígitos.
    # CPFs como "00000000000" e "11111111111" passam — ambos são inválidos.
    cpf_limpo = cpf.replace(".", "").replace("-", "")
    return len(cpf_limpo) == 11 and cpf_limpo.isdigit()
```

---

## 3. Exercício

### Material

| Arquivo | Papel |
|---|---|
| `prompt_original.md` | O prompt que gerou o código — leia primeiro |
| `codigo_gerado_por_ia.py` | Código Python a revisar (contém os 6 problemas) |
| `codigo_gerado_por_ia.ts` | Equivalente TypeScript |
| `checklist_revisao_ia.md` | Checklist completo para guiar a revisão |
| `gabarito_review.md` | Gabarito Python — abrir só depois de tentar |
| `gabarito_review_ts.md` | Gabarito TypeScript |
| `exercicios/roteiro-ia.md` | Trilha hands-on com IA real |

### Passo a passo

1. **Leia `prompt_original.md`** e observe o que ele não especificou — essa lista de omissões é o mapa dos problemas.

2. **Execute o código** para confirmar que o caminho feliz roda:
   ```bash
   python3 sessao-6/tutorial-12-revisao-critica-ia/codigo_gerado_por_ia.py
   npx ts-node sessao-6/tutorial-12-revisao-critica-ia/codigo_gerado_por_ia.ts
   ```
   Observe a saída: a demo exibe `"ok": false` mesmo para uma cobrança aprovada — esse é o Problema 3 em ação.

3. **Leia o código linha a linha** usando `checklist_revisao_ia.md` como guia. Para cada problema encontrado, anote: linha, categoria e como corrigir.

4. **Compare com o gabarito** (`gabarito_review.md` / `gabarito_review_ts.md`). Veja quantos dos 6 problemas você identificou e quais categorias do checklist você cobriu.

5. **Trilha hands-on:** siga `exercicios/roteiro-ia.md` para repetir o ciclo com um prompt seu e um assistente de IA real.

### Meta

- **6/6 problemas encontrados:** olhar calibrado para código de IA. Prossiga para o Tutorial 13.
- **4–5/6:** revise as categorias que você perdeu no checklist e releia os tutoriais 08–11 correspondentes.
- **Menos de 4:** faça a leitura linha a linha com o checklist aberto ao lado — o objetivo é desenvolver o hábito antes de automatizá-lo.

> Não existe penalidade por abrir o gabarito cedo — mas tente encontrar pelo menos 3 problemas antes de consultá-lo.

---

## 4. Checklist Resumido

O checklist completo está em `checklist_revisao_ia.md`. Versão rápida para usar durante a leitura:

| Categoria | Pergunta-chave |
|---|---|
| Correção | Condicionais têm os blocos no lado certo? A lógica faz o que o nome diz? |
| Segurança | Há segredos hardcoded? Entradas do usuário são escapadas antes de entrar em URLs? |
| Edge cases | O que acontece com valor zero, negativo ou string vazia? Há tratamento de timeout? |
| Legibilidade | Os comentários e docstrings descrevem o que o código *realmente* faz? |
| Dependências | Todos os métodos chamados existem na interface/SDK disponível? |
| Entendimento | O código resolve o problema pedido — ou uma versão mais simples dele? Há over-engineering? |

---

## 5. Referências

- **Clean Code**, Robert C. Martin — Cap. 2: *Meaningful Names*; Cap. 3: *Functions*; Cap. 4: *Comments*
- **Working Effectively with Legacy Code**, Michael Feathers — técnicas de inspeção de código não familiar
- Tutorial 05 — Code Review Simulado: [`sessao-2/tutorial-05-code-review/README.md`](../../sessao-2/tutorial-05-code-review/README.md)
- Tutorial 09 — Engenharia de Prompt: [`sessao-5/tutorial-09-engenharia-de-prompt/README.md`](../../sessao-5/tutorial-09-engenharia-de-prompt/README.md)
- Tutorial 13 — Segurança em Código de IA: [`sessao-6/tutorial-13-seguranca-codigo-ia/README.md`](../tutorial-13-seguranca-codigo-ia/README.md)

---

> **Próximo tutorial:** [Tutorial 13 — Segurança em Código de IA](../tutorial-13-seguranca-codigo-ia/README.md)
