// Teste de carga K6 bem estruturado — GET /pedidos sob carga controlada.
// Executar: k6 run teste_bons.js  (com o alvo em http://localhost:8000)
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  // stages: sobe a carga aos poucos, sustenta, e desce — em vez de um pico seco
  stages: [
    { duration: '10s', target: 10 }, // ramp-up: de 0 a 10 usuários virtuais
    { duration: '30s', target: 10 }, // carga sustentada em 10 usuários
    { duration: '10s', target: 0 },  // ramp-down: volta a 0
  ],
  // thresholds: os critérios de aprovação (o SLO) versionados junto do teste.
  // Se algum não for cumprido, o k6 encerra com código de saída diferente de 0,
  // o que reprova o job no CI.
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% das requisições abaixo de 500 ms
    http_req_failed: ['rate<0.01'],   // menos de 1% de falhas
  },
};

export default function () {
  const res = http.get('http://localhost:8000/pedidos');

  // check: valida cada resposta durante a carga. Diferente do threshold,
  // um check que falha não reprova o teste sozinho — ele registra a taxa de
  // acerto, revelando se a aplicação responde certo mesmo sob pressão.
  check(res, {
    'status é 200': (r) => r.status === 200,
    'corpo é uma lista de pedidos': (r) => Array.isArray(r.json()),
  });

  sleep(1); // pausa entre iterações, aproximando o ritmo de um usuário real
}
