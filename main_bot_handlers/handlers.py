from aiogram import Router
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from fsm.fsm import Form


def get_main_keyboard():
    buttons = [
        [KeyboardButton(text="/weather"), KeyboardButton(text="/forecast")],
        [KeyboardButton(text="/city_exchange"), KeyboardButton(text="/help")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

base_router = Router()

@base_router.message(default_state, Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        "Привет! Я бот для прогноза погоды.\n"
        "Отправь мне название своего города\n",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(Form.no_city)

@base_router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        "Привет! Я бот для прогноза погоды.\n"
        "Используй кнопки ниже или команды:\n"
        "/weather - текущая погода\n"
        "/forecast - прогноз на 3 дня\n"
        "/city_change - изменить город\n"
        "/help - список команд",
        reply_markup=get_main_keyboard()
    )
    await state.clear()

@base_router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📌 Список команд:\n"
        "/weather - Текущая погода\n"
        "/forecast - Прогноз на 3 дня\n"
        "/city_change - изменить город\n"
        "/start - Главное меню",
        reply_markup=get_main_keyboard()
    )


@base_router.message(Command("city_change"))
async def cmd_change(message: types.Message, state: FSMContext):
    await message.answer(
        "Отправь мне название своего нового города\n", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.change_city)