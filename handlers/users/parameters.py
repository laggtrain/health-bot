from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp
from states.user_data import UserData
from keyboards.inline.gender_keyboard import get_gender_keyboard
from utils.db_api.database import create_user


@dp.message_handler(lambda message: message.text == "Ввести свои параметры")
async def enter_parameters(message: types.Message):
    await message.answer("Введите ваш пол:", reply_markup=get_gender_keyboard())
    await UserData.waiting_for_gender.set()


@dp.callback_query_handler(Text(startswith="gender_"), state=UserData.waiting_for_gender)
async def process_gender(callback_query: types.CallbackQuery, state: FSMContext):
    gender = "Мужской" if callback_query.data == "gender_male" else "Женский"
    
    await state.update_data(gender=gender)
    await callback_query.message.edit_reply_markup(reply_markup=None)  # Убираем клавиатуру
    await callback_query.message.answer("Введите ваш возраст:")
    
    await UserData.waiting_for_age.set()


@dp.message_handler(state=UserData.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age <= 0 or age > 150:
            await message.answer("Возраст должен быть положительным числом до 150 лет. Пожалуйста, введите возраст еще раз:")
            return
        
        await state.update_data(age=age)
        await message.answer("Введите ваш вес:")
        
        await UserData.waiting_for_weight.set()
    except ValueError:
        await message.answer("Пожалуйста, введите возраст в виде числа:")


@dp.message_handler(state=UserData.waiting_for_weight)
async def process_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text.replace(',', '.'))
        if weight <= 0 or weight > 500:
            await message.answer("Вес должен быть положительным числом до 500 кг. Пожалуйста, введите вес еще раз:")
            return
        
        await state.update_data(weight=weight)
        await message.answer("Введите ваш рост:")
        
        await UserData.waiting_for_height.set()
    except ValueError:
        await message.answer("Пожалуйста, введите вес в виде числа:")


@dp.message_handler(state=UserData.waiting_for_height)
async def process_height(message: types.Message, state: FSMContext):
    try:
        height = int(message.text)
        if height <= 0 or height > 300:
            await message.answer("Рост должен быть положительным числом до 300 см. Пожалуйста, введите рост еще раз:")
            return
        
        await state.update_data(height=height)
        
        # Получаем все собранные данные
        data = await state.get_data()
        
        # Сохраняем данные пользователя в базу данных
        chat_id = message.from_user.id
        gender = data['gender']
        age = data['age']
        weight = data['weight']
        height = data['height']
        
        # Создаем или обновляем пользователя в базе данных
        create_user(chat_id=chat_id, gender=gender, age=age, weight=weight, height=height)
        
        # Отправляем подтверждение
        response = f"Ваши параметры:\n"
        response += f"Пол: {data['gender']}\n"
        response += f"Возраст: {data['age']} лет\n"
        response += f"Вес: {data['weight']} кг\n"
        response += f"Рост: {data['height']} см\n\n"
        response += "Параметры сохранены!"
        
        await message.answer(response)
        
        # Завершаем состояние
        await state.finish()
    except ValueError:
        await message.answer("Пожалуйста, введите рост в виде числа:")


@dp.message_handler(lambda message: message.text == "Рассчитать КБЖУ")
async def calculate_nutrition(message: types.Message, state: FSMContext):
    # Получаем chat_id пользователя
    chat_id = message.from_user.id
    
    # Пробуем получить данные из базы данных
    from utils.db_api.database import get_user
    user = get_user(chat_id)
    
    if not user:
        await message.answer("Для расчета КБЖУ необходимо ввести свои параметры. "
                           "Нажмите 'Ввести свои параметры' и заполните все поля.")
        return
    
    # Используем данные из базы данных
    gender = user.gender
    age = user.age
    weight = user.weight
    height = user.height
    
    # Рассчитываем BMR (Basal Metabolic Rate) по формулам:
    # Для мужчин: BMR = (10 × вес в кг) + (6,25 × рост в см) — (5 × возраст) + 5
    # Для женщин: BMR = (10 × вес в кг) + (6,25 × рост в см) — (5 × возраст) — 161
    if gender == "Мужской":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:  # Женский
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    # Рассчитываем TDEE (Total Daily Energy Expenditure) с учетом образа жизни
    # Уровни активности: минимальный, низкий, средний, высокий, экстремальный
    activity_multipliers = {
        "Минимальная активность (сидячий образ жизни)": 1.2,
        "Низкая активность (легкие тренировки 1-3 дня в неделю)": 1.375,
        "Средняя активность (тренировки 3-5 дней в неделю)": 1.55,
        "Высокая активность (интенсивные тренировки 6-7 дней в неделю)": 1.725,
        "Экстремальная активность (физическая работа или двойные тренировки)": 1.9
    }
    
    # Формируем сообщение с результатами
    response = f"Ваши параметры:\n"
    response += f"Пол: {gender}\n"
    response += f"Возраст: {age} лет\n"
    response += f"Вес: {weight} кг\n"
    response += f"Рост: {height} см\n\n"
    response += f"Ваш базовый метаболизм (BMR): {bmr:.2f} ккал/день\n\n"
    response += "Рекомендуемое количество калорий в день в зависимости от уровня активности:\n\n"
    
    for activity, multiplier in activity_multipliers.items():
        tdee = bmr * multiplier
        response += f"{activity}: {tdee:.2f} ккал\n"
    
    await message.answer(response)