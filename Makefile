set_locales:
	mkdir locales
	pybabel extract --input-dirs . -o locales/chape_bot.pot
set_lang:
	pybabel init -i locales/chape_bot.pot -d locales -D chape_bot -l en
	pybabel init -i locales/chape_bot.pot -d locales -D chape_bot -l ru
	pybabel init -i locales/chape_bot.pot -d locales -D chape_bot -l uz
update_locales:
	pybabel update -d locales -D chape_bot -i locales/chape_bot.pot
compile_locales:
	pybabel compile -d locales -D chape_bot