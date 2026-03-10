from sqlalchemy.orm import sessionmaker
from .models import engine, User

# Создаем сессию
SessionLocal = sessionmaker(bind=engine)

def create_user(chat_id: int, gender: str, age: int, weight: float, height: int):
    """
    Создает нового пользователя в базе данных
    """
    db = SessionLocal()
    try:
        # Проверяем, существует ли уже пользователь с таким chat_id
        existing_user = db.query(User).filter(User.chat_id == chat_id).first()
        
        if existing_user:
            # Обновляем существующего пользователя
            existing_user.gender = gender
            existing_user.age = age
            existing_user.weight = weight
            existing_user.height = height
        else:
            # Создаем нового пользователя
            db_user = User(
                chat_id=chat_id,
                gender=gender,
                age=age,
                weight=weight,
                height=height
            )
            db.add(db_user)
        
        db.commit()
        if existing_user:
            return existing_user
        else:
            return db_user
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_user(chat_id: int):
    """
    Возвращает пользователя по chat_id
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.chat_id == chat_id).first()
        return user
    finally:
        db.close()

def update_user(chat_id: int, **kwargs):
    """
    Обновляет данные пользователя
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.chat_id == chat_id).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def delete_user(chat_id: int):
    """
    Удаляет пользователя из базы данных
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.chat_id == chat_id).first()
        if user:
            db.delete(user)
            db.commit()
    finally:
        db.close()