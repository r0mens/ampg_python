# database_handler.py
import sqlite3

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

        
