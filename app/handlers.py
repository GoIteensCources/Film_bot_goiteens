from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, URLInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from app.commands import FILMS, CREATE_FILM
from app.database import get_all_films, get_film, add_film
from app.keyboards import (
    BUTTON_LIST_FILM,
    BUTTON_CREATE_FILM,
    FilmCallback,
    films_keyboard_markup,
    menu_keyboards,
)
from settings import DATABASE
from app.fsm import FilmForm


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

    text_message = f"Фільм: {film_data["title"]}\nОпис: {film_data["desc"]}\nRating: {film_data["rating"]}"
    
    if film_data["photo"].startswith("http"):
        photo_type = URLInputFile(film_data["photo"], 
                                  filename=f"{film_data["title"]}_poster.{film_data["photo"].split('.')[-1]}")
    else:
        photo_type = film_data["photo"]
    
    await callback.message.answer_photo(
        caption=f"{text_message}",
        photo=photo_type,
        filename=f"{film_data["title"]}_poster",
    )
    await callback.answer()


# FSM
@router.message(Command(CREATE_FILM))
@router.message(F.text == BUTTON_CREATE_FILM)
async def create_film(message: Message, state: FSMContext) -> None:
    await state.set_state(FilmForm.title)
    await message.answer(f"Введіть назву фільму: ", reply_markup=ReplyKeyboardRemove())


@router.message(FilmForm.title)
async def film_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(FilmForm.desc)
    await message.answer(f"Введіть опис фільму: ")


@router.message(FilmForm.desc)
async def film_description(message: Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await state.set_state(FilmForm.rating)
    await message.answer(f"Введіть рейтинг фільму: ")


@router.message(FilmForm.rating)
async def film_description(message: Message, state: FSMContext):
    if message.text.isdecimal() and len(message.text) <= 3:
        await state.update_data(rating=message.text+'%')
        await state.set_state(FilmForm.photo)
        await message.answer(f"Додайте постер фільму: ")
    else:
        data = await state.get_data()
        await message.answer(f"Ведіть число рейтингу для фільму {data.get("title")} 0-100: ")


@router.message(FilmForm.photo)
async def film_poster(message: Message, state: FSMContext):
    if message.photo:
        photo_id = message.photo[-1].file_id
        data_film = await state.update_data(photo=photo_id)
        
        add_film(DATABASE, data_film)
        
        await state.clear()
        await message.answer(f"Фільм збережено!", reply_markup=menu_keyboards())
    else:
        data = await state.get_data()
        await message.answer(f"Це не фото, додайте афішу до {data.get("title")}")
