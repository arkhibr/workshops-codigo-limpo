# Prompt Original — Gerador do Módulo de Gateway de Pagamento

> Este é o prompt usado para gerar `codigo_gerado_por_ia.py` e `codigo_gerado_por_ia.ts`.
> Observe: o prompt é razoável — mas não especificou restrições de segurança, edge cases
> nem como lidar com erros do gateway. Essas omissões se traduzem diretamente nos problemas
> encontrados no código gerado.

---

## Prompt enviado à IA

```
Crie um módulo Python de integração com um gateway de pagamento fictício chamado
"Gateway Pagamentos BR". O módulo deve ter três funções principais:

1. cobrar(valor, numero_cartao, cpf_titular, parcelas, descricao) — realiza uma
   cobrança no cartão de crédito e retorna um dicionário com status e código de
   autorização.

2. estornar(codigo_autorizacao, motivo) — estorna uma cobrança já aprovada.

3. consultar_status(codigo_autorizacao) — consulta o status atual de uma transação.

O gateway tem uma API REST com base URL "https://api.gateway-pagamentos.com.br/v2"
e autenticação via Bearer token no header Authorization.

Inclua validação de CPF e trate os casos de aprovação e recusa do gateway.
Use boas práticas de código limpo, com nomes descritivos e funções com
responsabilidade única.
```

---

## O que o prompt NÃO especificou

| Omissão | Consequência no código gerado |
|---|---|
| Como obter a chave de API | IA hardcodou um valor fictício (`sk-prod-...`) |
| Sanitização de parâmetros de query | IA concatenou `descricao` diretamente na URL |
| O que "validar CPF" significa exatamente | IA gerou uma verificação superficial, mas a docstring prometeu validação completa |
| O que fazer com valores zero ou negativos | IA não incluiu nenhuma guarda para esse edge case |
| Quais métodos do cliente HTTP estão disponíveis | IA inventou `post_parcelado()` para a função de parcelamento |
| Qual o comportamento esperado quando aprovado/recusado | IA inverteu a lógica da condição |

---

## Lição

Um prompt que descreve *o que* fazer mas não descreve *as restrições* deixa a IA preencher
lacunas com defaults plausíveis — que podem ser incorretos, inseguros ou inconsistentes
com o restante da base de código.

O Tutorial 09 mostrou como escrever prompts fortes. Este tutorial mostra o que acontece
quando o prompt é apenas razoável: o código parece funcionar, mas precisa de revisão crítica
antes de ir para produção.
