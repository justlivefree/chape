import enum

from sqlalchemy import Column, String, Integer, SmallInteger, DateTime, Text, Boolean, Enum, ForeignKey, func, \
    BigInteger, Float
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Gender(enum.Enum):
    male = 'male'
    female = 'female'


class ReportType(enum.Enum):
    sexual = 'sexual'
    pedophilia = 'pedophilia'
    hateful = 'hateful'
    dangerous = 'dangerous'


class BaseModel:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class User(Base, BaseModel):
    __tablename__ = 'users'

    # ----
    tg_id = Column(BigInteger, unique=True)
    username = Column(String(length=255), nullable=True)
    is_bot = Column(Boolean, default=False)
    fullname = Column(String(255))
    age = Column(SmallInteger)
    gender = Column(Enum(Gender))
    description = Column(Text, nullable=True, default=None)
    interests = relationship('Interest', back_populates='user', uselist=False)

    # ----
    lang = Column(String(5))
    locale = Column(String(5))
    city = Column(String(255))
    country = Column(String(255))
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)

    # ----
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)

    # ---
    sent_complaints = relationship('Report', foreign_keys='[Report.sender_id]')
    received_complaints = relationship('Report', foreign_keys='[Report.receiver_id]')

    # ----
    is_active = Column(Boolean, default=True)
    is_block = Column(Boolean, default=False)
    block_period = Column(DateTime, nullable=True)

    def __str__(self):
        return f'{self.id} {self.fullname}'


class Interest(Base, BaseModel):
    __tablename__ = 'interests'

    user_id = Column(ForeignKey('users.tg_id', ondelete='CASCADE'))
    user = relationship('User', back_populates='interests')

    anime = Column(Boolean, default=False)
    movie = Column(Boolean, default=False)
    music = Column(Boolean, default=False)

    cars = Column(Boolean, default=False)
    sport = Column(Boolean, default=False)

    books = Column(Boolean, default=False)
    study = Column(Boolean, default=False)
    math = Column(Boolean, default=False)
    design = Column(Boolean, default=False)
    art = Column(Boolean, default=False)
    programing = Column(Boolean, default=False)

    gaming = Column(Boolean, default=False)
    pubg = Column(Boolean, default=False)
    cs2 = Column(Boolean, default=False)
    mobile_legends = Column(Boolean, default=False)


class Report(Base, BaseModel):
    __tablename__ = 'reports'

    sender_id = Column(ForeignKey('users.tg_id', ondelete='CASCADE'), nullable=True)
    receiver_id = Column(ForeignKey('users.tg_id', ondelete='CASCADE'), nullable=True)
    report_type = Column(Enum(ReportType), nullable=True)
    description = Column(String(255), nullable=True)
    audio_id = Column(String(255), nullable=True)
    is_read = Column(Boolean, default=False)
