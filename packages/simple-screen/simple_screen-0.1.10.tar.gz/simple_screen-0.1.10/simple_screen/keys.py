import curses

# Definir las constantes de teclas especiales
ESC = chr(27)       # '\x1b'
ENTER = chr(10)     # '\n'
BACKSPACE = (chr(8), chr(127))  # '\x08'
TAB = chr(9)        # '\t'
STAB = "KEY_STAB"
UP = "KEY_UP"
DOWN = "KEY_DOWN"
LEFT = "KEY_LEFT"
RIGHT = "KEY_RIGHT"
IC = "KEY_IC"
DC = "KEY_DC"
HOME = "KEY_HOME"
END = "KEY_END"
PPAGE = "KEY_PPAGE"
NPAGE = "KEY_NPAGE"
F1 = "KEY_F1"
F2 = "KEY_F2"
F3 = "KEY_F3"
F4 = "KEY_F4"
F5 = "KEY_F5"
F6 = "KEY_F6"
F7 = "KEY_F7"
F8 = "KEY_F8"
F9 = "KEY_F9"
F10 = "KEY_F10"
F11 = "KEY_F11"
F12 = "KEY_F12"

# Mapear las teclas especiales a sus constantes
key_map = {
    curses.KEY_UP: UP,
    curses.KEY_DOWN: DOWN,
    curses.KEY_LEFT: LEFT,
    curses.KEY_RIGHT: RIGHT,
    curses.KEY_STAB: STAB,
    curses.KEY_IC: IC,
    curses.KEY_DC: DC,
    curses.KEY_HOME: HOME,
    curses.KEY_END: END,
    curses.KEY_PPAGE: PPAGE,
    curses.KEY_NPAGE: NPAGE,
    curses.KEY_F1: F1,
    curses.KEY_F2: F2,
    curses.KEY_F3: F3,
    curses.KEY_F4: F4,
    curses.KEY_F5: F5,
    curses.KEY_F6: F6,
    curses.KEY_F7: F7,
    curses.KEY_F8: F8,
    curses.KEY_F9: F9,
    curses.KEY_F10: F10,
    curses.KEY_F11: F11,
    curses.KEY_F12: F12,
    #ESC: ESC
}
