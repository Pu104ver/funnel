from pyrogram import filters, Client
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_connector import get_db
from app.database.models import User
from app.bot.keyboards import (
    get_services_keyboard,
    tarot_keyboard,
    horoscope_keyboard,
    fortune_keyboard,
    consultation_keyboard,
    zodiac_keyboard,
)
from app.bot.utils.functions import toggle_subscription, is_user_exists


def register_handlers(app: Client):
    pending_questions = {}

    @app.on_message(filters.command("start"))
    async def start(client, message: Message):
        async for db in get_db():
            db: AsyncSession
            user = await db.execute(
                select(User).filter(User.username == message.from_user.username)
            )
            user = user.scalars().first()

            if user is None:
                user = User(
                    username=message.from_user.username,
                    full_name=f"{message.from_user.first_name} {message.from_user.last_name}",
                )
                db.add(user)
                await db.commit()

                await message.reply_text(
                    f"🖖Привет, {message.from_user.first_name}! Ты успешно зарегистрирован."
                )

                return

            await message.reply_text(f"🖖Привет, {message.from_user.first_name}!")

    @app.on_message(filters.command("help"))
    async def help_command(client: Client, message: Message):
        help_text = (
            "🤖 Добро пожаловать!\n\n"
            "Этот бот предоставляет различные услуги (/services):\n"
            "🔮 Гадание\n"
            "🌟 Гороскоп\n"
            "🃏 Карты Таро\n\n"
            "📩 Вы также можете задать вопрос специалисту, нажав на кнопку.\n"
            "Если у вас возникли проблемы, свяжитесь с поддержкой – /support"
            "\n\nP.S. Я не знаю какие-именно вы хотели увидеть от меня тут вопросы и ответы на них, но, полагаю, вам все же скорее код мой инетересен, нежели содержание ответов. Работать с тз в 4 строчки довольно непросто😇"
        )

        await message.reply_text(help_text)

    @app.on_message(filters.command("support"))
    async def support_command(client: Client, message: Message):
        support_text = (
            "🆘 Техническая поддержка\n\n"
            "Если у вас возникли вопросы или проблемы, свяжитесь с нашей поддержкой:\n"
            "📧 Email: support@example.com\n"
            "💬 Telegram: @support_bot\n\n"
            "Мы постараемся помочь вам как можно скорее!"
        )

        await message.reply_text(support_text)

    @app.on_message(filters.command("services"))
    async def services(client, message: Message):
        async for db in get_db():
            db: AsyncSession
            username = message.from_user.username
            if not await is_user_exists(username, db):
                await message.reply_text(
                    "🤖 Пожалуйста, зарегистрируйтесь, чтобы получить доступ к услугам."
                )
                return

        keyboard = get_services_keyboard()

        await message.reply_text(
            f"Выберите услугу:",
            reply_markup=keyboard,
        )

    @app.on_message(filters.command("subscribe"))
    async def subscribe(client, message: Message):
        async for db in get_db():
            db: AsyncSession
            user = await is_user_exists(message.from_user.username, db)

            if not user:
                await message.reply_text(
                    "🤖 Пожалуйста, зарегистрируйтесь, чтобы получить доступ к услугам."
                )
                return

            await message.reply_text(await toggle_subscription(user, db))

    @app.on_message(filters.command("set_zodiac"))
    async def send_zodiac_buttons(client: Client, message: Message):
        async for db in get_db():
            db: AsyncSession
            if not await is_user_exists(message.from_user.username, db):
                await message.reply_text(
                    "🤖 Пожалуйста, зарегистрируйтесь, чтобы получить доступ к установке знака зодиака."
                )
                return

        keyboard = zodiac_keyboard()
        await message.reply("Выберите ваш знак зодиака:", reply_markup=keyboard)

    @app.on_callback_query(
        filters.regex(
            r"zodiac_(aries|taurus|gemini|cancer|leo|virgo|libra|scorpio|sagittarius|capricorn|aquarius|pisces)"
        )
    )
    async def change_zodiac(client: Client, callback_query: CallbackQuery):
        zodiac_dict = {
            "zodiac_aries": "Овен",
            "zodiac_taurus": "Телец",
            "zodiac_gemini": "Близнецы",
            "zodiac_cancer": "Рак",
            "zodiac_leo": "Лев",
            "zodiac_virgo": "Дева",
            "zodiac_libra": "Весы",
            "zodiac_scorpio": "Скорпион",
            "zodiac_sagittarius": "Стрелец",
            "zodiac_capricorn": "Козерог",
            "zodiac_aquarius": "Водолей",
            "zodiac_pisces": "Рыбы",
        }

        username = callback_query.from_user.username
        zodiac_sign = callback_query.data

        async for db in get_db():
            db: AsyncSession
            user = await is_user_exists(username, db)

            if user:
                user.zodiac_sign = zodiac_sign.removeprefix("zodiac_")
                await db.commit()
                await callback_query.answer(
                    f"Ваш знак зодиака изменен на {zodiac_dict[zodiac_sign]}."
                )
                await callback_query.message.edit_text(
                    f"Ваш знак зодиака изменен на {zodiac_dict[zodiac_sign]}."
                )
            else:
                await callback_query.answer("🤖 Пожалуйста, зарегистрируйтесь.")

    @app.on_callback_query(filters.regex("ask_question"))
    async def ask_question_callback(client: Client, callback_query: CallbackQuery):
        async for db in get_db():
            db: AsyncSession
            if not await is_user_exists(callback_query.from_user.username, db):
                await callback_query.answer(
                    "🤖 Пожалуйста, зарегистрируйтесь, чтобы получить доступ к услугам."
                )
                return

        chat_id = callback_query.message.chat.id

        await callback_query.answer("💬Пожалуйста, напишите ваш вопрос в чате.⬇️")
        await callback_query.message.edit_text(
            "Напишите свой вопрос, и мы передадим его специалисту."
        )
        pending_questions[chat_id] = True

    @app.on_message(filters.text & filters.private)
    async def handle_question(client: Client, message: Message):
        chat_id = message.chat.id

        if chat_id in pending_questions:
            user_question = message.text

            del pending_questions[chat_id]  # Убираем пользователя из списка ожидания

            await message.reply_text(
                f"Ваш вопрос: '{user_question}' записан!✍️ Специалист скоро с вами свяжется.🗣️"
            )

    @app.on_callback_query(filters.regex("consultation"))
    async def consultation_callback(client: Client, callback_query: CallbackQuery):
        async for db in get_db():
            db: AsyncSession
            if not await is_user_exists(callback_query.from_user.username, db):
                await callback_query.answer(
                    "🤖 Пожалуйста, зарегистрируйтесь, чтобы получить доступ к услугам."
                )
                return

        response_text = (
            "Вы хотите записаться на консультацию. Пожалуйста, уточните ваш вопрос⬇️:"
        )
        keyboard = consultation_keyboard()
        await callback_query.message.edit_text(response_text, reply_markup=keyboard)
        await callback_query.answer()

    @app.on_callback_query(filters.regex("fortune_yes"))
    async def fortune_yes_callback(client: Client, callback_query: CallbackQuery):
        await callback_query.answer("Вы выбрали гадание!")
        await callback_query.message.edit_text("Ваше гадание: Скоро будет удача!✨✨✨")

        # Логика для выполнения гадания (можно интегрировать сюда или вернуть результаты гадания)

    @app.on_callback_query(filters.regex("horoscope_yes"))
    async def horoscope_yes_callback(client: Client, callback_query: CallbackQuery):
        await callback_query.answer("Вы выбрали гороскоп!")
        await callback_query.message.edit_text(
            "Ваш гороскоп на сегодня: Будьте внимательны к деталям.🤓"
        )

        # Тут тоже можно сделать апи интеграцию

    @app.on_callback_query(filters.regex("tarot_yes"))
    async def tarot_yes_callback(client: Client, callback_query: CallbackQuery):
        await callback_query.answer("Вы выбрали Таро!")
        await callback_query.message.edit_text(
            "Ваш расклад на Таро: Карта дня — Император.🫅"
        )

        # Логика для расклада Таро

    @app.on_callback_query(
        filters.regex("fortune") | filters.regex("horoscope") | filters.regex("tarot"),
    )
    async def handle_service(client: Client, callback_query: CallbackQuery):
        response_text: str = ""
        keyboard: InlineKeyboardMarkup = None

        if callback_query.data == "fortune":
            response_text = "Вы выбрали услугу гадания. Хотите ли вы получить гадание прямо сейчас?🔮"
            keyboard = fortune_keyboard()

        elif callback_query.data == "horoscope":
            response_text = (
                "Вы выбрали услугу гороскопа. Хотите получить гороскоп на сегодня?🌃"
            )
            keyboard = horoscope_keyboard()

        elif callback_query.data == "tarot":
            response_text = "Вы выбрали Таро. Хотите провести расклад?🃏"
            keyboard = tarot_keyboard()

        await callback_query.message.edit_text(response_text, reply_markup=keyboard)
        await callback_query.answer()
