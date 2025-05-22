import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types.bot_command import BotCommand

from app.commands import FILMS, CREATE_FILM
from app.handlers import router
from app.keyboards import menu_keyboards
from settings import TOKEN

dp = Dispatcher()
dp.include_router(router)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Hello, {message.from_user.full_name}!", reply_markup=menu_keyboards()
    )


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands(
        [
            BotCommand(command=FILMS, description="Перегляд списку фільмів"),
            BotCommand(command="start", description="Зaпуск ботa"),
            BotCommand(command=CREATE_FILM, description="новий фільм"),
        ]
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
