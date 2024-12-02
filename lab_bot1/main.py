import logging, asyncio

from config import *
import handlers
from buttons import connect_db


async def main():
    await connect_db()
    await bot.delete_webhook(drop_pending_updates=True)  
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
