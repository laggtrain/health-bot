from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from keyboards.default.menu_keyboard import get_menu_keyboard


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    # Отправляем приветствие и меню
    welcome_text = (
        "Привет! 👋\n\n"
        "Я - бот для расчета калорий и КБЖУ (калории, белки, жиры, углеводы).\n"
        "Я помогу вам определить индивидуальные нормы питания для достижения ваших целей:\n"
        "• Похудение\n"
        "• Поддержание веса\n"
        "• Набор массы\n\n"
        "Выберите действие в меню ниже:"
    )
    await message.answer(welcome_text, reply_markup=get_menu_keyboard())
