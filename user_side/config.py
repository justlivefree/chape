from pathlib import Path

from aiogram.utils.i18n import I18n
from redis.asyncio import Redis

BASE_DIR = Path(__file__).parent.parent
i18n = I18n(path=BASE_DIR / 'locales', domain='chape_bot')
redis = Redis()


class words:
    policy = ("Hello, esteemed user. \nThrough this bot, you can connect with "
              "friends and meet new people. \n\nPlease note that the bot administrators "
              "continuously monitor its operation to ensure everything runs smoothly. "
              "If you come across any inappropriate images or videos with a questionable "
              "character, please report to us. We will take action thereafter. "
              "\n\nIn addition, the bot owner does not assume responsibility for any material "
              "or moral damage that may arise from your interaction with the bot. "
              "\n\nIf you have any questions or suggestions, feel free to contact us at %s.")
    welcome = 'Welcome and enjoy☺️'
    search_title = 'Write something sweet'
    income_message = 'You have %d messages'
    interests = {
        'Anime': 0,
        'Movie': 0,
        'Music': 0,

        'Cars': 0,
        'Sport': 0,

        'Books': 0,
        'Study': 0,
        'Math': 0,
        'Design': 0,
        'Art': 0,
        'Programing': 0,

        'Gaming': 0,
        'PUBG': 0,
        'CS2': 0,
        'Mobile Legends': 0,
    }
    ready = 'Ready⏩'
    back = 'Back⬅️'
    cancel = 'Cancel'
    location = 'Location'
    yes = 'Yes'
    no = 'No'
    activate = 'Activate'
    activate_msg = None
    deactivate_msg = 'Your account deactivated'

    class errors:
        type_number = 'Write number'
        send_one_media = 'Send only photo or video'
        age_range = 'Your age does not apply for policy'
        blocked = 'You have been blocked for %s days'
        deactivated = 'You deactivated. Click button below for activation'

    class signup:
        choose_lang = 'Choose language:'
        agree = 'Agree'
        disagree = 'Disagree'
        name = 'Name:'
        age = 'Age:'
        gender = type('gender', (), {'title': 'Gender:', 'male': 'Male🙋‍♂️', 'female': 'Female‍🙋‍♀️'})
        location = 'Location: '
        bio = 'Write about yourself:'
        info_choice = 'Choose your interests, it helps to make better conversation'
        choose = 'Choose:'
        media = 'Send profile photo or video'

    class main_panel:
        title = 'Main menu'
        search = 'Search 🚀'
        inbox = 'Inbox 📥'
        profile = 'Profile 👤'

    class search_panel:
        female = 'Girls 👸🏼'
        male = 'Boys 🥷'
        all = 'All ✈️'

    class profile:
        change_name = 'Change name'
        change_media = 'Change media'
        change_loc = 'Change location'
        change_lang = 'Change language'
        change_interests = 'Change interests'
        change_bio = 'Change bio'
        deactivate = 'Deactivate 🪓'
        deactivate_title = 'Are you sure you want to deactivate your account?'


print(repr(words.policy))
