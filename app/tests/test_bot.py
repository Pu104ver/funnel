from pyrogram import Client
from pyrogram.types import CallbackQuery
from unittest.mock import AsyncMock

from app.core.config import settings
from app.bot.handlers.commands_handlers import register_handlers

import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def bot():
    app = Client("test_bot", bot_token=settings.BOT_TOKEN, api_id=settings.API_ID, api_hash=settings.API_HASH)
    register_handlers(app)
    await app.start()
    yield app
    await app.stop()


# Тест команды /start
@pytest.mark.asyncio
async def test_start_command(bot: Client):
    message = AsyncMock()
    message.chat.id = 123456789
    message.text = "/start"

    bot.send_message = AsyncMock(
        return_value=AsyncMock(text="Привет! Добро пожаловать")
    )

    response = await bot.send_message(message.chat.id, "/start")
    assert "Привет" in response.text


# Тест команды /help
@pytest.mark.asyncio
async def test_help_command(bot: Client):
    message = AsyncMock()
    message.chat.id = 123456789
    message.text = "/help"

    bot.send_message = AsyncMock(
        return_value=AsyncMock(text="Добро пожаловать в бота!")
    )

    response = await bot.send_message(message.chat.id, "/help")
    assert "Добро пожаловать" in response.text


# Тест неизвестного сообщения
@pytest.mark.asyncio
async def test_unknown_message(bot: Client):
    message = AsyncMock()
    message.chat.id = 123456789
    message.text = "Какая погода?"

    bot.send_message = AsyncMock(return_value=AsyncMock(text="Я вас не понимаю"))

    response = await bot.send_message(message.chat.id, "Какая погода?")
    assert "не понимаю" in response.text


# Тест обработки inline-кнопки
@pytest.mark.asyncio
async def test_callback_query(bot: Client):
    callback_query = AsyncMock(spec=CallbackQuery)
    callback_query.id = "12345"
    callback_query.from_user = AsyncMock(id=123456789)
    callback_query.message = AsyncMock(chat=AsyncMock(id=123456789))
    callback_query.data = "ask_question"

    bot.answer_callback_query = AsyncMock(return_value=None)
    bot.send_message = AsyncMock(return_value=AsyncMock(text="Напишите ваш вопрос"))

    await bot.answer_callback_query(callback_query.id)
    response = await bot.send_message(
        callback_query.message.chat.id, "Напишите ваш вопрос"
    )

    assert "Напишите ваш вопрос" in response.text
