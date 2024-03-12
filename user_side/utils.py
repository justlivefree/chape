from aiogram.types import Message, InputMediaPhoto, InputMediaVideo
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim

from database.models import User
from user_side.config import words


def media_maker(message: Message):
    if message.photo:
        return {'type': 'photo', 'file_id': message.photo[0].file_id}
    if message.video:
        return {'type': 'video', 'file_id': message.video.file_id}


def user_info_maker(user: User):
    interests = filter(lambda key: getattr(user.interests, key.lower().replace(' ', '_')), words.interests.keys())
    interests = ''.join(map(lambda val: ' #' + val, interests))
    text = f"{user.fullname}, {user.age}, {user.city}\n{user.description}\n\n{interests}"
    return text


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
