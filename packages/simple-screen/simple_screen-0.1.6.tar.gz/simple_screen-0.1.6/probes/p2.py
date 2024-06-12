import simple_screen as ssc

with ssc.Screen_manager:
    x = ssc.DIMENSIONS.w // 2
    y = ssc.DIMENSIONS.h // 2

    ssc.pair(ssc.YELLOW, ssc.DARK_BLUE)
    ssc.cls()
    cad = "Pulsa q para salir"
    ssc.locate((ssc.DIMENSIONS.w - len(cad)) // 2, ssc.DIMENSIONS.h - 1, cad)

    tecla = ""
    while tecla != "q":
        tecla = ssc.inkey()
        ssc.locate(x, y, "*")
        ssc.pause(50)

        if tecla == ssc.KEY_UP:
            ssc.locate(x, y, " ")
            y = max(0, y - 1)
        elif tecla == ssc.KEY_DOwN:
            ssc.locate(x, y, " ")
            y = min(ssc.SHELLDIMENSIONS.h - 1, y + 1)
        elif tecla == ssc.KEY_LEFT:
            ssc.locate(x, y, " ")
            x = max(0, x - 1)
        elif tecla == ssc.KEY_RIGHT:
            ssc.locate(x, y, " ")
            x = min(ssc.DIMENSIONS.w - 1, x + 1)
        elif tecla == "i":
            valor = ssc.Input("Dime algo:")
            ssc.locate(0, y+1, valor)