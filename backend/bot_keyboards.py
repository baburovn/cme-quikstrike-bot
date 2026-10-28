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
                KeyboardButton(text="📢 Отправить Топ-5 в канал"),
                KeyboardButton(text="ℹ️ О терминале"),
            ]
        ],
        resize_keyboard=True
    )


def get_miniapp_inline_keyboard() -> InlineKeyboardMarkup:
    """Returns Inline Keyboard to launch Mini App with live charts and channel actions."""
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
                    text="🔄 Обновить текст",
                    callback_data="refresh_text_quotes"
                ),
                InlineKeyboardButton(
                    text="📢 В канал",
                    callback_data="publish_to_channel"
                )
            ]
        ]
    )


def get_oi_inline_keyboard() -> InlineKeyboardMarkup:
    """Returns Inline Keyboard for QuikStrike Most Actives reports."""
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
                    text="🔄 Обновить данные",
                    callback_data="refresh_oi_data"
                )
            ]
        ]
    )


def get_channel_inline_keyboard() -> InlineKeyboardMarkup:
    """Returns buttons attached to channel reports (direct URL link compatible with channels/groups)."""
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
                    text="🔄 Обновить отчет",
                    callback_data="refresh_channel_report"
                )
            ]
        ]
    )
