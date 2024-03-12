from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from database.orm import UserQuery
from ..config import words, i18n
from ..keyboards.base import main_menu, langs_kb
from ..middlewares import LangMiddleware
from ..states import SignupState, UserPanel

cmd_router = Router()
cmd_router.message.middleware(LangMiddleware(i18n=i18n))


@cmd_router.message(Command('start'))
async def cmd_start_handler(message: Message, state: FSMContext):
    await state.clear()
    user = await UserQuery.get_user(message.from_user.id)
    if user:
        await message.answer(_(words.main_panel.title), reply_markup=main_menu())
        await state.set_state(UserPanel.menu)
    else:
        await state.set_state(SignupState.lang)
        await state.update_data(tg_id=message.from_user.id, media=[])
        await message.answer(_(words.signup.choose_lang), reply_markup=langs_kb())
