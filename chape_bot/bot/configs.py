from pathlib import Path

from aiogram.utils.i18n import I18n

BASE_DIR = Path(__file__).parent.parent.parent
i18n = I18n(path=BASE_DIR / 'locales', domain='chape_bot')


def _(val):
    return val


class words:
    policy = _("Hello, esteemed user. \nThrough this bot, you can connect with "
               "friends and meet new people. \n\nPlease note that the bot administrators "
               "continuously monitor its operation to ensure everything runs smoothly. "
               "If you come across any inappropriate images or videos with a questionable "
               "character, please report to us. We will take action thereafter. "
               "\n\nIn addition, the bot owner does not assume responsibility for any material "
               "or moral damage that may arise from your interaction with the bot. "
               "\n\nIf you have any questions or suggestions, feel free to contact us at %s.")
    welcome = _('Welcome and enjoy☺️')
    search_title = _('Write something sweet')
    income_message = _('You have %d messages')
    interests_titles = (_('Anime'), _('Movie'),
                        _('Music'), _('Cars'),
                        _('Sport'), _('Books'),
                        _('Study'), _('Math'),
                        _('Design'), _('Art'),
                        _('Programing'), _('Gaming'))
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

    ready = _('Ready⏩')
    back = _('Back⬅️')
    cancel = _('Cancel')
    location = _('Location📍')
    yes = _('Yes')
    no = _('No')
    activate = _('Activate💡')
    deactivate_msg = _('Your account deactivated')
    sender_profile = _('Sender profile')

    class errors:
        type_number = _('Write number')
        send_one_media = _('Send only photo or video')
        age_range = _('Your age does not apply for policy')
        blocked = _('You have been blocked for %s days')
        deactivated = _('You deactivated. Click button below for activation')
        private_profile = _('Bot can\'t send user\'s profile, cause account is private')

    class signup:
        choose_lang = _('Choose language:')
        agree = _('Agree')
        disagree = _('Disagree')
        name = _('Name:')
        age = _('Age:')
        gender = type('gender', (), {'title': _('Gender:'), 'male': _('Male🙋‍♂️'), 'female': _('Female‍🙋‍♀️')})
        location = _('Location:')
        bio = _('Write about yourself:')
        info_choice = _('Choose your interests, it helps to make better conversation')
        choose = _('Choose:')
        media = _('Send profile photo or video')

    class main_panel:
        title = _('Main menu')
        search = _('Search 🚀')
        inbox = _('Inbox 📥')
        profile = _('Profile 👤')

    class report_panel:
        title = _('Report⚠️')
        sexual = _('Sexual')
        pedophilia = _('Pedophilia')
        hateful = _('Hateful')
        dangerous = _('Dangerous')
        send = _('Report send successfully.')

    class search_panel:
        title = _('Search settings')
        female = _('Girls 👸🏼')
        male = _('Boys 🥷')
        all = _('All ✈️')
        interest = _('Interest:')
        send_message = _('Send something sweet')

    class profile:
        change_name = _('Change name')
        change_media = _('Change media')
        change_loc = _('Change location')
        change_lang = _('Change language')
        change_interests = _('Change interests')
        change_bio = _('Change bio')
        deactivate = _('Deactivate 🪓')
        deactivate_title = _('Are you sure you want to deactivate your account?')

    class inbox:
        inbox_notif = _('📬\nYou have message.\nCheck your inbox...')
        like_notif = _('Someone sent you like❤️')
        reply_notif = _('Someone replied you📨')
        audio_notif = _('Someone sent you voice message')
        video_notif = _('Someone sent you video')
