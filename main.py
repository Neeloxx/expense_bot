import telebot
from telebot import types
from datetime import datetime
from database import create_table, add_expense, show_expenses, show_result
from  exceptions import *

# создаем объект бота
bot = telebot.TeleBot('5966973557:AAGTSMujWR28ClV89okIieeFYaqGrunIggU')

create_table()


# создаем клавиатуру
def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_add = types.KeyboardButton('Добавить расход')
    button_show = types.KeyboardButton('Показать расход')
    keyboard.add(button_add, button_show)
    return keyboard


# обработчик команды start
@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = create_keyboard()
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)


# обработчик кнопки добавлять расходы
@bot.message_handler(func=lambda message: message.text == 'Добавить расход')
def handle_add_expense(message):
    # Отправляем запрос описания расхода
    bot.send_message(message.chat.id, 'Введите описание расхода:')
    bot.register_next_step_handler(message, ask_amount)


def ask_amount(message):
    try:
        # Сохраняем опимание расхода
        description = message.text
        # Отправляем запрос суммы расходов
        bot.send_message(message.chat.id, 'Введите сумму расхода:')
        # сохраняем сумму расхода
        bot.register_next_step_handler(message, ask_date, description)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка {e}')


def ask_date(message, description):
    try:
        # Сохраняем сумму расходов
        amount = float(message.text)
        # Отправляем запрос даты расходов
        bot.send_message(message.chat.id, 'Введите дату расходов в формате дд.мм.гггг:')
        # Сохраняем дату расходов
        bot.register_next_step_handler(message, save_expense, description, amount)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат суммы. Введите число.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


def save_expense(message, description, amount):
    try:
        # Сохраняем сумму расходов
        date = datetime.strptime(message.text, '%d.%m.%Y')
        # Добавляем расход в базу данных
        add_expense(description, amount, date)
        bot.send_message(message.chat.id, 'Расход успешно добавлен!')
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат даты. Введите дату в формате дд.мм.гггг.")
    except (InvalidInputError, InvalidDateError, InvalidAmountError, DatabaseError) as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


# Обработчик кнопки Показать расходы
@bot.message_handler(func=lambda message: message.text == 'Показать расход')
def handle_show_expenses(message):
    try:
        expenses = show_expenses()
        result = show_result()
        if expenses:
            for expense in expenses:
                expense_text = f'Описание: {expense[0]}\nСумма: {expense[1]} руб.\nДата: {expense[2]}'
                bot.send_message(message.chat.id, expense_text)
            result_text = f'Общая сумма за все время {result} руб.'
            bot.send_message(message.chat.id, result_text)
        else:
            bot.send_message(message.chat.id, 'Расходы не найдены.')
    except DatabaseError as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')






bot.polling()
