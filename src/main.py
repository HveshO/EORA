import asyncio
from aiogram import Bot, Dispatcher
from config import settings
from bot.handlers import router
from rag.builder import build_faiss_index
from utils.logger import logger


async def main():
    logger.info("Starting EORA Retail Answers Bot...")
    if settings.BUILD_FAISS:
        build_faiss_index(
            settings.PATH_FILE_URLS,
            settings.PATH_STORAGE_INDEX,
        )
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    logger.info("Bot started")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
