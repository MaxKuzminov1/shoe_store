import sqlite3
import os

def create_tables():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Создаем или открываем базу данных
    db_path = os.path.join(base_dir, "database", "shoe_store.db")
    
    # Создаем или открываем базу данных
    conn = sqlite3.connect(db_path)


    # Создаем курсор для выполнения SQL-запросов
    cursor = conn.cursor()

    # Создаем таблицы

    # Таблица категорий
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Categories (
        CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
        CategoryName TEXT NOT NULL, 
        Description TEXT
    )
    """
    )

    # Таблица поставщиков
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Suppliers (
        SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        ContactName TEXT,
        Phone TEXT,
        Email TEXT,
        Address TEXT
    )
    """
    )

    # Таблица товаров
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Products (
        ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Brand TEXT,
        Size REAL,
        Color TEXT,
        Price REAL,
        QuantityInStock INTEGER,
        CategoryID INTEGER,
        FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
    )
    """
    )

    # Таблица клиентов
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Email TEXT,
        Phone TEXT,
        Address TEXT
    )
    """
    )

    # Таблица продавцов
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Employees (
            EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Username TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL,
            Phone TEXT,
            Email TEXT
        )
        """
    )

    # Таблица заказов
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Orders (
        OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
        OrderDate TEXT NOT NULL,
        CustomerID INTEGER,
        TotalAmount REAL,
        SalespersonID INTEGER,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
        FOREIGN KEY (SalespersonID) REFERENCES Salespersons(SalespersonID)
    )
    """
    )

    # Таблица деталей заказа
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS OrderDetails (
        OrderDetailID INTEGER PRIMARY KEY AUTOINCREMENT,
        OrderID INTEGER,
        ProductID INTEGER,
        Quantity INTEGER,
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
    )
    """
    )

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

    print("База данных и таблицы успешно созданы!")
