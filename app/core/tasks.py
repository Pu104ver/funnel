from app.celery import app_celery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx

from app.database.db_connector import get_db
from app.database.models import User
from app.bot.bot import app

import asyncio


@app_celery.task
def send_daily_horoscope():
    loop = asyncio.get_event_loop()

    loop.run_until_complete(_send_daily_horoscope())


async def _fetch_horoscope(sign: str):
    url = f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign={sign}&day=TODAY"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["data"]["horoscope_data"]
        return None


async def _send_daily_horoscope():
    async for db in get_db():
        db: AsyncSession
        users = await db.execute(select(User).filter(User.is_subscribed == True))
        users = users.scalars().all()

        for user in users:
            if user.zodiac_sign:
                horoscope = await _fetch_horoscope(user.zodiac_sign)
                if horoscope is None:
                    continue
                
                async with app as bot_app:
                    await bot_app.send_message(
                        user.username,
                        f"Ваш гороскоп на сегодня: {horoscope}",
                    )
            else:
                async with app as bot_app:
                    await bot_app.send_message(
                        user.username,
                        "У вас не установлен знак зодиака. Пожалуйста, выберите его в настройках.",
                    )
