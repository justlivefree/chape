import asyncio
from typing import Callable, Dict, Any, Awaitable, Optional

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, TelegramObject, CallbackQuery
from aiogram.utils.i18n import FSMI18nMiddleware

from database.orm import UserQuery
from .utils import media_maker


class MediaGroupMiddleware(BaseMiddleware):
    media_groups = {}
    latency = 0.2

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        media = media_maker(event)
        if mg_id := event.media_group_id:
            try:
                self.media_groups[mg_id].append(media)
            except KeyError:
                self.media_groups[mg_id] = [media]
            await asyncio.sleep(self.latency)
            data['media_group'] = {'tg_id': event.from_user.id, 'media': self.media_groups.get(mg_id)}
        if media:
            data['media'] = {'tg_id': event.from_user.id, 'media': media}
        return await handler(event, data)


class LangMiddleware(FSMI18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        fsm_context: Optional[FSMContext] = data.get("state")
        locale = None
        if fsm_context:
            fsm_data = await fsm_context.get_data()
            locale = fsm_data.get(self.key, None)
        if not locale:
            if isinstance(event, Message):
                user_id = event.from_user.id
            elif isinstance(event, CallbackQuery):
                user_id = event.message.from_user.id
            else:
                user_id = None
            user = await UserQuery.get_user(user_id)
            if user:
                locale = user.lang
                await self.set_locale(fsm_context, locale)
            else:
                locale = await super().get_locale(event=event, data=data)
                if fsm_context:
                    await fsm_context.update_data(data={self.key: locale})
        return locale
