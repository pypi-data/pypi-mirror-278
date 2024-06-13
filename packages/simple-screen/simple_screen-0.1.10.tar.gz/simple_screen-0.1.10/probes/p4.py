import curses

def main(stdscr):
    curses.curs_set(1)  # Mostrar el cursor
    stdscr.nodelay(0)   # Bloquear esperando la entrada
    stdscr.timeout(100)  # Esperar 100 ms por la entrada

    input_str = ""
    buffer = []

    stdscr.clear()
    stdscr.addstr(0, 0, "Escribe algo (pulsa ESC para salir): ")
    stdscr.refresh()

    while True:
        try:
            key = stdscr.get_wch()
            if key == '\x1b':  # ESC para salir
                break
            elif key == '\n':  # Enter para terminar la entrada
                buffer.append('\n')
            elif key in ('\b', '\x7f'):  # Backspace
                if buffer:
                    buffer.pop()
            else:
                buffer.append(key)
            
            # Convertir el buffer a una cadena
            input_str = ''.join(buffer)

            # Actualizar la pantalla
            stdscr.clear()
            stdscr.addstr(0, 0, "Escribe algo (pulsa ESC para salir): ")
            stdscr.addstr(1, 0, input_str)
            stdscr.refresh()

        except curses.error:
            pass  # Ignorar errores de curses cuando no hay entrada

if __name__ == "__main__":
    curses.wrapper(main)
