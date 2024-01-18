# order_of_colors.py
from tkinter import Toplevel, Listbox, Frame, Label, Entry, Button, Scrollbar, EXTENDED
from tkinter import *


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

