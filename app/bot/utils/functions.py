from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models import User
from app.database.db_connector import get_db


async def toggle_subscription(user: User, db: AsyncSession):
    """Переключает подписку на рассылку для пользователя.

    Если пользователь зарегистрирован, то переключает его подписку.
    Если пользователь не зарегистрирован, то возвращает сообщение об ошибке.
    """
    if user:
        if user.is_subscribed:
            user.is_subscribed = False
            await db.commit()
            return "Вы успешно отписались от рассылки!"
        else:
            user.is_subscribed = True
            db.add(user)
            await db.commit()
            return "Вы успешно подписаны на рассылки!"
    else:
        return "Пожалуйста, зарегистрируйтесь, прежде чем подписаться."
    

async def is_user_exists(username: str, db: AsyncSession) -> User | None:

    """
    Проверяет существование пользователя в базе данных по имени пользователя.

    Аргументы:
        username (str): Имя пользователя для поиска.
        db (AsyncSession): Сессия базы данных.

    Возвращает:
        User | None: Объект пользователя, если он существует, иначе None.
    """

    user = await db.execute(select(User).filter_by(username=username))
    return user.scalars().first() if user else None
