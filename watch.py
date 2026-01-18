from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import os

log_file = open("app.log", "a")

process = subprocess.Popen(
    ["python3", "app/main.py"],
    stdout=log_file,
    stderr=log_file
)

class RestartHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global process
        if event.src_path.endswith(".py"):
            print("Cambio detectado, reiniciando...")
            process.kill()
            process.wait()
            process = None
            time.sleep(0.5)
            process = subprocess.Popen(
                ["python3", "app/main.py"],
                stdout=log_file,
                stderr=log_file
            )

observer = Observer()
observer.schedule(RestartHandler(), path=".", recursive=True)
observer.start()

print("Watcher activo")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
