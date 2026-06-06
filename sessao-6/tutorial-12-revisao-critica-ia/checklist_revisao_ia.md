# Checklist de Revisão — Código Gerado por IA

> Checklist reutilizável para revisar qualquer trecho de código gerado por assistente de IA.
> Independente de linguagem, domínio ou ferramenta.

---

## 1. Correção

- [ ] A lógica central faz o que o nome/docstring diz? (ler o código, não só o comentário)
- [ ] Condicionais `if/else` têm os blocos no lado certo? Condições invertidas (`!=` onde deveria ser `==`) são erro frequente de IA.
- [ ] Laços têm os limites corretos? Verificar off-by-one em `<` vs `<=` e em índices de arrays.
- [ ] Funções de conversão (datas, moedas, codecs) usam o formato/base correto?
- [ ] Operações assíncronas são aguardadas onde necessário (`await`, callbacks)?

---

## 2. Segurança

- [ ] Há segredos, tokens ou senhas hardcoded? (buscar por strings que se parecem com chaves: `sk-`, `Bearer`, `password =`)
- [ ] Entradas do usuário são escapadas antes de serem concatenadas em URLs, SQL ou comandos shell?
- [ ] Dados sensíveis (CPF, cartão, senha) são logados ou incluídos em mensagens de erro?
- [ ] Tokens/chaves de API são lidos de variáveis de ambiente, não de constantes no código?
- [ ] O código usa algoritmos de hash seguros para senhas (`bcrypt`, `argon2`) — e não `md5`/`sha1`?

---

## 3. Edge cases

- [ ] O que acontece com valores zero, negativos ou `null`/`None`/`undefined`?
- [ ] O que acontece com strings vazias, listas vazias ou coleções com um único elemento?
- [ ] Há tratamento de timeout para chamadas de rede ou operações longas?
- [ ] O código lida com respostas parciais ou erros do serviço externo (status 4xx, 5xx)?
- [ ] Concorrência: o código é seguro se chamado simultaneamente por múltiplas threads/requisições?

---

## 4. Legibilidade e Coesão

- [ ] Os identificadores (variáveis, funções, classes) revelam intenção sem precisar de comentário?
- [ ] Comentários e docstrings descrevem o que o código *realmente* faz — não o que se esperava que ele fizesse?
- [ ] Cada função faz uma única coisa? Funções que "cobram E validam E logam" violam SRP.
- [ ] Há números mágicos soltos que deveriam ser constantes nomeadas?
- [ ] O idioma dos identificadores é consistente com o restante da base de código?

---

## 5. Dependências

- [ ] Todos os métodos e funções chamados existem na versão da lib/SDK que o projeto usa?
- [ ] Há imports de módulos que não estão instalados (`requirements.txt`, `package.json`)?
- [ ] A IA usou uma API descontinuada ou uma versão antiga de uma função?
- [ ] Dependências adicionadas são realmente necessárias, ou a funcionalidade já existe no projeto?

---

## 6. "A IA entendeu o pedido?"

- [ ] O código resolve o problema pedido — ou uma versão mais simples/diferente do problema?
- [ ] Requisitos não funcionais do prompt (idioma dos identificadores, padrão de erro, estrutura de retorno) foram respeitados?
- [ ] O código gerado é proporcional ao problema? Over-engineering (classes, abstrações, generics desnecessários) é sinal de que o prompt foi interpretado de forma mais ampla.
- [ ] Há funcionalidades extras não pedidas que aumentam a superfície de manutenção?

---

> **Como usar:** percorra cada categoria antes de aceitar o código gerado. Uma resposta "não sei" em qualquer item é sinal para investigar antes de commitar.
