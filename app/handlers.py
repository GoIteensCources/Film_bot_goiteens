from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, URLInputFile

from app.commands import FILMS
from app.database import get_all_films, get_film
from app.keyboards import BUTTON_LIST_FILM, FilmCallback, films_keyboard_markup
from settings import DATABASE

router = Router()


@router.message(Command(FILMS))
@router.message(F.text == BUTTON_LIST_FILM)
async def films(message: Message) -> None:
    films = get_all_films(DATABASE)
    markup = films_keyboard_markup(films)

    await message.answer(f"All films: ", reply_markup=markup)


@router.callback_query(FilmCallback.filter())
async def callb_film(callback: CallbackQuery, callback_data: FilmCallback) -> None:
    print(callback_data)
    film_id = callback_data.id
    film_data = get_film(DATABASE, film_id)

    text_message = f"Фільм: {film_data["title"]}\nОпис: {film_data["desc"]}\n"
    poster = film_data["photo"]
    await callback.message.answer_photo(
        caption=f"{text_message}",
        photo=URLInputFile(poster),
        filename=f"{film_data["title"]}_poster",
    )
    await callback.answer()
