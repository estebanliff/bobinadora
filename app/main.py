import tkinter as tk
from tkinter import font
from keypad import TargetCounter
from PIL import Image, ImageTk
from toggleSwitch import ToggleSwitch
from pulse_input import PulseInput
from counter import Counter
from motor import Motor

# -------------------------------------------------
# Configuración general
# -------------------------------------------------
WIDTH = 1024
HEIGHT = 600
BG_COLOR = "#1e1e1e"

root = tk.Tk()
root.title("HMI Contador de Vueltas")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg=BG_COLOR)

root.attributes("-fullscreen", True)

root.after(500, lambda: root.attributes("-fullscreen", True))

def close_app():
    root.destroy()   # cierra limpio tkinter

# Salir con ESC (solo para desarrollo)
root.bind("<Escape>", close_app)

def close_app():
    root.destroy()   # cierra limpio tkinter
def press_effect(btn, pressed_color="#CDCDCD", normal_color="#555555", delay=120):
    btn.config(bg=pressed_color, state="normal")
    root.after(delay, lambda: btn.config(bg=normal_color, state="normal"))
    
BTN_SIZE = 130
DIGITS = 4

# -------------------------------------------------
# Estados
# -------------------------------------------------
motor_running = False
current_count = Counter()
motor_controller = Motor()

target_logic = TargetCounter(digits=DIGITS)
target_var = tk.StringVar(value=target_logic.get_display())

# -------------------------------------------------
# Fuentes
# -------------------------------------------------
FONT_TITLE = ("Arial", 18, "bold")
FONT_BUTTON = ("Arial", 22, "bold")

# -------------------------------------------------
# Imagenes
# -------------------------------------------------
motor_on_img = Image.open("img/MotorOn.png").resize(
    (BTN_SIZE, BTN_SIZE), Image.LANCZOS
)
motor_on_img = ImageTk.PhotoImage(motor_on_img)

motor_off_img = Image.open("img/MotorOff.png").resize(
    (BTN_SIZE, BTN_SIZE), Image.LANCZOS
)
motor_off_img = ImageTk.PhotoImage(motor_off_img)

# Si la fuente 7 segmentos está instalada
try:
    FONT_7SEG_BIG = font.Font(family="DSEG7 Classic", size=65)
    FONT_7SEG_SMALL = font.Font(family="DSEG7 Classic", size=44)
except:
    FONT_7SEG_BIG = font.Font(family="Arial", size=65, weight="bold")
    FONT_7SEG_SMALL = font.Font(family="Arial", size=44, weight="bold")

# -------------------------------------------------
# Frames principales
# -------------------------------------------------
top_frame = tk.Frame(root, bg=BG_COLOR, height=150)
mid_frame = tk.Frame(root, bg=BG_COLOR)
bottom_frame = tk.Frame(root, bg=BG_COLOR, height=140)

top_frame.pack(fill="x")
mid_frame.pack(fill="both", expand=True)
bottom_frame.pack(fill="x")


# =================================================
# ZONA SUPERIOR – CONTADOR ACTUAL
# =================================================
top_row = tk.Frame(top_frame, bg=BG_COLOR)
top_row.pack(fill="x", padx=20, pady=5)

#tk.Label(
#    top_row,
#    text="CONTADOR ACTUAL",
#    font=FONT_TITLE,
#    fg="white",
#    bg=BG_COLOR
#).pack(side="left", padx=(0, 20))

top_row = tk.Frame(top_frame, bg=BG_COLOR)
top_row.pack(fill="x", padx=20, pady=5)

# ---------- IZQUIERDA: OBJETIVO ----------
left_top = tk.Frame(top_row, bg=BG_COLOR)
left_top.pack(side="left")

target_display = tk.Label(
    left_top,
    textvariable=target_var,
    font=FONT_7SEG_SMALL,
    fg="white",
    bg="black",
    width=8,
    anchor="e",
    padx=20,
    pady=10
)
target_display.pack()

# ---------- DERECHA: RESET ----------
right_top = tk.Frame(top_row, bg=BG_COLOR)
right_top.pack(side="right")

def reset_counter():
    current_count.reset()
    counter_var.set(str(current_count.get_value()).zfill(DIGITS))
    press_effect(reset_btn, "#e67e22", "#d35400")

reset_btn = tk.Button(
    right_top,
    text="↺",
    font=("Arial", 48, "bold"),
    bg="#d35400",
    fg="white",
    width=2,
    height=1,
    relief="flat",
    activebackground="#e67e22",
    takefocus=0,
    highlightthickness=0,
    command=reset_counter
)
reset_btn.pack()

# ---------- CENTRO: CONTADOR ACTUAL ----------
center_top = tk.Frame(top_row, bg=BG_COLOR)
center_top.pack(side="left", fill="x", expand=True)

counter_var = tk.StringVar(value=str(current_count.get_value()).zfill(DIGITS))

counter_display = tk.Label(
    center_top,
    textvariable=counter_var,
    font=FONT_7SEG_BIG,
    fg="#4cff4c",
    bg="black",
    width=8,
    anchor="e",
    padx=20,
    pady=10
)
counter_display.pack()

# =================================================
# Boton para cerrar la APP
# =================================================

close_btn = tk.Button(
    top_frame,
    text="✕",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="#c0392b",
    activebackground="#e74c3c",
    relief="flat",
    width=2,
    height=1,
    takefocus=0,
    highlightthickness=0,
    command=close_app
)

close_btn.place(
    x=10,
    y=10
)

# =================================================
# ZONA CENTRAL – OBJETIVO + TECLADO
# =================================================
left_mid = tk.Frame(mid_frame, bg=BG_COLOR)
right_mid = tk.Frame(mid_frame, bg=BG_COLOR)

left_mid.pack(side="left", fill="y", padx=20, pady=10)
right_mid.pack(side="right", fill="both", expand=False, padx=20, pady=10)

keypad_buttons = [reset_btn]

def set_target_value(value):
    global keypad_buttons
    target_logic.set_value(value)
    target_var.set(target_logic.get_display())

    for btn in keypad_buttons:
        root.after(150, lambda b=btn: b.config(state="normal"))


preset_frame = tk.Frame(left_mid, bg=BG_COLOR)
preset_frame.pack(pady=(0, 10))


# ---- BOTONES CON VUELTAS PREDEFINIDAS
def load_presets_from_file(file_path):
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()

        if not content:
            return []

        return [item.strip() for item in content.split(",")]

    except OSError:
        return []

TARGET_PRESETS = load_presets_from_file("cfg/presets.txt")

for i, val in enumerate(TARGET_PRESETS):
    btn = None
    btn = tk.Button(
        preset_frame,
        text=str(val),
        font=FONT_BUTTON,
        bg="#555555",
        activebackground="#CDCDCD",
        fg="white",
        width=6,
        height=2,
        command=lambda v=val: set_target_value(v)
    )
    if i>=2:
        row = 1
        col = i - 2
    else:
        row = 0
        col = i
    btn.grid(row=row, column=col, padx=10, pady=8, sticky="nsew")
    keypad_buttons.append(btn)



# ---- TOOGLE DE BAJA VELOCIDAD
def low_speed_toogle(state):
    low_speed_var.set(state)
    motor_controller.set_low_speed(state)


low_speed_row = tk.Frame(left_mid, bg=BG_COLOR)
low_speed_row.pack(fill="x", pady=(10, 0))

low_speed_var = tk.BooleanVar(value=False)

low_speed_switch = ToggleSwitch(
    low_speed_row,
    initial=False,
    command=lambda state: low_speed_toogle(state)
)
low_speed_switch.pack(side="left", padx=(0,20))

low_speed_label = tk.Label(
    low_speed_row,
    text="Baja velocidad",
    font=FONT_BUTTON,
    fg="white",
    bg=BG_COLOR
)
low_speed_label.pack(side="left")


# ----- Teclado numérico
keys = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["0", "←", "🗑"]
]


def on_keypad_press(key):
    target_logic.press(key)

    # Actualizar display mientras se escribe
    target_var.set(target_logic.get_display())

    for btn in keypad_buttons:
        root.after(150, lambda b=btn: b.config(state="normal"))

def disable_keypad():
    global keypad_buttons
    for btn in keypad_buttons:
        btn.config(state="disabled")

def enable_keypad():
    global keypad_buttons
    for btn in keypad_buttons:
        btn.config(state="normal")

for r, row in enumerate(keys):
    for c, key in enumerate(row):
        btn = tk.Button(
            right_mid,
            text=key,
            font=FONT_BUTTON,
            bg="#333333",
            activebackground="#CDCDCD",
            fg="white",
            width=6,
            height=1,
            command=lambda k=key: on_keypad_press(k)
        )
        btn.grid(row=r, column=c, padx=12, pady=12, sticky="nsew")
        keypad_buttons.append(btn)

for i in range(3):
    right_mid.columnconfigure(i, weight=1)
for i in range(4):
    right_mid.rowconfigure(i, weight=1)


# =================================================
# ZONA INFERIOR – MOTOR ON / OFF
# =================================================
def update_motor_ui():
    if motor_running:
        motor_on_btn.config(bg="#2ecc71", state="normal")
        disable_keypad()
    else:
        motor_on_btn.config(bg="green", state="normal")
        enable_keypad()

def start_motor():
    global motor_running

    if motor_running:
        return

    motor_running = True
    update_motor_ui()
    motor_controller.arrancar(solo_baja_velocidad=low_speed_var.get())

def stop_motor():
    global motor_running

    if not motor_running:
        return

    motor_controller.parar_rapido()
    motor_running = False
    update_motor_ui()

motor_on_btn = tk.Button(
    bottom_frame,
    image=motor_on_img,
    width=BTN_SIZE*3,
    height=BTN_SIZE,
    bg="green",
    activebackground="#2ecc71",
    relief="flat",
    bd=0,
    command=start_motor
)

motor_on_btn.pack(side="left", expand=True, padx=40, pady=20)

motor_off_btn = tk.Button(
    bottom_frame,
    image=motor_off_img,
    width=BTN_SIZE*3,
    height=BTN_SIZE,
    bg="red",
    #activebackground="#e74c3c",
    activebackground="red",
    relief="flat",
    bd=0,
    command=stop_motor
)

motor_off_btn.pack(side="right", expand=True, padx=40, pady=20)

# =================================================
# EVENTOS EXTERNOS
# =================================================

def evento_motor():
    global motor_running
    motor_running = motor_controller.esta_girando()
    root.after(0, update_motor_ui )

motor_controller.set_evento_motor(evento_motor)

def incrementar_contador():
    global current_count
    global counter_var
    global target_logic

    current_count.increment()
    counter_var.set(str(current_count.get_value()).zfill(DIGITS))
    vueltas_faltantes = target_logic.get_value() - current_count.get_value()
    motor_controller.set_vueltas_faltantes(vueltas_faltantes)


def on_pulse():
    root.after(0, incrementar_contador )


pulse_listener = PulseInput(
    pin=23,
    callback=on_pulse,
    debounce_ms=150
)

# -------------------------------------------------
root.mainloop()
