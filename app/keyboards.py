from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

BUTTON_LIST_FILM = "Перелік фільмів"
BUTTON_CREATE_FILM = "Додати новий фільм"


def menu_keyboards():
    builder = ReplyKeyboardBuilder()

    builder.button(text=BUTTON_LIST_FILM)
    builder.button(text=BUTTON_CREATE_FILM)

    markup = builder.as_markup()
    markup.resize_keyboard = True
    return markup


# fabric
class FilmCallback(CallbackData, prefix="film", sep=";"):
    id: int
    title: str


def films_keyboard_markup(films_list: list[dict]):
    builder = InlineKeyboardBuilder()

    for index, film in enumerate(films_list):
        callback_film = FilmCallback(id=index, title=film["title"])
        builder.button(
            text=f"{callback_film.title}", callback_data=callback_film.pack()
        )
    builder.adjust(1, repeat=True)
    return builder.as_markup()
