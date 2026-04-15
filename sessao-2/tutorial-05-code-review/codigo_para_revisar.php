<?php
/**
 * sistema_pedidos.php — Sistema de pedidos de uma lanchonete
 * Execute: php codigo_para_revisar.php
 */

define('DC', 0.1);
define('DC2', 0.15);
define('LM', 500.0);

class Lanchonete
{
    public $n;
    public $lm;
    public $p;
    public $pd;
    public $x;

    public function __construct($n, $lm = LM)
    {
        $this->n = $n;
        $this->lm = $lm;
        $this->p = [];
        $this->pd = [];
        $this->x = 0;
    }

    public function add($pid, $nm, $pr, $qt = 1)
    {
        // adiciona item
        if (isset($this->p[$pid])) {
            $this->p[$pid]['qt'] += $qt;
        } else {
            $this->p[$pid] = ['id' => $pid, 'n' => $nm, 'p' => $pr, 'qt' => $qt];
        }
        // atualiza x
        $this->x += 1;
    }

    // calcula o total
    public function calc(?string $cpd = null): float
    {
        $t = 0;
        foreach ($this->p as $k => $v) {
            $t = $t + ($v['p'] * $v['qt']); // soma preco * quantidade
        }
        // aplica desconto
        if ($cpd === 'PROMO10') {
            // desconto de 10%
            $t = $t * 0.9;
        } elseif ($cpd === 'PROMO15') {
            $t = $t - ($t * DC2);
        } elseif ($cpd === 'FIDELIDADE') {
            // TODO: implementar desconto fidelidade
        }
        return round($t, 2);
    }

    public function fechar(?string $cpd = null, ?string $end = null, string $obs = ''): array
    {
        // valida
        if (empty($this->p)) {
            return ['ok' => false, 'msg' => 'Pedido vazio'];
        }
        $t = $this->calc($cpd);
        if ($t > $this->lm) {
            return ['ok' => false, 'msg' => "Pedido acima do limite de R$ {$this->lm}"];
        }
        // TODO: salvar no banco
        // $db->save($this->p);
        // notificarCozinha($this->p);
        // enviarSms($this->n, $t);
        $num = 'PED-' . date('YmdHis');
        $r = [
            'ok' => true, 'num' => $num, 't' => $t,
            'itens' => array_values($this->p), 'end' => $end,
            'obs' => $obs, 'ts' => date('c'),
        ];
        $this->pd[] = $r;
        $this->p = [];
        return $r;
    }

    public function itens(): array
    {
        return array_values($this->p); // retorna lista de itens
    }

    public function hist(): array
    {
        // retorna historico
        return $this->pd;
    }

    private function _log(string $msg): void
    {
        // 10/01/2024 - João adicionou este log
        // 15/02/2024 - Maria mudou o formato
        // 03/03/2024 - Pedro removeu o arquivo de log
        echo "[{$this->n}] {$msg}" . PHP_EOL;
    }
}

$l = new Lanchonete('Lanchonete do Bairro');
$l->add('X001', 'X-Burguer', 18.50, 2);
$l->add('F001', 'Fritas Grandes', 8.90);
$l->add('R001', 'Refrigerante', 5.50, 3);
$l->add('X001', 'X-Burguer', 18.50, 1); // adiciona mais 1 X-Burguer
echo 'Itens do pedido: ' . json_encode($l->itens()) . PHP_EOL;
echo 'Total sem cupom: ' . $l->calc() . PHP_EOL;
echo 'Total com PROMO10: ' . $l->calc('PROMO10') . PHP_EOL;
echo 'Total com PROMO15: ' . $l->calc('PROMO15') . PHP_EOL;
$ped = $l->fechar('PROMO10', 'Rua das Flores, 42', 'Sem cebola no burguer');
echo PHP_EOL . 'Pedido fechado: ' . json_encode($ped) . PHP_EOL;
echo 'Histórico: ' . json_encode($l->hist()) . PHP_EOL;
