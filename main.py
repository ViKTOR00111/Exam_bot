import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from settings import config
from utils.logger import setup_logger
from handlers import router


TOKEN = config.BOT_TOKEN.get_secret_value()

dp = Dispatcher()
dp.include_router(router)


async def main() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    logger.trace(f"Exam_bot is running")
    await dp.start_polling(bot)


if __name__ == "__main__":
    setup_logger(settings=config)
    asyncio.run(main())
