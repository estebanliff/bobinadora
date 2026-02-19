import RPi.GPIO as GPIO
import threading
import os

def load_tiempos_config(path="cfg/tiempos.txt"):
    config = {
        "tiempo_subida_velocidad": 3,
        "pulso_parada_rapida": 2,
        "vueltas_para_velocidad_baja": 20
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

class Motor:
    def __init__(self, evento=None, pin_gira=17, pin_velocidad=22, pin_parada_rapida=27):
        self.pin_gira = pin_gira
        self.pin_velocidad = pin_velocidad
        self.pin_parada_rapida = pin_parada_rapida
        self.en_marcha = False
        self._vel_timer = None
        self.velocidad_baja = True
        self.evento = evento

        cfg = load_tiempos_config()
        self.tiempo_subida_velocidad = cfg["tiempo_subida_velocidad"]
        self.pulso_parada_rapida = cfg["pulso_parada_rapida"]
        self.vueltas_para_velocidad_baja = cfg["vueltas_para_velocidad_baja"]

        self._parada_timer = None
        self.tiempo_apagado_parada_normal = 5  # segundos

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pin_gira, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.pin_velocidad, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.pin_parada_rapida, GPIO.OUT, initial=GPIO.HIGH)

    def _cancelar_parada_timer(self):
        if self._parada_timer:
            self._parada_timer.cancel()
            self._parada_timer = None
 
    def _programar_alta_velocidad(self):
        self._cancelar_timer()

        self._vel_timer = threading.Timer(
            self.tiempo_subida_velocidad,
            self._pasar_a_alta_velocidad
        )
        self._vel_timer.start()

    def _pasar_a_alta_velocidad(self):
        if not self.en_marcha:
            return

        self.velocidad_baja = False
        GPIO.output(self.pin_velocidad, GPIO.LOW)

    def _cancelar_timer(self):
        if self._vel_timer:
            self._vel_timer.cancel()
            self._vel_timer = None

    def esta_girando(self):
        return self.en_marcha
    
    def set_evento_motor(self, evento):
        self.evento = evento
    
    def arrancar(self, solo_baja_velocidad=False):

        self._cancelar_parada_timer()

        # Seteo baja velocidad
        GPIO.output(self.pin_velocidad, GPIO.HIGH)

        # Activo giro
        GPIO.output(self.pin_gira, GPIO.LOW)

        # Activo señal parada rapida (ahora LOW en marcha)
        GPIO.output(self.pin_parada_rapida, GPIO.LOW)

        if not solo_baja_velocidad:
            self._programar_alta_velocidad()
        
        self.en_marcha = True
        self.velocidad_baja = True

    
    def parar_rapido(self):
        self._cancelar_timer()
        self._cancelar_parada_timer()

        # Desactivar giro
        GPIO.output(self.pin_gira, GPIO.HIGH)

        # Desactivar parada rapida
        GPIO.output(self.pin_parada_rapida, GPIO.HIGH)

        GPIO.output(self.pin_velocidad, GPIO.HIGH)

        self.en_marcha = False
        self.velocidad_baja = True

        if self.evento:
            self.evento()
   
    def parar_normal(self):
        self._cancelar_timer()
        self._cancelar_parada_timer()

        # Primero desactivo giro
        GPIO.output(self.pin_gira, GPIO.HIGH)

        # Programo desactivación diferida de parada_rapida
        self._parada_timer = threading.Timer(
            self.tiempo_apagado_parada_normal,
            lambda: GPIO.output(self.pin_parada_rapida, GPIO.HIGH)
        )
        self._parada_timer.start()

        GPIO.output(self.pin_velocidad, GPIO.HIGH)

        self.en_marcha = False
        self.velocidad_baja = True

        if self.evento:
            self.evento()
    
    def disminuir_velocidad(self):
        # Seteo la baja velocidad
        if self.en_marcha:
            GPIO.output(self.pin_velocidad, GPIO.HIGH)
            self.velocidad_baja = True
    
    def set_vueltas_faltantes(self, vueltas):
        if vueltas <= self.vueltas_para_velocidad_baja and not self.velocidad_baja:
           self.disminuir_velocidad()

        if vueltas <= 0:
            self.parar_normal()

    def cleanup(self):
        self._cancelar_timer()
        self._cancelar_parada_timer()
        GPIO.output(self.pin_gira, GPIO.HIGH)
        GPIO.output(self.pin_parada_rapida, GPIO.HIGH)
        GPIO.cleanup([
            self.pin_gira,
            self.pin_velocidad,
            self.pin_parada_rapida
        ])
    
    def set_low_speed(self, low_speed):
        if not self.en_marcha:
            return

        if low_speed:
            GPIO.output(self.pin_velocidad, GPIO.HIGH)
            self.velocidad_baja = True
            self._cancelar_timer()
        else:
            GPIO.output(self.pin_velocidad, GPIO.LOW)
            self.velocidad_baja = False
