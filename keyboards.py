from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=False)

    kb.row(
        KeyboardButton(" Записать день"),
        KeyboardButton(" Статистика"),
        KeyboardButton(" График")
    )

    kb.row(
        KeyboardButton(" История"),
        KeyboardButton(" Очистить данные"),
        KeyboardButton("Инсайты")
    )

    return kb