from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.database.models import User


def get_services_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Гадания", callback_data="fortune"),
                InlineKeyboardButton("Гороскопы", callback_data="horoscope"),
            ],
            [
                InlineKeyboardButton("Таро", callback_data="tarot"),
                InlineKeyboardButton(
                    "Записаться к специалисту", callback_data="consultation"
                ),
            ],
        ]
    )
    return keyboard


def fortune_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Да, хочу гадание", callback_data="fortune_yes")],
            [
                InlineKeyboardButton(
                    "Нет, хочу записаться на консультацию", callback_data="consultation"
                )
            ],
        ]
    )
    return keyboard


def horoscope_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Да, покажи мой гороскоп", callback_data="horoscope_yes"
                )
            ],
            [
                InlineKeyboardButton(
                    "Нет, хочу записаться на консультацию", callback_data="consultation"
                )
            ],
        ]
    )
    return keyboard


def tarot_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Да, проведи расклад", callback_data="tarot_yes")],
            [
                InlineKeyboardButton(
                    "Нет, хочу записаться на консультацию", callback_data="consultation"
                )
            ],
        ]
    )
    return keyboard


def consultation_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Задать вопрос специалисту", callback_data="ask_question"
                )
            ]
        ]
    )
    return keyboard


def zodiac_keyboard() -> InlineKeyboardMarkup:
    zodiac_dict = {
        "aries": "Овен",
        "taurus": "Телец",
        "gemini": "Близнецы",
        "cancer": "Рак",
        "leo": "Лев",
        "virgo": "Дева",
        "libra": "Весы",
        "scorpio": "Скорпион",
        "sagittarius": "Стрелец",
        "capricorn": "Козерог",
        "aquarius": "Водолей",
        "pisces": "Рыбы",
    }

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(value, callback_data=f"zodiac_{key}")]
            for key, value in zodiac_dict.items()
        ]
    )
    return keyboard
