from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    category = State()
    delete_category = State()
    name_auto = State()
    price = State()
    description = State()
    img = State()
    kolvo = State()
    engine_power = State()
    id_category = State()
    unique_code = State()


