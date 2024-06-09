import simple_screen as ssc

with ssc.Screen_manager:
    ssc.pen(ssc.YELLOW)
    ssc.paper(ssc.DARK_KHAKI)
    ssc.cls()
    ssc.locate(0, 50)
    ssc.Input("Pulsa tecla para finalizar")
    