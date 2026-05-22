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


def mood_keyboard():
    kb = InlineKeyboardMarkup(row_width=5)

    moods = [
        ("1 😞", "mood_1"),
        ("2 😐", "mood_2"),
        ("3 🙂", "mood_3"),
        ("4 😊", "mood_4"),
        ("5 🤩", "mood_5")
    ]

    buttons = [
        InlineKeyboardButton(text, callback_data=data)
        for text, data in moods
    ]

    kb.add(*buttons)

    return kb


def work_keyboard():
    kb = InlineKeyboardMarkup(row_width=3)

    values = ["0.5", "1", "2", "4", "6"]

    buttons = [
        InlineKeyboardButton(f"{v} ч", callback_data=f"work_{v}")
        for v in values
    ]

    kb.add(*buttons)

    kb.add(
        InlineKeyboardButton(
            "Другое",
            callback_data="work_other"
        )
    )

    return kb


def sleep_keyboard():
    kb = InlineKeyboardMarkup(row_width=3)

    values = ["6", "7", "8", "9", "10"]

    buttons = [
        InlineKeyboardButton(f"{v} ч", callback_data=f"sleep_{v}")
        for v in values
    ]

    kb.add(*buttons)

    kb.add(
        InlineKeyboardButton(
            "Другое",
            callback_data="sleep_other"
        )
    )

    return kb


def skip_keyboard():
    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton(
            "Пропустить",
            callback_data="skip_comment"
        )
    )

    return kb