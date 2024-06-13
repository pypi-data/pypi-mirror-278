import curses
from .entities import Position, Color, Dimensions
from .keys import key_map
from typing import Callable

STDSRC = None
POS = Position(0, 0)
FOREGROUND = Color(250, 250, 250)
BACKGROUND = Color(0, 0, 0)
DIMENSIONS = None
SHELLDIMENSIONS = None
MAX_PAIRS = -1
MAX_COLORS = -1
ACTIVE_PAIR = 1
SCROLLACUM = 0

KEY_UP = chr(curses.KEY_UP)
KEY_DOwN = chr(curses.KEY_DOWN)
KEY_LEFT = chr(curses.KEY_LEFT)
KEY_RIGHT = chr(curses.KEY_RIGHT)


class SimpleScreenException(Exception):
    pass


def _init_curses():
    pantalla = curses.initscr()

    curses.cbreak()
    curses.start_color()
    pantalla.keypad(True)

    return pantalla


def _end(scr):
    curses.nocbreak()
    scr.keypad(False)
    curses.echo()
    curses.endwin()


def pause(ms: int):
    curses.napms(ms)


def init():
    global STDSRC, POS, DIMENSIONS, MAX_PAIRS, MAX_COLORS, SHELLDIMENSIONS
    STDSRC = _init_curses()
    DIMENSIONS = Dimensions(*STDSRC.getmaxyx())
    SHELLDIMENSIONS = Dimensions(*STDSRC.getmaxyx())
    STDSRC.scrollok(True)
    '''
    La ventana logica tiene una linea de mas para poder simular 
    overflow hacia abajo.
    No hay buffer, al hacer scroll se pierden los contenidos de
    las lineas superiores
    '''
    STDSRC.resize(DIMENSIONS.h + 1, DIMENSIONS.w)
    MAX_PAIRS = curses.COLOR_PAIRS
    MAX_COLORS = curses.COLORS
    pair(FOREGROUND, BACKGROUND)


def finish():
    _end(STDSRC)


def cls(refresh: bool = True):
    STDSRC.clear()
    locate(0, 0)
    if refresh:
        STDSRC.refresh()


def locate(x: int, y: int, cad: object = None):
    global SCROLLACUM
    if not (0 <= x <= SHELLDIMENSIONS.w and 0 <= y <= SHELLDIMENSIONS.h):
        raise OverflowError(f"{x}, {y} out of window.")
    dif = max(0, y - (SHELLDIMENSIONS.h - 1))
    if dif > 0:
        STDSRC.resize(y+dif, DIMENSIONS.w)
        DIMENSIONS.h, DIMENSIONS.w = STDSRC.getmaxyx()
        SCROLLACUM += 1
        STDSRC.move(SHELLDIMENSIONS.h - 1, x)
    else:
        STDSRC.move(y, x)

    if cad:
        STDSRC.addstr(f"{cad}")
        STDSRC.refresh()


def Print(cadena: object = "", refresh: bool = True):
    global SCROLLACUM

    STDSRC.addstr(f"{str(cadena)}", curses.color_pair(ACTIVE_PAIR))
    STDSRC.scroll(SCROLLACUM)
    SCROLLACUM = 0
    if refresh:
        STDSRC.refresh()
    _retrievePos()
    locate(0, POS.y + 1)
    _retrievePos()


def Input(mensaje: str = "") -> str:
    curses.curs_set(1)
    STDSRC.nodelay(0)
    STDSRC.attron(curses.A_REVERSE)
    STDSRC.addstr(mensaje, curses.color_pair(ACTIVE_PAIR))
    curses.echo()
    user_input = STDSRC.getstr(curses.color_pair(ACTIVE_PAIR)).decode('utf-8')
    STDSRC.attroff(curses.A_REVERSE)
    curses.noecho()
    curses.curs_set(0)
    _retrievePos()
    return user_input


def center(cad: str) -> int:
    return (DIMENSIONS.w - len(cad)) // 2


def center_print(cad, fila: int = 0):
    locate(center(cad), fila)
    Print(cad)


def inkey(timeout: int = 100) -> str:
    curses.curs_set(0)
    curses.noecho()
    STDSRC.nodelay(1)
    STDSRC.timeout(timeout)
    try:
        key = STDSRC.get_wch()
        if key == chr(27):
            a = 3
    except curses.error:
        key = -1
    return "" if key == -1 else key_map.get(key, key)


def _create_color(ix: int, color: Color):
    curses.init_color(ix, *color.value)


def _retrievePos():
    POS.y, POS.x = STDSRC.getyx()


def pair(_pen: Color, _paper: Color, refresh: bool = True):
    global FOREGROUND, BACKGROUND
    _create_color(12, _pen)
    _create_color(13, _paper)
    curses.init_pair(ACTIVE_PAIR, 12, 13)
    FOREGROUND = _pen
    BACKGROUND = _paper
    STDSRC.bkgd(' ', curses.color_pair(ACTIVE_PAIR))
    if refresh:
        STDSRC.refresh()


def pen(color: Color, refresh: bool = True):
    pair(color, BACKGROUND, refresh)


def paper(color: Color, refresh: bool = True):
    pair(FOREGROUND, color, refresh)


def app(func: Callable[..., None]) -> Callable[..., None]:
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        finally:
            _end(STDSRC)

    return wrapper


class Simple_ScreenContextManager:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        finish()
        return False


init()
