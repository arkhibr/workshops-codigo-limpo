# Tutorial 08 — Clean Code no Contexto Real com IA

> Referência: *Clean Code*, Cap. 2–3 aplicados a código assistido por IA

---

## 1. Contexto e Motivação

Assistentes de IA geram código na velocidade de um júnior incansável: rápidos, prolíficos e sem fadiga. O desenvolvedor que antes escrevia cada linha agora passa a ser o **sênior que revisa** — e essa mudança de papel exige um conjunto diferente de atenção.

Os princípios das Sessões 1–2 continuam sendo o critério de qualidade: nomes que revelam intenção, funções com responsabilidade única, ausência de números mágicos, idioma consistente. O que muda é o contexto de aplicação: em vez de revisar código escrito por um colega, você revisa código gerado por uma máquina que não conhece o seu domínio, o seu padrão de nomenclatura nem a sua definição de "uma coisa só".

A boa notícia: a IA aceita especificações. Um **prompt bem escrito** funciona como uma especificação informal, e ele eleva significativamente o ponto de partida do código gerado. A má notícia: mesmo um bom prompt não substitui a revisão — o código ainda precisa ser lido criticamente antes de entrar na base.

---

## 2. Conceito Central

### O prompt como especificação informal

Um prompt vago produz código genérico e frágil. Compare:

```
# Prompt fraco
faz uma função de agendar consulta
```

Saída típica:

```python
def processar(d, p, h):       # o que é d? p? h?
    for item in data:
        if item["date"] == d and item["p"] == p:
            return -1         # código de erro sem mensagem
    data.append({"date": d, "p": p, "h": h, "dur": 30})  # número mágico
```

O prompt não especificou o domínio, os nomes esperados, o tratamento de erro nem a estrutura de dados. A IA preencheu as lacunas com defaults genéricos — inglês, abreviações, dict solto.

Agora com um prompt forte:

```
# Prompt forte (trecho)
Contexto: sistema de agendamento de uma clínica médica. Todos os
identificadores devem estar em português brasileiro.
...
Lança ValueError com mensagem descritiva se o paciente já tiver
consulta agendada na mesma data.
...
Sem números mágicos — extraia constantes nomeadas.
```

Saída típica:

```python
DURACAO_PADRAO_MIN = 30   # constante nomeada

@dataclass
class Consulta:
    data: str
    horario: str
    nome_paciente: str
    duracao_min: int = DURACAO_PADRAO_MIN
    status: str = "confirmada"

def agendar_consulta(data: str, horario: str, nome_paciente: str) -> Consulta:
    if _existe_conflito(data, nome_paciente):
        raise ValueError(f"Paciente '{nome_paciente}' já possui consulta em {data}.")
    ...
```

A diferença não é sorte — é especificação. O prompt forte embutiu os critérios de Clean Code na própria pergunta.

### O prompt não substitui a revisão

Mesmo partindo de um prompt forte, o código gerado precisa ser lido. A IA pode:

- Ignorar parte das restrições (especialmente as de idioma).
- Gerar validações incompletas para casos de borda não mencionados.
- Produzir funções ligeiramente maiores que o necessário.
- Usar padrões corretos mas com nomes que poderiam ser mais descritivos no contexto do seu domínio.

O checklist abaixo é o instrumento de revisão.

---

## 3. Exercício

O exercício está em `exercicios/` e tem duas partes:

**Parte estática** (`exercicio.py` / `exercicio.ts`): código de lista de espera gerado por IA a partir de um prompt fraco. Sua tarefa:
1. Reescreva o prompt para ser mais forte.
2. Refatore o código aplicando os princípios de Clean Code.
3. Liste os problemas que você encontrou.

```bash
# Veja o código a ser refatorado:
python3 exercicios/exercicio.py

# Compare com a solução de referência:
python3 exercicios/gabarito.py
```

**Parte hands-on** (`roteiro-ia.md`): use o seu assistente de IA com o prompt forte sugerido, gere a função, aplique o checklist e anote o resultado. Se não tiver acesso a um assistente, o `exercicio.*` serve de fallback.

> Arquivo: [`exercicios/exercicio.py`](exercicios/exercicio.py) · [`exercicios/exercicio.ts`](exercicios/exercicio.ts)  
> Gabarito: [`exercicios/gabarito.py`](exercicios/gabarito.py) · [`exercicios/gabarito.ts`](exercicios/gabarito.ts)  
> Revisão comentada: [`exercicios/gabarito_revisao.md`](exercicios/gabarito_revisao.md)  
> Roteiro hands-on: [`exercicios/roteiro-ia.md`](exercicios/roteiro-ia.md)

---

## 4. Checklist de Revisão de Código Gerado por IA

Use estas perguntas ao revisar qualquer saída de assistente de IA:

1. **Defini o domínio no prompt?** — O assistente conhecia o contexto de negócio, o idioma dos identificadores e a estrutura de dados esperada?
2. **Pedi responsabilidade única?** — Cada função gerada faz exatamente uma coisa, ou mistura validação, cálculo e persistência?
3. **Revisei os nomes?** — Os nomes revelam intenção sem precisar de comentário? Estão todos no mesmo idioma?
4. **Validei o comportamento?** — Testei os casos de borda mencionados no prompt (conflito de horário, fila vazia, posição inexistente)?
5. **Li o código inteiro?** — Não apenas a função pedida, mas as auxiliares geradas junto — elas seguem os mesmos critérios?
6. **Há números mágicos ou constantes sem nome?** — Valores literais que deveriam ser constantes nomeadas?

---

## 5. Referências

- **Clean Code**, Robert C. Martin — Capítulo 2: *Meaningful Names* (p. 17–30)
- **Clean Code**, Robert C. Martin — Capítulo 3: *Functions* (p. 31–52)
- Arquivos de exemplo: [`exemplos/prompt.md`](exemplos/prompt.md) · [`exemplos/agendamento_gerado.py`](exemplos/agendamento_gerado.py) · [`exemplos/agendamento_revisado.py`](exemplos/agendamento_revisado.py)

---

> **Próximo tutorial:** [Tutorial 09 — …](../tutorial-09/README.md) *(em breve)*
