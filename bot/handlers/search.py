from aiogram import F, Bot, Router
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from database.orm import UserQuery, InboxQuery, ReportQuery
from ..configs import words
from ..keyboards.base import main_menu, cancel_kb
from ..keyboards.search import search_settings_panel, search_panel, report_panel
from ..middlewares import media_middleware
from ..states import SearchPanel, UserPanel
from ..utils import user_info_sender

router = Router()
router.message.middleware(media_middleware)


@router.callback_query(SearchPanel.settings, F.data == 'ready')
async def start_selecting(callback: CallbackQuery, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()
        user, media = await UserQuery.select_partner(callback.from_user.id, **data['search_cfg'])
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await callback.message.answer('Ready', reply_markup=search_panel())
        await user_info_sender(bot, user, media, callback.message.chat.id)
        await state.update_data(partner_user_id=user.tg_id, search_cfg=data['search_cfg'])
        await state.set_state(SearchPanel.search)
    except TypeError:
        pass


@router.callback_query(SearchPanel.settings, F.data == 'back')
async def start_selecting(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await state.set_state(UserPanel.menu)
    await callback.message.answer(_(words.main_panel.title), reply_markup=main_menu())


@router.callback_query(SearchPanel.settings)
async def set_gender_option(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    if data['search_cfg']['gender'] == callback.data:
        return
    await state.update_data({'search_cfg': {'gender': callback.data}})
    await bot.edit_message_reply_markup(callback.message.chat.id,
                                        callback.message.message_id,
                                        callback.inline_message_id,
                                        reply_markup=search_settings_panel(gender=callback.data))
    await callback.answer()


@router.message(SearchPanel.search, F.text == '❤️')
async def searching_like(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user, media = await UserQuery.select_partner(message.from_user.id, **data['search_cfg'])
    await InboxQuery.create(receiver=data['partner_user_id'], sender=message.from_user.id, type='like', is_read=False)
    if user.tg_id > 1_000_000:
        await bot.send_message(data['partner_user_id'], _(words.inbox.inbox_notif))
    await user_info_sender(bot, user, media, message.chat.id)
    await state.update_data(partner_user_id=user.tg_id)


@router.message(SearchPanel.search, F.text == '👎')
async def searching_dislike(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await message.answer(_(words.main_panel.search), reply_markup=search_panel())
    user, media = await UserQuery.select_partner(message.from_user.id, **data['search_cfg'])
    await user_info_sender(bot, user, media, message.chat.id)
    await state.update_data(partner_user_id=user.tg_id)


@router.message(SearchPanel.search, F.text == '✉️')
async def searching_send_msg(message: Message, state: FSMContext):
    await message.answer(_(words.search_panel.send_message), reply_markup=cancel_kb())
    await state.set_state(SearchPanel.message)


@router.message(SearchPanel.search)
async def searching_property(message: Message, state: FSMContext):
    if message.text == _(words.cancel):
        await state.set_state(UserPanel.menu)
        await message.answer(_(words.main_panel.title), reply_markup=main_menu())
    elif message.text == _(words.report_panel.title):
        await state.set_state(SearchPanel.report)
        await message.answer(_(words.search_panel.send_report), reply_markup=report_panel())


@router.message(SearchPanel.message, F.text == __(words.cancel))
async def cancel_send_message(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user, media = await UserQuery.select_partner(message.from_user.id, **data['search_cfg'])
    await message.answer(_(words.main_panel.search), reply_markup=search_panel())
    await user_info_sender(bot, user, media, message.chat.id)
    await state.set_state(SearchPanel.search)
    await state.update_data(partner_user_id=user.tg_id)


@router.message(SearchPanel.message, ~F.media_group_id)
async def get_message(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    content_type = message.content_type
    body = {'is_read': False,
            'sender': message.from_user.id,
            'receiver': data['partner_user_id']}
    if content_type == ContentType.TEXT:
        body.update({'type': 'text', 'message': message.text})
    elif content_type == ContentType.PHOTO:
        body.update({'type': 'photo', 'message': message.photo[0].file_id})
    elif content_type == ContentType.VIDEO:
        body.update({'type': 'video', 'message': message.video.file_id})
    elif content_type == ContentType.VOICE:
        body.update({'type': 'audio', 'message': message.voice.file_id})
    elif content_type == ContentType.ANIMATION:
        body.update({'type': 'animation', 'message': message.document.file_id})
    else:
        return
    await InboxQuery.create(**body)
    await message.answer('📨🚀', reply_markup=search_panel())
    if data['partner_user_id'] > 1_000_000:
        await bot.send_message(data['partner_user_id'], _(words.inbox.inbox_notif))
    user, media = await UserQuery.select_partner(message.from_user.id, **data['search_cfg'])
    await user_info_sender(bot, user, media, message.chat.id)
    await state.set_state(SearchPanel.search)
    await state.update_data(partner_user_id=user.tg_id)


@router.message(SearchPanel.report)
async def get_report(message: Message, state: FSMContext, bot: Bot):
    text = message.text
    data = await state.get_data()
    if text != _(words.cancel):
        options = {
            "sender_id": message.from_user.id,
            "receiver_id": data['partner_user_id'],
        }
        if text == _(words.report_panel.sexual):
            options['report_type'] = 'sexual'
        elif text == _(words.report_panel.hateful):
            options['report_type'] = 'hateful'
        elif text == _(words.report_panel.dangerous):
            options['report_type'] = 'dangerous'
        else:
            options['description'] = message.text
        await ReportQuery.create(**options)
        await message.answer(_(words.report_panel.send), reply_markup=search_panel())
    else:
        await message.answer(_(words.main_panel.search), reply_markup=search_panel())
    user, media = await UserQuery.select_partner(message.from_user.id, **data['search_cfg'])
    await user_info_sender(bot, user, media, message.chat.id)
    await state.set_state(SearchPanel.search)
    await state.update_data(partner_user_id=user.tg_id)
