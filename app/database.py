from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# ВАЖНО: используем синхронный драйвер psycopg (добавляем +psycopg в URL)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:пароль@localhost/event_system")

# Создаём синхронный движок (не асинхронный!)
engine = create_engine(DATABASE_URL, echo=True)

# Фабрика сессий (синхронная)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Зависимость для получения сессии БД в эндпоинтах
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()