from typing import Dict

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _
from geopy.exc import GeocoderTimedOut

from database.models import Gender
from database.orm import UserQuery
from ..configs import words
from ..keyboards.base import main_menu, location_kb, agree_disagree
from ..keyboards.signup import interests_panel
from ..middlewares import MediaGroupMiddleware, media_middleware, i18n_middleware
from ..states import SignupState, UserPanel
from ..utils import get_location_data, check_location

router = Router()
router.message.middleware(media_middleware)


@router.callback_query(SignupState.lang)
async def start_signup(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await i18n_middleware.set_locale(state, callback.data)
    await state.update_data(locale=callback.from_user.language_code, lang=callback.data)
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await state.set_state(SignupState.policy)
    await callback.message.answer(_(words.policy), reply_markup=agree_disagree())


@router.message(SignupState.policy, F.text)
async def get_agreement(message: Message, state: FSMContext):
    if message.text == _(words.signup.agree):
        await state.set_state(SignupState.fullname)
        await message.answer(_(words.signup.name), reply_markup=ReplyKeyboardRemove())
    elif message.text == _(words.signup.disagree):
        await message.answer(_(words.signup.disagree_description), reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.delete()


@router.message(SignupState.fullname, F.text)
async def get_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(SignupState.age)
    await message.answer(_(words.signup.age))


@router.message(SignupState.age, F.text.isnumeric())
async def get_age(message: Message, state: FSMContext):
    age = int(message.text)
    if age >= 17:
        await state.update_data(age=age)
        await state.set_state(SignupState.gender)
        rkm = ReplyKeyboardMarkup(resize_keyboard=True,
                                  keyboard=[[KeyboardButton(text=_(words.signup.gender.male)),
                                             KeyboardButton(text=_(words.signup.gender.female))]])
        await message.answer(_(words.signup.gender.title), reply_markup=rkm)
    else:
        await message.answer(_(words.errors.age_range))


@router.message(SignupState.gender, F.text)
async def get_gender(message: Message, state: FSMContext):
    if message.text == _(words.signup.gender.male):
        gender = Gender.male.value
    elif message.text == _(words.signup.gender.female):
        gender = Gender.female.value
    else:
        return
    await state.update_data(gender=gender, interests=words.interests)
    await state.set_state(SignupState.interest)
    await message.answer(_(words.signup.info_choice), reply_markup=ReplyKeyboardRemove())
    await message.answer(_(words.signup.choose), reply_markup=interests_panel(words.interests))


@router.callback_query(SignupState.interest)
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


@router.message(SignupState.bio, F.text)
async def get_bio(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(SignupState.location)
    await message.answer(_(words.signup.location), reply_markup=location_kb())


@router.message(SignupState.location, F.location)
async def get_location(message: Message, state: FSMContext):
    try:
        loc = await get_location_data(message.location.latitude, message.location.longitude)
        await state.update_data(**loc)
        await state.set_state(SignupState.media)
        await message.answer(_(words.signup.media), reply_markup=ReplyKeyboardRemove())
    except (AttributeError, KeyError):
        await message.answer(_(words.errors.location_not_found))
    except GeocoderTimedOut:
        await message.answer(_(words.errors.server_error))


@router.message(SignupState.location, F.text)
async def get_location_orientation(message: Message, state: FSMContext):
    try:
        loc = await check_location(message.text)
        await state.update_data(**loc)
        await state.set_state(SignupState.media)
        await message.answer(_(words.signup.media), reply_markup=ReplyKeyboardRemove())
    except (AttributeError, KeyError):
        await message.answer(_(words.errors.location_not_found))
    except GeocoderTimedOut:
        await message.answer(_(words.errors.server_error))


@router.message(SignupState.media, ~F.media_group_id & (F.photo | F.video))
async def get_media(message: Message, state: FSMContext, media: Dict):
    data = await state.get_data()
    await UserQuery.create_media(**media)
    await UserQuery.create(**data)
    await state.set_state(UserPanel.menu)
    await message.answer(_(words.welcome), reply_markup=main_menu())


@router.message(SignupState.media, F.media_group_id)
async def get_media_group(message: Message, state: FSMContext, media_group: Dict):
    data = await state.get_data()
    if media_group['media']:
        del MediaGroupMiddleware.media_groups[message.media_group_id]
        await UserQuery.create(**data)
        await UserQuery.create_media(**media_group)
        await state.set_state(UserPanel.menu)
        await message.answer(_(words.welcome), reply_markup=main_menu())
