from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from ..config import words


def main_menu():
    kmb = ReplyKeyboardBuilder()
    kmb.add(KeyboardButton(text=_(words.main_panel.search)))
    kmb.row(*[KeyboardButton(text=_(words.main_panel.inbox)),
              KeyboardButton(text=_(words.main_panel.profile))])
    return kmb.as_markup(resize_keyboard=True)


def cancel_kb():
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text=_(words.cancel)))
    return rkb.as_markup(resize_keyboard=True)


def langs_kb(add_back=False):
    btns = [[InlineKeyboardButton(text='🇺🇸', callback_data='en'),
             InlineKeyboardButton(text='🇷🇺', callback_data='ru'),
             InlineKeyboardButton(text='🇺🇿', callback_data='uz')]]
    if add_back:
        btns.append([InlineKeyboardButton(text=_(words.cancel), callback_data='cancel')])
    ikm = InlineKeyboardMarkup(inline_keyboard=btns)
    return ikm


def location_kb(add_back=False):
    btns = [KeyboardButton(text=_(words.location), request_location=True)]
    if add_back:
        btns.append(KeyboardButton(text=_(words.cancel)))
    rkm = ReplyKeyboardMarkup(resize_keyboard=True,
                              keyboard=[btns])
    return rkm


def yes_no_kb():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Yes'), KeyboardButton(text='No')]])


def activate_kb():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=_(words.activate))]])
