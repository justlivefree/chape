from aiogram.types import Message, InputMediaPhoto, InputMediaVideo
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim
from chape_bot.bot.configs import words


def media_maker(message: Message):
    if message.photo:
        return {'type': 'photo', 'file_id': message.photo[0].file_id}
    if message.video:
        return {'type': 'video', 'file_id': message.video.file_id}


def media_group_maker(media: list, info: str):
    result = []
    is_add = True
    for m in media:
        if m['type'] == 'photo':
            result.append(InputMediaPhoto(media=m['file_id'], caption=info if is_add else None))
        else:
            result.append(InputMediaVideo(media=m['file_id'], caption=info if is_add else None))
        is_add *= False
    return result


async def get_location_data(lat, lon):
    async with Nominatim(user_agent='tg-bot-bot', adapter_factory=AioHTTPAdapter) as geolocator:
        result = await geolocator.reverse((float(lat), float(lon)), language='en')
        return result.raw.get('address')


async def user_info_sender(bot, user, media, chat_id, reply_markup=None):
    interests = filter(lambda key: getattr(user.interests, key.lower().replace(' ', '_')), words.interests.keys())
    interests = ''.join(map(lambda val: ' #' + val, interests))
    info = f"{user.fullname}, {user.age}, {user.city}\n{user.description}\n\n{interests}"
    if isinstance(media, dict):
        if media['type'] == 'video':
            return await bot.send_video(chat_id, media['file_id'], caption=info, reply_markup=reply_markup)
        else:
            return await bot.send_photo(chat_id, media['file_id'], caption=info, reply_markup=reply_markup)
    elif isinstance(media, list):
        return await bot.send_media_group(chat_id, media=media_group_maker(media, info))
