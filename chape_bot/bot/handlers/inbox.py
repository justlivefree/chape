from aiogram import Router, Bot
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from chape_bot.database.orm import InboxQuery, ReportQuery
from ..configs import words

router = Router()


@router.callback_query()
async def inbox_messages(callback: CallbackQuery, bot: Bot):
    type_msg, user_id = callback.data.split('_')
    if type_msg == 'like':
        await InboxQuery.create(is_read=False,
                                sender=callback.from_user.id,
                                receiver=int(user_id),
                                type='reply')
        await bot.send_message(user_id, _(words.inbox.inbox_notif))
    elif type_msg == 'report':
        await ReportQuery.create(sender_id=callback.from_user.id, receiver_id=int(user_id))
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.answer()

# @router.message(UserPanel.inbox)
# async def back_menu(message: Message, state: FSMContext):
#     if message.text == _(words.back):
#         await state.set_state(UserPanel.menu)
#         await message.answer(_(words.main_panel.title), reply_markup=main_menu())
