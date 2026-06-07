# Prompt — Testes de caracterização antes de adicionar uma faixa de peso

Este arquivo demonstra **como pedir ao modelo que escreva os testes de caracterização
primeiro e só depois faça a mudança** — para os três modelos de fronteira.

**Objetivo:** adicionar uma faixa "carga pesada" (> 20 kg) à função `calcular_frete`
sem quebrar o comportamento das faixas existentes.

---

## O problema sem caracterização prévia

```
Adicione à função calcular_frete uma nova faixa: envios acima de 20 kg
devem ter tarifa base de R$ 80,00. Mantenha as faixas existentes.
```

**Saída típica:** código polido, tipado, corretamente estruturado — e com uma
regressão silenciosa. Ao reposicionar as condicionais para encaixar a nova faixa,
o modelo muda `peso_kg <= 10` para `peso_kg < 10`. A faixa padrão perde o peso
de exatamente 10 kg. Nenhum teste existente detecta isso porque a suite original
só cobre 5 kg e 8 kg — valores que não tocam a fronteira.

---

## Com caracterização prévia (a abordagem correta)

### Claude (Claude Code / Opus 4.8)

O CLAUDE.md já está no contexto. Divida o pedido em dois turnos separados:

```
[turno 1 — caracterização]
Antes de modificar calcular_frete, escreva uma suite verificar_*() com a
convenção deste repositório (print "OK: <caso>" ou "FALHOU: <caso> (esperado X, obtido Y)").

A suite deve cobrir:
- Um valor mid-band de cada faixa existente (1 kg, 5 kg, 15 kg)
- Os valores de borda exatos: 2 kg (topo faixa leve), 10 kg (topo faixa padrão),
  20 kg (topo faixa intermediária) e o imediatamente acima de cada borda (2.1 kg,
  10.1 kg, 20.1 kg)
- Peso zero e peso negativo (devem levantar ValueError)

Rode a suite contra o código atual e confirme que todos os casos passam.
Aguarde minha confirmação antes de fazer qualquer mudança na lógica.

[turno 2 — mudança]
Agora adicione a faixa "carga pesada": envios acima de 20 kg com tarifa base
de R$ 80,00. Rode a suite de caracterização novamente e reporte qualquer caso
que falhar. Se algum falhar, a mudança introduziu regressão — corrija antes
de me entregar o código final.
```

**Por que funciona:** o turno 1 força o modelo a documentar o comportamento
atual antes de tocar no código. O turno 2 usa essa suite como guarda-rail.
Se o modelo deslocar `<= 10` para `< 10` ao encaixar a nova faixa, o caso
"10 kg, 100 km" vai imprimir FALHOU — e o modelo corrige antes de entregar.

**Diferença relevante do Claude:** o histórico de turno é preservado entre
os dois prompts na mesma sessão. O modelo conhece a suite que escreveu no
turno 1 e a aplica automaticamente no turno 2.

---

### OpenAI (Codex com AGENTS.md)

Configure `AGENTS.md` com as convenções do repositório. Use a declaração de
estratégia antes de cada etapa:

```
[developer/system message — vai em AGENTS.md]
You are a Python code generator for a Clean Code workshop (Brazilian Portuguese).
Conventions:
- All identifiers in Brazilian Portuguese (peso_kg, distancia_km, tarifa_base)
- Named constants at module top for all thresholds
- verificar_*() functions with print("OK: <caso>") or print("FALHOU: <caso> ...")
- No test framework — stdout-only verification
- if __name__ == "__main__": block with demo and all verificar_* calls

[turno 1 — estratégia de caracterização]
Before writing any code, answer:
  a) Which exact weight values are boundaries between faixas in the current code?
  b) Why is testing 5 kg and 8 kg insufficient to detect a boundary shift at 10 kg?
  c) What values would a complete characterization suite include?

[turno 2 — gerar a suite]
Write the characterization suite verificar_faixas_completo() covering:
  - mid-band: 1 kg, 5 kg, 15 kg
  - boundaries: 2.0, 2.1, 10.0, 10.1, 20.0, 20.1 kg
  - invalid: peso=0 and peso=-1 (must raise ValueError)
Run it against the current calcular_frete and confirm all OK.

[turno 3 — mudança]
Now add the "carga pesada" band: weight > 20 kg, tarifa_base = 80.00.
Re-run the full characterization suite. Report any FALHOU — fix before delivering.
```

**Diferença relevante do Codex:** o turno de declaração de estratégia (turno 1)
força o modelo a raciocinar explicitamente sobre quais bordas existem antes
de receber a tarefa de implementação. Se o modelo não souber citar 10 kg como
fronteira no turno 1, ele muito provavelmente vai deslocá-la no turno 3.
Corrija no turno 1 — antes de qualquer código.

**Nota de fallback:** sem Codex disponível, use o prompt de OpenAI como turno
único em qualquer modelo. O resultado será menos controlado, mas o checklist
do README se aplica da mesma forma ao output recebido.

---

### Gemini (Gemini CLI com GEMINI.md)

Configure `GEMINI.md` com as convenções. Cole `frete_revisado.py` como few-shot
antes do prompt — o Gemini usa a janela de contexto ampla para inferir o padrão:

```
# system_instruction (em GEMINI.md):
Você é um gerador de código para um workshop de Clean Code em português brasileiro.
Convenções:
- Identificadores em português (peso_kg, distancia_km, tarifa_base, faixa)
- Constantes nomeadas para todos os limiares e tarifas
- Funções verificar_*() com print("OK: <caso>") ou print("FALHOU: <caso> ...")
- Sem framework de teste — verificação apenas por stdout
- Bloco if __name__ == "__main__": com demo e todas as chamadas verificar_*

# prompt (cole frete_revisado.py inteiro como few-shot, depois este bloco):
Antes de gerar qualquer código, responda em uma frase:
  Quais são os valores de fronteira entre as faixas da função calcular_frete?

Depois siga este plano em dois passos:

Passo 1: escreva verificar_faixas_completo() cobrindo mid-band e bordas exatas
de cada faixa, incluindo peso zero (ValueError). Rode contra o código atual.
Confirme que todos passam antes de continuar.

Passo 2: adicione a faixa "carga pesada" (> 20 kg, tarifa_base = 80.00).
Rode verificar_faixas_completo() novamente. Se algum caso falhar, corrija
a regressão antes de entregar o código final.
```

**Vantagem:** colar `frete_revisado.py` como few-shot ancora o padrão de
suite completa com bordas de forma concreta. O Gemini vê `verificarFaixaPadrao()`
com o caso de 10 kg comentado como "fronteira crítica" e reproduz a estrutura —
sem precisar inferir por que apenas 5 kg e 8 kg são insuficientes.

**Diferença relevante do Gemini:** com a janela de contexto ampla, o few-shot
de um arquivo completo é mais eficaz do que uma descrição textual das convenções.
Cole o arquivo real, não um resumo. A suite que o modelo vai gerar espelha
a estrutura do exemplo que viu — incluindo os comentários explicativos nas bordas.

---

## O que muda na aderência

| Aspecto | Sem caracterização prévia | Com caracterização prévia |
|---|---|---|
| Regressão de fronteira detectada | Não — suite fraca não cobre 10 kg | Sim — suite completa inclui 10 kg |
| Quem escreve os testes | Ninguém (ou o modelo após a mudança) | Você (ou modelo, antes da mudança) |
| Momento da detecção | No cliente — semanas depois | No terminal — antes do commit |
| Confiança no output | Baseada na leitura visual | Baseada em evidência de execução |
| Iterações para acertar | 2–3 (descoberta + correção + re-entrega) | 1 (correto de primeira ou corrigido na sessão) |

**Conclusão:** os três modelos produzem código polido ao adicionar uma nova faixa.
A diferença está em **quando os testes existem**: se só existem depois da mudança,
eles caracterizam o comportamento novo — incluindo a regressão. Se existem antes,
eles são um guarda-rail que o próprio modelo usa para detectar e corrigir o erro.
