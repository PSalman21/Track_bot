import telebot

from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
from charts import create_mood_chart
from analyzer import generate_insights
from config import TOKEN
from database.database import db

from keyboards import (
    main_menu,
    mood_keyboard,
    work_keyboard,
    sleep_keyboard,
    skip_keyboard
)

state_storage = StateMemoryStorage()

bot = telebot.TeleBot(
    TOKEN,
    state_storage=state_storage
)
class States(StatesGroup):
    mood = State()

    work = State()
    custom_work = State()
    

    sleep = State()
    custom_sleep = State()

    comment = State()


@bot.message_handler(commands=['start'])
def start(message):
    text = (
        " Добро пожаловать в Mood Tracker!\n\n"

        "Я помогу отслеживать:\n"
        " настроение\n"
        " продуктивность\n"
        " сон\n\n"

        "Используй кнопки ниже "
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_menu()
    )
    # bot.send_message(
    # message.chat.id,
    # f"Твой ID: {message.from_user.id}"
    # )


@bot.message_handler(commands=['help'])
def help_command(message):
    text = (
        "Mood Tracker — справка\n\n"

        "Команды:\n"
        "/start — главное меню\n"
        "/help — справка\n"
        "/history — последние записи\n"
        "/stats — статистика\n"
        "/clear — удалить все данные\n\n"

        "Функции бота:\n"
        "• Запись дня — добавить настроение, работу и сон\n"
        "• История — посмотреть прошлые записи\n"
        "• Статистика — средние значения\n"
        "• График — визуализация настроения\n"
        "• Инсайты — анализ твоих данных\n"
    )

    bot.send_message(message.chat.id, text)





@bot.message_handler(commands=['clear'])
def clear_data(message):

    db.clear_user_data(message.from_user.id)

    bot.send_message(
        message.chat.id,
        "Все ваши данные удалены."
    )






@bot.message_handler(func=lambda m: m.text == "Инсайты")
def insights(message):

    rows = db.get_all_entries(message.from_user.id)

    text = generate_insights(rows)

    bot.send_message(
        message.chat.id,
        text
    )

@bot.message_handler(func=lambda m: m.text == "Записать день")
def add(message):


    bot.set_state(
        message.from_user.id,
        States.mood,
        message.chat.id
    )



    bot.send_message(
        message.chat.id,
        "Оцени настроение от 1 до 5:",
        reply_markup=mood_keyboard()
    )


@bot.message_handler(state=States.custom_work)
def custom_work(message):

    
    try:
        work = float(message.text)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["work"] = work

        bot.set_state(
            message.from_user.id,
            States.sleep,
            message.chat.id
        )

        bot.send_message(
            message.chat.id,
            "Сколько часов ты спал?",
            reply_markup=sleep_keyboard()
        )

    except:
        bot.send_message(
            message.chat.id,
            "Введите число."
        )


@bot.message_handler(state=States.custom_sleep)
def custom_sleep(message):

    try:
        sleep = float(message.text)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["sleep"] = sleep

        bot.set_state(
            message.from_user.id,
            States.comment,
            message.chat.id
        )

        bot.send_message(
            message.chat.id,
            "Добавь комментарий или пропусти:",
            reply_markup=skip_keyboard()
        )

    except:
        bot.send_message(
            message.chat.id,
            "Введите число."
        )




@bot.message_handler(state=States.comment)
def save_comment(message):

    comment = message.text

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

        mood = data["mood"]
        work = data["work"]
        sleep = data["sleep"]

    db.add_entry(
        user_id=message.from_user.id,
        mood=mood,
        work=work,
        sleep=sleep,
        comment=comment
    )

    bot.send_message(
        message.chat.id,
        " Данные сохранены!"
    )

    bot.delete_state(
        message.from_user.id,
        message.chat.id
    )


@bot.message_handler(commands=['history'])
@bot.message_handler(func=lambda m: m.text == "История")
def history(message):

    rows = db.get_history(message.from_user.id)

    if not rows:
        bot.send_message(
            message.chat.id,
            "История пуста."
        )
        return

    text = " Последние записи:\n\n"

    for row in rows:

        text += (
            f" {row[0]}\n"
            f" Настроение: {row[1]}\n"
            f" Работа: {row[2]} ч\n"
            f" Сон: {row[3]} ч\n"
            f" {row[4]}\n\n"
        )

    bot.send_message(
        message.chat.id,
        text
    )



    
@bot.message_handler(commands=['stats'])
@bot.message_handler(func=lambda m: m.text == "Статистика")
def stats(message):

    stats = db.get_stats(message.from_user.id)

    if not stats:
        bot.send_message(
            message.chat.id,
            "Нет данных."
        )
        return

    avg1 = round(stats[0], 2) if stats[0] else 0
    avg2 = round(stats[1], 2) if stats[1] else 0
    avg3 = round(stats[2], 2) if stats[2] else 0

    text = (
        "Твоя статистика:\n\n"

        f"Среднее настроение: {avg1}\n"
        f"Средняя работа: {avg2} ч\n"
        f"Средний сон: {avg3} ч"
    )

    bot.send_message(
        message.chat.id,
        text
    )


#Callback handlers

@bot.callback_query_handler(func=lambda call: call.data.startswith("mood_"))
def get_mood(call):

    mood = int(call.data.split("_")[1])

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data["mood"] = mood

    bot.set_state(
        call.from_user.id,
        States.work,
        call.message.chat.id
    )

    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None
    )

    bot.send_message(
        call.message.chat.id,
        "Сколько часов ты работал/учился?",
        reply_markup=work_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("work_"))
def get_work(call):

    value = call.data.split("_")[1]
    if value == "other":

        bot.set_state(
            call.from_user.id,
            States.custom_work,
            call.message.chat.id
        )

        bot.send_message(
            call.message.chat.id,
            "Введи количество часов работы:"
        )

        return

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data["work"] = float(value)

    bot.set_state(
        call.from_user.id,
        States.sleep,
        call.message.chat.id
    )

    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None
    )

    bot.send_message(
        call.message.chat.id,
        "Сколько часов ты спал?",
        reply_markup=sleep_keyboard()
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("sleep_"))
def get_sleep(call):

    value = call.data.split("_")[1]

    if value == "other":

        bot.set_state(
            call.from_user.id,
            States.custom_sleep,
            call.message.chat.id
        )

        bot.send_message(
            call.message.chat.id,
            "Введи количество часов сна:"
        )

        return

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data["sleep"] = float(value)




    bot.set_state(
        call.from_user.id,
        States.comment,
        call.message.chat.id
    )

    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None
    )

    bot.send_message(
        call.message.chat.id,
        "Добавь комментарий или пропусти:",
        reply_markup=skip_keyboard()
    )

@bot.callback_query_handler(func=lambda call: call.data == "skip_comment")
def skip_comment(call):

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:

        mood = data["mood"]
        work = data["work"]
        sleep = data["sleep"]

    db.add_entry(
        user_id=call.from_user.id,
        mood=mood,
        work=work,
        sleep=sleep,
        comment=None
    )

    bot.send_message(
        call.message.chat.id,
        " Данные сохранены!"
    )

    bot.delete_state(
        call.from_user.id,
        call.message.chat.id
    )

print("Бот запущен!")
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.infinity_polling()