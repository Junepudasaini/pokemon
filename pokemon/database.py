from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os


load_dotenv()

engine = create_async_engine(
    url = os.getenv('DATABASE_URL'),
    echo = True
)

session = async_sessionmaker(
    bind= engine,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

