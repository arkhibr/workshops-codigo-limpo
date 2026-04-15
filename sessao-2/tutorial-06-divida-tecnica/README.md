# Tutorial 06 — Dívida Técnica

> **Sessão 2 · Bloco 4 · 15 min de teoria + 15 min de exercício + 5 min de checklist**
> Referência: *Clean Code*, Capítulo 17 — Smells and Heuristics

---

## 1. Contexto e Motivação

Todo projeto acumula dívida técnica. A questão não é se ela vai existir, mas se você sabe reconhecê-la, nomeá-la e priorizá-la. Um time que não consegue falar sobre sua dívida técnica não consegue gerenciá-la — e eventualmente é governado por ela.

Este tutorial fecha o workshop conectando todos os tópicos anteriores: nomes ruins, funções longas, comentários desnecessários e formatação caótica são as formas mais visíveis de dívida técnica no código-fonte.

---

## 2. Conceito Central

### A Metáfora da Dívida Técnica

Ward Cunningham cunhou o termo em 1992: escrever código que funciona mas não está limpo é como tomar um empréstimo. Você entrega mais rápido hoje, mas paga juros amanhã — na forma de tempo extra para entender, modificar e testar o código.

> *"A little debt speeds development so long as it is paid back promptly with a rewrite. [...] The danger occurs when the debt is not repaid."*
> — Ward Cunningham

### A Teoria da Janela Quebrada

O Clean Code menciona no Capítulo 1 (p. 8) o conceito da Teoria da Janela Quebrada: um bairro com uma janela quebrada e não consertada rapidamente deteriora — mais janelas são quebradas, o lixo se acumula, e o estado de abandono se alastra. A mensagem implícita de uma janela quebrada é: "aqui ninguém se importa".

No código o efeito é o mesmo: um arquivo com nomes ruins, funções gigantes e sem testes convida mais código descuidado. Quem chega para modificar esse arquivo tende a "manter o padrão" — afinal, aparentemente não importa. A janela quebrada não é apenas um problema técnico; é um problema cultural que se retroalimenta.

### O Quadrante da Dívida Técnica

Martin Fowler expandiu o conceito com quatro quadrantes:

|  | **Prudente** | **Imprudente** |
|---|---|---|
| **Deliberada** | "Precisamos entregar agora e refatorar depois" | "Não temos tempo para design" |
| **Inadvertida** | "Agora sabemos como deveríamos ter feito" | "O que é arquitetura em camadas?" |

- **Deliberada + Prudente:** aceitável quando consciente e com plano de pagamento
- **Deliberada + Imprudente:** atalho irresponsável — nunca é justificável
- **Inadvertida + Prudente:** inevitável — todo projeto descobre melhores abordagens ao longo do tempo
- **Inadvertida + Imprudente:** resultado de falta de conhecimento — combate-se com capacitação (como este workshop)

### Como quantificar dívida técnica

Intuição é útil, mas métricas dão objetividade para priorizar:

- **Complexidade ciclomática** (`radon cc` em Python): mede o número de caminhos independentes numa função. Abaixo de 5 é simples; entre 5 e 10 é moderado; acima de 10 é sinal de alerta — a função provavelmente faz coisas demais e é difícil de testar completamente.
- **Cobertura de testes:** código sem teste tem custo de mudança muito mais alto. Cada linha sem cobertura é uma dívida latente — você só descobre o preço quando precisar modificar.
- **Proporção de comentários explicativos no código interno:** muitos comentários explicando "o quê" sinalizam código confuso. Se o código precisa de legenda para ser lido, o código precisa ser reescrito.

### Como priorizar o pagamento da dívida

Nem toda dívida precisa ser paga imediatamente — e tentar pagar tudo de uma vez costuma não funcionar.

- **Priorize dívidas em código que muda frequentemente:** alta frequência de mudança significa alto impacto. Se um módulo é tocado toda sprint, cada dívida nele é paga em juros toda sprint.
- **Dívidas em código estável que ninguém toca há anos podem esperar:** o risco é baixo porque a probabilidade de precisar mudar é baixa.
- **Use a Regra do Escoteiro** (Clean Code, p. 14): *"Deixe o código mais limpo do que encontrou."* Cada PR pode pagar uma pequena dívida na área que tocou — renomear uma variável obscura, extrair uma função longa, remover um TODO vencido. Sem sprint de refatoração, sem reunião de alinhamento: apenas o hábito contínuo de deixar o código um pouco melhor.

### Code Smells Mais Comuns

| Smell | Descrição |
|---|---|
| **Função longa** | Função com mais de 20 linhas geralmente faz coisas demais |
| **Classe grande** | Classe com muitas responsabilidades (viola SRP) |
| **Lista longa de parâmetros** | Mais de 3 parâmetros sugere necessidade de objeto |
| **Código duplicado** | A mesma lógica em dois lugares — mudança vira dois bugs |
| **Comentário como bengala** | Comentário que explica código confuso em vez de simplificá-lo |
| **Nomes obscuros** | Variáveis de 1-2 letras, abreviações, notação húngara |
| **Magic numbers** | `0.275`, `86400`, `3` soltos no código sem constante nomeada |
| **Dead code** | Código comentado, funções nunca chamadas, imports não usados |
| **Inveja de funcionalidades** | Método que usa mais dados de outra classe do que da própria |

---

## 3. O Problema na Prática

```python
# Dívida de nomes + função gigante + duplicação + magic numbers

def login(u, s, t="basico"):
    if not u or len(u) < 3:           # magic number: 3
        return {"ok": False, "msg": "usuario invalido"}
    if "@" not in u:
        return {"ok": False, "msg": "usuario invalido"}  # duplicação de retorno
    if not s or len(s) < 8:           # magic number: 8
        return {"ok": False, "msg": "senha fraca"}
    # ... mais 40 linhas de validação, hashing e geração de token
    tk = hashlib.md5(f"{u}{time.time()}".encode()).hexdigest()
    return {"ok": True, "tk": tk, "exp": int(time.time()) + 3600}  # magic: 3600
```

**Dívidas identificadas:**
- `u`, `s`, `t`, `tk` — nomes de uma letra sem contexto
- A função `login` valida, autentica, gera token e define expiração — 4 responsabilidades
- A validação de usuário aparece duplicada em `login` e em `renovar_token`
- `3`, `8`, `3600` são magic numbers

> Arquivo completo: [`exemplos/divida_antes.py`](exemplos/divida_antes.py)

---

## 4. A Solução

```python
# Constantes nomeadas
TAMANHO_MINIMO_USUARIO = 3
TAMANHO_MINIMO_SENHA   = 8
DURACAO_TOKEN_SEGUNDOS = 3600

# Funções pequenas com responsabilidade única
def usuario_eh_valido(email):
    return bool(email) and len(email) >= TAMANHO_MINIMO_USUARIO and "@" in email

def senha_eh_valida(senha):
    return bool(senha) and len(senha) >= TAMANHO_MINIMO_SENHA \
        and not senha.isdigit() and not senha.isupper()

def gerar_token(email):
    return hashlib.md5(f"{email}{time.time()}".encode()).hexdigest()

def calcular_expiracao(duracao_segundos=DURACAO_TOKEN_SEGUNDOS):
    return int(time.time()) + duracao_segundos

def autenticar(email, senha, tipo="basico"):
    if not usuario_eh_valido(email):
        raise ValueError("E-mail inválido")
    if not senha_eh_valida(senha):
        raise ValueError("Senha não atende os requisitos")
    return {"token": gerar_token(email), "expiracao": calcular_expiracao(), "tipo": tipo}
```

> Arquivo completo: [`exemplos/divida_depois.py`](exemplos/divida_depois.py)

---

## 5. Equivalentes em Outras Linguagens

### PHP — Dívida de duplicação

```php
// ❌ Mesma validação em dois lugares
function cadastrarUsuario($email) {
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) return false;
    // ...
}
function atualizarEmail($novoEmail) {
    if (!filter_var($novoEmail, FILTER_VALIDATE_EMAIL)) return false; // duplicado!
    // ...
}

// ✅ Extrair função
function emailEhValido(string $email): bool {
    return (bool) filter_var($email, FILTER_VALIDATE_EMAIL);
}
```

### TypeScript — Magic numbers

```typescript
// ❌ Magic numbers
const preco = valor * 1.12 * (1 - 0.05);

// ✅ Constantes nomeadas
const ALIQUOTA_ICMS    = 0.12;
const DESCONTO_FIDELIDADE = 0.05;
const preco = valor * (1 + ALIQUOTA_ICMS) * (1 - DESCONTO_FIDELIDADE);
```

### ADVPL/TLPP — Função gigante

```advpl
// ❌ Function que faz tudo: valida, processa, salva, notifica
Function ProcessarPedido( cPedido, cCliente, aItens, cEndereco )
    // 80 linhas...

// ✅ Responsabilidades separadas
Function ValidarPedido( cPedido, cCliente )
Function CalcularTotalPedido( aItens )
Function SalvarPedido( cPedido, nTotal, cEndereco )
Function NotificarCliente( cCliente, cPedido )
```

> Arquivos completos: [`exemplos/equivalente.php`](exemplos/equivalente.php) · [`exemplos/equivalente.ts`](exemplos/equivalente.ts) · [`exemplos/equivalente.tlpp`](exemplos/equivalente.tlpp)

---

## 6. Regras de Ouro

- **Dívida não paga gera juros** — cada mudança em código sujo custa mais do que custaria em código limpo
- **Nomeie a dívida antes de acumulá-la** — "estamos tomando um atalho deliberado, vamos criar um ticket"
- **Duplicação é a raiz de muitos males** — toda vez que você copia e cola, está abrindo dois lugares para o próximo bug
- **Magic numbers contam uma história incompleta** — `0.275` é o quê? `ALIQUOTA_INSS = 0.275` é autoexplicativo
- **Dead code mente** — código comentado gera dúvida: "foi removido? vai voltar? está certo?"

---

## 7. Exercício

**Tarefa (em duas partes):**

1. Leia o arquivo de exercício e **identifique pelo menos 4 dívidas técnicas**, adicionando um comentário `# DÍVIDA:` em cada uma com uma descrição do problema
2. **Implemente a versão refatorada** eliminando todas as dívidas identificadas

```bash
# Rode para entender o que o código faz:
python3 exercicios/exercicio.py

# Compare sua refatoração com o gabarito:
python3 exercicios/gabarito.py
```

> Arquivo: [`exercicios/exercicio.py`](exercicios/exercicio.py)
> Gabarito: [`exercicios/gabarito.py`](exercicios/gabarito.py)

---

## 8. Checklist de Qualidade do Time

Use esta lista no dia a dia — em code reviews, antes de um commit ou ao revisar código legado. A sigla entre colchetes indica o tutorial de origem, para que o time saiba onde aprofundar quando encontrar o problema.

**Nomes** `[N]`
- [ ] `[N]` Todas as variáveis, funções e classes têm nomes que revelam intenção?
- [ ] `[N]` Não há abreviações obscuras ou notação húngara (exceto prefixos de tipo em ADVPL/TLPP)?

**Funções** `[F]`
- [ ] `[F]` Cada função faz uma única coisa?
- [ ] `[F]` Nenhuma função tem mais de 20 linhas?
- [ ] `[F]` Nenhuma função tem flag booleana como parâmetro?

**Comentários** `[C]`
- [ ] `[C]` Os comentários explicam o *porquê*, não o *o quê*?
- [ ] `[C]` Não há código comentado sem explicação?
- [ ] `[C]` TODOs têm número de ticket e responsável?

**Formatação** `[FMT]`
- [ ] `[FMT]` O formatador automático foi executado antes do commit? (`black` / `prettier` / `php-cs-fixer`)
- [ ] `[FMT]` Imports estão organizados?

**Dívida Técnica** `[DT]`
- [ ] `[DT]` Não há magic numbers soltos — todas as constantes têm nome?
- [ ] `[DT]` Não há duplicação de lógica entre dois ou mais lugares?

> **Placeholder para o time:** substitua os itens acima pelos padrões específicos acordados após este workshop.

---

## 9. Para se Aprofundar

- **Clean Code**, Robert C. Martin — Capítulo 17: *Smells and Heuristics* (p. 285–314)
- **Refactoring**, Martin Fowler — Catálogo completo de code smells e refatorações
- **Managing Technical Debt**, Philippe Kruchten et al. — aprofundamento no quadrante de dívidas
- Ferramenta: [`radon`](https://radon.readthedocs.io/) mede complexidade ciclomática (Python)
- Ferramenta: [`sonarqube`](https://www.sonarqube.org/) detecta dívida técnica automaticamente em várias linguagens

---

> **Fim do workshop.** Parabéns por chegar até aqui!
> Volte ao [índice principal](../../README.md) para revisar os tutoriais anteriores.
