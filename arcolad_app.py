# arcolad_app.py
import tkinter as tk
from tkinter import PhotoImage, Canvas, filedialog
from threading import Thread
import time
from datetime import datetime as dt
from PIL import Image, ImageTk, ImageDraw
import fitz  # PyMuPDF
from order_of_colors import OrderOfColors
from job_entry_window import JobEntryWindow
from gradient import Gradient, GradientLabel, GradientButton
from database_handler import DatabaseHandler
from flashing_text import FlashingText
from menu_bar import MenuBar
from tkinter import WORD
from tkinter import END


class ArcoladApp:
    def __init__(self):
        self.root = tk.Tk()
        self.menu_bar = MenuBar(self.root, self)
        self.db_handler = DatabaseHandler()
        self.root.img_pdf = PhotoImage(file="pdf_icon.png")
        self.root.geometry('1290x700')
        self.root.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):

        # Создание рамки для всего приложения
        self.app_frame = tk.Frame(self.root, bd=3, relief=tk.GROOVE)
        self.app_frame.pack(expand=True, fill="both")
        self.flashing_text = FlashingText(self.app_frame)
        # Создание виджетов основного окна приложения
        label_date = tk.Label(self.app_frame, text="Дата:", font=("Arial", 12, "bold"))
        label_date.place(x=10, y=9)
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
        self.paper_format_before_x = tk.Entry(self.app_frame, width=4, font=("Arial", 12, "normal"))
        self.paper_format_before_x.place(x=756, y=40)
        self.setup_validation(self.paper_format_before_x, 4)
        label_paper_format_x = tk.Label(self.app_frame, text="X", font=("Arial", 12, "bold"))
        label_paper_format_x.place(x=797, y=40)
        self.paper_format_after_x = tk.Entry(self.app_frame, width=4, font=("Arial", 12, "normal"))
        self.paper_format_after_x.place(x=815, y=40)
        self.setup_validation(self.paper_format_after_x, 4)
        label_count_cheets = tk.Label(self.app_frame, text="Тираж(шт.):", font=("Arial", 12, "bold"))
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
        label_density = tk.Label(self.app_frame, text="г/м²", font=("Arial", 12, "bold"))
        label_density.place(x=1160, y=80)
        self.density = tk.Entry(self.app_frame, width=4, font=("Arial", 12, "normal"))
        self.density.place(x=1210, y=80)
        self.setup_validation(self.density, 4)
        label_count_plates = tk.Label(self.app_frame, text="Кол-во форм:", font=("Arial", 12, "bold"))
        label_count_plates.place(x=10, y=70)
        self.count_plates = tk.Entry(self.app_frame, width=2, font=("Arial", 12, "normal"))
        self.count_plates.place(x=140, y=70)
        self.setup_validation(self.count_plates, 2)

        gradient = Gradient(start_color=(120, 175, 235), end_color=(248, 247, 250))
        label_plates_format = GradientLabel(self.app_frame, width=250, height=30,  text="Размер печатной формы(мм):", 
            font=("Arial", 12, "bold"), gradient=gradient)
        label_plates_format.place(x=170, y=65)

        self.plates_format_before_x = tk.Entry(self.app_frame, width=4, font=("Arial", 13, "normal"))
        self.plates_format_before_x.place(x=430, y=70)
        self.setup_validation(self.plates_format_before_x, 4)
        label_plates_format_x = tk.Label(self.app_frame, text="X", font=("Arial", 13, "bold"))
        label_plates_format_x.place(x=472, y=70)
        self.plates_format_after_x = tk.Entry(self.app_frame, width=4, font=("Arial", 13, "normal"))
        self.plates_format_after_x.place(x=490, y=70)
        self.setup_validation(self.plates_format_after_x, 4)

        gradient = Gradient(start_color=(120, 175, 235), end_color=(248, 247, 250))
        button_orders_of_colors = GradientButton(self.app_frame, text="Порядок наложения цветов", font=("Arial", 12, "bold"), gradient=gradient, command=self.open_popup)
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
            self.image_item = canvas_image_item  # Set the image_item attribute

            # Bind mouse events to the canvas for moving the image
            self.canvas_show_pdf.bind("<ButtonPress-1>", self.on_canvas_click)
            self.canvas_show_pdf.bind("<B1-Motion>", self.on_canvas_drag)


   

      
    def on_canvas_click(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_canvas_drag(self, event):
        delta_x = event.x - self.start_x
        delta_y = event.y - self.start_y

        self.canvas_show_pdf.move(self.image_item, delta_x, delta_y)

        self.start_x = event.x
        self.start_y = event.y
    
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
        self.root.title("Arcolad-Главный экран")
        self.root.iconbitmap('arcolad_ico.ico')
        # Make the window initially fullscreen
        self.root.attributes('-fullscreen', False)
        # Bind the Escape key to toggle fullscreen mode
        self.root.bind("<Escape>", self.toggle_fullscreen)
        self.root.mainloop()
    
    def toggle_fullscreen(self, event):
        # Toggle fullscreen mode
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

