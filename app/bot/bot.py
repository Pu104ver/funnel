from pyrogram import Client

from app.core.config import settings
from .handlers.commands_handlers import register_handlers


api_id = settings.API_ID
api_hash = settings.API_HASH

app = Client(
    "funnel_bot", bot_token=settings.BOT_TOKEN, api_id=api_id, api_hash=api_hash
)


register_handlers(app)


if __name__ == "__main__":
    app.run()
