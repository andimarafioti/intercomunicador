import lcddriver

lcd = lcddriver.lcd()

# lcd.lcd_clear();
lcd.lcd_display_string("Lorem", 1)
lcd.lcd_display_string("Ipsum", 2)
