import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()

db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')

mongo_host = os.getenv('MONGO_HOSTNAME')

db_url = f'postgresql+asyncpg://{db_user}:{db_password}@127.0.0.1:5432/{db_name}'
mongo_url = f'mongodb://admin:1111@{mongo_host}:27017'

engine = create_async_engine(db_url, echo=True)

PGSession = async_sessionmaker(engine, expire_on_commit=False)
mongo_client = AsyncIOMotorClient(mongo_url)
mongo_db = mongo_client.chapebot
