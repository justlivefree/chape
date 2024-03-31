import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot
from aiogram.enums import ParseMode

from bot.dispatcher import get_dispatcher
from bot.utils import get_bot_commands


async def main():
    TOKEN = getenv("BOT_TOKEN")
    dp = get_dispatcher()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await bot.set_my_commands(get_bot_commands())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
