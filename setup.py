import os.path

import polib
from babel.messages.frontend import CommandLineInterface
from googletrans import Translator

LANGS = ('ru', 'uz')


def translate_locales():
    translator = Translator()
    for lang in LANGS[:-1]:
        path = f'locales/{lang}/LC_MESSAGES/chape_bot.po'
        pofile = polib.pofile(path)
        for entry in pofile:
            entry.msgstr = translator.translate(entry.msgid, dest=lang).text
        pofile.save(path)
    cmd = 'pybabel compile -d locales -D chape_bot'
    CommandLineInterface().run(cmd.split(' '))


def create_locales():
    os.mkdir('locales')
    cmds = ('pybabel extract --input-dirs chape_bot -o locales/chape_bot.pot',
            'pybabel init -i locales/chape_bot.pot -d locales -D chape_bot -l en',
            'pybabel init -i locales/chape_bot.pot -d locales -D chape_bot -l ru',
            'pybabel init -i locales/chape_bot.pot -d locales -D chape_bot -l uz')
    for cmd in cmds:
        CommandLineInterface().run(cmd.split(' '))
    translate_locales()


if __name__ == '__main__':
    if not os.path.exists('locales'):
        create_locales()
