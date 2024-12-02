from aiogram import Bot, Dispatcher

API_TOKEN = '7343584664:AAElC6aUJXQLvr1K-GlAH_o7RllvC9P-JnY'
MAX_COUNT = 1_000_000

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

DATABASE_CONFIG = {
    "user": "admin",
    "password": "admin",
    "database": "words",
    "host": "localhost"
}
