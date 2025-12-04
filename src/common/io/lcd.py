
from RPLCD import CharLCD
from RPi import GPIO
import time

# Common I2C addresses: 0x27 or 0x3F
lcd = CharLCD(pin_rs=24, pin_e=23, pins_data=[22, 27, 18, 17],
    numbering_mode=GPIO.BCM, cols=16, rows=2, dotsize=8)

def lcd_write(text: str):
    lcd.clear()
    # Simple 2-line wrap for 16x2
    line1 = text[:16].ljust(16)
    line2 = text[16:32].ljust(16)
    lcd.write_string(line1)
    lcd.cursor_pos = (1, 0)
    lcd.write_string(line2)

lcd_write("Hello LCD! This wraps onto line 2.")
time.sleep(5)
lcd.clear()
lcd.close()
