import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog
import sqlite3
from datetime import datetime
from tkinter import scrolledtext
import os

def connect_to_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Создаем или открываем базу данных
    db_path = os.path.join(base_dir, "database", "shoe_store.db")
    
    # Создаем или открываем базу данных
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    return conn, c


def close_connection(conn):
    conn.close()


def insert_good(name, brand, size, color, price, quantity, category_id):
    conn, c = connect_to_db()
    sql = """INSERT INTO Products (Name, Brand, Size, Color, Price, QuantityInStock, CategoryID) 
             VALUES (?, ?, ?, ?, ?, ?, ?)"""
    try:
        c.execute(sql, (name, brand, size, color, price, quantity, category_id))
        conn.commit()
        messagebox.showinfo("Успех", f"Товар '{name}' добавлен в базу данных.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при добавлении товара: {e}")
    close_connection(conn)


def get_goods():
    conn, c = connect_to_db()
    c.execute("SELECT * FROM Products")
    rows = c.fetchall()
    close_connection(conn)
    return rows


def delete_good(good_id):
    conn, c = connect_to_db()
    sql = """DELETE FROM Products WHERE ProductID = ?"""
    try:
        c.execute(sql, (good_id,))
        if c.rowcount == 0:
            messagebox.showerror("Ошибка", f"Товар с ID {good_id} не найден.")
        else:
            conn.commit()
            messagebox.showinfo("Успех", f"Товар с ID {good_id} удален из базы данных.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при удалении товара: {e}")
    close_connection(conn)


def delete_employee(employee_id):
    conn, c = connect_to_db()
    sql = """DELETE FROM Employees WHERE EmployeeID = ?"""
    try:
        c.execute(sql, (employee_id,))
        if c.rowcount == 0:
            messagebox.showerror("Ошибка", f"Продавец с ID {employee_id} не найден.")
        else:
            conn.commit()
            messagebox.showinfo(
                "Успех", f"Продавец с ID {employee_id} удален из базы данных."
            )
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при удалении продавца: {e}")
    close_connection(conn)


def add_good():
    dialog = tk.Toplevel()
    dialog.title("Добавить товар")

    tk.Label(dialog, text="Введите название товара:").pack()
    name_entry = tk.Entry(dialog)
    name_entry.pack()

    tk.Label(dialog, text="Введите бренд товара:").pack()
    brand_entry = tk.Entry(dialog)
    brand_entry.pack()

    tk.Label(dialog, text="Введите размер товара:").pack()
    size_entry = tk.Entry(dialog)
    size_entry.pack()

    tk.Label(dialog, text="Введите цвет товара:").pack()
    color_entry = tk.Entry(dialog)
    color_entry.pack()

    tk.Label(dialog, text="Введите цену:").pack()
    price_entry = tk.Entry(dialog)
    price_entry.pack()

    tk.Label(dialog, text="Введите количество:").pack()
    quantity_entry = tk.Entry(dialog)
    quantity_entry.pack()

    tk.Label(dialog, text="Введите ID категории:").pack()
    category_id_entry = tk.Entry(dialog)
    category_id_entry.pack()
    def submit():
        name = name_entry.get()
        brand = brand_entry.get()
        size = size_entry.get()
        color = color_entry.get()
        price = price_entry.get()
        quantity = quantity_entry.get()
        category_id = category_id_entry.get()
        if (
            name
            and brand
            and color
            and price.replace(".", "", 1).isdigit()
            and quantity.isdigit()
            and (size.replace(".", "", 1).isdigit() or size == "")):
            size = float(size) if size else None
            price = float(price)
            quantity = int(quantity)
            category_id = int(category_id)
            existing_good = get_good_by_name_and_brand(name, brand)
            if existing_good:
                existing_quantity = existing_good["quantity"] + quantity
                update_good(
                    existing_good["id"],
                    name,
                    brand,
                    size,
                    color,
                    price,
                    existing_quantity,
                    category_id,)  # Функция для обновления товара
            else:
                insert_good(name, brand, size, color, price, quantity, category_id)
            dialog.destroy()
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные данные.")
    tk.Button(dialog, text="Добавить товар", command=submit).pack()


def get_good_by_name_and_brand(name, brand):
    conn, c = connect_to_db()
    c.execute("SELECT * FROM Products WHERE Name = ? AND Brand = ?", (name, brand))
    good = c.fetchone()
    close_connection(conn)
    if good:
        return {"id": good[0], "quantity": good[6]}
    return None


def update_good(good_id, name, brand, size, color, price, quantity, category_id):
    conn, c = connect_to_db()
    c.execute(
        "UPDATE Products SET Name = ?, Brand = ?, Size = ?, Color = ?, Price = ?, QuantityInStock = ?, CategoryID = ? WHERE ProductID  = ?",
        (name, brand, size, color, price, quantity, category_id, good_id),
    )
    conn.commit()
    close_connection(conn)


def show_goods():
    goods = get_goods()
    if not goods:
        messagebox.showinfo("Список товаров", "Список товаров пуст.")
    else:
        goods_list = "\n".join(
            [
                f"ID: {row[0]}, Название: {row[1]}, Бренд: {row[2]}, Размер: {row[3]}, Цвет: {row[3]},Цена: {row[3]}"
                for row in goods
            ]
        )
        messagebox.showinfo("Список товаров", goods_list)


def remove_good():
    good_id = simpledialog.askinteger(
        "Удалить товар", "Введите ID товара для удаления:"
    )
    if good_id is not None:
        delete_good(good_id)


def show_employees():
    # Получаем данные о продавцах вместе с их данными о продажах
    conn, c = connect_to_db()

    c.execute(
        """
        SELECT 
            e.EmployeeID, 
            e.FirstName, 
            e.LastName, 
            e.Username, 
            COUNT(o.OrderID) AS SalesCount, 
            SUM(o.TotalAmount) AS TotalSales
        FROM 
            Employees e
        LEFT JOIN 
            Orders o ON e.EmployeeID = o.SalespersonID
        GROUP BY 
            e.EmployeeID
    """
    )
    employees = c.fetchall()

    if not employees:
        messagebox.showinfo("Список продавцов", "Список продавцов пуст.")
    else:
        employees_list = "\n\n".join(
        [
            f"ID: {row[0] if row[0] is not None else 'Не указано'}\n"
            f"Имя: {row[1] if row[1] is not None else 'Не указано'}\n"
            f"Фамилия: {row[2] if row[2] is not None else 'Не указано'}\n"
            f"Логин: {row[3] if row[3] is not None else 'Не указано'}\n"
            f"Количество продаж: {row[4] if row[4] is not None else 0}\n"
            f"Общая сумма продаж: {row[5] if row[5] is not None else 0:.2f} руб.\n"  # Проверка на None
            f"{'-' * 40}"  # Разделитель между продавцами
            for row in employees
        ]
    )

        messagebox.showinfo("Список продавцов", employees_list)
    conn.commit()
    close_connection(conn)


def remove_employee():
    employee_id = simpledialog.askinteger(
        "Удалить продавца", "Введите ID продавца для удаления:"
    )
    if employee_id is not None:
        delete_employee(employee_id)


def stat_store():
    conn, cursor = connect_to_db()

    # Запрос для получения всех заказов и суммы продаж
    cursor.execute(
        """
        SELECT OrderID, OrderDate, TotalAmount FROM Orders
    """
    )

    # Получение всех заказов
    orders = cursor.fetchall()

    # Создание строки для вывода всех заказов
    output = "Все продажи магазина:\n"
    for order in orders:
        output += f"ID Заказа: {order[0]}, Дата: {order[1]}, Сумма заказа: {order[2]}\n"

    # Запрос для получения суммы всех продаж
    cursor.execute(
        """
        SELECT SUM(TotalAmount) FROM Orders
    """
    )

    total_sales = cursor.fetchone()[0]

    # Добавление суммы продаж в вывод
    output += (
        f"\nСумма продаж за все время: {total_sales if total_sales is not None else 0}"
    )

    conn.close()

    return output


def show_statistics(text_area):
    stats = stat_store()
    text_area.delete(1.0, tk.END)  # Очистка текстового поля
    text_area.insert(tk.END, stats)  # Вставка статистики


def add_order(order_date, customer_id, total_amount, salesperson_id):
    conn, c = connect_to_db()
    c.execute(
        """
        INSERT INTO Orders (OrderDate, CustomerID, TotalAmount, SalespersonID)
        VALUES (?, ?, ?, ?)
    """,
        (order_date, customer_id, total_amount, salesperson_id),
    )
    order_id = c.lastrowid
    conn.commit()
    close_connection(conn)
    messagebox.showinfo("Успех", "Заказ добавлен успешно!")


def add_order_detail(order_id, product_id, quantity):
    conn, c = connect_to_db()
    c.execute(
        """
        INSERT INTO OrderDetails (OrderID, ProductID, Quantity)
        VALUES (?, ?, ?)
    """,
        (order_id, product_id, quantity),
    )
    conn.commit()
    conn.close()


def search_products(search_term, tree):

    conn, c = connect_to_db()
    if search_term.strip() == "":
        c.execute(
            """
            SELECT Products.*, Categories.CategoryName 
            FROM Products 
            LEFT JOIN Categories ON Products.CategoryID = Categories.CategoryID
        """
        )
    else:
        c.execute(
            """
            SELECT Products.*, Categories.CategoryName 
            FROM Products 
            LEFT JOIN Categories ON Products.CategoryID = Categories.CategoryID 
            WHERE Products.Name LIKE ? 
            OR Products.Brand LIKE ? 
            OR CAST(Products.Size AS TEXT) LIKE ? 
            OR Products.Color LIKE ? 
            OR CAST(Products.Price AS TEXT) LIKE ? 
        """,
            (
                "%" + search_term + "%",
                "%" + search_term + "%",
                "%" + search_term + "%",
                "%" + search_term + "%",
                "%" + search_term + "%",
            ),
        )

    products = c.fetchall()
    conn.close()
    for row in tree.get_children():
        tree.delete(row)
    if products:
        for product in products:
            tree.insert("", "end", values=product)
    else:
        messagebox.showinfo("Результаты поиска", "Товары не найдены.")
    close_connection(conn)


def stat_store_goods():
    root = tk.Tk()
    root.title("Статистика продаж магазина")
    text_area = scrolledtext.ScrolledText(root, width=70, height=20)

    button = tk.Button(
        root, text="Показать статистику", command=lambda: show_statistics(text_area)
    )
    button.pack(pady=10)

    text_area.pack(padx=10, pady=10)
    root.mainloop()
