from aiogram.types import KeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from chape_bot.bot.configs import words


def profile():
    kmb = ReplyKeyboardBuilder()
    kmb.add(*[
        KeyboardButton(text=_(words.profile.change_name)),
        KeyboardButton(text=_(words.profile.change_bio)),
        KeyboardButton(text=_(words.profile.change_media)),
        KeyboardButton(text=_(words.profile.change_loc)),
        KeyboardButton(text=_(words.profile.change_lang)),
        KeyboardButton(text=_(words.profile.change_interests)),
    ])
    kmb.adjust(2)
    kmb.row(KeyboardButton(text=_(words.profile.deactivate)))
    kmb.row(KeyboardButton(text=_(words.back)))
    return kmb.as_markup(resize_keyboard=True)
