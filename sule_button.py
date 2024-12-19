import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
from datetime import datetime
from tkinter import scrolledtext, messagebox, simpledialog
from main_window import *


def open_order_window():
    order_window = tk.Toplevel()
    order_window.title("Добавить заказ")
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")

    tk.Label(order_window, text="Дата заказа:").grid(row=0, column=0)
    order_date_entry = tk.Entry(order_window)
    order_date_entry.insert(0, current_time)
    order_date_entry.grid(row=0, column=1)

    tk.Label(order_window, text="ID клиента:").grid(row=1, column=0)
    customer_id_entry = tk.Entry(order_window)
    customer_id_entry.grid(row=1, column=1)

    tk.Label(order_window, text="ID продавца:").grid(row=2, column=0)
    salesperson_id_entry = tk.Entry(order_window)
    salesperson_id_entry.grid(row=2, column=1)

    tk.Label(order_window, text="ID продукта:").grid(row=3, column=0)
    product_id_entry = tk.Entry(order_window)
    product_id_entry.grid(row=3, column=1)

    tk.Label(order_window, text="Количество:").grid(row=5, column=0)
    quantity_entry = tk.Entry(order_window)
    quantity_entry.grid(row=5, column=1)

    tk.Label(order_window, text="Сумма заказа:").grid(row=6, column=0)
    total_amount_entry = tk.Entry(order_window)
    total_amount_entry.grid(row=6, column=1)

    def update_price_and_total():
        product_id = product_id_entry.get()
        quantity = quantity_entry.get()

        if product_id:
            conn, c = connect_to_db()
            c.execute("SELECT Price FROM Products WHERE ProductID = ?", (product_id,))
            result = c.fetchone()
            close_connection(conn)

            if result:
                price = result[0]
                if quantity.isdigit():
                    total_amount = price * int(quantity)
                    total_amount_entry.delete(0, tk.END)
                    total_amount_entry.insert(0, total_amount)
                else:
                    total_amount_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Ошибка", "Продукт не найден.")
                total_amount_entry.delete(0, tk.END)

    product_id_entry.bind("<FocusOut>", lambda e: update_price_and_total())
    quantity_entry.bind("<FocusOut>", lambda e: update_price_and_total())

    def submit_order():
        order_date = order_date_entry.get()
        customer_id = customer_id_entry.get()
        total_amount = total_amount_entry.get()
        salesperson_id = salesperson_id_entry.get()

        if not order_date or not customer_id or not total_amount or not salesperson_id:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля заказа.")
            return
        try:
            total_amount = float(total_amount)
            order_id = add_order(order_date, customer_id, total_amount, salesperson_id)
            product_id = product_id_entry.get()
            quantity = quantity_entry.get()
            if not product_id or not quantity:
                messagebox.showerror(
                    "Ошибка", "Пожалуйста, заполните все поля деталей заказа."
                )
                return

            try:
                quantity = int(quantity)
                add_order_detail(order_id, product_id, quantity)
                conn, c = connect_to_db()
                c.execute(
                    "UPDATE Products SET QuantityInStock = QuantityInStock - ? WHERE ProductID = ?",
                    (quantity, product_id),
                )
                conn.commit()
                close_connection(conn)
                order_window.destroy()
                messagebox.showinfo("Успех", "Заказ и детали заказа добавлены успешно!")
            except ValueError:
                messagebox.showerror(
                    "Ошибка", "Количество должно быть целым числом, а цена - числом."
                )
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма заказа должна быть числом.")

    tk.Button(order_window, text="Добавить заказ", command=submit_order).grid(
        row=7, columnspan=4
    )
