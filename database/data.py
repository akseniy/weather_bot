from aiogram import Router
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from keyboards.keyboard import get_main_keyboard, status_weather
from fsm.fsm import Form
from services.api_client import test_city, weather, forecast

data_router = Router()


@data_router.message(Form.no_city)
async def cmd_start(message: types.Message, state: FSMContext, admin_token, pool):
    city = str(message.text)
    code, json_data = test_city(admin_token=admin_token, city=city)
    if code == 200:
        user_id = message.from_user.id
        async with pool.acquire() as conn:
            await conn.execute("INSERT INTO cities (user_id, city) VALUES ($1, $2)", str(user_id), city)

        await message.answer(
            "Отлично, нашли твой город\n"
            f"Твой город - {city}\n\n"
            "Используй кнопки ниже или команды:\n"
            "/weather - текущая погода\n"
            "/forecast - прогноз на 3 дня\n"
            "/city_change - изменить город\n"
            "/help - список команд",
            reply_markup=get_main_keyboard()
            )

        await state.set_state(Form.city)
    else:
        if json_data['error']['code'] == 1006:
            await message.answer(
            "Извини, твой город не найден\n"
            "Попробуй ввести корректно"
            )
        else:
            await message.answer(
            "Прости, бот сейчас не доступен\n"
            "Попробуй еще раз позже"
            )



@data_router.message(Command("weather"))
async def cmd_weather(message: types.Message, state: FSMContext, admin_token, pool):
    user_id = message.from_user.id

    async with pool.acquire() as conn:
            city = await conn.fetchval("SELECT city FROM cities WHERE user_id = $1", str(user_id))

    code, json_data = weather(admin_token=admin_token, city=city)
    if code == 200:
        temp = json_data['current']['temp_c']
        state_code = json_data['current']['condition']['code']
        status = status_weather(state_code)
        await message.answer(
            f"Ваш город - {city}\n"
            f"Сейчас тут {temp}°C\n"
            f"{status}\n\n"
            "Используй кнопки ниже или команды:\n"
            "/weather - текущая погода\n"
            "/forecast - прогноз на 3 дня\n"
            "/city_change - изменить город\n"
            "/help - список команд",
            reply_markup=get_main_keyboard()
            )

        await state.set_state(Form.city)
    else:
        if json_data['error']['code'] == 1006:
            await message.answer(
            "Извини, твой город не найден\n"
            "Попробуй изменить его"
            )
            await state.set_state(Form.no_city)
        else:
            await message.answer(
            "Прости, бот сейчас не доступен\n"
            "Попробуй еще раз позже"
            )


@data_router.message(Command("forecast"))
async def cmd_forecast(message: types.Message, state: FSMContext, admin_token, pool):
    user_id = message.from_user.id

    async with pool.acquire() as conn:
            city = await conn.fetchval("SELECT city FROM cities WHERE user_id = $1", str(user_id))

    code, json_data = forecast(admin_token=admin_token, city=city)
    if code == 200:
        days = json_data['forecast']['forecastday']
        day1 = days[0]['day']
        state_code = day1['condition']['code']
        status1 = status_weather(state_code)
        day2 = days[1]['day']
        state_code = day2['condition']['code']
        status2 = status_weather(state_code)
        day3 = days[2]['day']
        state_code = day3['condition']['code']
        status3 = status_weather(state_code)
        await message.answer(
            f"Ваш город - {city}\n"
            f"Тут сегодня в среднем {days[0]['day']['avgtemp_c']}°С\n"
            f"{status1}\n\n"
            f"Завтра в среднем - {days[1]['day']['avgtemp_c']}°С\n"
            f"{status2}\n\n"
            f"Послезавтра в среднем - {days[2]['day']['avgtemp_c']}°С\n"
            f"{status3}\n\n\n"
            "/weather - текущая погода\n"
            "/forecast - прогноз на 3 дня\n"
            "/city_change - изменить город\n"
            "/help - список команд",
            reply_markup=get_main_keyboard()
            )

        await state.set_state(Form.city)
    else:
        if json_data['error']['code'] == 1006:
            await message.answer(
            "Извини, твой город не найден\n"
            "Попробуй изменить его"
            )
            await state.set_state(Form.no_city)
        else:
            await message.answer(
            "Прости, бот сейчас не доступен\n"
            "Попробуй еще раз позже"
            )


@data_router.message(Form.change_city)
async def cmd_start(message: types.Message, state: FSMContext, admin_token, pool):
    city = str(message.text)
    code, json_data = test_city(admin_token=admin_token, city=city)
    if code == 200:
        user_id = message.from_user.id
        async with pool.acquire() as conn:
            await conn.execute("UPDATE cities SET city = $1 WHERE user_id = $2", city, str(user_id))

        await message.answer(
            "Отлично, нашли твой город\n"
            f"Твой город - {city}\n\n"
            "Используй кнопки ниже или команды:\n"
            "/weather - текущая погода\n"
            "/forecast - прогноз на 3 дня\n"
            "/city_change - изменить город\n"
            "/help - список команд",
            reply_markup=get_main_keyboard()
            )

        await state.set_state(Form.city)
    else:
        if json_data['error']['code'] == 1006:
            await message.answer(
            "Извини, твой город не найден\n"
            "Попробуй ввести корректно"
            )
            await state.set_state(Form.no_city)
        else:
            await message.answer(
            "Прости, бот сейчас не доступен\n"
            "Попробуй еще раз позже"
            )