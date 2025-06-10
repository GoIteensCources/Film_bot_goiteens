from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, URLInputFile

from app.commands import CREATE_FILM, DELETE_FILM, FILMS, SEARCH
from app.database import add_film, get_all_films, get_film
from app.fsm import FilmForm, FilmStates
from app.keyboards import (
    BUTTON_CREATE_FILM,
    BUTTON_DELETE,
    BUTTON_LIST_FILM,
    BUTTON_SEARCH,
    FilmCallback,
    films_keyboard_markup,
    menu_keyboards,
)
from settings import DATABASE

router = Router()


# all films
@router.message(Command(FILMS))
@router.message(F.text == BUTTON_LIST_FILM)
async def films(message: Message) -> None:
    films = get_all_films(DATABASE)
    markup = films_keyboard_markup(films)

    await message.answer("All films: ", reply_markup=markup)


# calback for pagination buttons
@router.callback_query(F.data.startswith("page_"))
async def pagination_films(callback: CallbackQuery) -> None:
    page = int(callback.data.split("_")[1])
    films_list = get_all_films(DATABASE)
    keyboard = films_keyboard_markup(films_list, page)

    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@router.callback_query(FilmCallback.filter())
async def callb_film(callback: CallbackQuery, callback_data: FilmCallback) -> None:
    film_id = callback_data.id
    film_data = get_film(DATABASE, film_id)

    text_message = f"Фільм: {film_data["title"]}\nОпис: {film_data["desc"]}\nRating: {film_data["rating"]}"

    if film_data["photo"].startswith("http"):
        photo_type = URLInputFile(
            film_data["photo"],
            filename=f"{film_data["title"]}_poster.{film_data["photo"].split('.')[-1]}",
        )
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
    await message.answer("Введіть назву фільму: ", reply_markup=ReplyKeyboardRemove())


@router.message(FilmForm.title)
async def film_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(FilmForm.desc)
    await message.answer("Введіть опис фільму: ")


@router.message(FilmForm.desc)
async def film_description(message: Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await state.set_state(FilmForm.rating)
    await message.answer("Введіть рейтинг фільму: ")


@router.message(FilmForm.rating)
async def film_rating(message: Message, state: FSMContext):
    if message.text.isdecimal() and len(message.text) <= 3:
        await state.update_data(rating=message.text + "%")
        await state.set_state(FilmForm.photo)
        await message.answer("Додайте постер фільму: ")
    else:
        data = await state.get_data()
        await message.answer(
            f"Ведіть число рейтингу для фільму {data.get("title")} 0-100: "
        )


@router.message(FilmForm.photo)
async def film_poster(message: Message, state: FSMContext):
    if message.photo:
        photo_id = message.photo[-1].file_id
        data_film = await state.update_data(photo=photo_id)

        add_film(DATABASE, data_film)

        await state.clear()
        await message.answer("Фільм збережено!", reply_markup=menu_keyboards())
    else:
        data = await state.get_data()
        await message.answer(f"Це не фото, додайте афішу до {data.get("title")}")


# search
@router.message(Command(SEARCH))
@router.message(F.text == BUTTON_SEARCH)
async def search_film(message: Message, state: FSMContext):
    await state.set_state(FilmStates.search_title)
    await message.answer(
        "Введіть назву фільму для пошуку: ", reply_markup=ReplyKeyboardRemove()
    )


@router.message(FilmStates.search_title)
async def make_search(message: Message, state: FSMContext):
    title = message.text.lower()
    await state.update_data(title=message.text)

    list_films: list[dict] = get_all_films(DATABASE)

    result = [film for film in list_films if title in film["title"].lower()]
    if result:
        for film in result:
            await message.reply(
                f"знайшли: {film["title"]}: {film["desc"]}",
                reply_markup=menu_keyboards(),
            )
            break
    else:
        await message.reply("Нiчого немає", reply_markup=menu_keyboards())

    await state.clear()


# delete
@router.message(Command(DELETE_FILM))
@router.message(F.text == BUTTON_DELETE)
async def delete_film(message: Message, state: FSMContext):
    await state.set_state(FilmStates.delete_film)
    await message.answer(
        "Введіть назву фільму для видалення: ", reply_markup=ReplyKeyboardRemove()
    )


@router.message(FilmStates.delete_film)
async def make_delete(message: Message, state: FSMContext):
    # title = message.text.lower()
    ...
    await state.set_state(FilmStates.delete_confirm)


@router.message(FilmStates.delete_confirm)
async def make_delete_copnfirm(message: Message, state: FSMContext):
    # title = message.text.lower()  # yes/no
    ...

    await state.clear()
