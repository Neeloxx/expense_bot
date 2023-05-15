import sqlite3
from datetime import datetime
from exceptions import InvalidInputError, InvalidDateError, InvalidAmountError, DatabaseError


def create_table():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id REAL,
                description TEXT,
                amount REAL,
                date TEXT)''')

    conn.commit()
    conn.close()


def add_expense(user_id, description, amount, date):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    if not description:
        raise InvalidInputError('Описание расхода не может быть пустым')

    if not isinstance(amount, (float, int)) or amount <= 0:
        raise InvalidAmountError('Сумма расхода должна быть положительной')

    if not isinstance(date, datetime):
        raise InvalidDateError('Неверный формат даты')

    try:
        c.execute('INSERT INTO expenses (user_id, description, amount, date) VALUES (?, ?, ?, ?)',
                  (user_id, description, amount, date.strftime('%d.%m.%Y')))
        conn.commit()

    except Exception:
        raise DatabaseError('Ошибка базы данных')

    conn.close()


def show_expenses(user_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute('SELECT * FROM expenses WHERE user_id = ?', (user_id,))
    rows = c.fetchall()
    expenses = []

    for row in rows:
        expenses.append(row[2:5])

    return expenses



def show_result(user_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ?', (user_id,))
    rows = c.fetchall()
    result = rows[0][0]
    return result




