# -*- coding: utf-8 -*-
"""
Telegram Bot Keyboards & UI Components for CME Metals Terminal.
Centralizes all reply and inline keyboard builders.
"""
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

import config
from urllib.parse import quote_plus


def get_share_url(text: str = "", url: str = "") -> str:
    """Builds native Telegram share URL (t.me/share/url)."""
    bot_name = getattr(config, "BOT_USERNAME", "cme_daily_info_bot")
    target_url = url or f"https://t.me/{bot_name}?start=report"
    share_text = text or "📊 CME QuikStrike — ТОП-5 опционных контрактов и открытый интерес (OI)"
    return f"https://t.me/share/url?url={quote_plus(target_url)}&text={quote_plus(share_text)}"


def get_guide_url() -> str:
    """Builds deep-link URL to open the CME analytics beginner guide inside the bot."""
    bot_name = getattr(config, "BOT_USERNAME", "cme_daily_info_bot")
    return f"https://t.me/{bot_name}?start=guide"


def get_miniapp_reply_keyboard() -> ReplyKeyboardMarkup:
    """Returns persistent Telegram Reply Keyboard with Mini App and QuikStrike buttons."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📈 Открыть Терминал CME 🟡⚪",
                    web_app=WebAppInfo(url=config.WEBAPP_URL)
                )
            ],
            [
                KeyboardButton(text="🎯 Most Actives OI (≥1000)"),
                KeyboardButton(text="📊 Котировки"),
            ],
            [
                KeyboardButton(text="📖 Пояснение терминов"),
                KeyboardButton(text="ℹ️ О терминале"),
            ]
        ],
        resize_keyboard=True
    )


def get_miniapp_inline_keyboard() -> InlineKeyboardMarkup:
    """Returns Inline Keyboard to launch Mini App with live charts, share, and guide actions."""
    share_text = "📈 Онлайн-терминал CME Group: котировки металлов, валют и опционы QuikStrike в реальном времени"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Запустить CME Mini App (Графики Live)",
                    web_app=WebAppInfo(url=config.WEBAPP_URL)
                )
            ],
            [
                InlineKeyboardButton(
                    text="📖 Пояснение терминов",
                    callback_data="open_cme_guide"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Обновить",
                    callback_data="refresh_text_quotes"
                ),
                InlineKeyboardButton(
                    text="↗️ Поделиться",
                    url=get_share_url(text=share_text)
                )
            ]
        ]
    )


def get_oi_inline_keyboard(symbol: str = "GC") -> InlineKeyboardMarkup:
    """Returns Inline Keyboard for QuikStrike Most Actives reports."""
    inst_name = "Золото (Gold)" if symbol == "GC" else ("Серебро (Silver)" if symbol == "SI" else symbol)
    share_text = f"🎯 Отчет CME QuikStrike Most Actives ({inst_name}): открытый интерес и объемы опционов"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎯 Открыть QuikStrike Most Actives в Mini App",
                    web_app=WebAppInfo(url=f"{config.WEBAPP_URL}#most-actives")
                )
            ],
            [
                InlineKeyboardButton(
                    text="📖 Пояснение терминов",
                    callback_data="open_cme_guide"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Обновить данные",
                    callback_data=f"refresh_oi_data:{symbol.upper()}"
                ),
                InlineKeyboardButton(
                    text="↗️ Поделиться",
                    url=get_share_url(text=share_text)
                )
            ]
        ]
    )


def get_channel_inline_keyboard(share_text: str = "", share_url: str = "") -> InlineKeyboardMarkup:
    """Returns buttons attached to channel reports (direct URL link compatible with channels/groups)."""
    text = share_text or "📊 Актуальный срез CME QuikStrike: ТОП-5 контрактов по открытому интересу (OI)"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Открыть QuikStrike Терминал (Mini App)",
                    url=config.WEBAPP_URL
                )
            ],
            [
                InlineKeyboardButton(
                    text="📖 Пояснение терминов",
                    url=get_guide_url()
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Обновить отчет",
                    callback_data="refresh_channel_report"
                ),
                InlineKeyboardButton(
                    text="↗️ Поделиться",
                    url=get_share_url(text=text, url=share_url)
                )
            ]
        ]
    )
