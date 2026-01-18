import os

class Counter:
    def __init__(self, digits=6, max_value=999999, file_path="cfg/contador.txt"):
        self.digits = digits
        self.max_value = max_value
        self.file_path = file_path

        self.value = self._load_from_file()

        if self.value > self.max_value:
            self.value = self.max_value
            self._save_to_file()

    # -------------------------
    # Persistencia
    # -------------------------
    def _load_from_file(self):
        if not os.path.exists(self.file_path):
            return 0

        try:
            with open(self.file_path, "r") as f:
                return int(f.read().strip())
        except (ValueError, OSError):
            return 0

    def _save_to_file(self):
        try:
            with open(self.file_path, "w") as f:
                f.write(str(self.value))
        except OSError:
            pass  # opcional: log de error

    # -------------------------
    # API pública
    # -------------------------
    def get_value(self):
        return self.value

    def increment(self):
        if self.value < self.max_value:
            self.value += 1
            self._save_to_file()

    def reset(self):
        self.value = 0
        self._save_to_file()
