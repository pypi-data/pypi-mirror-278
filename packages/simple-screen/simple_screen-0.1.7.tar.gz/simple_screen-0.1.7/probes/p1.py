import simple_screen as ssc

with ssc.Screen_manager:
    ssc.pen(ssc.YELLOW)
    ssc.paper(ssc.DARK_KHAKI)
    ssc.cls()
    ssc.locate(0, 5)
    ssc.Input()
    ssc.pair(ssc.DARK_KHAKI, ssc.YELLOW, number=3)
    ssc.Print("Texto", pair=3)
    ssc.Input()
    