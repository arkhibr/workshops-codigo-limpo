# Spec — Sistema de Reservas de Sala

> Versão: 1.0 — Tutorial 18 (spec-first na geração de código)

Esta spec é o contrato entre o requisito informal e o código gerado.
O modelo deve ler esta spec antes de gerar qualquer código.

---

## Objetivo

Módulo de reservas de sala para o workshop de Clean Code.
Implementar as operações de **criar reserva** e **listar reservas**.
Domínio: sala de reunião com horário de início e fim, responsável.

---

## Entidades e campos

```
Reserva:
  id:            int         — identificador sequencial, gerado automaticamente
  sala:          str         — nome da sala (ex: "Sala A", "Sala B")
  inicio:        datetime    — horário de início (data + hora)
  fim:           datetime    — horário de fim (data + hora)
  responsavel:   str         — nome do responsável pela reserva
```

---

## Regras de negócio

### R1 — Sem sobreposição de horário na mesma sala (exigência implícita crítica)

Duas reservas na mesma sala **não podem ter sobreposição de horário**.
Diz-se que duas reservas se sobrepõem quando o intervalo [início, fim] de uma
intersecta o intervalo [início, fim] da outra.

Fórmula de sobreposição:
```
sobreposição = inicio_nova < fim_existente AND fim_nova > inicio_existente
```

Reservas **adjacentes** (fim de uma = início da outra) **não se sobrepõem**.
Reservas em **salas diferentes** são independentes — sem restrição entre elas.

Se a nova reserva violar R1, levantar `ReservaSobrepostaError` com mensagem
descrevendo a sala e o horário em conflito.

### R2 — Horário de fim após o início

`fim` deve ser estritamente após `inicio`. Se `fim <= inicio`, levantar
`ValueError` com mensagem descritiva.

### R3 — Campos obrigatórios não vazios

`sala` e `responsavel` não podem ser strings vazias. Se forem, levantar
`ValueError`.

---

## Exemplos de contrato (entrada → saída esperada)

Estes exemplos são o contrato verificável. O código gerado deve produzir
exatamente estes resultados.

```
Data de referência: 2026-06-10

# Caso 1 — criação normal (OK)
criar_reserva("Sala A", 10:00, 11:00, "Ana")
→ Reserva criada com id=1

# Caso 2 — sobreposição total (ERRO)
criar_reserva("Sala A", 10:30, 11:30, "Bob")
→ ReservaSobrepostaError: "Sala A já está reservada das 10:00 às 11:00"
  (10:30 < 11:00 AND 11:30 > 10:00 → sobrepõe)

# Caso 3 — sobreposição parcial no fim (ERRO)
criar_reserva("Sala A", 09:30, 10:30, "Carlos")
→ ReservaSobrepostaError
  (09:30 < 11:00 AND 10:30 > 10:00 → sobrepõe)

# Caso 4 — adjacente após (OK — não sobrepõe)
criar_reserva("Sala A", 11:00, 12:00, "Dana")
→ Reserva criada com id=2
  (11:00 < 11:00 é FALSO → não sobrepõe)

# Caso 5 — sala diferente no mesmo horário (OK)
criar_reserva("Sala B", 10:00, 11:00, "Eva")
→ Reserva criada com id=3

# Caso 6 — fim antes do início (ERRO)
criar_reserva("Sala A", 14:00, 13:00, "Felipe")
→ ValueError: "Horário de fim deve ser após o início"
```

---

## Assinaturas-alvo

```python
# Python
class ReservaSobrepostaError(Exception): ...

@dataclass
class Reserva:
    id:           int
    sala:         str
    inicio:       datetime
    fim:          datetime
    responsavel:  str

def criar_reserva(
    sala:        str,
    inicio:      datetime,
    fim:         datetime,
    responsavel: str,
) -> Reserva: ...

def listar_reservas(sala: Optional[str] = None) -> list[Reserva]: ...
```

```typescript
// TypeScript
class ReservaSobrepostaError extends Error { ... }

interface Reserva {
  id:          number;
  sala:        string;
  inicio:      Date;
  fim:         Date;
  responsavel: string;
}

function criarReserva(sala: string, inicio: Date, fim: Date, responsavel: string): Reserva
function listarReservas(sala?: string): Reserva[]
```

---

## Restrições de implementação

- Sem dependências externas — repositório em memória (array/lista)
- Sem camadas Repository/Service separadas — módulo plano com funções livres
- `@dataclass` para a entidade `Reserva` (Python) / `interface` (TypeScript)
- `ValueError` / `Error` para entradas inválidas; `ReservaSobrepostaError` para sobreposição
- Bloco `__main__` (Python) ou chamadas no final do arquivo (TypeScript) com demo stdout
- O demo deve exercitar todos os 6 casos do contrato acima

---

## O que este módulo NÃO cobre

- Persistência em banco de dados
- Autenticação ou autorização
- Cancelamento de reservas (ver `exercicios/exercicio.py`)
- Notificações ou integrações externas
