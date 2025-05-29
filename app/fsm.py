from aiogram.fsm.state import State, StatesGroup


class FilmForm(StatesGroup):
    title = State()
    desc = State()
    rating = State()
    photo = State()


class FilmStates(StatesGroup):
    search_title = State()
    
    delete_film = State()
    delete_confirm = State()
    
    edit_film = State()
    
    change_rating = State()
    