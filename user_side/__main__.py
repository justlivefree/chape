import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
from redis.asyncio import Redis

from user_side.hendlers.commands import cmd_router
from user_side.hendlers.menu import main_panel
from user_side.hendlers.signup import signup_router
from user_side.hendlers.profile import profile_panel

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
redis_client = Redis()
user_dp = Dispatcher(storage=RedisStorage(redis_client))
user_bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def main():
    user_dp.include_routers(cmd_router, signup_router, main_panel, profile_panel)
    await user_dp.start_polling(user_bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
