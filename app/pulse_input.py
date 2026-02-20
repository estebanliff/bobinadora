import os
import RPi.GPIO as GPIO
import time
from logging.handlers import RotatingFileHandler
import logging

handler = RotatingFileHandler(
    "pulse_debug.log",
    maxBytes=1_000_000,
    backupCount=3
)

formatter = logging.Formatter(
    "%(asctime)s.%(msecs)03d | %(message)s",
    "%H:%M:%S"
)

handler.setFormatter(formatter)

logger = logging.getLogger("pulse")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def load_tiempos_config(path="cfg/tiempos.txt"):
    config = {
        "tiempo_subida_velocidad": 3,
        "pulso_parada_rapida": 2,
        "vueltas_para_velocidad_baja": 20,
        "debounce_time_ms": 150
    }

    if not os.path.exists(path):
        try:
            with open(path, "w") as f:
                f.write("tiempo_subida_velocidad=3\n")
                f.write("pulso_parada_rapida=2\n")
                f.write("vueltas_para_velocidad_baja=4\n")
                f.write("debounce_time_ms=150\n")
            print(f"[CONFIG] Archivo no encontrado. Se creó uno nuevo en {path}")
        except OSError as e:
            print(f"[CONFIG][ERROR] No se pudo crear el archivo {path}: {e}")
        return config

    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    print(f"[CONFIG][WARN] Línea inválida (sin '='): {line}")
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                if key in config:
                    try:
                        config[key] = int(value)
                    except ValueError:
                        print(f"[CONFIG][ERROR] Valor inválido para '{key}': {value}")
                else:
                    print(f"[CONFIG][WARN] Clave desconocida en config: {key}")

    except OSError as e:
        print(f"[CONFIG][ERROR] No se pudo leer el archivo {path}: {e}")

    return config

class PulseInput:
    def __init__(
        self,
        pin=23,
        callback=None
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
        self._last_pulse_time = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(
            self.pin,
            GPIO.FALLING,           # pulso a GND
            callback=self._handle_event,
            bouncetime=1
        )

    def _handle_event(self, channel):
        now = time.time() * 1000  # ms
        delta = now - self._last_pulse_time
        estado = GPIO.input(self.pin)

        logger.info(f"PULSE | Δ={delta:.1f} ms | estado={estado}")

        if delta < self.debounce_ms:
            logger.info("  -> Ignorado por debounce")
            return

        if estado == GPIO.LOW:
            logger.info("  -> Pulso válido")
            self._last_pulse_time = now
            if self.callback:
                self.callback()
        else:
            logger.info("  -> Evento espurio (no LOW)")

    def cleanup(self):
        GPIO.remove_event_detect(self.pin)