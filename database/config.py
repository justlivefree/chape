import logging
import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

mongo_host = os.getenv('MONGO_HOST')
mongo_port = os.getenv('MONGO_PORT')
mongo_admin = os.getenv('MONGO_ADMIN')
mongo_password = os.getenv('MONGO_PASSWORD')
mondo_db = os.getenv('MONGO_DB')

db_url = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
mongo_url = f'mongodb://admin:1111@{mongo_host}:{mongo_port}'

engine = create_async_engine(db_url, echo=True)

session = async_sessionmaker(engine, expire_on_commit=False)
mongo_client = AsyncIOMotorClient(mongo_url)
mongo_db = mongo_client.media_data
# logging.getLogger('sqlalchemy').setLevel(logging.INFO)
