import tkinter as tk

class ToggleSwitch(tk.Canvas):
    def __init__(
        self,
        parent,
        width=150,
        height=64,
        bg_off="#CDCDCD",
        bg_on="#2ecc71",
        knob_color="white",
        initial=False,
        command=None
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent["bg"],
            highlightthickness=0
        )

        self.enabled = True
        self.state = initial
        self.command = command

        self.bg_off = bg_off
        self.bg_on = bg_on
        self.knob_color = knob_color

        self.bind("<Button-1>", self.toggle)
        self.draw()

    def enable(self, estado):
        self.enabled = estado

    def draw(self):
        self.delete("all")

        w = int(self["width"])
        h = int(self["height"])
        r = h // 2

        bg_color = self.bg_on if self.state else self.bg_off

        # Fondo
        self.create_oval(0, 0, h, h, fill=bg_color, outline=bg_color)
        self.create_oval(w - h, 0, w, h, fill=bg_color, outline=bg_color)
        self.create_rectangle(r, 0, w - r, h, fill=bg_color, outline=bg_color)

        # Knob
        cx = w - r if self.state else r
        self.create_oval(
            cx - r + 4, 4,
            cx + r - 4, h - 4,
            fill=self.knob_color,
            outline=""
        )

    def toggle(self, event=None):
        if self.enabled:
            self.state = not self.state
            self.draw()
            if self.command:
                self.command(self.state)

    def get(self):
        return self.state

    def set(self, value: bool):
        self.state = value
        self.draw()