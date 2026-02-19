import os
import RPi.GPIO as GPIO

def load_tiempos_config(path="cfg/tiempos.txt"):
    config = {
        "debunce_time_ms": 150
    }

    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("tiempo_subida_velocidad=3\n")
            f.write("pulso_parada_rapida=2\n")
            f.write("vueltas_para_velocidad_baja=4\n")
            f.write("debounce_time_ms=150\n")
        return config

    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                if key in config:
                    config[key] = int(value)

    except OSError:
        pass

    return config

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
        config = load_tiempos_config()
        self.pin = pin
        self.callback = callback
        self.debounce_ms = config["debounce_time_ms"]

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