import tkinter as tk
import sqlite3
from tkinter import PhotoImage
from tkinter import filedialog
from datetime import datetime as dt
from threading import Thread
import time

class JobEntryWindow:
    def __init__(self, parent):
        self.job_entry_window = tk.Toplevel(parent)
        self.job_entry_window.title("Создание нового заказа")

        # Add widgets for entering job details in job_entry_window...
        label_date = tk.Label(self.job_entry_window, text="Дата:")  
        label_date.grid(row=0, column=0, padx=10, pady=10)
        self.entry_date = tk.Entry(self.job_entry_window)
        self.entry_date.grid(row=0, column=1, padx=10, pady=10)

        label_printer_name = tk.Label(self.job_entry_window, text="Машина:")
        label_printer_name.grid(row=1, column=0, padx=10, pady=10)
        self.entry_printer_name = tk.Entry(self.job_entry_window)
        self.entry_printer_name.grid(row=1, column=1, padx=10, pady=10)

        save_button = tk.Button(self.job_entry_window, text="Сохранить", command=self.save_job)
        save_button.grid(row=2, columnspan=2, pady=20)

    def save_job(self):
        # Add code to save job details to the database...
        date = self.entry_date.get()
        printer_name = self.entry_printer_name.get()
        print("Saving job details to the database:", date, printer_name)
        # You can call the necessary method from your main application class to save the job details.
class FlashingText:
    def __init__(self, master):
        self.master = master
        self.text_label = tk.Label(master, text="Формат бумаги/картона(мм.):", font=("Arial", 13, "bold"))
        self.text_label.place(x=470, y=40)
        Thread(target=self.flashing, daemon=True).start()

    def flashing(self):
        while True:
            self.text_label.config(fg='red', text="1-e значение-это Direction/Grain", font=("Arial", 13, "bold"))
            time.sleep(0.9)
            self.text_label.config(fg='black', text="Формат бумаги/картона(мм.):", font=("Arial", 13, "bold"))
            time.sleep(0.9)
class MenuBar:
    def __init__(self, root, app):
        self.app = app
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Помощь", menu=help_menu)

        file_menu.add_command(label="Открыть PDF", command=self.open_pdf)
        file_menu.add_command(label="Оформить новый заказ", command=self.new_job)
        file_menu.add_command(label="Изменить", command=self.dummy_command)
        file_menu.add_command(label="Вставить", command=self.dummy_command)
        file_menu.add_command(label="Сохранить", command=self.dummy_command)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=root.destroy)

        help_menu.add_command(label="Инструкция пользователя", command=self.dummy_command)
        help_menu.add_command(label="Связь с разработчиками", command=self.dummy_command)
        help_menu.add_command(label="Справка", command=self.dummy_command)

        

    def dummy_command(self):
        print("This is a dummy command.")

    def new_job(self):
        self.app.create_job_entry_window()

    
    



    def open_pdf(self):
        pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if pdf_file_path:
            self.app.db_handler.insert_print_job("2023-12-22", "Printer1", "Job1", 1, 100, 50, pdf_file_path)

class DatabaseHandler:
    def __init__(self, db_name='arcolad_database.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        # Create the table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS print_jobs (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                number TEXT NOT NULL,
                machine TEXT NOT NULL,
                material TEXT NOT NULL,
                paper_format TEXT NOT NULL,
                count_sheets TEXT NOT NULL,
                paper_thickness TEXT NOT NULL,
                paper_density TEXT NOT NULL,
                count_plates TEXT NOT NULL,
                plates_format TEXT NOT NULL,
                count_colors_names TEXT NOT NULL,
                description TEXT NOT NULL,
                count_material TEXT NOT NULL,
                count_stock_material TEXT NOT NULL,
                remainder_material TEXT NOT NULL,
                setup_material TEXT NOT NULL,
                inks_print_name TEXT NOT NULL,
                inks_print_job TEXT NOT NULL,
                alco_print_count TEXT NOT NULL,
                pH_print_name TEXT NOT NULL,
                pH_print_count TEXT NOT NULL,
                other_materials_name TEXT NOT NULL,
                other_materials_count TEXT NOT NULL,
                pdf_content BLOB
            )
        ''')
        self.connection.commit()

    def insert_print_job(name, date, number, machine, material, paper_format, count_sheets, paper_thickness,
                         paper_density, count_plates, plates_format, count_colors_names, description,
                          count_material, count_stock_material, remainder_material, setup_material, 
                          inks_print, inks_print_job, alko_print_count, pH_print_name, pH_print_count, 
                          other_materials_name, other_materials_count, pdf_content):
        # Insert a new print job record into the table
        self.cursor.execute('''
            INSERT INTO print_jobs (name, date, number, machine, material, paper_format, count_sheets, paper_thickness, paper_density, count_plates, plates_format, count_colors_names, description, count_material, count_stock_material, remainder_material, setup_material, inks_print, inks_print_job, alko_print_count, pH_print_name, pH_print_count, other_materials_name, other_materials_count, pdf_content)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, date, number, machine, material, paper_format, count_sheets, paper_thickness, paper_density, count_plates, plates_format, count_colors_names, description, count_material, count_stock_material, remainder_material, setup_material, inks_print, inks_print_job, alko_print_count, pH_print_name, pH_print_count, other_materials_name, other_materials_count, pdf_content))
        self.connection.commit()
        print("Inserting job into the database:", name, date, number, machine, material, paper_format, count_sheets, paper_thickness, paper_density, count_plates, plates_format, count_colors_names, description, count_material, count_stock_material, remainder_material, setup_material, inks_print, inks_print_job, alko_print_count, pH_print_name, pH_print_count, other_materials_name, other_materials_count, pdf_content)

    def read_pdf_content(self, pdf_file_path):
        # Read the binary content of the PDF file
        with open(pdf_file_path, 'rb') as file:
            pdf_content = file.read()
        return pdf_content

    def fetch_all_print_jobs(self):
        # Get all print job records from the table
        self.cursor.execute('SELECT * FROM print_jobs')
        return self.cursor.fetchall()

    def close_connection(self):
        # Close the database connection
        self.connection.close()

class ArcoladApp:
    def __init__(self):
        self.root = tk.Tk()
        self.flashing_text = FlashingText(self.root)
        self.menu_bar = MenuBar(self.root, self)
        self.db_handler = DatabaseHandler()
        self.create_widgets()

    def create_widgets(self):
        # Создание виджетов основного окна приложения
        label_date = tk.Label(self.root, text="Дата:", font=("Arial", 13, "bold"))
        label_date.place(x=10, y=10)
        self.entry_date = tk.Entry(self.root, width=9, font=("Arial", 12, "normal"))
        self.entry_date.place(x=60, y=10)
        label_y = tk.Label(self.root, text="г.", font=("Arial", 13, "normal"))
        label_y.place(x=145, y=10)
        label_name = tk.Label(self.root, text="Название заказа:", font=("Arial", 13, "bold"))
        label_name.place(x=160, y=10)
        self.entry_name = tk.Entry(self.root, width=60, font=("Arial", 12, "normal"))
        self.entry_name.place(x=310, y=10)
        label_number = tk.Label(self.root, text="Заказ№:", font=("Arial", 13, "bold"))
        label_number.place(x=870, y=10)
        self.entry_number = tk.Entry(self.root, width=12, font=("Arial", 12, "normal"))
        self.entry_number.place(x=950, y=10)
        label_machine = tk.Label(self.root, text="Машина:", font=("Arial", 13, "bold"))
        label_machine.place(x=870, y=40)
        self.entry_machine = tk.Entry(self.root, width=20, font=("Arial", 12, "normal"))
        self.entry_machine.place(x=950, y=40)
        label_material = tk.Label(self.root, text="Материал(название):", font=("Arial", 13, "bold"))
        label_material.place(x=10, y=40)
        self.material = tk.Entry(self.root, width=30, font=("Arial", 12, "normal"))
        self.material.place(x=190, y=40)
        #Формат и направление волокна на бумаге
        #Первая цифра указывает на Grain вдоль которой идет направление
        self.paper_format_before_x = tk.Entry(self.root, width=4, font=("Arial", 12, "normal"))
        self.paper_format_before_x.place(x=756, y=40)
        label_paper_format_x = tk.Label(self.root, text="X", font=("Arial", 13, "bold"))
        label_paper_format_x.place(x=797, y=40)
        self.paper_format_after_x = tk.Entry(self.root, width=4, font=("Arial", 12, "normal"))
        self.paper_format_after_x.place(x=815, y=40)


        label_count_cheets = tk.Label(self.root, text="Тираж(шт.):", font=("Arial", 13, "bold"))
        label_count_cheets.place(x=1055, y=10)
        self.count_sheets = tk.Entry(self.root, width=12, font=("Arial", 12, "normal"))
        self.count_sheets.place(x=1150, y=10)

        self.l_thickness = tk.Label(self.root)
        self.l_thickness.image = tk.PhotoImage(file="thickness.png")
        self.l_thickness.config(image=self.l_thickness.image)
        self.l_thickness.place(x=1140, y=40)
        self.thickness = tk.Entry(self.root, width=7, font=("Arial", 16, "bold"))
        self.thickness.place(x=1180, y=40)

        label_density = tk.Label(self.root, text="г/м²", font=("Arial", 13, "bold"))
        label_density.place(x=1160, y=80)
        self.density = tk.Entry(self.root, width=4, font=("Arial", 12, "normal"))
        self.density.place(x=1210, y=80)

        label_count_plates = tk.Label(self.root, text="Кол-во форм:", font=("Arial", 13, "bold"))
        label_count_plates.place(x=10, y=70)
        self.count_plates = tk.Entry(self.root, width=2, font=("Arial", 12, "normal"))
        self.count_plates.place(x=140, y=70)
    
    # Register validation functions for each widget
        validate_cmd_density = self.root.register(lambda P: self.validate_entry(P, max_length=4))
        self.density.config(validate="key", validatecommand=(validate_cmd_density, '%P'))

        

    def validate_entry(self, new_text, max_length):
        # Allow only up to max_length characters
        return len(new_text) <= max_length


    def save_job(self):
        # Concatenate the values entered before and after 'X' and save to the database...
        before_x = self.paper_format_before_x.get()
        after_x = self.paper_format_after_x.get()
        paper_format = f"{before_x}X{after_x}"    

        # Insert the current date when creating the widget
        self.insert_date()

    def create_job_entry_window(self):
        job_entry_window = JobEntryWindow(self.root)

    def insert_date(self):
        # Get the current date and insert it into the Entry
        current_date = dt.now().date()
        formatted_date = current_date.strftime('%d.%m.%Y')
        self.entry_date.insert(0, formatted_date)
        print(formatted_date)

    def run(self):
        self.root.title("Arcolad")
        self.root.iconbitmap('arcolad_ico.ico')

        # Make the window initially fullscreen
        self.root.attributes('-fullscreen', False)

        # Bind the Escape key to toggle fullscreen mode
        self.root.bind("<Escape>", self.toggle_fullscreen)
        self.root.mainloop()
    
    def toggle_fullscreen(self, event):
        # Toggle fullscreen mode
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))



if __name__ == '__main__':
    arcolad = ArcoladApp()
    arcolad.run()
