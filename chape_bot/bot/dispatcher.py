import os

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from .handlers.commands import router as cmd_router
from .handlers.inbox import router as inbox_router
from .handlers.menu import router as menu_router
from .handlers.profile import router as profile_router
from .handlers.search import router as search_router
from .handlers.signup import router as signup_router
from .middlewares import private_chat_middleware, i18n_middleware


def get_dispatcher():
    redis_client = Redis(host=os.getenv('REDIS_HOSTNAME'))
    dp = Dispatcher(storage=RedisStorage(redis_client))
    routers = (cmd_router, signup_router, menu_router, search_router, profile_router, inbox_router)

    # private chat
    dp.message.outer_middleware(private_chat_middleware)
    dp.callback_query.outer_middleware(private_chat_middleware)
    # lang setting
    dp.message.middleware(i18n_middleware)
    dp.callback_query.middleware(i18n_middleware)

    dp.include_routers(*routers)

    return dp
