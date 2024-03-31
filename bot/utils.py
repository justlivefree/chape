from aiogram.types import Message, InputMediaPhoto, InputMediaVideo, BotCommand
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim

from bot.configs import words


def media_maker(message: Message):
    if message.photo:
        return {'type': 'photo', 'file_id': message.photo[0].file_id}
    if message.video:
        return {'type': 'video', 'file_id': message.video.file_id}


def media_group_maker(media: list, info: str):
    result = [InputMediaPhoto(media=media[0]['file_id'], caption=info)]
    for m in media[1:]:
        if m['type'] == 'photo':
            result.append(InputMediaPhoto(media=m['file_id']))
        else:
            result.append(InputMediaVideo(media=m['file_id']))
    return result


async def get_location_data(lat, lon):
    async with Nominatim(user_agent='tg-bot-bot', adapter_factory=AioHTTPAdapter) as geolocator:
        result = await geolocator.reverse((float(lat), float(lon)), language='en')
        loc = result.raw['address']
        return {
            'lat': lat,
            'lon': lon,
            'country': loc['country'],
            'city': loc.get('city'),
            'state': loc.get('state')
        }


async def check_location(loc_name):
    async with Nominatim(user_agent='tg-bot-bot', adapter_factory=AioHTTPAdapter) as geolocator:
        result = await geolocator.geocode(query=loc_name, language='en')
        loc = result.raw
        print(loc)
        address_type = loc['addresstype']
        if address_type not in ('city', 'state'):
            address_type = 'state'
        return {
            'lat': float(loc['lat']),
            'lon': float(loc['lon']),
            'country': loc['display_name'].split(', ')[-1],
            address_type: loc['name'].split()[0],
        }


async def user_info_sender(bot, user, media, chat_id, reply_markup=None):
    interests = filter(lambda key: getattr(user.interests, key.lower().replace(' ', '_')), words.interests.keys())
    interests = ''.join(map(lambda val: ' #' + val, interests))
    loc = (user.city if user.city else user.state) + f', {user.country}'
    info = '📍{location}\n📄{name}, {age}\n{bio}\n\n{interests}'. \
        format(name=user.fullname, age=user.age,
               location=loc,
               bio=user.description, interests=interests)
    if isinstance(media, dict):
        if media['type'] == 'video':
            return await bot.send_video(chat_id, media['file_id'], caption=info, reply_markup=reply_markup)
        else:
            return await bot.send_photo(chat_id, media['file_id'], caption=info, reply_markup=reply_markup)
    elif isinstance(media, list):
        return await bot.send_media_group(chat_id, media=media_group_maker(media, info))


def get_bot_commands():
    return [BotCommand(command='start', description=words.cmd_start),
            BotCommand(command='help', description=words.cmd_help),
            BotCommand(command='admin', description=words.cmd_admin)]
