import datetime
from datetime import datetime, timedelta

from sqlalchemy import update, select, func, delete
from sqlalchemy.orm import selectinload, joinedload

from chape_bot.database.config import PGSession, mongo_client, engine, mongo_db
from chape_bot.database.models import User, Interest, Report, Base


class DBQuery:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def drop_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @staticmethod
    async def create_media_col():
        db = mongo_client.chapebot
        collection = db.users
        await collection.insert_one({"title": "delete me", "created_at": datetime.utcnow()})


class UserQuery:
    @staticmethod
    async def create(**kwargs):
        async with PGSession() as session:
            interests = {k.lower().replace(' ', '_'): bool(v) for k, v in kwargs['interests'].items()}
            del kwargs['interests'], kwargs['media']
            user = User(**kwargs)
            session.add(user)
            session.add(Interest(user=user, **interests))
            await session.commit()

    @staticmethod
    async def update(tg_id, **kwargs):
        async with PGSession() as session:
            query = update(User).where(User.tg_id == tg_id).values(**kwargs)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def update_interests(tg_id, kwargs):
        async with PGSession() as session:
            data = {}
            for k, v in kwargs.items():
                data[k.lower().replace(' ', '_')] = v
            query = update(Interest).where(Interest.user_id == tg_id).values(**data)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def activate_user(tg_id):
        async with PGSession() as session:
            query = update(User).where(User.tg_id == tg_id).values(is_active=True)
            result = await session.execute(query)
            if result.rowcount:
                await session.commit()
                return True

    @staticmethod
    async def deactivate_user(tg_id):
        async with PGSession() as session:
            query = update(User).where(User.tg_id == tg_id).values(is_active=False)
            result = await session.execute(query)
            if result.rowcount:
                await session.commit()
                return True

    @staticmethod
    async def delete_user(tg_id):
        async with PGSession() as session:
            query = delete(User).where(User.tg_id == tg_id).options(selectinload(User.interests))
            result = await session.execute(query)
            if result.rowcount:
                await session.commit()
                return True

    # media
    @staticmethod
    async def create_media(tg_id, media):
        await mongo_db.media.insert_one({
            'user_id': int(tg_id),
            'media': media
        })

    @staticmethod
    async def update_media(tg_id, media):
        await mongo_db.media.update_one({'user_id': int(tg_id)}, {'$set': {'media': media}})

    @staticmethod
    async def delete_media(tg_id):
        await mongo_db.media.delete_one({'user_id': int(tg_id)})

    # get data
    @staticmethod
    async def get_user(tg_id, load_all=False):
        async with PGSession() as session:
            query = select(User).where(User.tg_id == tg_id)
            if load_all:
                query = query.options(joinedload(User.interests),
                                      selectinload(User.received_complaints),
                                      selectinload(User.sent_complaints))
            user = await session.execute(query)
            return user.scalar()

    @staticmethod
    async def get_interests(tg_id):
        async with PGSession() as session:
            query = select(Interest).where(Interest.user_id == tg_id)
            result = await session.execute(query)
            return result.scalar()

    @staticmethod
    async def get_media(tg_id):
        result = await mongo_db.media.find_one({'user_id': int(tg_id)})
        return result.get('media')

    @staticmethod
    async def select_partner(tg_id, **options):
        async with PGSession() as session:
            query = select(User).where(User.tg_id != tg_id)
            if (gender := options.get('gender')) != 'any':
                query = query.where(User.gender == gender)
            if interest := options.get('interest'):
                query = query.where(getattr(Interest, interest) == True)
            if city := options.get('city'):
                query = query.where(User.city == city)
            query = query.where((User.is_active == True) & (User.is_block == False)). \
                join(Interest).options(joinedload(User.interests)). \
                order_by(func.random()).limit(1)
            try:
                user = (await session.execute(query)).scalar()
                media = await UserQuery.get_media(user.tg_id)
                if user and media:
                    return user, media
            except AttributeError:
                pass


class ReportQuery:
    @staticmethod
    async def create(**kwargs):
        async with PGSession() as session:
            session.add(Report(**kwargs))
            await session.commit()

    @staticmethod
    async def delete(report_id):
        async with PGSession() as session:
            query = delete(Report).where(Report.id == report_id)
            session.execute(query)
            await session.commit()

    @staticmethod
    async def delete_old(period):
        async with PGSession() as session:
            threshold_date = datetime.utcnow() - timedelta(days=period)
            query = delete(Report).where(Report.created_at <= threshold_date)
            session.execute(query)
            await session.commit()

    @staticmethod
    async def read(report_id):
        async with PGSession() as session:
            query = update(Report).where(Report.id == report_id).values(is_read=True)
            await session.execute(query)
            await session.commit()


class InboxQuery:
    @staticmethod
    async def create(**kwargs):
        await mongo_db.inbox.insert_one(kwargs)

    @staticmethod
    async def update(message_id):
        pass

    @staticmethod
    async def make_messages_read(receiver):
        await mongo_db.inbox.update_many({'receiver': receiver}, {'$set': {'is_read': True}})

    @staticmethod
    async def delete(receiver_id):
        await mongo_db.inbox.delete_one({'receiver': receiver_id})

    @staticmethod
    async def get_all(receiver):
        return await mongo_db.inbox.find({'receiver': receiver, 'is_read': False}).to_list(length=100)
