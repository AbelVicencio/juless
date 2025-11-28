#!/usr/bin/env python3
"""Servidor web de Tic Tac Toe en un solo archivo.

Este script ejecuta un servidor web local que permite jugar Tic Tac Toe
contra una inteligencia artificial (IA) en un navegador web.

Para ejecutarlo:
    python3 tictactoe.py

Luego, abre en el navegador la dirección:
    http://localhost:8000

El servidor sirve una página HTML con JavaScript que renderiza el tablero
y maneja la interacción del usuario. La IA utiliza el algoritmo minimax,
lo que garantiza que nunca perderá.
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
  """Implementa el algoritmo minimax recursivamente para determinar la mejor jugada.

  Esta función evalúa el estado del tablero y explora todas las posibles
  jugadas futuras para encontrar la que maximice las posibilidades de ganar de la IA.

  Args:
    tablero (list): Una lista de 9 elementos que representa el tablero.
                    Cada elemento puede ser 'X', 'O', o None.
    jugador (str): El jugador actual cuyo turno se está evaluando ('X' o 'O').
    jugador_ia (str): El símbolo que representa a la IA.
    jugador_humano (str): El símbolo que representa al jugador humano.

  Returns:
    tuple: Una tupla `(puntaje, indice_de_jugada)` donde:
           - `puntaje` es 1 si la IA gana, -1 si el humano gana, o 0 para un empate.
           - `indice_de_jugada` es el índice (0-8) de la mejor jugada posible.
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
  """Verifica si hay un ganador en el tablero.

  Args:
    tablero (list): La lista de 9 elementos que representa el tablero.

  Returns:
    str or None: El símbolo del ganador ('X' o 'O') o `None` si no hay ganador.
  """
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
    body { font-family: system-ui, sans-serif; display:flex; flex-direction:column; align-items:center; padding:20px; background:#fafafa; }
    .board { display:grid; grid-template-columns: repeat(3, 110px); gap:10px; background:transparent; padding:6px; }
    .cell { width:110px; height:110px; background:#ffffff; display:flex; align-items:center; justify-content:center; font-size:48px; cursor:pointer; border-radius:8px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); border:2px solid #ddd; transition:transform .06s ease, background .08s ease; }
    .cell:hover { transform: translateY(-2px); background:#f0f8ff }
    .cell.disabled { cursor:default; opacity:0.8 }
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
    """Manejador de peticiones HTTP.

    Sirve la página principal del juego y responde a las solicitudes
    para la jugada de la IA a través del endpoint `/jugada_ia`.
    """

    def _establecer_encabezados(self, status=200, content_type='text/html'):
        """Envía los encabezados HTTP básicos.

        Args:
            status (int): El código de estado HTTP a enviar.
            content_type (str): El tipo de contenido de la respuesta.
        """
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Responde a las solicitudes OPTIONS de pre-vuelo (preflight) para CORS."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Sirve la página HTML principal del juego."""
        if self.path == '/' or self.path.startswith('/index'):
            self._establecer_encabezados(200, 'text/html; charset=utf-8')
            self.wfile.write(PAGINA_HTML.encode('utf-8'))
        else:
            self.send_error(404, 'Not Found')

    def do_POST(self):
        """Maneja el endpoint `/jugada_ia` para la jugada de la IA."""
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
  """Inicia el servidor HTTP y lo mantiene en ejecución.

  El servidor se mantendrá activo hasta que se interrumpa con Ctrl-C.

  Args:
      server_class: La clase del servidor a utilizar (por defecto, HTTPServer).
      handler_class: La clase del manejador de peticiones (por defecto, Manejador).
  """
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
