import RPi.GPIO as GPIO
import time


class PulseInput:
    def __init__(
        self,
        pin=23,
        callback=None,
        debounce_ms=50
    ):
        """
        pin: GPIO BCM
        callback: función a llamar cuando llega un pulso
        debounce_ms: anti-rebote
        """
        self.pin = pin
        self.callback = callback
        self.debounce_ms = debounce_ms

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(
            self.pin,
            GPIO.FALLING,           # pulso a GND
            callback=self._handle_event,
            bouncetime=self.debounce_ms
        )

    def _handle_event(self, channel):
        if self.callback:
            self.callback()

    def cleanup(self):
        GPIO.remove_event_detect(self.pin)