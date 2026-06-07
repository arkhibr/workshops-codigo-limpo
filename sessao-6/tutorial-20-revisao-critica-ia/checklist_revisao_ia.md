# Checklist de Revisão Crítica — Código Gerado por IA

> Checklist reutilizável para revisar qualquer saída de modelo de fronteira.
> Aplique a cada geração antes de integrar ao codebase.

---

## 1. Correção

- [ ] A lógica central está correta? Trace manualmente ao menos um caso feliz e um caso de fronteira.
- [ ] Há operadores de comparação que poderiam ser `<` vs `<=`, `>` vs `>=`? Verifique loops e condições de guarda.
- [ ] Arredondamentos monetários usam a precisão correta? (ex.: `round(valor, 2)` vs truncamento)
- [ ] O código produz o resultado certo para entradas extremas (zero, valor máximo, lista vazia)?
- [ ] Contagens, índices e ranges usam os limites corretos (off-by-one)?

---

## 2. Segurança

- [ ] Comparações de tokens, assinaturas ou senhas usam operações constant-time? (`hmac.compare_digest`, `crypto.timingSafeEqual`)
- [ ] Dados sensíveis (CPF, cartão, tokens) são logados ou incluídos em mensagens de erro?
- [ ] Há concatenação de strings para montar queries, URLs ou comandos de shell?
- [ ] Segredos estão em variáveis de ambiente, não hardcoded?
- [ ] Entradas externas (webhooks, parâmetros de API) são validadas antes de serem processadas?

> Ver Tutorial 14 para uma análise completa de segurança em código gerado por IA.

---

## 3. Edge Cases

- [ ] Valores zero, negativos ou nulos são tratados explicitamente?
- [ ] Listas e coleções vazias produzem o resultado correto (sem `IndexError`/`TypeError`)?
- [ ] Timeouts de rede e falhas parciais são tratados?
- [ ] O código funciona no limite superior do domínio? (ex.: 12 parcelas, valor máximo permitido)
- [ ] Chamadas externas que podem retornar `null`/`None`/`undefined` são guardadas?

---

## 4. Legibilidade e Coesão

- [ ] Cada função tem uma responsabilidade? Funções longas que fazem validação + cálculo + I/O precisam ser divididas.
- [ ] Docstrings e comentários descrevem o que o código **realmente** faz? Leia o corpo e compare com a documentação.
- [ ] Há abstrações que o pedido não pedia? (factories, strategies, camadas de cache) Remova o que não agrega valor agora.
- [ ] Os nomes de variáveis, funções e classes são expressivos e no idioma do projeto?
- [ ] Constantes estão nomeadas? Não há magic numbers soltos?

---

## 5. Dependências e Alucinação

- [ ] Todas as funções, métodos e classes referenciadas existem na versão da biblioteca usada?
- [ ] Os imports compilam sem erro? (`pip install` / `npm install` confirma os pacotes)
- [ ] Comportamentos de API foram verificados na documentação oficial, não apenas inferidos do nome?
- [ ] O código não chama endpoints ou métodos que parecem plausíveis mas não existem?
- [ ] Versões de bibliotecas estão fixadas? Comportamento pode mudar entre versões.

---

## 6. A IA entendeu o pedido?

- [ ] O código implementa exatamente o que foi pedido — nem mais, nem menos?
- [ ] Regras de negócio críticas (fornecidas no prompt) estão presentes e corretas?
- [ ] A estrutura gerada (classes, módulos, camadas) corresponde ao pedido ou foi inventada pelo modelo?
- [ ] O modelo adicionou features não solicitadas que introduzem complexidade?
- [ ] O código gerado é coerente com as convenções do projeto (nomes, estrutura, padrões)?

---

> **Dica de processo:** aplique este checklist em pares — uma pessoa lê o código em voz alta enquanto
> a outra vai marcando os itens. Alucinações e edge cases são mais fáceis de detectar quando
> alguém está descrevendo o código para outra pessoa.
