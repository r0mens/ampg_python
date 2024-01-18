# job_entry_window.py
import tkinter as tk
from gradient import Gradient, GradientLabel, GradientButton

class JobEntryWindow:
    def __init__(self, parent):
        self.job_entry_window = tk.Toplevel(parent)
        self.job_entry_window.title("Создание нового заказа")

        
        self.f_job = tk.Frame(self.job_entry_window, relief=tk.SOLID)
        self.f_job.pack(expand=True, fill="both")

        gradient = Gradient(start_color=(120, 175, 235), end_color=(248, 247, 250))
        gradient_label_name_job = GradientLabel(self.f_job, width=150, height=20, text="Название заказа:", gradient=gradient)
        gradient_label_name_job.grid(row=0, column=0, padx=5, pady=5)
        self.entry_name_job = tk.Entry(self.f_job, width=30)
        self.entry_name_job.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        
        label_number_job = tk.Label(self.f_job, text="Заказ №:")
        label_number_job.grid(row=0, column=3, padx=5, pady=5)
        self.entry_number_job = tk.Entry(self.f_job, width=8)
        self.entry_number_job.grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        
        label_material_job = tk.Label(self.f_job, text="Материал(название):")
        label_material_job.grid(row=1, column=0, padx=5, pady=5)
        self.entry_material_job = tk.Entry(self.f_job, width=25)
        self.entry_material_job.grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        gradient_save_button = GradientButton(self.f_job, width=150, height=20, text="Сохранить", gradient=gradient, command=self.save_job)
        gradient_save_button.grid(row=2, columnspan=2, pady=20)

    def save_job(self):
        # Add code to save job details to the database...
        name = self.entry_name_job.get()
        number = self.entry_number_job.get()
        material = self.entry_material_job.get()
        print("Saving job details to the database:", name, number, material)
        # You can call the necessary method from your main application class to save the job details.
