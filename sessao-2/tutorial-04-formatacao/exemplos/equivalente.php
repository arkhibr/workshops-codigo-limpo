<?php
/**
 * EQUIVALENTE PHP — Formatação (PSR-12)
 * Referência: Clean Code, Cap. 5
 *
 * PSR-12 é o padrão de formatação da comunidade PHP moderna.
 * Ferramentas: phpcs (verificar) e php-cs-fixer (corrigir automaticamente).
 */

// ════════════════════════════════════════════════════════════════
// ANTES — PSR-12 violada
// ════════════════════════════════════════════════════════════════

// ❌ Imports desorganizados, sem espaçamento, chaves na mesma linha com espaço errado
use App\Models\Produto;use App\Services\EstoqueService;use Carbon\Carbon;

class GerenciadorDeEstoque_Ruim {
    private $produtos=[];
    private $log=[];
    public function adicionarProduto($codigo,$nome,$preco,$quantidade,$categoria="geral"){
        if($codigo===null||$nome===null){throw new \InvalidArgumentException("Código e nome são obrigatórios");}
        if($preco<=0){throw new \InvalidArgumentException("Preço deve ser positivo");}
        $this->produtos[$codigo]=["codigo"=>$codigo,"nome"=>$nome,"preco"=>$preco,"quantidade"=>$quantidade,"categoria"=>$categoria];
        $this->log[]="ADICIONADO: ".$codigo." - ".$nome;
    }
    public function calcularValorTotal(bool $aplicarDesconto=false,float $percentualDesconto=0.05,bool $incluirImpostos=false,float $aliquotaImposto=0.12):float{
        $total=0.0;
        foreach($this->produtos as $produto){$valorItem=$produto["preco"]*$produto["quantidade"];if($aplicarDesconto){$valorItem=$valorItem*(1-$percentualDesconto);}if($incluirImpostos){$valorItem=$valorItem*(1+$aliquotaImposto);}$total+=$valorItem;}
        return round($total,2);
    }
}


// ════════════════════════════════════════════════════════════════
// DEPOIS — PSR-12 aplicada
// ════════════════════════════════════════════════════════════════

// ✅ Imports agrupados e ordenados alfabeticamente
use App\Models\Produto;
use App\Services\EstoqueService;
use Carbon\Carbon;

// ✅ Constantes no topo, fora da classe quando são globais ao módulo
const DESCONTO_PADRAO = 0.05;
const ALIQUOTA_IMPOSTO_PADRAO = 0.12;

class GerenciadorDeEstoque
{
    private array $produtos = [];
    private array $log = [];

    // ── Operações públicas ────────────────────────────────────────────────

    public function adicionarProduto(
        string $codigo,
        string $nome,
        float $preco,
        int $quantidade,
        string $categoria = 'geral',
    ): void {
        $this->validarProdutoNovo($codigo, $preco);

        $this->produtos[$codigo] = [
            'codigo'     => $codigo,
            'nome'       => $nome,
            'preco'      => $preco,
            'quantidade' => $quantidade,
            'categoria'  => $categoria,
        ];

        $this->log[] = "ADICIONADO: {$codigo} - {$nome}";
    }

    public function calcularValorTotal(
        bool $aplicarDesconto = false,
        float $percentualDesconto = DESCONTO_PADRAO,
        bool $incluirImpostos = false,
        float $aliquotaImposto = ALIQUOTA_IMPOSTO_PADRAO,
    ): float {
        $total = 0.0;

        foreach ($this->produtos as $produto) {
            $valorItem = $produto['preco'] * $produto['quantidade'];

            if ($aplicarDesconto) {
                $valorItem *= 1 - $percentualDesconto;
            }

            if ($incluirImpostos) {
                $valorItem *= 1 + $aliquotaImposto;
            }

            $total += $valorItem;
        }

        return round($total, 2);
    }

    // ── Operações privadas ────────────────────────────────────────────────

    private function validarProdutoNovo(string $codigo, float $preco): void
    {
        if (isset($this->produtos[$codigo])) {
            throw new \InvalidArgumentException("Produto {$codigo} já existe.");
        }

        if ($preco <= 0) {
            throw new \InvalidArgumentException('Preço deve ser positivo.');
        }
    }
}
