import simple_screen as ssc
éwith ssc.Screen_manager:
    tecla = ssc.inkey()
    ssc.pair(ssc.YELLOW, ssc.DARK_BLUE)
    while tecla != ssc.ESC:
        if tecla:
            ssc.cls()
            ssc.locate(ssc.center(""), 1)
            if tecla not in ssc.BACKSPACE:
                ssc.Print(tecla)
            else:
                ssc.Print("BORRA")
            ssc.Print(tecla)
            
        tecla = ssc.inkey()
