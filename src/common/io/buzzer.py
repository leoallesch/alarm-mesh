from gpiozero import TonalBuzzer, Buzzer
from gpiozero.tones import Tone
from time import sleep

class BuzzerController:
    def __init__(self, buzzer_pin, tone="alarm"):
        self.tone = tone

        # Try to use TonalBuzzer for passive buzzers
        try:
            self.buzzer = TonalBuzzer(buzzer_pin)
            self.tonal = True
        except Exception:
            # Fallback for active buzzers
            self.buzzer = Buzzer(buzzer_pin)
            self.tonal = False

        self.is_on = False

    def turn_on(self):
        self.is_on = True

        if self.tonal:
            # Alarm-like tone pattern for passive buzzer
            try:
                for freq in [440, 660, 880, 660]:
                    self.buzzer.play(Tone(freq))
                    sleep(0.15)
                self.buzzer.stop()
                return
            except Exception:
                pass

        # Fallback for active buzzer: simple beep
        for _ in range(3):
            self.buzzer.on()
            sleep(0.1)
            self.buzzer.off()
            sleep(0.1)

    def turn_off(self):
        self.is_on = False

        if self.tonal:
            self.buzzer.stop()
        else:
            self.buzzer.off()
