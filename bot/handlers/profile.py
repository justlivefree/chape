from typing import Dict

from aiogram import F, Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from geopy.exc import GeocoderTimedOut

from database.orm import UserQuery
from ..configs import words
from ..keyboards.base import cancel_kb, langs_kb, main_menu, location_kb, yes_no_kb, activate_kb
from ..keyboards.profile import profile
from ..keyboards.signup import interests_panel
from ..middlewares import i18n_middleware, media_middleware
from ..states import UserPanel, ProfileSettings
from ..utils import get_location_data, check_location

router = Router()

router.message.middleware(media_middleware)


@router.message(UserPanel.profile)
async def profile_menu(message: Message, state: FSMContext, bot: Bot):
    data = message.text
    if data == _(words.profile.change_name):
        await state.set_state(ProfileSettings.change_name)
        await message.answer(_(words.signup.name), reply_markup=cancel_kb())
    elif data == _(words.profile.change_bio):
        await state.set_state(ProfileSettings.change_bio)
        await message.answer(_(words.signup.bio), reply_markup=cancel_kb())
    elif data == _(words.profile.change_media):
        await state.set_state(ProfileSettings.change_media)
        await message.answer(_(words.profile.change_media), reply_markup=cancel_kb())
    elif data == _(words.profile.change_loc):
        await state.set_state(ProfileSettings.change_loc)
        await message.answer(_(words.signup.location), reply_markup=location_kb(True))
    elif data == _(words.profile.change_lang):
        await state.set_state(ProfileSettings.change_lang)
        msg = await bot.send_message(message.chat.id, _(words.signup.choose_lang), reply_markup=ReplyKeyboardRemove())
        await bot.delete_message(message.chat.id, msg.message_id)
        await message.answer(_(words.signup.choose_lang), reply_markup=langs_kb(True))
    elif data == _(words.profile.change_interests):
        interests = await UserQuery.get_interests(message.from_user.id)
        tmp = words.interests
        for k, v in words.interests.items():
            tmp[k] = getattr(interests, k.lower().replace(' ', '_'))
        await state.update_data(interests=words.interests)
        await state.set_state(ProfileSettings.change_interests)
        msg = await bot.send_message(message.chat.id, _(words.signup.info_choice), reply_markup=ReplyKeyboardRemove())
        await bot.delete_message(message.chat.id, msg.message_id)
        await message.answer(_(words.signup.info_choice), reply_markup=interests_panel(tmp))
    elif data == _(words.profile.change_bio):
        await state.set_state(ProfileSettings.change_bio)
        await message.answer(_(words.signup.bio))
    elif data == _(words.profile.deactivate):
        await state.set_state(ProfileSettings.deactivate)
        await message.answer(_(words.profile.deactivate_title), reply_markup=yes_no_kb())
    elif data == _(words.back):
        await state.set_state(UserPanel.menu)
        await message.answer(_(words.main_panel.title), reply_markup=main_menu())


@router.message(ProfileSettings.change_name, F.text)
async def change_name(message: Message, state: FSMContext):
    text = _(words.main_panel.profile)
    if message.text != _(words.cancel):
        await UserQuery.update(message.from_user.id, fullname=message.text)
        text = '✅'
    await message.answer(text, reply_markup=profile())
    await state.set_state(UserPanel.profile)


@router.message(ProfileSettings.change_bio, F.text)
async def change_bio(message: Message, state: FSMContext):
    text = _(words.main_panel.profile)
    if message.text != _(words.cancel):
        await UserQuery.update(message.from_user.id, description=message.text)
        text = '✅'
    await message.answer(text, reply_markup=profile())
    await state.set_state(UserPanel.profile)


@router.message(ProfileSettings.change_media, ~F.media_group_id & ~F.text)
async def change_media(message: Message, state: FSMContext, media: Dict):
    await UserQuery.update_media(**media)
    await state.set_state(UserPanel.profile)
    await message.answer('✅', reply_markup=profile())


@router.message(ProfileSettings.change_media, F.media_group_id)
async def change_media_group(message: Message, state: FSMContext, media_group: Dict):
    if media_group['media']:
        del media_middleware.media_groups[message.media_group_id]
        await UserQuery.update_media(**media_group)
        await state.set_state(UserPanel.profile)
        await message.answer('✅', reply_markup=profile())


@router.message(ProfileSettings.change_media, F.text)
async def change_media_cancel(message: Message, state: FSMContext):
    if message.text == _(words.cancel):
        await state.set_state(UserPanel.profile)
        await message.answer(_(words.main_panel.profile), reply_markup=profile())


@router.message(ProfileSettings.change_loc, F.location)
async def change_location(message: Message, state: FSMContext):
    lat, lon = message.location.latitude, message.location.longitude
    try:
        loc = await get_location_data(lat, lon)
        await UserQuery.update(message.from_user.id, **loc)
        await state.set_state(UserPanel.profile)
        await message.answer('✅', reply_markup=profile())
    except (AttributeError, KeyError):
        await message.answer(_(words.errors.location_not_found))
    except GeocoderTimedOut:
        await message.answer(_(words.errors.server_error))


@router.message(ProfileSettings.change_loc, F.text == __(words.cancel))
async def change_location_cancel(message: Message, state: FSMContext):
    await state.set_state(UserPanel.profile)
    await message.answer(_(words.main_panel.profile), reply_markup=profile())


@router.message(ProfileSettings.change_loc, F.text)
async def change_location_orientation(message: Message, state: FSMContext):
    try:
        loc = await check_location(message.text)
        await UserQuery.update(message.from_user.id, **loc)
        await state.set_state(UserPanel.profile)
        await message.answer('✅', reply_markup=profile())
    except (AttributeError, KeyError):
        await message.answer(_(words.errors.location_not_found))
    except GeocoderTimedOut:
        await message.answer(_(words.errors.server_error))


@router.callback_query(ProfileSettings.change_lang)
async def change_lang(callback: CallbackQuery, state: FSMContext, bot: Bot):
    text = _(words.main_panel.profile)
    if callback.data != 'cancel':
        await UserQuery.update(callback.from_user.id, lang=callback.data)
        await i18n_middleware.set_locale(state, callback.data)
        await callback.answer()
        text = '✅'
    await state.set_state(UserPanel.profile)
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer(text, reply_markup=profile())


@router.callback_query(ProfileSettings.change_interests)
async def change_interests(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    interests = data.pop('interests')
    if callback.data == 'cancel':
        await UserQuery.update_interests(callback.from_user.id, interests)
        await state.set_state(UserPanel.profile)
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await callback.message.answer('✅', reply_markup=profile())
        await state.set_data(data)
        await callback.answer()
        return
    interests[callback.data] = not interests[callback.data]
    await state.update_data(interests=interests)
    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id,
                                        callback.inline_message_id, reply_markup=interests_panel(interests))
    await callback.answer()


@router.message(ProfileSettings.deactivate)
async def deactivate_user(message: Message, state: FSMContext):
    if message.text == _(words.yes):
        await UserQuery.update(message.from_user.id, is_active=False)
        await message.answer(_(words.deactivate_msg), reply_markup=activate_kb())
        await state.set_state(ProfileSettings.deactivated)
    else:
        await state.set_state(UserPanel.profile)
        await message.answer(_(words.main_panel.profile), reply_markup=profile())


@router.message(ProfileSettings.deactivated)
async def activate_user(message: Message, state: FSMContext):
    if message.text == _(words.activate):
        await UserQuery.update(message.from_user.id, is_active=True)
        await state.set_state(UserPanel.menu)
        await message.answer(_(words.main_panel.title), reply_markup=main_menu())
