// Gabarito — mesmo objetivo de exercicio.js (POST /pedidos sob carga), agora
// com ramp-up por stages, SLO em thresholds e validação por check.
// Executar: k6 run gabarito.js  (com o alvo em http://localhost:8000)
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  // ✅ carga que sobe, sustenta e desce
  stages: [
    { duration: '10s', target: 10 },
    { duration: '30s', target: 10 },
    { duration: '10s', target: 0 },
  ],
  // ✅ SLO versionado: reprova o teste (exit code != 0) se não for cumprido
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

const CORPO = JSON.stringify({
  cliente: 'Ana',
  itens: [{ produto: 'Livro', quantidade: 1, preco_unitario: 30.0 }],
});
const PARAMS = { headers: { 'Content-Type': 'application/json' } };

export default function () {
  const res = http.post('http://localhost:8000/pedidos', CORPO, PARAMS);

  // ✅ valida a resposta sob carga: status de criação e status inicial do pedido
  check(res, {
    'status é 201': (r) => r.status === 201,
    'pedido criado como aberto': (r) => r.json('status') === 'aberto',
  });

  sleep(1);
}
