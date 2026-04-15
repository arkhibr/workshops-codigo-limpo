<?php
/**
 * TUTORIAL 07 — Código Legado em PHP
 * Conceito: Seams (Costuras) via Injeção de Dependência
 *
 * Um "seam" é um ponto onde você pode substituir um comportamento
 * sem editar o código que o usa. A técnica mais simples: injeção
 * de dependência em vez de instanciação direta.
 */

// ==========================================================================
// ANTES — classe legada impossível de testar em isolamento
// O problema: new Mailer() e new FaturaRepository() dentro da classe.
// Para testar, você precisaria de um servidor de e-mail e um banco de dados.
// Não há "seam" — não há ponto onde você possa substituir os colaboradores.
// ==========================================================================

class FaturaServiceLegado
{
    public function emitir(array $dados): array
    {
        // Dependências criadas internamente — sem seam, sem testabilidade
        $repo = new FaturaRepository();      // acessa banco de dados real
        $mailer = new Mailer();              // envia e-mail real

        $fatura = [
            'id'    => uniqid('F'),
            'valor' => $dados['valor'] * 1.12,
            'cli'   => $dados['cliente_id'],
        ];

        $repo->salvar($fatura);
        $mailer->enviar($dados['email'], "Fatura {$fatura['id']} emitida.");

        return $fatura;
    }
}

// Para "testar" a classe acima você precisaria:
// - Um banco de dados real configurado
// - Um servidor SMTP real
// - Aceitar que o teste vai enviar e-mails de verdade
// Resultado: ninguém escreve o teste. O código cresce sem cobertura.


// ==========================================================================
// DEPOIS — introduzindo seams via injeção de dependência
// Nenhuma lógica de negócio foi alterada. Apenas a forma como os
// colaboradores chegam à classe foi modificada.
// ==========================================================================

interface RepositorioFaturaInterface
{
    public function salvar(array $fatura): void;
}

interface MailerInterface
{
    public function enviar(string $destinatario, string $mensagem): void;
}

class FaturaService
{
    public function __construct(
        private RepositorioFaturaInterface $repositorio,
        private MailerInterface $mailer
    ) {}

    public function emitir(array $dados): array
    {
        $fatura = [
            'id'    => uniqid('F'),
            'valor' => $dados['valor'] * 1.12,
            'cli'   => $dados['cliente_id'],
        ];

        // Mesma lógica — mas agora os colaboradores são injetados (seams)
        $this->repositorio->salvar($fatura);
        $this->mailer->enviar($dados['email'], "Fatura {$fatura['id']} emitida.");

        return $fatura;
    }
}


// ==========================================================================
// Em produção: implementações reais
// ==========================================================================

class FaturaRepository implements RepositorioFaturaInterface
{
    public function salvar(array $fatura): void
    {
        // INSERT INTO faturas ... (banco de dados real)
        echo "[DB] Fatura {$fatura['id']} persistida.\n";
    }
}

class Mailer implements MailerInterface
{
    public function enviar(string $destinatario, string $mensagem): void
    {
        // smtp_send(...) (servidor real)
        echo "[EMAIL] Para: {$destinatario} | {$mensagem}\n";
    }
}


// ==========================================================================
// Em testes: implementações falsas (test doubles) — sem banco, sem SMTP
// ==========================================================================

class FaturaRepositoryFake implements RepositorioFaturaInterface
{
    public array $salvas = [];

    public function salvar(array $fatura): void
    {
        $this->salvas[] = $fatura;  // apenas armazena em memória
    }
}

class MailerFake implements MailerInterface
{
    public array $enviados = [];

    public function enviar(string $destinatario, string $mensagem): void
    {
        $this->enviados[] = ['para' => $destinatario, 'msg' => $mensagem];
    }
}


// ==========================================================================
// Demonstração
// ==========================================================================

echo "=== Produção ===\n";
$serviceReal = new FaturaService(new FaturaRepository(), new Mailer());
$serviceReal->emitir(['valor' => 1000, 'cliente_id' => 'C001', 'email' => 'cliente@empresa.com']);

echo "\n=== Teste (sem banco, sem SMTP) ===\n";
$repoFake   = new FaturaRepositoryFake();
$mailerFake = new MailerFake();
$service    = new FaturaService($repoFake, $mailerFake);

$fatura = $service->emitir(['valor' => 500, 'cliente_id' => 'C002', 'email' => 'joao@email.com']);

// Asserções que funcionam sem infraestrutura
assert(count($repoFake->salvas) === 1,   "Fatura deve ter sido persistida");
assert($repoFake->salvas[0]['valor'] === 560.0, "Valor com imposto deve ser 560");
assert(count($mailerFake->enviados) === 1, "E-mail deve ter sido enviado");

echo "Fatura criada: {$fatura['id']} | Valor: R$ {$fatura['valor']}\n";
echo "Repositório fake contém " . count($repoFake->salvas) . " fatura(s).\n";
echo "Mailer fake registrou " . count($mailerFake->enviados) . " envio(s).\n";
echo "Todos os asserts passaram.\n";
