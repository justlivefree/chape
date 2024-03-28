from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from chape_bot.database.orm import UserQuery
from ..configs import words
from ..keyboards.base import main_menu, langs_kb
from ..states import SignupState, UserPanel

router = Router()


@router.message(Command('start'))
async def cmd_start_handler(message: Message, state: FSMContext):
    await state.clear()
    user = await UserQuery.get_user(message.from_user.id)
    if user:
        if user.is_active:
            await message.answer(_(words.main_panel.title), reply_markup=main_menu())
            await state.set_state(UserPanel.menu)
        elif user.is_block:
            pass
        else:
            pass
    else:
        await state.set_state(SignupState.lang)
        await state.update_data(tg_id=message.from_user.id,
                                username=message.from_user.username,
                                media=[])
        await message.answer(_(words.signup.choose_lang), reply_markup=langs_kb())
