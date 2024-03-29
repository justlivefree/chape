import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot
from aiogram.enums import ParseMode

from database.orm import DBQuery
from .dispatcher import get_dispatcher


async def main():
    await DBQuery.create_tables()
    TOKEN = getenv("BOT_TOKEN")
    dp = get_dispatcher()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())