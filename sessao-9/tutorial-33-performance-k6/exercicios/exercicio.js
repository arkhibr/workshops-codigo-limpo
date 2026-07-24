// Exercício — transforme este gerador de tráfego em um teste de carga de verdade.
//
// Objetivo: exercitar POST /pedidos sob carga e verificar que a criação de
// pedidos continua correta e rápida enquanto a carga sobe.
//
// Como está, o script dispara todos os usuários de uma vez, não define nenhum
// critério de aprovação e não valida as respostas. Ele gera tráfego, mas não
// testa nada — passa em qualquer situação.
//
// Sua tarefa (compare com gabarito.js quando terminar):
//   1. Troque `vus`/`duration` por `stages` com ramp-up, carga sustentada e ramp-down.
//   2. Adicione `thresholds` com um SLO: p(95) da duração e taxa de falhas.
//   3. Adicione um `check` que valide o status 201 e o corpo da resposta.
import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  // ❌ pico seco, sem ramp-up
  vus: 50,
  duration: '5s',
  // ❌ falta thresholds — nenhum critério de aprovação (SLO)
};

const CORPO = JSON.stringify({
  cliente: 'Ana',
  itens: [{ produto: 'Livro', quantidade: 1, preco_unitario: 30.0 }],
});
const PARAMS = { headers: { 'Content-Type': 'application/json' } };

export default function () {
  http.post('http://localhost:8000/pedidos', CORPO, PARAMS);
  // ❌ falta check — a resposta nunca é validada
  sleep(1);
}
