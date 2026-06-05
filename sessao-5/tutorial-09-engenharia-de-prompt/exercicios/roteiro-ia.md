# Roteiro Hands-on — Engenharia de Prompt para Código Limpo

> Duração estimada: 20–30 minutos  
> Pré-requisito: acesso a um assistente de IA (ChatGPT, Claude, Gemini, Copilot ou similar)

---

## Objetivo

Montar um template de prompt reutilizável e aplicá-lo para gerar a função de cupom de desconto — comparando o resultado com a saída do prompt fraco do exercício.

---

## Passo a Passo

### 1. Leia o exercício e anote os problemas

Abra `exercicio.py` (ou `exercicio.ts`) e rode localmente:

```bash
python3 sessao-5/tutorial-09-engenharia-de-prompt/exercicios/exercicio.py
```

Leia o código com cuidado. Antes de continuar, liste pelo menos **4 problemas** que você identificou. Use as categorias do Tutorial 09:

- Nomes sem significado ou em inglês?
- Números mágicos?
- Funções com mais de uma responsabilidade?
- Falha silenciosa onde deveria haver exceção?
- Estrutura de dados frágil?

---

### 2. Monte o seu template de prompt

Copie o template abaixo e preencha os placeholders com base no domínio de cupons:

```
## Contexto
[Descreva o domínio. Ex.: módulo de cupons de desconto de um sistema de e-commerce.]

## Domínio
[Liste os termos que a IA deve usar. Ex.: use 'valorCompra', não 'val' ou 'price'.]
Idioma dos identificadores: português brasileiro — sem mistura de idiomas.

## Restrições
- [O que a IA NÃO deve fazer. Ex.: sem bibliotecas externas.]
- Sem números mágicos — extraia constantes nomeadas.
- Cada função com uma única responsabilidade.
- Erros tratados com exceções e mensagens descritivas.

## Exemplo do padrão desejado (few-shot)
[Cole um trecho do código do gabarito ou do preco_revisado.py como referência de estilo.]

## Formato de saída
[Especifique o contrato. Ex.: retorna float arredondado em 2 casas decimais;
lança ValueError se o cupom não existir.]

Linguagem: Python 3.10+. Sem frameworks externos.
```

> Dica: use o `gabarito_revisao.md` como referência para o prompt estruturado sugerido — mas tente construir o seu antes de abrir o gabarito.

---

### 3. Envie o prompt fraco primeiro

Para comparar os resultados, comece com o prompt fraco:

```
cria um módulo de cupom de desconto pra loja
```

Copie a resposta da IA para um arquivo temporário (`minha_saida_fraca.py`) e rode. Anote quantos dos problemas que você listou no Passo 1 a IA reproduziu.

---

### 4. Envie o seu prompt estruturado

Agora envie o template que você montou no Passo 2. Copie o código gerado para outro arquivo (`minha_saida_forte.py`) e rode:

```bash
python3 minha_saida_forte.py
```

---

### 5. Compare os dois resultados

Responda para cada critério abaixo, marcando ✓ (atendido) ou ✗ (violado), para **cada versão**:

| # | Critério                                                       | Prompt fraco | Prompt estruturado |
|---|----------------------------------------------------------------|--------------|--------------------|
| 1 | Todos os identificadores em português (sem mistura)?           |              |                    |
| 2 | Nomes revelam intenção sem precisar de comentário?             |              |                    |
| 3 | Cada função tem uma única responsabilidade?                    |              |                    |
| 4 | Sem números mágicos (todos em constantes nomeadas)?            |              |                    |
| 5 | Erros tratados com exceções e mensagens descritivas?           |              |                    |
| 6 | Estrutura de dados tipada (dataclass/interface), não dict/any? |              |                    |

---

### 6. Itere o prompt

Para cada critério marcado com ✗ na coluna "Prompt estruturado", adicione uma instrução explícita ao prompt e reenvie. Anote a instrução que você adicionou e se o resultado melhorou.

> Exemplo: se a IA gerou `type` em inglês mesmo com a instrução de idioma, adicione: "Os campos do enum devem ter nomes em português: use PERCENTUAL e VALOR_FIXO, não 'pct' e 'fixed'."

---

### 7. Compare com o gabarito

Abra `gabarito.py` e `gabarito_revisao.md`:

- Quantos dos problemas que você listou no Passo 1 o gabarito também menciona?
- O código gerado pela IA (prompt forte) ficou mais próximo do gabarito ou do exercício?
- Qual foi o critério que a IA teve mais dificuldade em atender, mesmo com o prompt forte?

---

## Aviso — Fallback sem IA

Se você não tiver acesso a um assistente de IA no momento, use diretamente `exercicio.py` / `exercicio.ts` como se fosse a saída do prompt fraco. O objetivo é a **revisão crítica e a reescrita do prompt**, não a geração em si. O template do Passo 2 pode ser preenchido mesmo sem enviar para uma IA — compare-o mentalmente com o prompt fraco e anote o que muda.

---

## Reflexão final

> Um prompt estruturado é uma especificação informal de Clean Code. A qualidade do prompt determina o ponto de partida — mas não elimina a revisão. O papel do desenvolvedor sênior é escrever especificações claras e revisar o resultado com o mesmo rigor que aplicaria ao código de um colega.

Discuta com o grupo: qual elemento do template (contexto, domínio, restrições, exemplo, formato) teve maior impacto na qualidade do código gerado? Por quê?
