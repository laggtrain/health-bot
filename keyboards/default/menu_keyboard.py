from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    btn1 = KeyboardButton("Ввести свои параметры")
    btn2 = KeyboardButton("Рассчитать КБЖУ")
    
    keyboard.row(btn1)
    keyboard.row(btn2)
    
    return keyboard