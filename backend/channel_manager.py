import asyncio
import json
import logging
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

from aiogram import Bot
from aiogram.enums import ParseMode

import config
from bot_keyboards import get_channel_inline_keyboard
from cme_fetcher import format_channel_report_message

logger = logging.getLogger("cme-channel-manager")

CONFIG_PATH = Path(__file__).resolve().parent / "channel_config.json"
TZ_MSK = timezone(timedelta(hours=3))


def get_channel_config() -> Dict[str, Any]:
    """Reads saved channel configuration."""
    if not CONFIG_PATH.exists():
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading channel config: {e}")
        return {}


def save_channel_config(
    channel_id: int | str,
    channel_title: str = "",
    channel_username: str = "",
    last_post_date: Optional[str] = None,
    last_post_id: Optional[int] = None,
    last_scrape_date: Optional[str] = None
) -> Dict[str, Any]:
    """Saves or updates channel configuration."""
    cfg = get_channel_config()
    cfg["channel_id"] = int(channel_id) if str(channel_id).lstrip("-").isdigit() else str(channel_id)
    if channel_title:
        cfg["channel_title"] = channel_title
    if channel_username:
        cfg["channel_username"] = channel_username
    if last_post_date:
        cfg["last_post_date"] = last_post_date
    if last_post_id is not None:
        cfg["last_post_id"] = last_post_id
    if last_scrape_date:
        cfg["last_scrape_date"] = last_scrape_date
    cfg["updated_at"] = datetime.now(TZ_MSK).strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved channel config: {cfg.get('channel_title')} ({cfg.get('channel_id')})")
    except Exception as e:
        logger.error(f"Error saving channel config: {e}")

    return cfg


async def trigger_cme_scraper() -> Tuple[bool, str]:
    """
    Executes cme_scraper.py under xvfb-run to update quikstrike_cache.json with fresh CME data.
    """
    scraper_path = Path(__file__).resolve().parent / "cme_scraper.py"
    cmd = ["xvfb-run", "-a", sys.executable, str(scraper_path)]
    logger.info(f"Launching CME scraper: {' '.join(cmd)}")

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        out_str = stdout.decode("utf-8", errors="ignore").strip()
        err_str = stderr.decode("utf-8", errors="ignore").strip()

        if proc.returncode == 0:
            today_str = datetime.now(TZ_MSK).strftime("%Y-%m-%d")
            cfg = get_channel_config()
            save_channel_config(channel_id=cfg.get("channel_id", 0), last_scrape_date=today_str)
            logger.info(f"CME scraper completed successfully: {out_str}")
            return True, "✅ Свежие данные QuikStrike успешно собраны и обновлены!"
        else:
            logger.error(f"CME scraper failed (code {proc.returncode}): {err_str or out_str}")
            return False, f"❌ Ошибка парсера CME: {err_str or out_str}"
    except Exception as e:
        logger.error(f"Exception running CME scraper: {e}")
        return False, f"❌ Ошибка запуска парсера: {e}"


def is_channel_configured() -> bool:
    cfg = get_channel_config()
    return bool(cfg.get("channel_id"))


async def send_report_to_channel(bot: Bot) -> Tuple[bool, str]:
    """
    Sends the Top-5 Largest Contracts and Market Quotes report to the connected channel.
    Returns (success: bool, message: str).
    """
    cfg = get_channel_config()
    channel_id = cfg.get("channel_id")
    if not channel_id:
        return False, "Канал не настроен. Добавьте бота в канал или используйте /setchannel @имя_канала"

    text = format_channel_report_message()
    kb = get_channel_inline_keyboard()

    try:
        sent = await bot.send_message(
            chat_id=channel_id,
            text=text,
            reply_markup=kb,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        today_str = datetime.now(TZ_MSK).strftime("%Y-%m-%d")
        save_channel_config(
            channel_id=channel_id,
            last_post_date=today_str,
            last_post_id=sent.message_id
        )
        title = cfg.get("channel_title") or str(channel_id)
        logger.info(f"Report successfully sent to channel {title} (id: {channel_id}, msg_id: {sent.message_id})")
        return True, f"✅ Отчет успешно опубликован в канал «{title}»!"
    except Exception as e:
        logger.error(f"Failed to send report to channel {channel_id}: {e}")
        return False, f"❌ Ошибка отправки в канал ({channel_id}): {e}"


async def start_channel_scheduler(bot: Bot):
    """
    Background scheduler loop:
    Runs Monday through Friday.
    Scrapes fresh CME data at 09:15 MSK and posts daily report at 09:30 MSK.
    On weekends (Saturday & Sunday), the exchange is closed.
    Friday's final data is scraped and posted on Monday morning.
    """
    logger.info("Channel scheduler started (Weekdays: Scrape 09:15 MSK, Post 09:30 MSK).")
    while True:
        try:
            now_msk = datetime.now(TZ_MSK)
            today_str = now_msk.strftime("%Y-%m-%d")
            weekday = now_msk.weekday()  # 0=Monday ... 4=Friday, 5=Saturday, 6=Sunday

            # In weekends exchange is closed; Friday data is visible and scraped on Monday morning
            if weekday >= 5:
                await asyncio.sleep(60)
                continue

            # 1. Automatic scraping at 09:15 MSK (Monday-Friday)
            if now_msk.hour == 9 and now_msk.minute == 15:
                cfg = get_channel_config()
                if cfg.get("last_scrape_date") != today_str:
                    day_name = "понедельник (срез за пятницу)" if weekday == 0 else f"день {today_str}"
                    logger.info(f"Triggering scheduled 09:15 MSK CME scraper for {day_name}...")
                    await trigger_cme_scraper()
                    await asyncio.sleep(65)
                    continue

            # 2. Daily channel report at 09:30 MSK (Monday-Friday)
            if now_msk.hour == 9 and now_msk.minute == 30:
                cfg = get_channel_config()
                if cfg.get("channel_id") and cfg.get("last_post_date") != today_str:
                    # If scraper hasn't run yet today, run it before posting
                    if cfg.get("last_scrape_date") != today_str:
                        logger.info("Scraper has not run today, running before daily 09:30 MSK post...")
                        await trigger_cme_scraper()

                    logger.info(f"Triggering scheduled 09:30 MSK channel post for date {today_str}...")
                    success, msg = await send_report_to_channel(bot)
                    if success:
                        logger.info("Daily scheduled post published successfully!")
                    else:
                        logger.warning(f"Daily scheduled post failed: {msg}")
                    # Sleep 65s so we don't post again within minute 30
                    await asyncio.sleep(65)
                    continue

        except Exception as e:
            logger.error(f"Error in channel scheduler: {e}")

        # Check every 25 seconds
        await asyncio.sleep(25)
