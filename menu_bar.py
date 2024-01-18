# menu_bar.py
import tkinter as tk
from tkinter import filedialog
from order_of_colors import OrderOfColors
from tkinter import *

class MenuBar:
    def __init__(self, root, app):
    	
        self.app = app
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        format_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Форматы", menu=format_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Помощь", menu=help_menu)
        
        file_menu.add_command(label="Открыть PDF", command=self.open_pdf)
        file_menu.add_command(label="Оформить новый заказ", command=self.new_job)
        file_menu.add_command(label="Изменить", command=self.dummy_command)
        file_menu.add_command(label="Вставить", command=self.dummy_command)
        file_menu.add_command(label="Сохранить", command=self.dummy_command)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=root.destroy)
        format_menu.add_command(label="Форматы бумаги", command=self.dummy_command)
        format_menu.add_command(label="Форматы бумаги советские", command=self.dummy_command)
        format_menu.add_command(label="Рулонные материалы", command=self.dummy_command)
        format_menu.add_command(label="Свои стандарты", command=self.dummy_command)
        format_menu.add_separator()
        format_menu.add_command(label="Часто используемые", command=self.dummy_command)
        help_menu.add_command(label="Инструкция пользователя", command=self.dummy_command)
        help_menu.add_command(label="Связь с разработчиками", command=self.dummy_command)
        help_menu.add_separator()
        help_menu.add_command(label="Справка", command=self.dummy_command)
        
    def dummy_command(self):
        print("This is a dummy command.")
    def new_job(self):
        self.app.create_job_entry_window()
    
    
    def open_pdf(self):
        pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        self.app.filepath_field.delete(1.0, END)
        self.app.filepath_field.insert(1.0, pdf_file_path)
        if pdf_file_path:
            self.app.show_pdf_on_canvas(pdf_file_path)

