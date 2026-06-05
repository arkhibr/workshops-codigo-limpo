# Roteiro Hands-on — Clean Code com Assistente de IA

> Duração estimada: 20–30 minutos  
> Pré-requisito: acesso a um assistente de IA (ChatGPT, Claude, Gemini, Copilot ou similar)

---

## Objetivo

Experimentar na prática como a qualidade do prompt afeta a qualidade do código gerado — e exercitar o papel de revisor sênior sobre a saída da IA.

---

## Passo a Passo

### 1. Abra seu assistente de IA

Use o assistente de sua preferência: ChatGPT, Claude, Gemini, Copilot ou qualquer outro. Não há diferença de procedimento entre eles para este exercício.

---

### 2. Cole o prompt forte de lista de espera

Copie o prompt abaixo na íntegra e envie para o assistente:

```
Contexto: sistema de gestão de clínica médica. Todos os identificadores
devem estar em português brasileiro — sem mistura de idiomas.

Implemente um módulo de lista de espera com as seguintes funções:

1. `adicionar_na_fila(nome_paciente, tipo_atendimento)` → None
   - Gera um número de posição sequencial (constante nomeada para o valor inicial).
   - Cria uma EntradaFila (dataclass) com: posicao, nome_paciente,
     tipo_atendimento, registrado_em (datetime atual), atendido=False.
   - Armazena na lista em memória. Não retorna valor (CQS: é um comando).

2. `remover_da_fila(posicao)` → None
   - Remove a entrada com a posição informada.
   - Lança ValueError com mensagem descritiva se não encontrada.

3. `exibir_lista_de_espera()` → None
   - Exibe cada entrada com marcador visual para atendido/pendente.

4. `chamar_proximo_paciente()` → EntradaFila
   - Marca o primeiro paciente pendente como atendido e o retorna.
   - Lança RuntimeError se a fila estiver vazia.

Restrições de Clean Code:
- Sem números mágicos — use constantes nomeadas.
- Sem mistura de idiomas nos nomes.
- Cada função tem uma única responsabilidade.
- Erros tratados com exceções, não com códigos de retorno.

Linguagem: Python 3.10+. Sem frameworks externos.
```

---

### 3. Receba o código gerado

Aguarde a resposta. Copie o código gerado para um arquivo temporário (ex.: `minha_saida.py`) e rode localmente:

```bash
python3 minha_saida.py
```

Se o código não tiver um bloco `if __name__ == "__main__":`, adicione uma chamada manual para ver o comportamento.

---

### 4. Aplique o checklist de revisão de código

Leia o código gerado e responda cada item abaixo, marcando ✓ (atendido) ou ✗ (violado). Estes critérios são a contraparte de revisão de código das perguntas de *prompting* da seção 4 do README — lá você verifica o prompt; aqui, a saída:

| # | Pergunta                                                                 | ✓ / ✗ |
|---|--------------------------------------------------------------------------|-------|
| 1 | Os nomes de funções e variáveis revelam intenção sem precisar de comentário? | |
| 2 | Todos os identificadores estão em português (sem mistura de idiomas)?    | |
| 3 | Cada função tem uma única responsabilidade?                              | |
| 4 | Há números mágicos no código? (constantes devem ter nome)                | |
| 5 | Erros são tratados com exceções e mensagens descritivas?                 | |
| 6 | Você consegue entender o que o código faz sem executá-lo?                | |

---

### 5. Anote suas observações

Para cada critério marcado com ✗, escreva:
- O trecho problemático (copie o identificador ou linha).
- Por que viola o princípio.
- Como você o corrigiria.

Exemplo:
> `ts` viola nomes descritivos — abreviação ambígua. Corrigiria para `registrado_em`.

---

### 6. Compare com o gabarito

Abra `gabarito.py` e `gabarito_revisao.md` e compare:
- Quantos problemas você encontrou que o gabarito também lista?
- Encontrou algum problema que o gabarito não menciona? (Isso é ótimo — anote.)
- O código gerado pela IA ficou mais próximo do gabarito ou do exercício?

---

## Aviso — Fallback sem IA

Se você não tiver acesso a um assistente de IA no momento, use diretamente o arquivo `exercicio.py` / `exercicio.ts` como se fosse a saída da IA. O objetivo do exercício é a **revisão crítica**, não a geração em si. O `exercicio.*` foi construído para ter os mesmos tipos de problemas que a IA produziria.

---

## Reflexão final

> O papel do desenvolvedor sênior muda com a IA: ele passa a ser o revisor permanente de um júnior incansável. Os princípios de Clean Code continuam sendo o critério de qualidade — agora aplicados à velocidade da máquina.

Discuta com o grupo: qual foi o critério que a IA teve mais dificuldade de atender? Por quê?
