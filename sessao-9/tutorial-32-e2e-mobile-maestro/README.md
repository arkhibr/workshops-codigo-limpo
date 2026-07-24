# Tutorial 32 — E2E Mobile com Maestro

> Referência: Maestro — documentação oficial (maestro.mobile.dev); Martin Fowler, "TestPyramid" (martinfowler.com)

## 1. Contexto e Motivação

O Tutorial 31 usou o Maestro para testar uma página web e, ao fazê-lo, apresentou os fundamentos que valem para qualquer plataforma: o flow como um roteiro em YAML, o seletor estável em vez da coordenada, a assertion no lugar da espera fixa, a idempotência. Este tutorial usa a mesma ferramenta, com os mesmos comandos, para testar um aplicativo mobile — e o foco aqui é apenas no que muda quando o alvo deixa de ser uma página no navegador e passa a ser um app instalado em um aparelho.

O que muda começa pelo próprio alvo. Uma página web recarrega do zero a cada `launchApp`: o Tutorial 31 ganhou a idempotência de graça porque o carrinho voltava a zero sozinho. Um app mobile não funciona assim. Ele mantém estado entre uma abertura e a seguinte — a sessão de quem fez login continua ativa, o cache permanece, os dados locais ficam gravados. Além do estado, o ambiente mobile traz elementos que não existem na web: diálogos de permissão do sistema operacional, gestos como deslizar e rolar, o botão "voltar" físico do Android, um teclado virtual que cobre parte da tela. Cada um desses pontos é uma fonte de instabilidade que um flow mobile precisa tratar de forma explícita.

Vale dizer o que este tutorial não inclui: ele não traz um aplicativo pronto para instalar. Construir e empacotar um app Android ou iOS está fora do escopo do workshop. Os flows aqui assumem um app de pedidos hipotético, com o identificador `br.com.workshop.pedidos`, e servem para estudar a estrutura de um teste mobile. Para executá-los de fato, é preciso um emulador ou simulador com um app real instalado — o próprio Maestro publica aplicativos de exemplo que servem a esse propósito.

---

## 2. Conceito Central

### Estado do app entre execuções: `clearState` e `stopApp`

O comando `launchApp`, sozinho, abre o app no estado em que ele ficou. Se a execução anterior terminou com um usuário logado, a próxima começa logada também. Isso faz um flow passar numa hora e falhar em outra pela razão mais frustrante possível: o resultado depende do que sobrou de antes, não do que o flow faz.

A forma de resolver é reiniciar o estado no início do flow. `launchApp` aceita a opção `clearState`, que apaga os dados do aplicativo — sessão, cache, banco local — antes de abrir. Com ela, o flow começa sempre do mesmo ponto: deslogado, com o carrinho vazio, como numa instalação recém-feita.

```yaml
# ❌ Abre o app no estado que sobrou — pode começar logado, pode não começar
- launchApp

# ✅ Apaga o estado antes de abrir — começa sempre do zero, deslogado
- launchApp:
    clearState: true
```

Existe ainda `stopApp`, que encerra o app sem apagar os dados, útil quando o flow precisa simular o usuário fechando e reabrindo o aplicativo no meio de um cenário. A diferença entre os dois é o que se quer reiniciar: `clearState` zera os dados; `stopApp` apenas encerra o processo.

### Permissões do sistema operacional

Um app mobile costuma pedir permissões — localização, câmera, notificações — por meio de um diálogo do próprio sistema operacional, que aparece por cima da interface do app. Um flow que não espera esse diálogo trava, porque tenta tocar em um elemento do app que está encoberto pela caixa de permissão.

O `launchApp` aceita declarar como essas permissões devem ser respondidas, de modo que o flow não fique à mercê do diálogo:

```yaml
- launchApp:
    clearState: true
    permissions:
      location: allow
```

Definir as permissões no início deixa o flow determinístico quanto a esse ponto: ele não depende de o diálogo aparecer, nem de alguém tocar em "Permitir" na hora certa.

### Gestos: `swipe` e `scroll`

Na web do Tutorial 31, toda interação se resumia a tocar. No mobile, boa parte do conteúdo só aparece depois de rolar a tela, e algumas ações — descartar um card, revelar um menu — são feitas por gestos. O Maestro tem comandos para isso: `scroll` rola a tela na direção do conteúdo que se procura, e `swipe` executa um deslize entre dois pontos. Um flow que precisa tocar em um item mais abaixo na lista rola até ele antes, em vez de presumir que ele já está visível.

### O botão "voltar" e o teclado

Duas particularidades do mobile aparecem com frequência nos flows. A primeira é o botão "voltar" do Android, acionado pelo comando `back` — um caminho de navegação que não tem equivalente direto no iOS nem na web, e que muitos apps usam para fechar telas. A segunda é o teclado virtual: ao tocar em um campo e usar `inputText`, o teclado sobe e pode cobrir o botão que o próximo passo precisa tocar. O comando `hideKeyboard` fecha o teclado antes de seguir — é por isso que ele aparece nos flows de exemplo deste tutorial, entre o preenchimento da senha e o toque em "Entrar".

### Diferenças entre iOS e Android

O mesmo flow roda nas duas plataformas, mas nem tudo se comporta igual. O `back` existe no Android e não no iOS. Os diálogos de permissão têm textos e botões diferentes em cada sistema. A árvore de elementos de uma tela — de onde saem os `id` e os textos que os seletores usam — pode variar entre as duas plataformas, porque quem construiu o app pode ter nomeado as coisas de forma diferente em cada uma. Um flow escrito para os dois sistemas se apoia em seletores que existem em ambos, e a ferramenta `maestro studio` (descrita na próxima seção) ajuda a descobrir quais são esses seletores em cada aparelho.

---

## 3. Ferramentas Modernas por Linguagem

Como no Tutorial 31, os flows do Maestro são escritos em **YAML**, e essa é a única forma de escrevê-los — não há uma sintaxe do Maestro em Python, PHP, TypeScript ou ADVPL/TLPP. Por isso este tutorial também não traz arquivos `equivalente.*`: o par bom/ruim vive nos dois YAML de `exemplos/`.

**Pré-requisitos para executar os flows deste tutorial:**

- O Maestro instalado (`curl -Ls "https://get.maestro.mobile.dev" | bash`).
- Um emulador Android ou simulador iOS em execução.
- Um app instalado nesse emulador cujo `appId` corresponda ao do flow. Este tutorial não fornece o app; use um dos aplicativos de exemplo do Maestro e ajuste o `appId` no cabeçalho do flow.

**Rodar um flow**, com o emulador ativo e o app instalado:

```bash
maestro test sessao-9/tutorial-32-e2e-mobile-maestro/exemplos/fluxo_bons.yaml
```

**Inspecionar a tela** para descobrir os `id` e textos disponíveis:

```bash
maestro studio
```

O `maestro studio` abre uma interface que mostra a árvore de elementos da tela atual do emulador, com os seletores que cada elemento aceita. É a forma prática de escrever seletores estáveis em vez de recorrer a coordenadas — e de conferir as diferenças de árvore entre Android e iOS mencionadas na seção 2. O Maestro não está instalado neste ambiente de workshop; os flows aqui foram verificados por validação estrutural do YAML, não por execução contra um emulador.

---

## 4. Exercício

Os arquivos [`exercicios/exercicio.yaml`](exercicios/exercicio.yaml) e [`exercicios/gabarito.yaml`](exercicios/gabarito.yaml) trazem um fluxo com o objetivo de fazer login como "ana", abrir o catálogo e adicionar o livro ao carrinho, confirmando que o carrinho passou a ter um item.

O `exercicio.yaml` está escrito com os dois problemas centrais de um flow mobile: abre o app sem `clearState`, presumindo uma sessão que talvez não exista, e localiza os elementos por coordenada de tela.

**Etapas:**

1. Leia [`exercicios/exercicio.yaml`](exercicios/exercicio.yaml) e identifique onde ele depende de estado anterior e onde usa coordenadas.
2. Adicione `clearState: true` ao `launchApp` e escreva o login explícito — o fluxo precisa funcionar mesmo começando deslogado.
3. Troque cada coordenada por um seletor estável (os `id` e textos usados em [`exemplos/fluxo_bons.yaml`](exemplos/fluxo_bons.yaml): `campo_usuario`, `campo_senha`, `produto_livro`, e os textos "Entrar", "Adicionar ao carrinho").
4. Termine com uma `assertVisible` confirmando o item no carrinho, e compare com [`exercicios/gabarito.yaml`](exercicios/gabarito.yaml).

```bash
# Validar a estrutura YAML de ambos (não substitui rodar com o Maestro instalado)
python3 -c "import yaml; list(yaml.safe_load_all(open('sessao-9/tutorial-32-e2e-mobile-maestro/exercicios/exercicio.yaml')))"
python3 -c "import yaml; list(yaml.safe_load_all(open('sessao-9/tutorial-32-e2e-mobile-maestro/exercicios/gabarito.yaml')))"
```

---

## 5. Checklist

- [ ] O flow começa com `launchApp: clearState: true` (ou um reset equivalente), sem depender de sessão ou dados deixados por uma execução anterior?
- [ ] As permissões de que o app precisa são declaradas no `launchApp`, para o flow não travar num diálogo do sistema?
- [ ] Os elementos são localizados por `id` ou texto — descobertos com `maestro studio` — em vez de coordenadas de tela?
- [ ] Quando o teclado virtual pode cobrir o próximo elemento, o flow o fecha com `hideKeyboard` antes de seguir?
- [ ] O flow depende apenas de seletores que existem tanto no Android quanto no iOS, se o objetivo é rodar nas duas plataformas?
- [ ] Cada ação relevante termina com uma assertion que confirma o resultado esperado, e não apenas a execução do passo?

---

## 6. Referências

- **Maestro.** Documentação oficial.
  `https://maestro.mobile.dev`
  Referência dos comandos mobile (`launchApp` com `clearState` e `permissions`, `swipe`, `scroll`, `back`, `hideKeyboard`, `stopApp`), do `maestro studio` e dos aplicativos de exemplo usados para praticar.

- **FOWLER, Martin.** "TestPyramid" (bliki).
  `https://martinfowler.com/bliki/TestPyramid.html`
  O modelo da pirâmide, já usado na Sessão 7 e no Tutorial 31 — o E2E mobile é tão caro e lento quanto o E2E web, e fica no mesmo topo raro da pirâmide.
