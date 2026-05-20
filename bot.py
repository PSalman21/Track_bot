import telebot
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot import custom_filters

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