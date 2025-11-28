#!/usr/bin/env python3
"""
Tic Tac Toe webserver (single-file).

Ejecuta: python3 tictactoe.py
Abre en el navegador: http://localhost:8000

El servidor sirve una página HTML/JS con un tablero y un SVG de gato.
La IA usa minimax (no pierde).
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import urllib
import sys
import threading

ANFITRION = '0.0.0.0'
PUERTO = 8000


def algoritmo_minimax(tablero, jugador, jugador_ia='O', jugador_humano='X'):
  """
  Algoritmo Minimax recursivo.

  Args:
    tablero: lista de 9 elementos 'X','O' o None.
    jugador: jugador actual ('X' o 'O').
    jugador_ia: símbolo usado por la IA.
    jugador_humano: símbolo usado por el humano.

  Returns:
    Tupla (puntaje, indice_de_jugada) donde puntaje: 1 IA gana, -1 humano gana, 0 empate.
  """
  ganador = verificar_ganador(tablero)
  if ganador == jugador_ia:
    return (1, None)
  elif ganador == jugador_humano:
    return (-1, None)
  elif all(celda is not None for celda in tablero):
    return (0, None)

  if jugador == jugador_ia:
    mejor_puntaje = -2
    mejor_jugada = None
    for i in range(9):
      if tablero[i] is None:
        tablero[i] = jugador_ia
        puntaje, _ = algoritmo_minimax(tablero, jugador_humano, jugador_ia, jugador_humano)
        tablero[i] = None
        if puntaje > mejor_puntaje:
          mejor_puntaje = puntaje
          mejor_jugada = i
    return (mejor_puntaje, mejor_jugada)
  else:
    mejor_puntaje = 2
    mejor_jugada = None
    for i in range(9):
      if tablero[i] is None:
        tablero[i] = jugador_humano
        puntaje, _ = algoritmo_minimax(tablero, jugador_ia, jugador_ia, jugador_humano)
        tablero[i] = None
        if puntaje < mejor_puntaje:
          mejor_puntaje = puntaje
          mejor_jugada = i
    return (mejor_puntaje, mejor_jugada)


def verificar_ganador(tablero):
  """Devuelve 'X' o 'O' si hay ganador, o None si no lo hay."""
  wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
  for a,b,c in wins:
    if tablero[a] and tablero[a] == tablero[b] == tablero[c]:
      return tablero[a]
  return None


PAGINA_HTML = r'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Tic Tac Toe - Gato</title>
  <style>
    body { font-family: system-ui, sans-serif; display:flex; flex-direction:column; align-items:center; padding:20px; }
    .board { display:grid; grid-template-columns: repeat(3, 100px); gap:8px; }
    .cell { width:100px; height:100px; background:#f7f7f7; display:flex; align-items:center; justify-content:center; font-size:48px; cursor:pointer; border-radius:8px; box-shadow: 0 1px 2px rgba(0,0,0,0.1);} 
    .cell.disabled { cursor:default; opacity:0.7 }
    #info { margin:12px 0 }
    .cat { width:160px; margin-top:18px }
  </style>
</head>
<body>
  <h1>Tic Tac Toe — Gato</h1>
  <div id="info">Tu: <strong>X</strong> — IA: <strong>O</strong></div>
  <div id="board" class="board"></div>
  <div id="info2"></div>

  <!-- SVG del gato -->
  <div class="cat">
  <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Gato">
    <defs>
      <linearGradient id="g" x1="0" x2="1">
        <stop offset="0%" stop-color="#f7b"/>
        <stop offset="100%" stop-color="#f79"/>
      </linearGradient>
    </defs>
    <g transform="translate(100,100)">
      <ellipse cx="0" cy="30" rx="60" ry="40" fill="#ffc" stroke="#333" stroke-width="2" />
      <circle cx="-28" cy="-10" r="30" fill="#ffd" stroke="#333" stroke-width="2" />
      <circle cx="28" cy="-10" r="30" fill="#ffd" stroke="#333" stroke-width="2" />
      <polygon points="-55,-35 -40,-70 -25,-35" fill="#ffd" stroke="#333" stroke-width="2" />
      <polygon points="55,-35 40,-70 25,-35" fill="#ffd" stroke="#333" stroke-width="2" />
      <circle cx="-18" cy="-10" r="6" fill="#333" />
      <circle cx="18" cy="-10" r="6" fill="#333" />
      <path d="M -10 6 Q 0 18 10 6" stroke="#b33" stroke-width="3" fill="none" stroke-linecap="round" />
      <path d="M -35 0 Q -10 10 0 12 Q 10 10 35 0" stroke="#333" stroke-width="2" fill="none" />
    </g>
  </svg>
  </div>

  <script>
    const tableroEl = document.getElementById('board');
    const info2 = document.getElementById('info2');
    let tablero = Array(9).fill(null);
    let juegoTerminado = false;

    // Dibuja el tablero en la página
    function renderizar(){
      tableroEl.innerHTML = '';
      for(let i=0;i<9;i++){
        const celda = document.createElement('div');
        celda.className = 'cell' + (tablero[i] ? ' disabled' : '');
        celda.textContent = tablero[i] || '';
        celda.addEventListener('click', ()=> alClic(i));
        tableroEl.appendChild(celda);
      }
    }

    // Maneja el clic del jugador humano
    function alClic(i){
      if(juegoTerminado || tablero[i]) return;
      tablero[i] = 'X';
      renderizar();
      // verificar victoria local rápido
      if(verificarGanador(tablero)) return terminarJuego(verificarGanador(tablero));
      if(tablero.every(c=>c)) return terminarJuego(null);
      // pedir jugada al servidor
      fetch('/jugada_ia', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({board: tablero})
      }).then(r=>r.json()).then(data=>{
        if(data.error){ info2.textContent = data.error; return; }
        if(typeof data.move === 'number'){
          tablero[data.move] = 'O';
        }
        renderizar();
        const w = verificarGanador(tablero);
        if(w) terminarJuego(w);
        else if(tablero.every(c=>c)) terminarJuego(null);
      }).catch(err=>{ info2.textContent = 'Error comunicando con el servidor'; });
    }

    // Verifica si hay ganador en el tablero (cliente)
    function verificarGanador(b){
      const wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
      for(const [a,b1,c] of wins){
        if(b[a] && b[a] === b[b1] && b[a] === b[c]) return b[a];
      }
      return null;
    }

    function terminarJuego(ganador){
      juegoTerminado = true;
      if(ganador === 'X') info2.textContent = 'Has ganado 🎉';
      else if(ganador === 'O') info2.textContent = 'IA gana — mejor suerte la próxima';
      else info2.textContent = 'Empate';
    }

    renderizar();
  </script>
</body>
</html>
'''


class Manejador(BaseHTTPRequestHandler):
    """Manejador HTTP que sirve la página y responde la jugada de la IA."""

    def _establecer_encabezados(self, status=200, content_type='text/html'):
        """Envía encabezados HTTP básicos y CORS."""
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        # Responder a peticiones CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        # Servir la página principal
        if self.path == '/' or self.path.startswith('/index'):
            self._establecer_encabezados(200, 'text/html; charset=utf-8')
            self.wfile.write(PAGINA_HTML.encode('utf-8'))
        else:
            self.send_error(404, 'Not Found')

    def do_POST(self):
        # Endpoint para calcular la jugada de la IA
        if self.path == '/jugada_ia':
            longitud = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(longitud)
            try:
                datos = json.loads(raw.decode('utf-8'))
                b = datos.get('board')
                if not isinstance(b, list) or len(b) != 9:
                    raise ValueError('El tablero debe ser una lista de 9 elementos')
                # normalizar: aceptar null/None
                tablero = [None if x is None else (str(x) if x else None) for x in b]
                # ejecutar algoritmo minimax para la IA 'O'
                puntaje, jugada = algoritmo_minimax(tablero, 'O', jugador_ia='O', jugador_humano='X')
                resp = {'move': jugada, 'score': puntaje}
                self._establecer_encabezados(200,'application/json')
                self.wfile.write(json.dumps(resp).encode('utf-8'))
            except Exception as e:
                self._establecer_encabezados(400,'application/json')
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_error(404, 'Not Found')


def ejecutar(server_class=HTTPServer, handler_class=Manejador):
  """Inicia el servidor HTTP y lo deja escuchando hasta Ctrl-C."""
  server_address = (ANFITRION, PUERTO)
  httpd = server_class(server_address, handler_class)
  print(f"Sirviendo en http://{ANFITRION}:{PUERTO}  — pulsa Ctrl-C para salir")
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    print('\nDetenido por usuario')
  finally:
    httpd.server_close()


if __name__ == '__main__':
  ejecutar()
