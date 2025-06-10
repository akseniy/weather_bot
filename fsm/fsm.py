from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    city = State()
    no_city = State()
    change_city = State()