from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from settings import PAGE_SIZE


BUTTON_LIST_FILM = "Перелік фільмів"
BUTTON_CREATE_FILM = "Додати новий фільм"
BUTTON_SEARCH = "Знайти фільм"
BUTTON_DELETE = "Видалити фільм"


def menu_keyboards():
    builder = ReplyKeyboardBuilder()

    builder.button(text=BUTTON_LIST_FILM)
    builder.button(text=BUTTON_CREATE_FILM)
    builder.button(text=BUTTON_SEARCH)
    builder.button(text=BUTTON_DELETE)
    
    markup = builder.as_markup()
    markup.resize_keyboard = True
    return markup


# fabric
class FilmCallback(CallbackData, prefix="film", sep=";"):
    id: int
    title: str


def films_keyboard_markup(films_list: list[dict], page:int = 1):
    builder = InlineKeyboardBuilder()

    total_pages = (len(films_list) + PAGE_SIZE-1) // PAGE_SIZE
    start_idx = (page-1) * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE
    
    for index, film in enumerate(films_list[start_idx: end_idx], start=start_idx):
        callback_film = FilmCallback(id=index, title=film["title"])
        builder.button(
            text=f"{callback_film.title}", callback_data=callback_film.pack()
        )
    builder.adjust(1, repeat=True)
    
    # navigation 
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text='< back', callback_data = f"page_{page-1}"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text='forward >', callback_data = f"page_{page+1}"))
    if nav_buttons:
        builder.row(*nav_buttons)
    
    return builder.as_markup()
