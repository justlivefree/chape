from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _

from chape_bot.database.orm import UserQuery, InboxQuery
from ..configs import words
from ..keyboards.inbox import inbox_message_panel, inbox_reply_panel
from ..keyboards.profile import profile
from ..keyboards.search import search_settings_panel
from ..states import UserPanel, SearchPanel
from ..utils import user_info_sender

router = Router()


@router.message(UserPanel.menu)
async def main_menu(message: Message, state: FSMContext, bot: Bot):
    if message.text == _(words.main_panel.search):
        cfg = {'gender': 'any'}
        await state.set_state(SearchPanel.settings)
        await state.update_data({'search_cfg': cfg})
        msg = await message.answer(_(words.search_panel.title), reply_markup=ReplyKeyboardRemove())
        await bot.delete_message(message.chat.id, msg.message_id)
        await message.answer(_(words.search_panel.title), reply_markup=search_settings_panel(**cfg))
    elif message.text == _(words.main_panel.inbox):
        # all messages
        messages = await InboxQuery.get_all(message.from_user.id)
        if messages:
            for msg in messages:
                # send sender info
                sender = await UserQuery.get_user(msg['sender'], load_all=True)
                sender_media = await UserQuery.get_media(msg['sender'])
                msg_type = msg['type']
                inbox_message = msg.get('message')
                msg_btn = inbox_message_panel(msg['sender'], sender.username)
                await user_info_sender(bot, sender, sender_media, message.chat.id)

                # send inbox message
                if msg_type == 'like':
                    await bot.send_message(message.chat.id, _(words.inbox.like_notif), reply_markup=msg_btn)
                elif msg_type == 'reply':
                    await bot.send_message(message.chat.id, _(words.inbox.reply_notif),
                                           reply_markup=inbox_reply_panel(msg['sender'], sender.username))
                elif msg_type == 'photo':
                    await bot.send_photo(message.chat.id, inbox_message, reply_markup=msg_btn)
                elif msg_type == 'video':
                    await bot.send_video(message.chat.id, inbox_message, reply_markup=msg_btn)
                elif msg_type == 'audio':
                    await bot.send_voice(message.chat.id, inbox_message, reply_markup=msg_btn)
                elif msg_type == 'animation':
                    await bot.send_animation(message.chat.id, inbox_message, reply_markup=msg_btn)
            await InboxQuery.make_messages_read(message.from_user.id)
    elif message.text == _(words.main_panel.profile):
        user = await UserQuery.get_user(message.from_user.id, True)
        media = await UserQuery.get_media(message.from_user.id)
        await user_info_sender(bot, user, media, message.chat.id)
        await state.set_state(UserPanel.profile)
        await message.answer(_(words.main_panel.profile), reply_markup=profile())
