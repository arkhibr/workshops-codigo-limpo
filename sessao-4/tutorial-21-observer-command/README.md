# Tutorial 21 — Observer e Command

> Referência: Gang of Four, *Design Patterns*, Cap. 5 — Behavioral Patterns

## 1. Contexto e Motivação

Dois padrões para sistemas reativos: Observer para desacoplar quem dispara de quem reage; Command para encapsular operações e habilitar undo.

## 2. Observer

**Problema:** `ProcessadorPagamento.processar()` chama `ServicoEmail`, `ServicoAuditoria`, `ServicoFraude` diretamente. Adicionar SMS exige alterar `processar()`.

**Solução:** Defina um protocolo `ObservadorPagamento`. O processador mantém uma lista de observadores e notifica todos ao confirmar. Adicionar SMS = nova classe + `registrar_observador()`.

**Quando usar:**
- Mudança de estado que precisa notificar vários consumidores independentes
- Consumidores devem poder ser adicionados/removidos sem alterar o publicador
- Desacoplamento entre produtor e consumidor de eventos

**Quando NÃO usar:**
- Apenas 1 consumidor fixo — injeção direta é mais simples
- Ordem de notificação importa e é complexa — use Event Bus com prioridade

## 3. Command

**Problema:** `estornar_pagamento()` não mantém estado anterior. Impossível desfazer.

**Solução:** Encapsule a operação em um objeto `Comando` com `executar()` e `desfazer()`. `HistoricoComandos` mantém a pilha e permite `desfazer_ultimo()`.

**Quando usar:**
- Operações que precisam de undo/redo
- Histórico de ações para auditoria ou rollback
- Operações que podem ser enfileiradas ou agendadas

**Quando NÃO usar:**
- Operação sem estado relevante para reverter (log-only)
- Sistema sem requisito de undo

## 4. Observer vs Event Bus vs Callback Direto

| Dimensão | Callback Direto | Observer | Event Bus |
|----------|-----------------|----------|-----------|
| Acoplamento | Alto | Baixo | Muito baixo |
| Descoberta | Compile-time | Registro | Dinâmica |
| Ordem garantida | Sim | Sim (lista) | Não |
| ADVPL | Codeblock | Array de codeblocks | Não nativo |

## 5. Exercício

Domínio: sistema de pagamentos.

**`exercicios/exercicio.py`** — `ProcessadorPagamento` com 3 serviços acoplados + `estornar_pagamento()` sem undo.

**Objetivo:** Refatorar para Observer + Command.

## 6. Checklist

- [ ] Identifiquei os consumidores acoplados ao processador
- [ ] Criei o protocolo/interface ObservadorPagamento
- [ ] Adicionei registrar_observador() ao processador
- [ ] Criei ComandoEstorno com executar() e desfazer()
- [ ] HistoricoComandos permite desfazer o último

## 7. Referências

- GoF, *Design Patterns*, Cap. 5 — Observer (p. 293) e Command (p. 233)
- Fowler, *Patterns of Enterprise Application Architecture* — Event Sourcing
