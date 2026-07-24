# Tutorial 31 — E2E Web com Maestro

> Referência: Martin Fowler, "TestPyramid" (martinfowler.com); Maestro — documentação oficial (maestro.mobile.dev)

## 1. Contexto e Motivação

A Sessão 7 apresentou a pirâmide de testes e situou o teste end-to-end no topo: poucos, lentos, caros, mas insubstituíveis para uma pergunta que nenhum teste de unidade ou de integração consegue responder sozinho — o sistema funciona da forma como a pessoa que usa o produto de fato o usa?

Um teste de unidade chama uma função com parâmetros conhecidos e confere o retorno. Um teste de integração, como os da Sessão 8, envia uma requisição HTTP para uma rota e examina a resposta. Os dois verificam o sistema por dentro, a partir do código ou do contrato de API. Nenhum dos dois abre uma página no navegador, clica em um botão e olha o que aparece na tela — e é exatamente esse último passo que separa "o back-end calcula o total corretamente" de "a pessoa que compra consegue finalizar o pedido".

Esse é o papel do teste end-to-end: percorrer um fluxo completo do jeito que ele acontece na interface real, sem atalho para dentro do código. Ele encontra uma categoria de defeito que os dois andares de baixo da pirâmide não alcançam — o botão que existe no HTML mas não dispara o evento certo, o texto que o JavaScript esquece de atualizar, o elemento que fica escondido atrás de outro. Nenhum desses problemas aparece testando a função de cálculo isoladamente; todos aparecem na tela.

Este tutorial cobre o fundamento de E2E web usando o Maestro, uma ferramenta que descreve o fluxo de teste como um arquivo YAML em vez de como código imperativo. O Tutorial 32 aplica a mesma ferramenta a um app mobile; o Tutorial 33 fecha a Sessão 9 com K6, testando não a interface, mas a carga que o sistema aguenta.

---

## 2. Conceito Central

### O que é um flow do Maestro

Um **flow** é a unidade de trabalho do Maestro: um arquivo YAML que descreve, passo a passo, o que uma pessoa faria ao usar a aplicação — abrir a tela, tocar em um botão, esperar algo aparecer, verificar um texto. Em vez de escrever esse roteiro em código (como se faz em ferramentas como Playwright ou Cypress), o Maestro pede que ele seja declarado como uma lista de comandos, o que o torna legível por alguém que nunca programou em nenhuma dessas linguagens.

O arquivo tem duas partes, separadas pela marcação `---` do YAML. A primeira é o cabeçalho, com o campo `appId` — o identificador do aplicativo mobile ou, no caso deste tutorial, a URL que o navegador deve abrir. A segunda é a lista de comandos, executados em ordem, de cima para baixo:

```yaml
appId: "http://localhost:8080"
---
- launchApp
- assertVisible:
    id: "produto-livro"
- tapOn:
    id: "adicionar"
```

`launchApp` abre a aplicação — no caso web, o Maestro sobe um navegador e navega até o `appId`. `tapOn` clica em um elemento. `assertVisible` e `assertNotVisible` verificam se um elemento está, ou não, visível na tela. `inputText` digita em um campo. Um flow pode ainda chamar outro com `runFlow`, o que permite reaproveitar um trecho comum — o login, por exemplo — em vários fluxos diferentes.

### Como o Maestro localiza um elemento: o seletor

Para tocar em um botão ou verificar um texto, o Maestro precisa de alguma forma de apontar para o elemento certo na tela. Essa forma de apontar chama-se **seletor**, e a escolha do seletor é a decisão mais importante para a estabilidade do flow.

Um seletor **estável** identifica o elemento por algo que descreve o que ele é, e que não muda quando o design muda: um `id` fixo, um texto visível, uma propriedade de acessibilidade. `id: "adicionar"` continua apontando para o botão "Adicionar", esteja ele no canto superior da tela ou embaixo de um carrossel novo, tenha ele oito pixels de padding ou vinte.

Um seletor **frágil** identifica o elemento por onde ele está, não pelo que ele é. O exemplo mais comum é a coordenada de tela — `point: "50%, 30%"` — que só acerta o botão certo na resolução e no layout em que alguém mediu aquele ponto na hora de escrever o flow. Mude o tamanho da fonte, adicione um banner acima, rode o mesmo teste num celular com tela maior, e a coordenada passa a apontar para outro elemento, ou para nenhum. O flow não fica devagar nem impreciso: ele simplesmente clica no lugar errado e segue em frente, relatando sucesso.

```yaml
# ❌ Frágil — depende da posição exata na tela
- tapOn:
    point: "50%, 30%"

# ✅ Estável — depende do que o elemento é, não de onde está
- tapOn:
    id: "adicionar"
```

### Assertion contra espera fixa

A segunda decisão que separa um flow confiável de um instável é como ele espera que algo aconteça. Depois de tocar em "Adicionar", o total do carrinho leva um instante para ser recalculado e reescrito na tela — geralmente milissegundos, mas o tempo exato varia com a máquina, a carga do sistema, a versão do navegador.

Uma **espera fixa** resolve isso apostando em um número: pausar por dois segundos e seguir em frente, na esperança de que o total já tenha sido atualizado. Essa aposta erra dos dois lados. Numa máquina mais lenta ou sob carga, dois segundos podem não ser suficientes, e o teste falha por lentidão do ambiente — não porque a aplicação tem um defeito. Numa máquina rápida, os dois segundos viram tempo desperdiçado a cada execução, multiplicado por centenas de flows numa suíte.

Uma **assertion** resolve o mesmo problema de outra forma: em vez de esperar um tempo fixo, ela espera pela condição que interessa. `assertVisible` fica tentando localizar o elemento até um tempo-limite, e segue assim que o encontra — nem antes, nem depois do necessário. Isso também é o que torna a assertion uma verificação, e não apenas uma pausa: se o elemento nunca aparecer, o flow falha, e falha pela razão certa.

```yaml
# ❌ Espera fixa — lenta quando não precisa, curta demais quando precisa
- extendedWaitUntil:
    visible:
        text: "Total"
    timeout: 2000

# ✅ Assertion — espera exatamente a condição, falha se ela nunca ocorrer
- assertVisible:
    text: "Total: R$ 30,00"
```

Repare que a assertion acima também verifica o valor do total, não apenas a palavra "Total". Um flow que só confirma a presença de um rótulo genérico pode passar mesmo quando o cálculo está errado — o mesmo problema, descrito na Sessão 8, de um teste de integração que confere só o código de status HTTP e ignora o corpo da resposta. A assertion precisa examinar o resultado que importa, não só um sinal de que alguma coisa aconteceu.

### Um flow sem assertion não testa nada

Existe ainda um terceiro defeito, mais silencioso que os dois anteriores: um flow que executa uma sequência de ações — abrir a tela, tocar em botões — e termina sem verificar nada. Ele "passa" sempre, porque o Maestro só reporta falha quando um comando não consegue ser executado. Se o botão "Finalizar" parar de funcionar por completo, e a tela de confirmação nunca aparecer, um flow sem `assertVisible` no fim não percebe a diferença. Ele tocou no botão; a tarefa dele terminou ali.

Um flow de E2E existe para verificar um resultado, não para demonstrar que os passos foram executados. Cada ação relevante — adicionar um item, finalizar um pedido — deveria ser seguida de uma assertion que confirma o efeito esperado dela.

### Idempotência: o flow precisa rodar mais de uma vez

Um flow bem escrito produz o mesmo resultado toda vez que roda, independentemente de quantas vezes já rodou antes. Isso parece óbvio até se considerar o que acontece quando o alvo tem estado: se o carrinho de compras não for reiniciado a cada execução, um flow que soma "Total: R$ 30,00" na primeira vez pode encontrar "Total: R$ 60,00" na segunda, porque o item da execução anterior continua lá. A assertion que passava ontem falha hoje, sem que nada tenha quebrado de fato — o ambiente é que não foi devolvido ao estado inicial.

Por isso, um flow começa tipicamente com `launchApp`, que reabre a aplicação do zero, e evita depender de qualquer estado deixado por uma execução anterior ou por outro flow. O alvo deste tutorial é uma página estática sem back-end: cada `launchApp` recarrega a página e o carrinho volta a zero, o que dá ao flow essa idempotência de graça. Alvos com estado persistente (banco de dados, sessão de servidor) exigem um passo explícito de reset antes de cada execução.

---

## 3. Ferramentas Modernas por Linguagem

Os flows do Maestro são escritos em **YAML**, e é assim para as três plataformas que a ferramenta suporta — web, Android e iOS. Não existe uma sintaxe do Maestro em Python, PHP, TypeScript ou ADVPL/TLPP: o YAML é a própria linguagem nativa da ferramenta, não uma escolha deste workshop. Por isso este tutorial não traz `equivalente.php`, `equivalente.ts` nem `equivalente.tlpp` — o par bom/ruim vive inteiramente nos dois arquivos YAML descritos acima.

**Instalar o Maestro:**

```bash
curl -Ls "https://get.maestro.mobile.dev" | bash
```

**Servir o alvo deste tutorial** — uma página de checkout estática, sem back-end, em [`exemplos/alvo/index.html`](exemplos/alvo/index.html):

```bash
python3 -m http.server 8080 --directory sessao-9/tutorial-31-e2e-web-maestro/exemplos/alvo
```

**Rodar um flow**, com o servidor acima ativo em outro terminal:

```bash
maestro test sessao-9/tutorial-31-e2e-web-maestro/exemplos/fluxo_bons.yaml
```

O suporte do Maestro a aplicações web é mais recente do que o suporte a Android e iOS, e a sintaxe exata de alguns comandos pode variar entre versões da ferramenta. Os comandos usados neste tutorial — `launchApp`, `tapOn`, `assertVisible`, `assertNotVisible`, `inputText`, `runFlow` — são os documentados oficialmente e considerados estáveis, mas, antes de rodar contra uma versão específica do Maestro, vale conferir a sintaxe atual em maestro.mobile.dev. O Maestro não está instalado neste ambiente de workshop; os flows aqui foram verificados por validação estrutural do YAML, não por execução real contra um navegador.

---

## 4. Exercício

Os arquivos [`exercicios/exercicio.yaml`](exercicios/exercicio.yaml) e [`exercicios/gabarito.yaml`](exercicios/gabarito.yaml) trazem um fluxo com objetivo simples: adicionar o livro duas vezes ao carrinho e finalizar o pedido, confirmando que o total soma R$ 60,00 e que a confirmação aparece.

O `exercicio.yaml` está escrito com os dois defeitos discutidos na seção 2: toca nos botões por coordenada de tela, e não verifica nenhum resultado ao longo do caminho — nem o total depois de cada clique, nem a confirmação no final.

**Etapas:**

1. Leia [`exercicios/exercicio.yaml`](exercicios/exercicio.yaml) e identifique cada `tapOn` por coordenada, e cada ponto onde falta uma assertion.
2. Reescreva o flow trocando cada coordenada pelo seletor estável correspondente — os mesmos `id` usados em [`exemplos/fluxo_bons.yaml`](exemplos/fluxo_bons.yaml): `produto-livro`, `adicionar`, `finalizar`, `confirmacao`.
3. Adicione uma `assertVisible` depois de cada ação relevante: o total depois do primeiro clique em "Adicionar", o total depois do segundo, e a confirmação depois de "Finalizar".
4. Compare o resultado com [`exercicios/gabarito.yaml`](exercicios/gabarito.yaml).

```bash
# Validar a estrutura YAML de ambos (não substitui rodar com o Maestro instalado)
python3 -c "import yaml; list(yaml.safe_load_all(open('sessao-9/tutorial-31-e2e-web-maestro/exercicios/exercicio.yaml')))"
python3 -c "import yaml; list(yaml.safe_load_all(open('sessao-9/tutorial-31-e2e-web-maestro/exercicios/gabarito.yaml')))"
```

---

## 5. Checklist

- [ ] O flow localiza cada elemento por `id`, texto ou propriedade de acessibilidade — nunca por coordenada de tela?
- [ ] Cada ação relevante (tocar em um botão, preencher um campo) é seguida de uma `assertVisible` que confirma o efeito esperado?
- [ ] As assertions verificam o conteúdo que importa (o valor do total, o texto da confirmação), não apenas a presença de um rótulo genérico?
- [ ] O flow evita espera fixa (`sleep`, `extendedWaitUntil` com timeout arbitrário) onde uma assertion resolveria o mesmo problema de forma mais rápida e mais confiável?
- [ ] O flow começa com `launchApp` e roda de forma idêntica na primeira e na décima execução, sem depender de estado deixado por uma execução anterior?

---

## 6. Referências

- **Maestro.** Documentação oficial.
  `https://maestro.mobile.dev`
  Referência de comandos (`launchApp`, `tapOn`, `assertVisible` e os demais), instalação e o estado atual do suporte a web — vale conferir antes de rodar flows novos, já que essa parte da ferramenta evolui rápido.

- **FOWLER, Martin.** "TestPyramid" (bliki).
  `https://martinfowler.com/bliki/TestPyramid.html`
  O modelo de proporção entre unidade, integração e e2e apresentado na Sessão 7 — a base para entender por que este tutorial trata E2E como o topo raro e caro da pirâmide, não como o ponto de partida.
