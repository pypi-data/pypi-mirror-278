import simple_screen as ssc
with ssc.Screen_manager:
    tecla = ssc.inkey()
    ssc.pair(ssc.YELLOW, ssc.DARK_BLUE)
    while tecla != " ":
        if tecla:
            ssc.cls()
            ssc.locate(0, 0)
            ssc.Print(tecla)
            
        tecla = ssc.inkey()
         