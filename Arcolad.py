import tkinter as tk
import sqlite3
from PIL import Image
from datetime import datetime as dt
from threading import Thread
import time
from tkinter import *
import fitz  # PyMuPDF
from tkinter import Tk, Canvas, PhotoImage, filedialog
from PIL import Image, ImageTk





class OrderOfColors:
    def __init__(self, master):
        self.master = master
        self.order_of_colors = Toplevel(master)
        self.order_of_colors.title("Порядок цветов")
        self.order_of_colors.geometry('270x180+200+100')
        self.order_of_colors.resizable(False, False)
        # Добавьте необходимые виджеты для вашего всплывающего окна
        self.box = Listbox(self.order_of_colors, selectmode=EXTENDED)
        self.box.pack(side=LEFT)
        scroll = Scrollbar(command=self.box.yview)
        scroll.pack(side=LEFT, fill=Y)
        self.box.config(yscrollcommand=scroll.set)
        f = Frame(self.order_of_colors)
        f.pack(side=LEFT, padx=10)
        self.label =Label(f, text="название заказа")
        self.label.pack(anchor=N)
        self.entry = Entry(f)
        self.entry.pack(anchor=S, pady=5)
        Button(f, text="Добавить", command=self.add_item).pack(fill=X)
        Button(f, text="Удалить", command=self.del_list).pack(fill=X)
        Button(f, text="Изменить", command=self.update_item).pack(fill=X)
        Button(f, text="Сохранить", command=self.save_list).pack(fill=X)
        # Переменная для отслеживания обновления
        self.updated = False
        # Загрузка данных из файла при запуске
        self.load_list()
    def add_item(self):
        if self.updated:
            # Если было обновление, вставляем в выбранное место
            select = self.box.curselection()
            if select:
                index = select[0]
                self.box.delete(index)
                self.box.insert(index, self.entry.get())
                self.entry.delete(0, END)
                self.updated = False
        else:
            # В противном случае добавляем в конец
            self.box.insert(END, self.entry.get())
            self.entry.delete(0, END)
    def del_list(self):
        select = list(self.box.curselection())
        select.reverse()
        for i in select:
            self.box.delete(i)
        # Устанавливаем флаг обновления после удаления
        self.updated = True
    def save_list(self):
        with open('list000.txt', 'w') as f:
            f.writelines("\n".join(self.box.get(0, END)))
    def load_list(self):
        try:
            with open('list000.txt', 'r') as f:
                lines = f.read().splitlines()
                self.box.delete(0, END)
                for line in lines:
                    self.box.insert(END, line)
        except FileNotFoundError:
            pass
    def update_item(self):
        select = self.box.curselection()
        if select:
            index = select[0]
            selected_text = self.box.get(index)
            self.entry.delete(0, END)
            self.entry.insert(0, selected_text)
            self.updated = True
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
        if pdf_file_path:
            self.app.show_pdf_on_canvas(pdf_file_path)
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
        #self.flashing_text = FlashingText(self.root)
        self.menu_bar = MenuBar(self.root, self)
        self.db_handler = DatabaseHandler()
        self.root.img_pdf = PhotoImage(file="pdf_icon.png")
        self.root.geometry('1290x700')
        self.root.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):

        # Создание рамки для всего приложения
        self.app_frame = tk.Frame(self.root, bd=5, relief=tk.SOLID)
        self.app_frame.pack(expand=True, fill="both")
        self.flashing_text = FlashingText(self.app_frame)
        # Создание виджетов основного окна приложения
        label_date = tk.Label(self.app_frame, text="Дата:", font=("Arial", 13, "bold"))
        label_date.place(x=10, y=10)
        self.entry_date = tk.Entry(self.app_frame, width=10, font=("Arial", 12, "normal"))
        self.entry_date.place(x=60, y=10)
        self.setup_validation(self.entry_date, 10)
        # Insert the current date when creating the widget
        self.insert_date()
        label_y = tk.Label(self.app_frame, text="г.", font=("Arial", 13, "normal"))
        label_y.place(x=145, y=10)
        label_name = tk.Label(self.app_frame, text="Название заказа:", font=("Arial", 13, "bold"))
        label_name.place(x=160, y=10)
        self.entry_name = tk.Entry(self.app_frame, width=60, font=("Arial", 12, "normal"))
        self.entry_name.place(x=310, y=10)
        label_number = tk.Label(self.app_frame, text="Заказ№:", font=("Arial", 13, "bold"))
        label_number.place(x=870, y=10)
        self.entry_number = tk.Entry(self.app_frame, width=12, font=("Arial", 12, "normal"))
        self.entry_number.place(x=950, y=10)
        label_machine = tk.Label(self.app_frame, text="Машина:", font=("Arial", 13, "bold"))
        label_machine.place(x=870, y=40)
        self.entry_machine = tk.Entry(self.app_frame, width=20, font=("Arial", 12, "normal"))
        self.entry_machine.place(x=950, y=40)
        label_material = tk.Label(self.app_frame, text="Материал(название):", font=("Arial", 13, "bold"))
        label_material.place(x=10, y=40)
        self.material = tk.Entry(self.app_frame, width=30, font=("Arial", 12, "normal"))
        self.material.place(x=190, y=40)
        
        #Формат и направление волокна на бумаге
        #Первая цифра указывает на Grain вдоль которой идет направление
        self.paper_format_before_x = tk.Entry(self.app_frame, width=4, font=("Arial", 13, "normal"))
        self.paper_format_before_x.place(x=756, y=40)
        self.setup_validation(self.paper_format_before_x, 4)
        label_paper_format_x = tk.Label(self.app_frame, text="X", font=("Arial", 13, "bold"))
        label_paper_format_x.place(x=797, y=40)
        self.paper_format_after_x = tk.Entry(self.app_frame, width=4, font=("Arial", 13, "normal"))
        self.paper_format_after_x.place(x=815, y=40)
        self.setup_validation(self.paper_format_after_x, 4)
        label_count_cheets = tk.Label(self.app_frame, text="Тираж(шт.):", font=("Arial", 13, "bold"))
        label_count_cheets.place(x=1055, y=10)
        self.count_sheets = tk.Entry(self.app_frame, width=12, font=("Arial", 12, "normal"))
        self.count_sheets.place(x=1150, y=10)
        self.l_thickness = tk.Label(self.app_frame)
        self.l_thickness.image = tk.PhotoImage(file="thickness.png")
        self.l_thickness.config(image=self.l_thickness.image)
        self.l_thickness.place(x=1140, y=40)
        self.thickness = tk.Entry(self.app_frame, width=7, font=("Arial", 16, "bold"))
        self.thickness.place(x=1180, y=40)
        self.setup_validation(self.thickness, 7)
        label_density = tk.Label(self.app_frame, text="г/м²", font=("Arial", 13, "bold"))
        label_density.place(x=1160, y=80)
        self.density = tk.Entry(self.app_frame, width=4, font=("Arial", 12, "normal"))
        self.density.place(x=1210, y=80)
        self.setup_validation(self.density, 4)
        label_count_plates = tk.Label(self.app_frame, text="Кол-во форм:", font=("Arial", 13, "bold"))
        label_count_plates.place(x=10, y=70)
        self.count_plates = tk.Entry(self.app_frame, width=2, font=("Arial", 12, "normal"))
        self.count_plates.place(x=140, y=70)
        self.setup_validation(self.count_plates, 2)
        label_plates_format = tk.Label(self.app_frame, text="Размер печатной формы(мм):", font=("Arial", 13, "bold"))
        label_plates_format.place(x=170, y=70)
        self.plates_format_before_x = tk.Entry(self.app_frame, width=4, font=("Arial", 13, "normal"))
        self.plates_format_before_x.place(x=430, y=70)
        self.setup_validation(self.plates_format_before_x, 4)
        label_plates_format_x = tk.Label(self.app_frame, text="X", font=("Arial", 13, "bold"))
        label_plates_format_x.place(x=472, y=70)
        self.plates_format_after_x = tk.Entry(self.app_frame, width=4, font=("Arial", 13, "normal"))
        self.plates_format_after_x.place(x=490, y=70)
        self.setup_validation(self.plates_format_after_x, 4)
        button_orders_of_colors = tk.Button(self.app_frame, text="Порядок наложения цветов", font=("Arial", 13, "bold"), command=self.open_popup)
        button_orders_of_colors.place(x=535, y=70)
        self.select_button = tk.Button(self.app_frame, image=self.root.img_pdf, command=self.open_pdf)
        self.select_button.place(x=790, y=70) 
        self.filepath_field = tk.Text(self.app_frame, width=20, height=2, font=("Arial", 12, "normal"), wrap=WORD)
        self.filepath_field.place(x=950, y=70) 
        # Create canvas for displaying images
        self.canvas_show_pdf = Canvas(self.app_frame, width=1255, height=500, bg='green')
        self.canvas_show_pdf.place(x=10, y=120)
       
        
    def open_popup(self):
        # Создайте экземпляр всплывающего окна
        popup_window = OrderOfColors(self.root)
   

    def open_pdf(self):
        pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

        self.filepath_field.delete(1.0, END)
        self.filepath_field.insert(1.0, pdf_file_path)
        if pdf_file_path:
            self.show_pdf_on_canvas(pdf_file_path)

    def show_pdf_on_canvas(self, pdf_file_path):
        doc = fitz.open(pdf_file_path)

        for i in range(doc.page_count):
            page = doc.load_page(i)
            pix = page.get_pixmap()
            pil_img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            pil_img = pil_img.convert("RGBA")

            # Convert PIL image to Tkinter PhotoImage
            tk_image = ImageTk.PhotoImage(pil_img)

            # Update the canvas size to fit the new image
            self.canvas_show_pdf.config(width=tk_image.width(), height=tk_image.height())

            # Display the image on the canvas
            canvas_image_item = self.canvas_show_pdf.create_image(0, 0, anchor=tk.NW, image=tk_image)
            self.canvas_show_pdf.image = tk_image  # Keep a reference to prevent garbage collection

   

      

    
    def setup_validation(self, widget, max_length, validate_func=None):
        if validate_func is None:
            validate_func = self.validate_entry  # Use default validation if none provided
        validation_cmd = self.root.register(lambda P, max_length=max_length: validate_func(P, max_length))
        widget.config(validate="key", validatecommand=(validation_cmd, '%P'))
    def validate_entry(self, new_text, max_length):
        #print(f"Validating: {new_text}, Max Length: {max_length}")
        result = len(new_text) <= max_length
        #print(f"Validation result: {result}")
        return result
    def validate_date(self, new_text):
        # Validate date format (dd.mm.yyyy)
        return re.match(r'^\d{1,2}\.\d{1,2}\.\d{4}$', new_text) is not None
    def save_paper_format(self):
        # Concatenate the values entered before and after 'X' and save to the database...
        before_x = self.paper_format_before_x.get()
        after_x = self.paper_format_after_x.get()
        paper_format = f"{before_x}X{after_x}"    
    
    def save_plates_format(self):
        # Concatenate the values entered before and after 'X' and save to the database...
        plates_before = self.plates_format_before_x.get()
        plates_after = self.plates_format_after_x.get()
        plates_format = f"{plates_before}X{plates_after}" 
       
    def create_job_entry_window(self):
        job_entry_window = JobEntryWindow(self.root)
     
    def insert_date(self):
        # Get the current date and insert it into the Entry
        current_date = dt.now().date()
        formatted_date = current_date.strftime('%d.%m.%Y')
        self.entry_date.insert(0, formatted_date)
        self.entry_date.focus_set()  # Set focus on the date entry
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




