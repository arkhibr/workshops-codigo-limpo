# Tutorial 04 — Formatação

> **Sessão 2 · Bloco 1 · 20 min de teoria + 10 min de exercício**
> Referência: *Clean Code*, Capítulo 5 — Formatting

---

## 1. Contexto e Motivação

Formatação é comunicação. Quando você abre um arquivo e o código está espremido, sem espaços, com imports embaralhados e linhas quilométricas, o seu cérebro gasta energia processando a estrutura antes mesmo de começar a processar a lógica. Esse custo se repete toda vez que alguém lê o arquivo.

Robert Martin classifica a formatação em dois eixos: **vertical** (como o código se organiza de cima para baixo) e **horizontal** (como cada linha está organizada). Ambos seguem uma única ideia: **o código deve parecer escrito por uma só pessoa**, mesmo sendo escrito por dezenas.

---

## 2. Conceito Central

### Formatação Vertical

| Princípio | Descrição |
|---|---|
| **Conceitos relacionados ficam juntos** | Variáveis declaradas perto de onde são usadas |
| **Conceitos não relacionados ficam separados** | Linha em branco entre grupos lógicos distintos |
| **Dependências ficam próximas** | Funções que chamam outras ficam logo acima ou abaixo |
| **Ordem de leitura natural** | Funções públicas no topo; funções privadas abaixo |

### Formatação Horizontal

| Princípio | Descrição |
|---|---|
| **Espaço ao redor de operadores** | `x = a + b`, não `x=a+b` |
| **Sem espaço entre função e parêntese** | `calcular(x)`, não `calcular (x)` |
| **Comprimento máximo de linha** | 88 chars (Python/black), 80 chars (PSR-12 PHP) |
| **Alinhamento consistente** | Atribuições em bloco alinhadas pela coluna do `=` |

---

## 3. O Problema na Prática

```python
# ❌ Formatação ruim: sem espaços, linhas longas, imports desorganizados
import os
import json
from datetime import datetime
import sys

LIMITE_ITENS=100
DESCONTO_PADRAO=0.05

class GerenciadorDeEstoque:
    def __init__(self,nome_loja,capacidade_maxima):
        self.nome_loja=nome_loja
        self.capacidade_maxima=capacidade_maxima
        self._produtos={}
    def adicionar_produto(self,codigo,nome,preco,quantidade,categoria="geral",fornecedor=None,data_validade=None,peso_kg=0.0,ativo=True):
        if codigo in self._produtos:
            raise ValueError(f"Produto {codigo} já existe no estoque")
        self._produtos[codigo]={"codigo":codigo,"nome":nome,"preco":preco,"quantidade":quantidade}
    def calcular_valor_total_estoque(self,apenas_ativos=True,aplicar_desconto=False,percentual_desconto=DESCONTO_PADRAO,incluir_impostos=False,aliquota_imposto=0.12):
        total=0.0
        for codigo,produto in self._produtos.items():
            if apenas_ativos and not produto["ativo"]:continue
            valor_item=produto["preco"]*produto["quantidade"]
            if aplicar_desconto:valor_item=valor_item*(1-percentual_desconto)
            total+=valor_item
        return round(total,2)
```

> Arquivo completo: [`exemplos/formatacao_ruim.py`](exemplos/formatacao_ruim.py)

---

## 4. A Solução

```python
# ✅ Formatação correta: imports ordenados, constantes no topo, espaços, linhas quebradas

# ── Stdlib ──────────────────────────────────────────────────────
import json
import os
import sys
from datetime import datetime
from typing import Optional

# ── Constantes ──────────────────────────────────────────────────

DESCONTO_PADRAO = 0.05
ALIQUOTA_IMPOSTO_PADRAO = 0.12

class GerenciadorDeEstoque:

    def __init__(self, nome_loja: str, capacidade_maxima: int) -> None:
        self.nome_loja = nome_loja
        self.capacidade_maxima = capacidade_maxima
        self._produtos: dict = {}

    def adicionar_produto(
        self,
        codigo: str,
        nome: str,
        preco: float,
        quantidade: int,
        categoria: str = "geral",
    ) -> None:
        self._validar_produto_novo(codigo, preco, quantidade)
        self._produtos[codigo] = {
            "codigo": codigo, "nome": nome,
            "preco": preco, "quantidade": quantidade,
        }

    def calcular_valor_total_estoque(
        self,
        apenas_ativos: bool = True,
        aplicar_desconto: bool = False,
        percentual_desconto: float = DESCONTO_PADRAO,
    ) -> float:
        total = 0.0
        for produto in self._produtos.values():
            if apenas_ativos and not produto["ativo"]:
                continue
            valor_item = produto["preco"] * produto["quantidade"]
            if aplicar_desconto:
                valor_item *= 1 - percentual_desconto
            total += valor_item
        return round(total, 2)

    # ── Privados abaixo dos públicos ────────────────────────────

    def _validar_produto_novo(self, codigo, preco, quantidade):
        ...
```

> Arquivo completo: [`exemplos/formatacao_boa.py`](exemplos/formatacao_boa.py)

---

## 5. Equivalentes em Outras Linguagens

### PHP (PSR-12)

```php
// ❌ Ruim: sem espaços, chaves na mesma linha da classe, imports emendados
use App\Models\Produto;use App\Services\EstoqueService;
class GerenciadorDeEstoque_Ruim {
    public function adicionarProduto($codigo,$nome,$preco,$quantidade){
        if($codigo===null){throw new \InvalidArgumentException("...");}
        $this->produtos[$codigo]=["codigo"=>$codigo,"nome"=>$nome];
    }
}

// ✅ Bom: PSR-12 — chave na própria linha da classe, 4 espaços, um import por linha
use App\Models\Produto;
use App\Services\EstoqueService;

class GerenciadorDeEstoque
{
    public function adicionarProduto(
        string $codigo,
        string $nome,
        float $preco,
        int $quantidade,
    ): void {
        if ($codigo === null) {
            throw new \InvalidArgumentException('Código é obrigatório.');
        }
        $this->produtos[$codigo] = [
            'codigo' => $codigo,
            'nome'   => $nome,
        ];
    }
}
```

Ferramentas: `phpcs --standard=PSR12` para verificar; `php-cs-fixer fix` para corrigir automaticamente.

### TypeScript (ESLint + Prettier)

```typescript
// ❌ Ruim
import {calcularDesconto} from './descontos';import {Logger} from './logger';
class GerenciadorEstoque_Ruim {
  adicionarProduto(id:string,nm:string,pr:number,qt:number):void{
    if(id in this.produtos)throw new Error(`${id} já existe`);
    this.produtos[id]={id,nm,pr,qt};
  }
}

// ✅ Bom — Prettier e ESLint
import { calcularDesconto } from "./descontos";
import { Logger } from "./logger";

class GerenciadorDeEstoque {
  adicionarProduto(
    codigo: string,
    nome: string,
    preco: number,
    quantidade: number,
  ): void {
    if (codigo in this.produtos) {
      throw new Error(`Produto ${codigo} já existe`);
    }
    this.produtos[codigo] = { codigo, nome, preco, quantidade };
  }
}
```

Ferramentas: `prettier --write` para formatar; `eslint --fix` para regras semânticas.

### ADVPL/TLPP

```advpl
// ❌ Ruim: sem espaços, tudo comprimido
Function Calc_Ruim(aE,lD,lI)
Local nT:=0
Local nI:=0
For nI:=1 To Len(aE)
nT:=nT+(aE[nI]["preco"]*aE[nI]["qtd"])
If lD;nT:=nT*0.95;EndIf
Next nI
Return Round(nT,2)

// ✅ Bom: 4 espaços, alinhamento, um comando por linha
Function CalcularTotalEstoque( aEstoque, lDesconto, lImposto )
    Local nTotal     := 0
    Local nValorItem := 0
    Local nIndice    := 0

    For nIndice := 1 To Len( aEstoque )
        nValorItem := aEstoque[nIndice]["preco"] * aEstoque[nIndice]["qtd"]

        If lDesconto
            nValorItem := nValorItem * ( 1 - DESCONTO_PADRAO )
        EndIf

        nTotal := nTotal + nValorItem
    Next nIndice

Return Round( nTotal, 2 )
```

> Arquivos completos: [`exemplos/equivalente.php`](exemplos/equivalente.php) · [`exemplos/equivalente.ts`](exemplos/equivalente.ts) · [`exemplos/equivalente.tlpp`](exemplos/equivalente.tlpp)

---

## 6. Regras de Ouro

- **Limite de linha** — 88 chars para Python (black), 80 chars para PHP (PSR-12); editores modernos mostram a régua
- **Imports ordenados** — stdlib → terceiros → locais; dentro de cada grupo, em ordem alfabética
- **Constantes no topo** — nunca intercaladas com lógica; nomeadas em `SCREAMING_SNAKE_CASE`
- **Métodos públicos antes dos privados** — o leitor lê a interface pública primeiro, os detalhes depois
- **Uma linha em branco entre métodos, duas entre classes** — a formatação vertical comunica agrupamento

---

## 7. Exercício

**Tarefa:** Formate a classe `ProcessadorDePagamentos` do arquivo de exercício. Não altere nenhuma linha de lógica — apenas reorganize imports, adicione espaços, quebre linhas longas e separe métodos.

```bash
# Rode antes para ver o output esperado (a lógica funciona mesmo mal formatada):
python exercicios/exercicio.py

# Depois de formatar, o output deve ser idêntico:
python exercicios/gabarito.py

# Opcional: verifique com flake8
pip install flake8
flake8 exercicios/gabarito.py --max-line-length 88
```

> Arquivo: [`exercicios/exercicio.py`](exercicios/exercicio.py)
> Gabarito: [`exercicios/gabarito.py`](exercicios/gabarito.py)

---

## 8. Para se Aprofundar

- **Clean Code**, Robert C. Martin — Capítulo 5: *Formatting* (p. 75–92)
- **PEP 8** — Guia oficial de estilo Python: [peps.python.org/pep-0008](https://peps.python.org/pep-0008/)
- **PSR-12** — Extended Coding Style (PHP): [php-fig.org/psr/psr-12](https://www.php-fig.org/psr/psr-12/)
- Ferramenta Python: [`black`](https://black.readthedocs.io/) — formatador automático sem configuração
- Ferramenta Python: [`flake8`](https://flake8.pycqa.org/) — linter que verifica PEP 8
- Ferramenta TS/JS: [`prettier`](https://prettier.io/) — formatador automático para TS, JS, JSON, CSS
- Ferramenta PHP: [`php-cs-fixer`](https://github.com/PHP-CS-Fixer/PHP-CS-Fixer) — aplica PSR-12 automaticamente

---

> **Próximo tutorial:** [Tutorial 05 — Code Review Simulado](../tutorial-05-code-review/README.md)
