import datetime
from datetime import datetime, timedelta

from sqlalchemy import update, select, func, delete
from sqlalchemy.orm import selectinload, joinedload

from database.config import session, mongo_client, mongo_db, engine
from database.models import User, Interest, Report, Base


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
        db = mongo_client.media_data
        coll = db.users
        await coll.insert_one({"created_at": datetime.utcnow()})


class UserQuery:
    # user
    @staticmethod
    async def create(**kwargs):
        async with session() as _session:
            interests = {k.lower().replace(' ', '_'): bool(v) for k, v in kwargs['interests'].items()}
            del kwargs['interests'], kwargs['media']
            user = User(**kwargs)
            _session.add(user)
            _session.add(Interest(user=user, **interests))
            await _session.commit()

    @staticmethod
    async def update(tg_id, **kwargs):
        async with session() as _session:
            query = update(User).where(User.tg_id == tg_id).values(**kwargs)
            await _session.execute(query)
            await _session.commit()

    @staticmethod
    async def update_interests(tg_id, kwargs):
        async with session() as _session:
            data = {}
            for k, v in kwargs.items():
                data[k.lower().replace(' ', '_')] = v
            query = update(Interest).where(Interest.user_id == tg_id).values(**data)
            await _session.execute(query)
            await _session.commit()

    @staticmethod
    async def activate_user(tg_id):
        async with session() as _session:
            query = update(User).where(User.tg_id == tg_id).values(is_active=True)
            result = await _session.execute(query)
            if result.rowcount:
                await _session.commit()
                return True

    @staticmethod
    async def deactivate_user(tg_id):
        async with session() as _session:
            query = update(User).where(User.tg_id == tg_id).values(is_active=False)
            result = await _session.execute(query)
            if result.rowcount:
                await _session.commit()
                return True

    @staticmethod
    async def delete_user(tg_id):
        async with session() as _session:
            query = delete(User).where(User.tg_id == tg_id).options(selectinload(User.interests))
            result = await _session.execute(query)
            if result.rowcount:
                await _session.commit()
                return True

    # media
    @staticmethod
    async def create_media(tg_id, media):
        await mongo_db.users.insert_one({
            'user_id': int(tg_id),
            'media': media
        })

    @staticmethod
    async def update_media(tg_id, media):
        await mongo_db.users.update_one({'user_id': int(tg_id)}, {'$set': {'media': media}})

    @staticmethod
    async def delete_media(tg_id):
        await mongo_db.users.delete_one({'user_id': int(tg_id)})

    # get data
    @staticmethod
    async def get_user(tg_id, load_all=False):
        async with session() as _session:
            query = select(User).where(User.tg_id == tg_id)
            if load_all:
                query = query.options(joinedload(User.interests),
                                      selectinload(User.received_complaints),
                                      selectinload(User.sent_complaints))
            user = await _session.execute(query)
            return user.scalar()

    @staticmethod
    async def get_interests(tg_id):
        async with session() as _session:
            query = select(Interest).where(Interest.user_id == tg_id)
            result = await _session.execute(query)
            return result.scalar()

    @staticmethod
    async def get_media(tg_id):
        return (await mongo_db.users.find_one({'user_id': int(tg_id)})).get('media')

    @staticmethod
    async def select_partner(**options):
        async with session() as _session:
            query = select(User).join(Interest).options(joinedload(User.interests))
            if gender := options.get('gender'):
                query = query.where(User.gender == gender)
            if interest := options.get('interest'):
                query = query.where(getattr(Interest, interest) == True)
            if city := options.get('city'):                query = query.where(User.city == city)
            query = query.where(User.is_active == True).order_by(func.random()).limit(1)
            user, media = (await _session.execute(query)).scalar(), None
            if user:
                media = await UserQuery.get_media(user.tg_id)
            return user, media


class ReportQuery:
    @staticmethod
    async def create(**kwargs):
        async with session() as _session:
            _session.add(Report(**kwargs))
            await _session.commit()

    @staticmethod
    async def delete(report_id):
        async with session() as _session:
            query = delete(Report).where(Report.id == report_id)
            _session.execute(query)
            await _session.commit()

    @staticmethod
    async def delete_old(period):
        async with session() as _session:
            threshold_date = datetime.utcnow() - timedelta(days=period)
            query = delete(Report).where(Report.created_at <= threshold_date)
            _session.execute(query)
            await _session.commit()

    @staticmethod
    async def read(report_id):
        async with session() as _session:
            query = update(Report).where(Report.id == report_id).values(is_read=True)
            _session.execute(query)
            await _session.commit()
