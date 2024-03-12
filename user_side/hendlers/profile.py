from typing import Dict

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _

from database.orm import UserQuery
from ..config import words, i18n
from ..keyboards.base import cancel_kb, langs_kb, main_menu, location_kb, yes_no_kb, activate_kb
from ..keyboards.profile import profile
from ..keyboards.signup import interests_panel
from ..middlewares import LangMiddleware, MediaGroupMiddleware
from ..states import UserPanel, ProfileSettings
from ..utils import get_location_data

profile_panel = Router(name='user_panel_router')
i18n_middleware = LangMiddleware(i18n=i18n)
profile_panel.message.middleware(i18n_middleware)
profile_panel.callback_query.middleware(i18n_middleware)
profile_panel.message.middleware(MediaGroupMiddleware())


@profile_panel.message(UserPanel.profile)
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


@profile_panel.message(ProfileSettings.change_name, F.text)
async def change_name(message: Message, state: FSMContext):
    text = _(words.main_panel.profile)
    if message.text != _(words.cancel):
        await UserQuery.update(message.from_user.id, fullname=message.text)
        text = '✅'
    await message.answer(text, reply_markup=profile())
    await state.set_state(UserPanel.profile)


@profile_panel.message(ProfileSettings.change_bio, F.text)
async def change_bio(message: Message, state: FSMContext):
    text = _(words.main_panel.profile)
    if message.text != _(words.cancel):
        await UserQuery.update(message.from_user.id, description=message.text)
        text = '✅'
    await message.answer(text, reply_markup=profile())
    await state.set_state(UserPanel.profile)


@profile_panel.message(ProfileSettings.change_media, ~F.media_group_id & ~F.text)
async def change_media(message: Message, state: FSMContext, media: Dict):
    await UserQuery.update_media(**media)
    await state.set_state(UserPanel.profile)
    await message.answer('✅', reply_markup=profile())


@profile_panel.message(ProfileSettings.change_media, F.media_group_id)
async def change_media_group(message: Message, state: FSMContext, media_group: Dict):
    if media_group['media']:
        del MediaGroupMiddleware.media_groups[message.media_group_id]
        await UserQuery.update_media(**media_group)
        await state.set_state(UserPanel.profile)
        await message.answer('✅', reply_markup=profile())


@profile_panel.message(ProfileSettings.change_media, F.text)
async def change_media_cancel(message: Message, state: FSMContext):
    if message.text == _(words.cancel):
        await state.set_state(UserPanel.profile)
        await message.answer(_(words.main_panel.profile), reply_markup=profile())


@profile_panel.message(ProfileSettings.change_loc, F.location)
async def change_location(message: Message, state: FSMContext):
    lat, lon = message.location.latitude, message.location.longitude
    loc = await get_location_data(lat, lon)
    result = {'lat': lat, 'lon': lon, 'city': loc['city'], 'country': loc['country']}
    await UserQuery.update(message.from_user.id, **result)
    await state.set_state(UserPanel.profile)
    await message.answer('✅', reply_markup=profile())


@profile_panel.message(ProfileSettings.change_loc, F.text)
async def change_location_cancel(message: Message, state: FSMContext):
    if message.text == _(words.cancel):
        await state.set_state(UserPanel.profile)
        await message.answer(_(words.main_panel.profile), reply_markup=profile())


@profile_panel.callback_query(ProfileSettings.change_lang, F.data.in_({'en', 'ru', 'uz', 'cancel'}))
async def change_lang(callback: CallbackQuery, state: FSMContext, bot: Bot):
    text = _(words.main_panel.profile)
    if callback.data != 'cancel':
        await UserQuery.update(callback.message.from_user.id, lang=callback.data)
        await i18n_middleware.set_locale(state, callback.data)
        await callback.answer()
        text = '✅'
    await state.set_state(UserPanel.profile)
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.answer(text, reply_markup=profile())


@profile_panel.callback_query(ProfileSettings.change_interests)
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


@profile_panel.message()
async def deactivate_user(message: Message, state: FSMContext):
    if message.text == _(words.yes):
        await UserQuery.deactivate_user(message.from_user.id)
        await message.answer(_(words.deactivate_msg), reply_markup=activate_kb())
        await state.clear()
    else:
        await state.set_state(UserPanel.profile)
        await message.answer(_(words.main_panel.profile), reply_markup=profile())
