# -*- coding: utf-8 -*-
"""
CME Metals & FX Telegram Mini App Bot.
Handles commands, callbacks, automated reporting, and Mini App entry points.
"""
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    ChatMemberUpdated,
    Message,
    MenuButtonWebApp,
    WebAppInfo,
)

import config
from bot_keyboards import (
    get_miniapp_reply_keyboard,
    get_miniapp_inline_keyboard,
    get_oi_inline_keyboard,
    get_channel_inline_keyboard,
)
from cme_fetcher import (
    get_all_quotes,
    format_quikstrike_telegram_message,
    format_channel_report_message,
)
from channel_manager import (
    get_channel_config,
    save_channel_config,
    is_channel_configured,
    send_report_to_channel,
    start_channel_scheduler,
    trigger_cme_scraper,
)
from credentials_manager import save_cme_credentials

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

router = Router()


def format_text_quotes() -> str:
    """Formats live quotes into a compact Telegram message."""
    quotes = get_all_quotes()
    lines = [
        "📊 **CME GROUP — МЕТАЛЛЫ И ВАЛЮТЫ**",
        "⏱ *Автообновление: каждые 10 секунд*\n",
        "───────────────"
    ]
    for q in quotes:
        icon = "🟡" if q["symbol"] == "GC" else ("⚪" if q["symbol"] == "SI" else "🔹")
        trend = "🟢" if q.get("trend") == "up" else ("🔴" if q.get("trend") == "down" else "⚪")
        lines.append(
            f"{icon} **{q['symbol']}** — {q['name']}\n"
            f"   {trend} **Цена:** `${q['price']}` ({q.get('change_pct', 0):+.2f}%)\n"
            f"   📈 **Объем:** `{q.get('volume', 0):,}` | **OI:** `{q.get('open_interest', 0):,}`\n"
        )
    lines.append("───────────────")
    lines.append("💡 *Для интерактивных графиков TradingView нажмите кнопку ниже:*")
    return "\n".join(lines)


# =====================================================================
# Navigation & Mini App Launch Handlers
# =====================================================================

@router.message(Command("start"))
async def cmd_start(message: Message, bot: Bot):
    welcome_text = (
        "🪙 **Добро пожаловать в CME Metals Terminal!**\n\n"
        "Мы превратили бота в **полноценный Telegram Mini App** с интерактивными графиками TradingView в реальном времени.\n\n"
        "✨ **Возможности Mini App:**\n"
        "• 📈 **Свечные графики** TradingView (Gold GC, Silver SI, Copper HG, FX)\n"
        "• ⚡ **Live-тикеры** с обновлением каждые 10 секунд без спама в чат\n"
        "• 📊 **Объемы и открытый интерес (OI)** по всем ключевым металлам\n"
        "• 📳 Нативный виброотклик и авто-адаптация к теме Telegram\n\n"
        "👇 **Нажмите кнопку ниже, чтобы открыть терминал:**"
    )
    await message.answer(
        welcome_text,
        reply_markup=get_miniapp_inline_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )


@router.message(Command("app"))
@router.message(Command("terminal"))
@router.message(F.text == "📈 Открыть Терминал CME 🟡⚪")
async def cmd_open_app(message: Message):
    await message.answer(
        "Нажмите кнопку для входа в терминал:",
        reply_markup=get_miniapp_inline_keyboard()
    )


# =====================================================================
# Market Quotes Handlers
# =====================================================================

@router.message(Command("quotes"))
@router.message(Command("metals"))
@router.message(F.text == "📊 Котировки")
@router.message(F.text == "📊 Текстовые котировки")
async def cmd_text_quotes(message: Message):
    await message.answer(
        format_text_quotes(),
        reply_markup=get_miniapp_inline_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )


# =====================================================================
# QuikStrike Most Actives OI Handlers
# =====================================================================

@router.message(Command("oi"))
@router.message(Command("mostactive"))
@router.message(Command("options"))
@router.message(F.text == "🎯 Most Actives OI (≥1000)")
@router.message(F.text.lower().contains("most active") | F.text.lower().contains("открытый интерес") | F.text.lower().contains("quikstrike"))
async def cmd_quikstrike_oi(message: Message):
    text = format_quikstrike_telegram_message(min_oi=1000)
    await message.answer(
        text,
        reply_markup=get_oi_inline_keyboard(),
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )


@router.callback_query(F.data == "refresh_oi_data")
async def cb_refresh_oi(query: CallbackQuery):
    await query.answer("Данные QuikStrike обновлены!")
    text = format_quikstrike_telegram_message(min_oi=1000)
    try:
        await query.message.edit_text(
            text,
            reply_markup=get_oi_inline_keyboard(),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
    except Exception:
        pass


@router.callback_query(F.data == "refresh_text_quotes")
async def cb_refresh_text(query: CallbackQuery, bot: Bot):
    await query.answer("Котировки обновлены!")
    try:
        await query.message.edit_text(
            format_text_quotes(),
            reply_markup=get_miniapp_inline_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception:
        pass

    # When user clicks "Обновить текст", if channel is configured, also push update
    if is_channel_configured():
        try:
            await send_report_to_channel(bot)
        except Exception as e:
            logger.warning(f"Auto-update channel on refresh error: {e}")


@router.callback_query(F.data == "publish_to_channel")
async def cb_publish_to_channel(query: CallbackQuery, bot: Bot):
    if not is_channel_configured():
        await query.answer("Канал еще не настроен! Добавьте бота в канал администратором.", show_alert=True)
        return
    success, msg = await send_report_to_channel(bot)
    await query.answer(msg, show_alert=True)


@router.callback_query(F.data == "refresh_channel_report")
async def cb_refresh_channel_report(query: CallbackQuery):
    await query.answer("Отчет обновлен!")
    try:
        await query.message.edit_text(
            format_channel_report_message(),
            reply_markup=get_channel_inline_keyboard(),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
    except Exception:
        pass


# =====================================================================
# Channel & Group Integration Handlers
# =====================================================================

@router.my_chat_member()
async def on_my_chat_member(event: ChatMemberUpdated, bot: Bot):
    if event.chat.type in ("channel", "supergroup", "group"):
        new_status = event.new_chat_member.status
        if new_status in ("administrator", "member"):
            save_channel_config(
                channel_id=event.chat.id,
                channel_title=event.chat.title or "",
                channel_username=event.chat.username or ""
            )
            logger.info(f"Bot connected to {event.chat.type} «{event.chat.title}» ({event.chat.id})")
            try:
                await bot.send_message(
                    chat_id=event.chat.id,
                    text=(
                        f"✅ **Бот подключен к каналу «{event.chat.title}»!**\n\n"
                        f"⏰ Автоматический отчет: **ежедневно в 12:30 (GMT+5)**\n"
                        f"📊 В отчет входит: Топ-5 самых крупных контрактов (Open Interest).\n"
                        f"🚀 [Открыть CME Mini App]({config.WEBAPP_URL})"
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
            except Exception as e:
                logger.warning(f"Could not send welcome post to channel: {e}")


@router.message(Command("post"))
@router.message(Command("send"))
@router.message(F.text == "📢 Отправить Топ-5 в канал")
async def cmd_post_to_channel(message: Message, bot: Bot):
    if not is_channel_configured():
        await message.answer(
            "⚠️ **Канал еще не привязан!**\n\n"
            "1. Добавьте бота @cme_daily_info_bot в ваш канал как **Администратора**.\n"
            "2. Или напишите команду `/setchannel @имя_канала`\n\n"
            "После этого бот сможет автоматически отправлять отчет в 12:30 GMT+5 и по кнопке.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    await message.answer("⏳ Публикую актуальный отчет Топ-5 контрактов в канал...")
    success, status_msg = await send_report_to_channel(bot)
    await message.answer(status_msg, parse_mode=ParseMode.MARKDOWN)


@router.message(Command("setchannel"))
async def cmd_set_channel(message: Message, bot: Bot):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        cfg = get_channel_config()
        current = cfg.get("channel_title") or cfg.get("channel_id") or "Не настроен"
        await message.answer(
            f"📢 **Текущий канал:** {current}\n\n"
            "Чтобы привязать канал, укажите его username или ID:\n"
            "`/setchannel @ваш_канал` или `/setchannel -1001234567890`\n\n"
            "💡 *Бот должен быть предварительно добавлен в канал как администратор.*",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    target = parts[1].strip()
    try:
        chat = await bot.get_chat(target)
        save_channel_config(
            channel_id=chat.id,
            channel_title=chat.title or target,
            channel_username=chat.username or ""
        )
        await message.answer(
            f"✅ **Канал успешно привязан:**\n"
            f"• Название: **{chat.title or target}**\n"
            f"• ID: `{chat.id}`\n"
            f"• Расписание: **Ежедневно в 12:30 GMT+5**\n\n"
            f"👉 Чтобы отправить отчет прямо сейчас: /post",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await message.answer(
            f"❌ Не удалось подключиться к `{target}`.\n"
            f"Убедитесь, что бот добавлен в канал администратором.\n"
            f"Ошибка: `{e}`",
            parse_mode=ParseMode.MARKDOWN
        )


@router.message(Command("channel"))
async def cmd_channel_status(message: Message):
    cfg = get_channel_config()
    if not cfg.get("channel_id"):
        await message.answer(
            "⚠️ Канал не привязан.\nДобавьте бота администратором в канал или используйте `/setchannel @имя_канала`.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    title = cfg.get("channel_title") or "Канал"
    cid = cfg.get("channel_id")
    last_d = cfg.get("last_post_date") or "Ещё не было"
    await message.answer(
        f"📢 **Привязанный канал:**\n\n"
        f"• **Название:** {title}\n"
        f"• **ID:** `{cid}`\n"
        f"• **Авто-отправка:** Ежедневно в 12:30 GMT+5\n"
        f"• **Последний отчет:** `{last_d}`\n\n"
        f"👉 Для отправки отчета сейчас: /post",
        parse_mode=ParseMode.MARKDOWN
    )


# =====================================================================
# Scraper & Credentials Administrative Handlers
# =====================================================================

@router.message(Command("update_oi"))
@router.message(Command("scrape"))
async def cmd_update_oi(message: Message, bot: Bot):
    await message.answer("🔄 **Запуск сбора свежих данных QuikStrike с CME...**\nОжидайте 30–60 секунд...", parse_mode=ParseMode.MARKDOWN)
    success, msg = await trigger_cme_scraper()
    if success:
        await message.answer(
            f"✅ **Данные QuikStrike успешно обновлены!**\n\n{msg}\n\n"
            "👉 Чтобы отправить свежий отчет в канал, нажмите /post",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await message.answer(
            f"❌ **Не удалось обновить данные:**\n{msg}",
            parse_mode=ParseMode.MARKDOWN
        )


@router.message(Command("setcme"))
async def cmd_set_cme(message: Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer(
            "ℹ️ **Смена логина и пароля CME:**\n\n"
            "Формат команды:\n"
            "`/setcme ваш_логин ваш_пароль`\n\n"
            f"Текущий логин в системе: `{config.CME_LOGIN}`\n\n"
            "💡 Также логин и пароль можно менять прямо в файле `backend/cme_credentials.py`.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    new_login = parts[1].strip()
    new_password = parts[2].strip()

    success, err_msg = save_cme_credentials(new_login, new_password)
    if success:
        await message.answer(
            f"✅ **Учетные данные CME успешно обновлены!**\n\n"
            f"• Логин: `{new_login}`\n"
            f"• Пароль: `{'*' * len(new_password)}`\n\n"
            "Теперь парсер будет использовать эти данные.",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await message.answer(f"❌ {err_msg}", parse_mode=ParseMode.MARKDOWN)


@router.message(Command("info"))
@router.message(F.text == "ℹ️ О терминале")
async def cmd_info(message: Message):
    info_text = (
        "ℹ️ **О терминале CME Metals:**\n\n"
        f"• **Telegram Mini App URL:** `{config.WEBAPP_URL}`\n"
        "• **Стек:** FastAPI, WebSockets, Lightweight Charts, aiogram 3, Playwright\n"
        "• **Отчеты:** QuikStrike Options Open Interest Profile (Most Actives)\n"
        f"• **Частота обновления котировок:** {config.UPDATE_INTERVAL_SECONDS} сек.\n"
        f"• **Логин CME:** `{config.CME_LOGIN}` (изменить: /setcme)\n"
        "• **Автопостинг в канал:** Ежедневно в 12:30 GMT+5 (сбор в 12:15)\n"
        "• **Команды:** /post, /update_oi, /channel, /setchannel, /setcme, /oi, /quotes\n"
    )
    await message.answer(info_text, parse_mode=ParseMode.MARKDOWN)


# =====================================================================
# Main Application Loop
# =====================================================================

async def main():
    bot = Bot(token=config.BOT_TOKEN)

    try:
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="📈 Терминал",
                web_app=WebAppInfo(url=config.WEBAPP_URL)
            )
        )
        await bot.set_my_commands([
            BotCommand(command="start", description="🚀 Главное меню и запуск Mini App"),
            BotCommand(command="oi", description="🎯 Most Actives OI (Крупные контракты ≥1000)"),
            BotCommand(command="post", description="📢 Отправить Топ-5 контрактов в канал"),
            BotCommand(command="update_oi", description="🔄 Спарсить свежие данные CME QuikStrike"),
            BotCommand(command="channel", description="📢 Проверить привязанный канал"),
            BotCommand(command="setchannel", description="⚙️ Привязать канал вручную"),
            BotCommand(command="setcme", description="🔑 Настроить логин/пароль CME"),
            BotCommand(command="quotes", description="📊 Текстовый список котировок"),
            BotCommand(command="info", description="ℹ️ О системе"),
        ])
        logger.info("Успешно установлена кнопка меню Mini App в Telegram!")
    except Exception as e:
        logger.warning(f"Ошибка настройки меню Telegram: {e}")

    dp = Dispatcher()
    dp.include_router(router)

    # Start automated 12:30 GMT+5 channel scheduler task
    asyncio.create_task(start_channel_scheduler(bot))

    logger.info("🚀 Бот CME Metals Mini App запущен с поддержкой каналов и расписанием 12:30 GMT+5!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
