from aiogram.fsm.state import StatesGroup, State


class SignupState(StatesGroup):
    lang = State()
    policy = State()
    fullname = State()
    age = State()
    gender = State()
    interest = State()
    bio = State()
    location = State()
    media = State()


class UserPanel(StatesGroup):
    menu = State()
    search = State()
    inbox = State()
    profile = State()


class ProfileSettings(StatesGroup):
    change_name = State()
    change_media = State()
    change_loc = State()
    change_lang = State()
    change_interests = State()
    change_bio = State()
    deactivate = State()
    deactivated = State()


class SearchPanel(StatesGroup):
    settings = State()
    search = State()
    message = State()
    report = State()
