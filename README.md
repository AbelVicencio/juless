# Tic-Tac-Toe con IA Invencible

Un juego clásico de Tic-Tac-Toe (también conocido como Gato, Tres en Raya o Ta-Te-Ti) con una interfaz web sencilla y un oponente de inteligencia artificial que es imposible de vencer.

Este proyecto está contenido en un único archivo de Python, que actúa como servidor web para servir el juego y calcular los movimientos de la IA.

## Características

*   **Interfaz de Usuario Limpia:** Una interfaz web minimalista y agradable para jugar sin distracciones.
*   **IA Invencible:** El oponente está impulsado por el algoritmo **minimax**, lo que garantiza que siempre hará el movimiento óptimo. No puedes ganar, ¡solo empatar o perder!
*   **Todo en Uno:** El servidor web, la lógica del juego y la interfaz de usuario están contenidos en un solo archivo (`tictactoe.py`).
*   **Cero Dependencias:** Solo necesitas Python 3 para ejecutarlo. No se requieren bibliotecas externas.
*   **Incluye un Gato:** Porque todo es mejor con un gato.

## Manual de Uso

1.  **Clona o descarga este repositorio.**
2.  Abre una terminal o línea de comandos.
3.  Navega al directorio donde se encuentra el archivo `tictactoe.py`.
4.  Ejecuta el siguiente comando:
    ```bash
    python3 tictactoe.py
    ```
5.  Abre tu navegador web y ve a la siguiente dirección:
    [http://localhost:8000](http://localhost:8000)

¡Y eso es todo! Ya puedes empezar a jugar. Tú eres 'X' y la IA es 'O'.

## Justificación Social del Juego del Gato

El Tic-Tac-Toe, en su aparente simplicidad, es más que un simple pasatiempo. Es una de las primeras herramientas con las que muchos niños aprenden conceptos fundamentales de lógica, estrategia y planificación.

*   **Pensamiento Crítico:** Enseña a los jugadores a pensar en el futuro, a anticipar los movimientos del oponente y a entender las consecuencias de sus propias acciones.
*   **Herramienta Educativa:** Sirve como una excelente introducción a la teoría de juegos y a los principios de la inteligencia artificial, como se demuestra con el algoritmo minimax en este mismo proyecto.
*   **Universalidad y Accesibilidad:** No requiere recursos, solo una superficie para dibujar. Esta simplicidad lo convierte en un juego universalmente accesible que trasciende barreras culturales, sociales y generacionales, permitiendo la interacción y la conexión entre personas de cualquier origen.

Es, en esencia, un campo de entrenamiento para la mente, envuelto en un paquete rápido y entretenido.

## Detalles Técnicos

*   **Backend:** El servidor está construido con el módulo `http.server` de la biblioteca estándar de Python. No utiliza frameworks externos.
*   **Endpoint de la IA:** El servidor expone un endpoint `POST /jugada_ia` que recibe el estado actual del tablero y devuelve el siguiente movimiento calculado por la IA.
*   **Inteligencia Artificial:** La lógica de la IA se basa en el algoritmo **minimax**, una estrategia recursiva que explora todas las posibles jugadas futuras para minimizar la máxima pérdida posible.
*   **Frontend:** El cliente es una página HTML simple con CSS y JavaScript vainilla, servida directamente desde el script de Python. Se comunica con el servidor mediante peticiones `fetch`.
