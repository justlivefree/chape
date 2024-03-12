from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from database.orm import UserQuery
from ..config import words, i18n
from ..keyboards.profile import profile
from ..middlewares import LangMiddleware
from ..states import UserPanel
from ..utils import user_info_maker, media_group_maker

main_panel = Router()
main_panel.message.middleware(LangMiddleware(i18n=i18n))


@main_panel.message(UserPanel.menu)
async def main_menu(message: Message, state: FSMContext, bot: Bot):
    data = message.text
    if data == _(words.main_panel.search):
        pass
    elif data == _(words.main_panel.inbox):
        pass
    elif data == _(words.main_panel.profile):
        user = await UserQuery.get_user(message.from_user.id, True)
        info = user_info_maker(user)
        media = await UserQuery.get_media(message.from_user.id)
        if isinstance(media, dict):
            if media['type'] == 'video':
                await bot.send_video(message.chat.id, media['file_id'], caption=info)
            else:
                await bot.send_photo(message.chat.id, media['file_id'], caption=info)
        elif isinstance(media, list):
            await bot.send_media_group(message.chat.id, media=media_group_maker(media, info))
        await state.set_state(UserPanel.profile)
        await message.answer(_(words.main_panel.profile), reply_markup=profile())
