from pathlib import Path
from tkinter import *
from main_window import *
from register_app import *
from sule_button import *
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсу, который будет работать как в режиме разработки, так и в собранном приложении. """
    try:
        # PyInstaller создает временную папку и хранит пути в атрибуте _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def create_window_admin():
    window = Tk()
    window.geometry("700x500")
    window.configure(bg="#9D8D8F")
    canvas = Canvas(
        window,
        bg="#d9d9da",
        height=500,
        width=700,
        bd=0,
        highlightthickness=0,
        relief="ridge",)
    canvas.place(x=0, y=0)
    username = "admin"
    button_image_1 = ImageTk.PhotoImage(Image.open(resource_path("images/button_1.png")))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=show_employees,
        relief="flat",)
    button_1.place(x=30.0, y=375.0, width=200.0, height=50.0)
    button_image_2 = ImageTk.PhotoImage(Image.open(resource_path("images/button_2.png")))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=stat_store_goods,
        relief="flat",)
    button_2.place(x=30.0, y=436.0, width=200.0, height=50.0)
    button_image_3 = ImageTk.PhotoImage(Image.open(resource_path("images/button_3.png")))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=add_good,
        relief="flat",)
    button_3.place(x=470.0, y=375.0, width=200.0, height=50.0)
    button_image_4 = ImageTk.PhotoImage(Image.open(resource_path("images/button_4.png")))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=remove_good,
        relief="flat",)
    button_4.place(x=470.0, y=436.0, width=200.0, height=50.0)
    button_image_5 = ImageTk.PhotoImage(Image.open(resource_path("images/button_5.png")))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=on_login,
        relief="flat",)
    button_5.place(x=250.0, y=375.0, width=200.0, height=50.0)
    button_image_7 = ImageTk.PhotoImage(Image.open(resource_path("images/button_7.png")))
    button_7 = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=remove_employee,
        relief="flat",)
    button_7.place(x=250.0, y=436.0, width=200.0, height=50.0)
    entry_image_1 = ImageTk.PhotoImage(Image.open(resource_path("images/entry_1.png")))
    entry_1 = Entry(bd=0, bg="#BCA4B4", fg="#000000", highlightthickness=0)
    entry_1.place(x=33.0, y=16.0, width=634.0, height=47.0)
    button_image_8 = ImageTk.PhotoImage(Image.open(resource_path("images/button_8.png")))
    button_8 = Button(
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: search_products(entry_1.get(), tree),
        relief="flat",)
    button_8.place(x=640.0, y=16.0, width=50.0, height=50.0)
    button_image_6 = ImageTk.PhotoImage(Image.open(resource_path("images/button_6.png")))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=open_order_window,
        relief="flat",)
    button_6.place(x=174.0, y=318.0, width=351.0, height=46.0)
    tree = ttk.Treeview(
        window,
        columns=(
            "ProductID",
            "Name",
            "Brand",
            "Size",
            "Color",
            "Price",
            "QuantityInStock",
            "CategoryName",),
        show="headings",)
    tree.heading("ProductID", text="ID")
    tree.heading("Name", text="Название")
    tree.heading("Brand", text="Бренд")
    tree.heading("Size", text="Размер")
    tree.heading("Color", text="Цвет")
    tree.heading("Price", text="Цена")
    tree.heading("QuantityInStock", text="Количество")
    tree.heading("CategoryName", text="Категория")

    tree.column("ProductID", width=10, anchor="center")
    tree.column("Name", width=30, anchor="center")
    tree.column("Brand", width=30, anchor="center")
    tree.column("Size", width=20, anchor="center")
    tree.column("Color", width=30, anchor="center")
    tree.column("Price", width=30, anchor="center")
    tree.column("QuantityInStock", width=40, anchor="center")
    tree.column("CategoryName", width=20, anchor="center")
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    style.configure(
        "Treeview.Heading",
        font=("Arial", 10, "bold"),
        background="lightblue",
        foreground="black",)
    style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
    style.map("Treeview", background=[("selected", "lightgreen")])
    tree.place(x=0.0, y=70.0, width=700.0, height=200.0)
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.place(x=705, y=70, height=200)
    window.resizable(False, False)
    window.mainloop()


# create_window_admin()