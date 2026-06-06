# Roteiro Hands-on — Segurança em Código Gerado por IA

> Duração estimada: 25–35 minutos  
> Pré-requisito: acesso a um assistente de IA (ChatGPT, Claude, Gemini, Copilot ou similar)

---

## Objetivo

Aplicar o checklist de segurança do tutorial à saída real de um assistente de IA para um endpoint de busca — e endurecer o código resultante antes de aceitá-lo como base.

---

## Passo a Passo

### 1. Abra seu assistente de IA

Use o assistente de sua preferência. Não há diferença de procedimento entre eles para este exercício.

---

### 2. Cole o prompt funcional puro (ponto de partida inseguro)

Copie e envie o prompt abaixo na íntegra para ver o que a IA produz sem restrições de segurança:

```
Cria uma função Python que recebe o nome de um cliente e retorna os pedidos
desse cliente consultando um banco de dados.
Use credenciais de banco de dados e chave de API no código.
```

Aguarde a resposta. Não corrija ainda — você vai analisar o código gerado.

---

### 3. Aplique o checklist de segurança na saída recebida

Leia o código gerado e responda cada item abaixo, marcando ✓ (seguro) ou ✗ (brecha):

| # | Pergunta | ✓ / ✗ | Trecho problemático |
|---|----------|-------|---------------------|
| 1 | Há segredos, tokens ou senhas hardcoded no código? | | |
| 2 | Entradas do usuário são concatenadas em strings de query SQL, shell ou template? | | |
| 3 | A entrada é validada (formato, tamanho, tipo) antes de ser usada? | | |
| 4 | O código usa permissões mínimas (leitura quando só precisa ler)? | | |
| 5 | Dados sensíveis (nome, email, valores) aparecem em logs ou mensagens de erro? | | |
| 6 | As versões de dependências sugeridas são recentes e sem CVEs conhecidos? | | |

Para cada ✗, anote:
- O trecho exato do código.
- Por que é uma brecha.
- Como você corrigiria.

---

### 4. Reenvie com o prompt de segurança

Agora envie o prompt abaixo para o mesmo assistente — na mesma conversa ou em uma nova:

```
Contexto: sistema de gestão de pedidos de e-commerce.
Todos os identificadores devem estar em português brasileiro — sem mistura de idiomas.

Cria uma função que busca pedidos de um cliente pelo nome, com os seguintes
requisitos de segurança obrigatórios:

Segurança:
- Não use segredos, credenciais ou chaves de API hardcoded no código.
  Leia de variáveis de ambiente (ou de um dict de configuração nomeado, para demonstração).
- Parametrize a busca — nunca concatene o nome do cliente em strings de query SQL.
- Valide a entrada: o nome deve conter apenas letras e espaços, entre 2 e 80 caracteres.
  Rejeite com ValueError e mensagem descritiva se inválido.
- Sem números mágicos — use constantes nomeadas para limites de validação.

Clean Code:
- Identificadores em português brasileiro.
- Cada função tem uma única responsabilidade.
- Mensagens de erro descritivas com o valor recebido.

Linguagem: Python 3.10+. Sem frameworks externos.
Simule o banco de dados com uma lista de dicts em memória.
```

---

### 5. Compare as duas saídas

Execute as duas versões localmente e preencha a tabela:

| Critério | Saída do prompt fraco | Saída do prompt forte |
|----------|-----------------------|-----------------------|
| Credencial hardcoded? | | |
| Concatenação na query? | | |
| Entrada validada? | | |
| Identificadores em PT? | | |
| Responsabilidade única? | | |

**Perguntas para reflexão:**
- O prompt forte eliminou todas as brechas? Ou ainda havia alguma para corrigir na revisão?
- Qual brecha a IA teve mais dificuldade de evitar, mesmo com o prompt forte?
- O código do prompt forte ficou mais próximo do `gabarito.py` ou ainda tinha diferenças?

---

### 6. Compare com o gabarito

```bash
# Veja o gabarito comentado:
python3 sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/gabarito.py

# Leia a revisão explicada:
# sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/gabarito_revisao.md
```

- Quantas brechas do gabarito_revisao você identificou na etapa 3?
- O código do prompt forte ainda precisava de ajustes em relação ao gabarito?
- Você encontrou alguma brecha que o gabarito não menciona? (Anote — é uma contribuição.)

---

## Aviso — Fallback sem IA

Se você não tiver acesso a um assistente de IA no momento, use os arquivos do tutorial diretamente:

```bash
# Exercício (simula a saída da IA com prompt fraco):
python3 sessao-6/tutorial-13-seguranca-codigo-ia/exercicios/exercicio.py

# Exemplos do tutorial (prompt fraco vs. prompt forte):
python3 sessao-6/tutorial-13-seguranca-codigo-ia/exemplos/consulta_gerado.py
python3 sessao-6/tutorial-13-seguranca-codigo-ia/exemplos/consulta_revisado.py
```

Aplique o checklist da etapa 3 ao `exercicio.py` / `consulta_gerado.py` como se fossem saídas da IA. O objetivo do exercício é a **revisão crítica com olhar de segurança**, não a geração em si.

---

## Reflexão final

> A IA gera código funcional — mas "funcional" não é "seguro". O papel do desenvolvedor sênior inclui agora auditar a saída da IA com um checklist de segurança antes de qualquer commit. Um prompt com requisitos de segurança explícitos reduz o trabalho de revisão, mas não o elimina.

Discuta com o grupo: qual das três brechas (segredo hardcoded, concatenação de string, ausência de validação) é mais fácil de passar despercebida em uma revisão de código rápida? Por quê?
