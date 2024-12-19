from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
from PIL import Image, ImageTk
import tkinter as tk
import sqlite3
import hashlib
from db_create import *
from gui_user import create_window_user
from gui_admin import create_window_admin
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

def check_credentials_in_db(username):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Создаем или открываем базу данных
    db_path = os.path.join(base_dir, "database", "shoe_store.db")
    
    # Создаем или открываем базу данных
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT Password FROM Employees WHERE Username=?", (username, ))
    result = c.fetchone()
    conn.close()
    return result

def check_credentials():
    username = username_entry.get()
    password = password_entry.get()
    credentials = check_credentials_in_db(username)
    if credentials:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password == credentials[0]:
            messagebox.showinfo("Успех", "Авторизация успешна!")
            window.destroy()
            if username == "admin":
                create_window_admin()
            else:
                create_window_user()
        else:
            messagebox.showerror("Ошибка", "Неверный пароль")
    else:
        messagebox.showerror("Ошибка", "Пользователь не найден")


def reg():
    global window
    window = tk.Tk()
    window.title("Авторизация")
    window.geometry("676x354")
    window.configure(bg="#7161FB")
    background_image = Image.open(resource_path("images/bg.png"))
    background_photo = ImageTk.PhotoImage(background_image)

    global canvas
    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=676,
        width=1280,
        bd=0,
        highlightthickness=0,
        relief="ridge",
    )
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")
    global username_entry, password_entry, login_button

    entry_image_1 = ImageTk.PhotoImage(Image.open(resource_path("images/entry_log.png")))
    entry_bg_1 = canvas.create_image(354.0, 122.5, image=entry_image_1)
    username_entry = Entry(bd=0,
                           bg="#CC8AF2",
                           fg="#000716",
                           highlightthickness=0)
    username_entry.place(x=259.0, y=107.0, width=190.0, height=29.0)

    password_label = ImageTk.PhotoImage(Image.open(resource_path("images/entry_pass.png")))
    password_label = canvas.create_image(354.0, 186.5, image=password_label)
    password_entry = Entry(bd=0,
                           bg="#CC8AF2",
                           fg="#000716",
                           highlightthickness=0,
                           show="*")
    password_entry.place(x=259.0, y=171.0, width=190.0, height=29.0)

    canvas.create_text(
        323.0,
        79.0,
        anchor="nw",
        text="Логин",
        fill="#16113D",
        font=("Inter Medium", 20 * -1),
    )

    canvas.create_text(
        317.0,
        143.0,
        anchor="nw",
        text="Пароль",
        fill="#16113D",
        font=("Inter Medium", 20 * -1),
    )

    login_button_image =  ImageTk.PhotoImage(Image.open(resource_path("images/button_log.png")))
    login_button = Button(
        image=login_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=check_credentials,
        relief="flat",
    )
    login_button.place(x=257.0, y=228.0, width=197.0, height=36.0)
    create_tables()

    # create_widgets()
    window.resizable(False, False)
    window.mainloop()

