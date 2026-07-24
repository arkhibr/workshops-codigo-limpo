// Teste de carga K6 mal estruturado — gera tráfego, mas não valida nada.
// Executar: k6 run teste_ruins.js  (com o alvo em http://localhost:8000)
import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  // ❌ Anti-padrão 1: sem stages. 50 usuários entram de uma vez, num pico seco.
  // Isso não representa uma carga real (que sobe aos poucos) e mede sobretudo
  // como o servidor reage ao susto da largada, não ao regime sustentado.
  vus: 50,
  duration: '5s',
  // ❌ Anti-padrão 2: sem thresholds. O teste não tem critério de aprovação.
  // Ele sempre "passa", porque nunca define o que seria reprovar — nenhum SLO
  // versionado, nada que faça o CI falhar quando a latência degradar.
};

export default function () {
  const res = http.get('http://localhost:8000/pedidos');

  // ❌ Anti-padrão 3: sem check. O teste não verifica se a resposta está correta.
  // Sob carga, o servidor pode passar a devolver 500 ou um corpo vazio, e este
  // teste seguiria gerando tráfego sem acusar nada.

  // ❌ Anti-padrão 4: console.log por iteração, para "olhar no olho".
  // Além de inundar a saída sob carga, transfere para um humano a decisão que
  // um check deveria tomar automaticamente.
  console.log(res.body);

  sleep(0.01); // ❌ pausa mínima: martela o alvo em vez de imitar um usuário
}
