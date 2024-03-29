from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, KeyboardButton, \
    ReplyKeyboardBuilder

from ..configs import words


def search_settings_panel(**kwargs):
    male, female, _any = _(words.search_panel.male), _(words.search_panel.female), _(words.search_panel.all)
    gender = kwargs['gender']
    if gender == 'male':
        male += ' ✅'
    elif gender == 'female':
        female += ' ✅'
    elif gender == 'any':
        _any += ' ✅'
    ikb = InlineKeyboardBuilder()
    ikb.row(*[InlineKeyboardButton(text=male, callback_data='male'),
              InlineKeyboardButton(text=female, callback_data='female'),
              InlineKeyboardButton(text=_any, callback_data='any')])
    ikb.row(*[InlineKeyboardButton(text=_(words.back), callback_data='back'),
              InlineKeyboardButton(text=_(words.ready), callback_data='ready')])
    return ikb.as_markup()


def search_panel():
    rkb = ReplyKeyboardBuilder()
    rkb.row(*[KeyboardButton(text='✉️'),
              KeyboardButton(text='❤️'),
              KeyboardButton(text='👎')])
    rkb.row(*[KeyboardButton(text=_(words.cancel)), KeyboardButton(text=_(words.report_panel.title))])
    return rkb.as_markup(resize_keyboard=True)


def report_btn():
    ikb = InlineKeyboardBuilder(
        [[InlineKeyboardButton(text=_(words.report_panel.title), callback_data=words.report_panel.title)]])
    return ikb.as_markup()


def report_panel():
    ikb = ReplyKeyboardBuilder()
    ikb.add(*[KeyboardButton(text=_(words.report_panel.hateful)),
              KeyboardButton(text=_(words.report_panel.dangerous)),
              KeyboardButton(text=_(words.report_panel.sexual))])
    ikb.row(*[KeyboardButton(text=_(words.cancel))])
    ikb.adjust(2)
    return ikb.as_markup(resize_keyboard=True)
