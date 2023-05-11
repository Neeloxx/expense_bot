import sqlite3
from datetime import datetime
from exceptions import InvalidInputError, InvalidDateError, InvalidAmountError, DatabaseError


def create_table():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                amount REAL,
                date TEXT)''')

    conn.commit()
    conn.close()


def add_expense(description, amount, date):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    if not description:
        raise InvalidInputError('Описание расхода не может быть пустым')

    if not isinstance(amount, (float, int)) or amount <= 0:
        raise InvalidAmountError('Сумма расхода должна быть положительной')

    if not isinstance(date, datetime):
        raise InvalidDateError('Неверный формат даты')

    try:
        c.execute('INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)',
                  (description, amount, date.strftime('%d.%m.%Y')))
        conn.commit()

    except Exception:
        raise DatabaseError('Ошибка базы данных')

    conn.close()


def show_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute('SELECT * FROM expenses')
    rows = c.fetchall()
    expenses = []

    for row in rows:
        expenses.append(row[1:4])

    return expenses



def show_result():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute('SELECT SUM(amount) FROM expenses')
    rows = c.fetchall()
    result = rows[0][0]
    return result




