from celery import Celery
from datetime import timedelta

from app.core.config import settings


app_celery = Celery(
    "funnel",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL,
    include=["app.core.tasks"],
)

app_celery.autodiscover_tasks()

app_celery.conf.beat_schedule = {
    "send_daily_horoscope": {
        "task": "app.core.tasks.send_daily_horoscope",
        "schedule": (
            timedelta(seconds=25) if settings.DEBUG else timedelta(days=1)
        ),  # для теста сделал каждые 25 сек
    },
}
