# Tic Tac Toe (Gato) con IA

Este proyecto es un sencillo servidor web para jugar Tic Tac Toe (también conocido como "Gato") contra una inteligencia artificial (IA) invencible. El juego se presenta en una interfaz web simple y limpia.

## Propósito

El objetivo de este proyecto es demostrar:
- Un servidor web autónomo en Python usando el módulo `http.server`.
- La implementación del algoritmo **minimax** para una IA de juego perfecta.
- Una aplicación de una sola página (SPA) con HTML, CSS y JavaScript vainilla.

## Características

- **Servidor Ligero**: Todo el backend se ejecuta en un único archivo Python sin dependencias externas.
- **IA Invencible**: El oponente de la IA utiliza el algoritmo minimax, lo que significa que nunca cometerá un error y es imposible de vencer.
- **Interfaz Web Simple**: La interfaz de usuario es limpia, minimalista y fácil de usar.

## Configuración y Ejecución

Para ejecutar el juego, solo necesitas tener Python 3 instalado. No se requieren bibliotecas adicionales.

1. **Clona el repositorio** (o descarga los archivos).

2. **Navega al directorio del proyecto** en tu terminal:
   ```bash
   cd ruta/al/directorio
   ```

3. **Ejecuta el servidor**:
   ```bash
   python3 tictactoe.py
   ```

4. **Abre el juego en tu navegador**:
   Una vez que el servidor esté en marcha, verás un mensaje en la terminal:
   ```
   Sirviendo en http://0.0.0.0:8000 — pulsa Ctrl-C para salir
   ```
   Abre tu navegador web y ve a `http://localhost:8000`.

## Cómo Jugar

- El tablero de 3x3 se mostrará en la página.
- Tú juegas como **'X'** y la IA juega como **'O'**.
- Para hacer un movimiento, simplemente haz clic en una celda vacía.
- Después de tu movimiento, la IA hará el suyo automáticamente.
- El juego terminará cuando un jugador gane o cuando haya un empate. El resultado se mostrará debajo del tablero.
