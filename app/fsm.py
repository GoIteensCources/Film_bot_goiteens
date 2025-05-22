from aiogram.fsm.state import State, StatesGroup


class FilmForm(StatesGroup):
    title = State()
    desc = State()
    rating = State()
    url = State()
    photo = State()
