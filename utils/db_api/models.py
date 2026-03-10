from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    gender = Column(String(10), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<User(chat_id={self.chat_id}, gender='{self.gender}', age={self.age}, weight={self.weight}, height={self.height})>"

# Создаем движок и сессию
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем параметры подключения из переменных окружения
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
SessionLocal = sessionmaker(bind=engine)

# Функция для получения сессии
def get_db_session():
    return SessionLocal()