from simple_screen import *

with Screen_manager:
    for i in range(30):
        Print(f"{i:2d} - {POS.x}, {POS.y}, id(POS): {id(POS)}")
        pause(50)
    Input("Pulsa una tecla para salir")
    

