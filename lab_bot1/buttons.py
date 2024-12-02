from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F

from config import *
from db import Database

db = Database(DATABASE_CONFIG)

async def connect_db():
    await db.connect()
    await db.create_tables()


class WordBotStates(StatesGroup):
    adding_word = State()
    deleting_word = State()
    adding_button = State()
    deleting_button = State()
    idle = State()


@dp.message(F.text == "Добавить слово")
async def start_adding_word(message: Message, state: FSMContext):
    await state.set_state(WordBotStates.adding_word)
    await message.answer("Введите слово и его перевод через двоеточие (например: 'cat:кот')")


@dp.message(WordBotStates.adding_word)
async def add_word(message: Message, state: FSMContext):
    if ":" in message.text:
        word, translation = map(str.strip, message.text.split(":", 1))
        user_id = message.from_user.id

        user_words = await db.get_words(user_id)
        if word in user_words and translation == user_words[word]:
            await message.answer("Слово с таким переводом уже есть")
            return

        if len(user_words) + 1 > MAX_COUNT:
            await message.answer("Максимальное кол-во слов уже достигнуто")
            return

        await db.save_words(user_id, {word: translation})
        await state.set_state(WordBotStates.idle)
        await message.answer(f"Слово '{word}' с переводом '{translation}' добавлено. Выберите следующую команду.")
    else:
        await message.answer("Неверный формат. Введите слово и перевод через двоеточие (например: 'cat:кот').")


@dp.message(F.text == "Удалить слово")
async def start_deleting_word(message: Message, state: FSMContext):
    user_words = await db.get_words(message.from_user.id)
    if len(user_words) == 0:
        await message.answer("Список слов пуст.")
    else:
        await state.set_state(WordBotStates.deleting_word)
        await message.answer("Введите слово, которое хотите удалить:")


@dp.message(WordBotStates.deleting_word)
async def delete_word(message: Message, state: FSMContext):
    word = message.text.strip()
    user_id = message.from_user.id

    user_words = await db.get_words(user_id)
    user_buttons = await db.get_buttons(user_id)
    if word in user_words:
        await db.delete_word(user_id, word)
        if word in user_buttons:
            await db.delete_button(user_id, word)
        await state.set_state(WordBotStates.idle)
        await message.answer(f"Слово '{word}' удалено. Выберите следующую команду.")
    else:
        await message.answer(f"Слово '{word}' не найдено. Попробуйте снова или выберите другую команду.")


@dp.message(F.text == "Посмотреть слова")
async def show_words(message: Message):
    user_words = await db.get_words(message.from_user.id)
    if len(user_words) == 0:
        await message.answer("Список слов пуст.")
    else:
        word_list = "\n".join([f"{word} — {translation}" for word, translation in user_words.items()])
        await message.answer(f"Ваши слова:\n{word_list}")


@dp.message(F.text == "Посмотреть слова без перевода")
async def show_words_without_translation(message: Message):
    user_id = message.from_user.id
    user_words = await db.get_words(user_id)
    if len(user_words) == 0:
        await message.answer("Список слов пуст.")
    else:
        untranslated_words = "\n".join(user_words.keys())
        await message.answer(f"Ваши слова без перевода:\n{untranslated_words}")


@dp.message(F.text == "Добавить кнопку")
async def start_adding_button(message: Message, state: FSMContext):
    await state.set_state(WordBotStates.adding_button)
    await message.answer("Введите слово для добавления кнопки (например: 'cat'):")


@dp.message(WordBotStates.adding_button)
async def add_button(message: Message, state: FSMContext):
    word = message.text.strip()
    user_id = message.from_user.id

    user_words = await db.get_words(user_id)
    if word in user_words:
        await db.save_buttons(user_id, {word: user_words[word]})
        await state.set_state(WordBotStates.idle)
        await message.answer(f"Кнопка для слова '{word}' добавлена. Выберите следующую команду.")
    else:
        await message.answer(f"Слово '{word}' не найдено в списке. Добавьте его сначала с помощью команды 'Добавить слово'.")


@dp.message(F.text == "Удалить кнопку")
async def start_deleting_button(message: Message, state: FSMContext):
    await state.set_state(WordBotStates.deleting_button)
    await message.answer("Введите слово для удаления кнопки (например: 'cat'):")


@dp.message(WordBotStates.deleting_button)
async def delete_button(message: Message, state: FSMContext):
    word = message.text.strip()
    user_id = message.from_user.id

    user_buttons = await db.get_buttons(user_id)
    if word in user_buttons:
        await db.delete_button(user_id, word)
        await state.set_state(WordBotStates.idle)
        await message.answer(f"Кнопка для слова '{word}' удалена. Выберите следующую команду.")
    else:
        await message.answer(f"Кнопка для слова '{word}' не найдена. Попробуйте снова или выберите другую команду.")


@dp.message(F.text == "Посмотреть кнопки")
async def show_buttons(message: Message):
    user_buttons = await db.get_buttons(message.from_user.id)
    if len(user_buttons) == 0:
        await message.answer("У вас нет добавленных кнопок.")
    else:
        buttons = [
            [InlineKeyboardButton(text=word, callback_data=word)]
            for word in user_buttons
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.answer("Нажмите на кнопку, чтобы увидеть перевод:", reply_markup=keyboard)


@dp.callback_query()
async def handle_button_callback(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    buttons = await db.get_buttons(user_id) 
    word = callback_query.data

    if word in buttons:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, f"Перевод для {word} - {buttons[word]}")
    else:
        await bot.answer_callback_query(callback_query.id, text="Перевод не найден.")
