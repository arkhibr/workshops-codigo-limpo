"""Alvo HTTP para o teste de carga K6 — biblioteca padrão, sem dependências.

Sobe uma API de pedidos mínima em http://localhost:8000, com uma latência
artificial de ~20 ms por requisição para que o teste de carga tenha o que medir.

Executar:  python3 servidor.py   (encerra com Ctrl+C)
"""
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

_pedidos = [{"id": 1, "cliente": "Ana", "total": 30.0}]


class Handler(BaseHTTPRequestHandler):
    def _responder(self, codigo: int, corpo: object) -> None:
        dados = json.dumps(corpo).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        time.sleep(0.02)  # latência artificial: dá ao teste de carga o que medir
        if self.path == "/pedidos":
            self._responder(200, _pedidos)
        else:
            self._responder(404, {"detail": "não encontrado"})

    def do_POST(self):
        time.sleep(0.02)
        if self.path == "/pedidos":
            self._responder(201, {"id": len(_pedidos) + 1, "status": "aberto"})
        else:
            self._responder(404, {"detail": "não encontrado"})

    def log_message(self, *args):
        pass  # silencia o log por requisição — vira ruído sob carga


if __name__ == "__main__":
    servidor = ThreadingHTTPServer(("localhost", 8000), Handler)
    print("Alvo ouvindo em http://localhost:8000 (Ctrl+C para encerrar)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.shutdown()
