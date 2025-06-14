import asyncio
import datetime as dt
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types.bot_command import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.commands import CREATE_FILM, DELETE_FILM, FILMS, SEARCH
from app.handlers import router
from app.keyboards import menu_keyboards
from settings import TOKEN

logger = logging.getLogger(__name__)

dp = Dispatcher()
dp.include_router(router)
USER_ID = 494037148


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    global USER_ID
    USER_ID = message.from_user.id
    logger.info(f"connect user: {USER_ID}")
    await message.answer(
        f"Hello, {message.from_user.full_name}!with ID {message.from_user.id}",
        reply_markup=menu_keyboards(),
    )


async def message_cron(bot: Bot, user_id: int):
    await bot.send_message(user_id, text=f"This message send at {dt.datetime.now()}")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Зaпуск ботa"),
            BotCommand(command=FILMS, description="Перегляд списку фільмів"),
            BotCommand(command=CREATE_FILM, description="Новий фільм"),
            BotCommand(command=SEARCH, description="Пошук фільму"),
            BotCommand(command=DELETE_FILM, description="Видалити фільм"),
            BotCommand(command="cancel", description="Прервати додавання фільму"),
        ]
    )

    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        message_cron,
        trigger="interval",
        minutes=0.3,
        start_date=dt.datetime.now(),
        kwargs={"bot": bot, "user_id": USER_ID},
    )

    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
