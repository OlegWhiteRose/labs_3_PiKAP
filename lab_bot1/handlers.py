from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.filters import Command

from buttons import *


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я бот, который помогает тебе изучать английский. Вызвать меню: /menu.")


@dp.message(Command("menu"))
async def menu_command(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить слово")],
            [KeyboardButton(text="Удалить слово")],
            [KeyboardButton(text="Посмотреть слова")],
            [KeyboardButton(text="Посмотреть слова без перевода")],
            [KeyboardButton(text="Добавить кнопку")],
            [KeyboardButton(text="Удалить кнопку")],
            [KeyboardButton(text="Посмотреть кнопки")],
        ],
        resize_keyboard=True
    )
    await message.answer("Выбери кнопку:", reply_markup=keyboard)


@dp.message(F.text)
async def text_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()  
    match current_state:
        case WordBotStates.adding_word.state:
            await add_word(message, state)
        case WordBotStates.deleting_word.state:
            await delete_word(message, state)
        case WordBotStates.adding_button.state:
            await add_button(message, state)
        case WordBotStates.deleting_button.state:
            await delete_button(message, state)
        case WordBotStates.idle.state:
            match message.text:
                case "Добавить слово":
                    await start_adding_word(message, state)
                case "Удалить слово":
                    await start_deleting_word(message, state)
                case "Посмотреть слова":
                    await show_words(message)
                case "Посмотреть слова без перевода":
                    await show_words_without_translation(message)
                case "Добавить кнопку":
                    await start_adding_button(message, state)
                case "Удалить кнопку":
                    await start_deleting_button(message, state)
                case "Посмотреть кнопки":
                    await show_buttons(message)
                case _:
                    await message.answer("Неизвестная команда. Выберите команду из меню.")
