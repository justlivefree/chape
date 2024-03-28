import polib
from googletrans import Translator

LANGS = ('ru', 'uz')


def translate_locales():
    translator = Translator()
    for lang in LANGS:
        path = f'locales/{lang}/LC_MESSAGES/chape_bot.po'
        pofile = polib.pofile(path)
        for entry in pofile:
            entry.msgstr = translator.translate(entry.msgid, dest=lang).text
        pofile.save(path)


if __name__ == '__main__':
    translate_locales()
