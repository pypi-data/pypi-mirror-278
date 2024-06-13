# key_constants.py

ESC = chr(27)
ENTER = chr(10)
BACKSPACE = chr(8)
TAB = chr(9)
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

# Mapa de valores curses a nuestras constantes
key_map = {
    353: STAB,
    259: UP,
    258: DOWN,
    260: LEFT,
    261: RIGHT,
    331: IC,
    330: DC,
    262: HOME,
    360: END,
    339: PPAGE,
    338: NPAGE,
    265: F1,
    266: F2,
    267: F3,
    268: F4,
    269: F5,
    270: F6,
    271: F7,
    272: F8,
    273: F9,
    274: F10,
    275: F11,
    276: F12,
}
