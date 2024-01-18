# flashing_text.py
import tkinter as tk
from threading import Thread
import time

class FlashingText:
    def __init__(self, master):
        self.master = master
        self.text_label = tk.Label(master, text="Формат бумаги/картона(мм.):", font=("Arial", 12, "bold"))
        self.text_label.place(x=470, y=40)
        Thread(target=self.flashing, daemon=True).start()

    def flashing(self):
        while True:
            self.text_label.config(fg='red', text="1-e значение-это Direction/Grain", font=("Arial", 12, "bold"))
            time.sleep(0.9)
            self.text_label.config(fg='black', text="Формат бумаги/картона(мм.):", font=("Arial", 12, "bold"))
            time.sleep(0.9)
