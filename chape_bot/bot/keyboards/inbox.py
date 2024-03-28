from aiogram.types import InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from chape_bot.bot.configs import words


def inbox_message_panel(user_id, username=None):
    ikb = InlineKeyboardBuilder()
    if username:
        ikb.row(*[InlineKeyboardButton(text=_(words.sender_profile), url=f'tg://user?id={user_id}')])
    ikb.row(*[InlineKeyboardButton(text='❤️', callback_data=f'like_{user_id}'),
              InlineKeyboardButton(text='👎', callback_data=f'dislike_{user_id}')])
    ikb.row(*[InlineKeyboardButton(text=_(words.report_panel.title), callback_data=f'report_{user_id}')])
    return ikb.as_markup()


def inbox_reply_panel(user_id, username=None):
    ikb = InlineKeyboardBuilder()
    if username:
        ikb.row(*[InlineKeyboardButton(text=_(words.sender_profile), url=f'tg://user?id={user_id}')])
    ikb.row(*[InlineKeyboardButton(text=_(words.report_panel.title), callback_data=f'report_{user_id}')])
    return ikb.as_markup()
