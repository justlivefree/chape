from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from chape_bot.bot.configs import words


def interests_panel(interests):
    ikm = InlineKeyboardBuilder()
    for title, check in interests.items():
        tmp = title.capitalize() + ('✅' if check else '')
        ikm.add(InlineKeyboardButton(text=_(tmp), callback_data=title))
    ikm.adjust(3)
    ikm.row(InlineKeyboardButton(text=_(words.ready), callback_data='cancel'))
    return ikm.as_markup()
