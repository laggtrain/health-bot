from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_gender_keyboard():
    keyboard = InlineKeyboardMarkup()
    
    male_button = InlineKeyboardButton("Мужской", callback_data="gender_male")
    female_button = InlineKeyboardButton("Женский", callback_data="gender_female")
    
    keyboard.row(male_button, female_button)
    
    return keyboard