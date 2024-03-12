from aiogram.utils.i18n import gettext as _


class words:
    policy = _("Hello, esteemed user. \nThrough this bot, you can connect with "
               "friends and meet new people. \n\nPlease note that the bot administrators "
               "continuously monitor its operation to ensure everything runs smoothly. "
               "If you come across any inappropriate images or videos with a questionable "
               "character, please report to us. We will take action thereafter. "
               "\n\nIn addition, the bot owner does not assume responsibility for any material "
               "or moral damage that may arise from your interaction with the bot. "
               "\n\nIf you have any questions or suggestions, feel free to contact us at %s.")
    wellcome = _('Wellcome')
    search_title = _('Write something sweet')
    income_message = _('You %d have messages')
    interests = (
        _('Anime'), _('Movie'), _('Music'),
        _('Cars'), _('Sport'),
        _('Books'), _('Study'),
        _('Math'), _('Design'),
        _('Art'), _('Programing'),
        _('Gaming'), _('PUBG'),
        _('CS2'), _('Mobile Legends'))
    ready = _('Ready⏩')
    back = _('Back⬅️')

    class errors:
        type_number = _('Write number')
        send_one_media = _('Send only photo or video')
        age_range = _('Your age does not apply for policy')
        blocked = _('You have been blocked for %s days')
        deactivated = _('You deactivated. Click button below for activation')

    class signup:
        agree = _('Agree')
        disagree = _('Disagree')
        fullname = _('Name:')
        age = _('Age:')
        gender = (_('Gender:'), _('Male🙋‍♂️'), _('Female‍🙋‍♀️'))
        city = _('City:')
        bio = _('Write about yourself:')
        info_choice = _('Choose your interests, it helps to make better conversation')
        choose = _('Choose:')
        media = _('Send profile photo or video')

    class main_panel:
        title = _('Main menu')
        search = _('Search 🚀')
        inbox = _('Inbox 📥')
        profile = _('Profile 👤')

    class search_panel:
        female = _('Girls 👸🏼')
        male = _('Boys 🥷')
        all = _('All ✈️')

    class profile:
        change_name = _('Change name')
        change_photo = _('Change photo')
        change_city = _('Change city')
        change_interests = _('Change interests')
        change_bio = _('Change bio')
        deactivate = _('Deactivate 🪓')
        hello = _('NOTHING')
