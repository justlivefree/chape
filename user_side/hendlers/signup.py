from typing import Dict

from aiogram import Bot, F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _, FSMI18nMiddleware

from database.orm import UserQuery
from ..config import i18n, words
from ..keyboards.base import main_menu, location_kb
from ..keyboards.signup import interests_panel
from ..middlewares import MediaGroupMiddleware
from ..states import SignupState, UserPanel
from ..utils import get_location_data

signup_router = Router()
i18n_middleware = FSMI18nMiddleware(i18n=i18n, key='lang')
signup_router.message.middleware(MediaGroupMiddleware())
signup_router.callback_query.middleware(i18n_middleware)
signup_router.message.middleware(i18n_middleware)


@signup_router.callback_query(SignupState.lang)
async def start_signup(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await i18n_middleware.set_locale(state, callback.data)
    await state.update_data(locale=callback.data)
    rmk = ReplyKeyboardMarkup(resize_keyboard=True,
                              keyboard=[
                                  [KeyboardButton(text=_(words.signup.agree))],
                                  [KeyboardButton(text=_(words.signup.disagree))]
                              ])
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await state.set_state(SignupState.policy)
    await callback.message.answer(_(words.policy), reply_markup=rmk)


@signup_router.message(SignupState.policy)
async def get_agreement(message: Message, state: FSMContext):
    if message.text == _(words.signup.agree):
        await state.set_state(SignupState.fullname)
        await message.reply(_(words.signup.name), reply_markup=ReplyKeyboardRemove())
    elif message.text == _(words.signup.disagree):
        await state.clear()
    else:
        await message.delete()


@signup_router.message(SignupState.fullname)
async def get_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(SignupState.age)
    await message.answer(_(words.signup.age))


@signup_router.message(SignupState.age)
async def get_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        if 15 <= age <= 25:
            await state.update_data(age=age)
            await state.set_state(SignupState.gender)
            rkm = ReplyKeyboardMarkup(resize_keyboard=True,
                                      keyboard=[[KeyboardButton(text=_(words.signup.gender.male)),
                                                 KeyboardButton(text=_(words.signup.gender.female))]])
            await message.answer(_(words.signup.gender.title), reply_markup=rkm)
        else:
            await message.answer(_(words.errors.age_range))
    except ValueError:
        await message.answer(_(words.errors.type_number))


@signup_router.message(SignupState.gender)
async def get_gender(message: Message, state: FSMContext, bot: Bot):
    f, m = map(_, (words.signup.gender.male, words.signup.gender.female))
    if message.text in (f, m):
        await state.update_data(gender=(message.text == m), interests=words.interests)
        await state.set_state(SignupState.interest)
        await message.answer(_(words.signup.info_choice), reply_markup=ReplyKeyboardRemove())
        await message.answer(_(words.signup.choose), reply_markup=interests_panel(words.interests))


@signup_router.callback_query(SignupState.interest)
async def get_interests(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if callback.data == 'cancel':
        await state.set_state(SignupState.bio)
        await callback.message.answer(_(words.signup.bio))
        await callback.answer()
        return
    try:
        data = await state.get_data()
        interests = data['interests']
        interests[callback.data] = not interests[callback.data]
        await state.update_data(interests=interests)
        await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id,
                                            callback.inline_message_id, reply_markup=interests_panel(interests))
        await callback.answer()
    except KeyError:
        pass


@signup_router.message(SignupState.bio)
async def get_bio(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(SignupState.city)
    await message.answer(_(words.signup.location), reply_markup=location_kb())


@signup_router.message(SignupState.city, F.location)
async def get_location(message: Message, state: FSMContext):
    lat, lon = message.location.latitude, message.location.longitude
    loc = await get_location_data(lat, lon)
    await state.update_data(**{'lat': lat, 'lon': lon, 'city': loc['city'], 'country': loc['country']})
    await state.set_state(SignupState.media)
    await message.answer(_(words.signup.media))


@signup_router.message(SignupState.media, ~F.media_group_id)
async def get_media(message: Message, state: FSMContext, media: Dict):
    data = await state.get_data()
    await UserQuery.create_media(**media)
    await UserQuery.create(**data)
    await state.set_state(UserPanel.menu)
    await message.answer(_(words.welcome), reply_markup=main_menu())


@signup_router.message(SignupState.media, F.media_group_id)
async def get_media_group(message: Message, state: FSMContext, media_group: Dict):
    data = await state.get_data()
    if media_group['media']:
        del MediaGroupMiddleware.media_groups[message.media_group_id]
        await UserQuery.create(**data)
        await UserQuery.create_media(**media_group)
        await state.set_state(UserPanel.menu)
        await message.answer(_(words.welcome), reply_markup=main_menu())
