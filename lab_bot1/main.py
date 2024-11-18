import logging, asyncio

from config import *
import handlers


async def main():
    await bot.delete_webhook(drop_pending_updates=True)  
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
