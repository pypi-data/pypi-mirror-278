import curses

def main(stdscr):
    # Inicializar curses
    curses.curs_set(1)
    stdscr.clear()
    stdscr.keypad(True)  # Habilitar la captura de teclas especiales

    # Obtener las dimensiones actuales de la ventana
    height, width = stdscr.getmaxyx()
    new_height = height + 5  # Aumentar la altura de la ventana para demostrar el desplazamiento

    # Preparar el contenido
    content = [f"This is line {i + 1}" for i in range(new_height)]

    # Variables para el desplazamiento
    start_y = 0

    while True:
        # Limpiar la ventana
        stdscr.clear()

        # Dibujar el contenido visible
        for i in range(start_y, min(start_y + height, new_height)):
            stdscr.addstr(i - start_y, 0, content[i])

        stdscr.refresh()

        # Esperar la entrada del usuario para desplazarse
        key = stdscr.getch()

        # Desplazarse según la tecla presionada
        if key == curses.KEY_UP and start_y > 0:
            start_y -= 1
        elif key == curses.KEY_DOWN and start_y < new_height - height:
            start_y += 1
        elif key == ord('q'):
            break

# Iniciar el programa curses
curses.wrapper(main)
