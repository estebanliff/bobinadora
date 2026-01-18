# keypad_logic.py

class TargetCounter:
    def __init__(self, digits=6, max_value=999999):
        self.digits = digits
        self.max_value = max_value
        load_value = self.load_target_value()
        if load_value > 0:
            self.buffer = str(load_value)
        else:
            self.buffer = ""
    
    def load_target_value(self):
        try:
            with open("cfg/valor_objetivo.txt", "r") as f:
                value = int(f.read().strip())
                return value
        except:
            return 0
    
    def save_target_value(self, value):
        with open("cfg/valor_objetivo.txt", "w") as f:
            f.write(str(value))

    def press(self, key):
        """
        Procesa una tecla presionada
        """
        if key.isdigit():
            if len(self.buffer) < self.digits:
                self.buffer += key

        elif key == "←":
            self.buffer = self.buffer[:-1]

        elif key == "🗑":
            self.buffer = ""
        
        self.save_target_value(int(self.buffer.zfill(self.digits)))
        
    def get_value(self):
        """
        Confirma el valor ingresado
        """
        if self.buffer == "":
            return 0

        value = int(self.buffer)
        value = min(value, self.max_value)

        return value

    def get_display(self):
        """
        Devuelve el valor formateado para mostrar
        """
        return self.buffer.zfill(self.digits)
    
    def set_value(self, value):
        self.buffer = value
        self.save_target_value(int(self.buffer.zfill(self.digits)))
