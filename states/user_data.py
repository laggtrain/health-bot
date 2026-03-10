from aiogram.dispatcher.filters.state import State, StatesGroup


class UserData(StatesGroup):
    waiting_for_gender = State()      # Ожидание выбора пола
    waiting_for_age = State()         # Ожидание ввода возраста
    waiting_for_weight = State()      # Ожидание ввода веса
    waiting_for_height = State()      # Ожидание ввода роста