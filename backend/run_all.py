import asyncio
import logging
import sys
import uvicorn

from app import app
from bot import router, main as bot_main
from channel_manager import start_channel_scheduler
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, WebAppInfo, MenuButtonWebApp
import config

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("cme-miniapp-runner")


async def run_fastapi():
    cfg = uvicorn.Config(
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        log_level="info",
        access_log=False
    )
    server = uvicorn.Server(cfg)
    await server.serve()


async def run_bot():
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
            BotCommand(command="oi", description="🎯 Most Actives OI (Крупные контракты)"),
            BotCommand(command="post", description="📢 Отправить Топ-5 контрактов в канал"),
            BotCommand(command="update_oi", description="🔄 Спарсить свежие данные CME QuikStrike"),
            BotCommand(command="channel", description="📢 Проверить привязанный канал"),
            BotCommand(command="setchannel", description="⚙️ Привязать канал вручную"),
            BotCommand(command="setcme", description="🔑 Настроить логин/пароль CME"),
            BotCommand(command="quotes", description="📊 Текстовый список котировок"),
            BotCommand(command="info", description="ℹ️ О системе"),
        ])
        logger.info("Кнопка меню WebApp и команды установлены в Telegram!")
    except Exception as e:
        logger.warning(f"Ошибка настройки меню Telegram: {e}")

    dp = Dispatcher()
    dp.include_router(router)

    # Start automated 09:30 MSK channel scheduler task
    asyncio.create_task(start_channel_scheduler(bot))

    logger.info("Бот aiogram запущен с планировщиком канала (09:30 МСК)!")
    await dp.start_polling(bot)


async def main():
    logger.info("Запуск единого сервиса: FastAPI WebApp + Telegram Bot...")
    await asyncio.gather(
        run_fastapi(),
        run_bot()
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Сервис остановлен.")
