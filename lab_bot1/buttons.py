from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F

from config import *


class WordBotStates(StatesGroup):
    adding_word = State()
    deleting_word = State()
    adding_button = State()
    deleting_button = State()
    idle = State()



words = {}
button_words = {}


@dp.message(F.text == "Добавить слово")
async def start_adding_word(message: Message, state: FSMContext):
    await state.set_state(WordBotStates.adding_word) 
    await message.answer("Введите слово и его перевод через двоеточие (например: 'cat:кот')")


@dp.message(WordBotStates.adding_word)
async def add_word(message: Message, state: FSMContext):
    if ":" in message.text:
        word, translation = map(str.strip, message.text.split(":", 1))
        words[word] = translation
        await state.set_state(WordBotStates.idle)  
        await message.answer(f"Слово '{word}' с переводом '{translation}' добавлено. Выберите следующую команду.")
    else:
        await message.answer("Неверный формат. Введите слово и перевод через двоеточие (например: 'cat:кот').")


@dp.message(F.text == "Удалить слово")
async def start_deleting_word(message: Message, state: FSMContext):
    if len(words) == 0:
        await message.answer("Список слов пуст.")
    else:
        await state.set_state(WordBotStates.deleting_word) 
        await message.answer("Введите слово, которое хотите удалить:")


@dp.message(WordBotStates.deleting_word)
async def delete_word(message: Message, state: FSMContext):
    if message.text in words:
        del words[message.text]
        await state.set_state(WordBotStates.idle) 
        await message.answer(f"Слово '{message.text}' удалено. Выберите следующую команду.")
    else:
        await message.answer(f"Слово '{message.text}' не найдено. Попробуйте снова или выберите другую команду.")


@dp.message(F.text == "Посмотреть слова")
async def show_words(message: Message):
    if len(words) == 0:
        await message.answer("Список слов пуст.")
    else:
        word_list = "\n".join([f"{word} — {translation}" for word, translation in words.items()])
        await message.answer(f"Ваши слова:\n{word_list}")


@dp.message(F.text == "Посмотреть слова без перевода")
async def show_words_without_translation(message: Message):
    if len(words) == 0:
        await message.answer("Список слов пуст.")
    else:
        untranslated_words = "\n".join(words.keys())
        await message.answer(f"Ваши слова без перевода:\n{untranslated_words}")


@dp.message(F.text == "Добавить кнопку")
async def start_adding_button(message: Message, state: FSMContext):
    await state.set_state(WordBotStates.adding_button)  
    await message.answer("Введите слово для добавления кнопки (например: 'cat'):")


@dp.message(WordBotStates.adding_button)
async def add_button(message: Message, state: FSMContext):
    word = message.text.strip()
    if word in words:
        button_words[word] = words[word]  
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
    if word in button_words:
        del button_words[word]  
        await state.set_state(WordBotStates.idle) 
        await message.answer(f"Кнопка для слова '{word}' удалена. Выберите следующую команду.")
    else:
        await message.answer(f"Кнопка для слова '{word}' не найдена. Попробуйте снова или выберите другую команду.")


@dp.message(F.text == "Посмотреть кнопки")
async def show_buttons(message: Message):
    if len(button_words) == 0:
        await message.answer("У вас нет добавленных кнопок.")
    else:
        keyboard = InlineKeyboardMarkup(row_width=1)
        for word, translation in button_words.items():
            keyboard.add(InlineKeyboardButton(text=word, callback_data=word))
        await message.answer("Нажмите на кнопку, чтобы увидеть перевод:", reply_markup=keyboard)


@dp.callback_query()
async def handle_button(callback_query: Message):
    word = callback_query.data 
    translation = button_words.get(word)
    if translation:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, f"Перевод для '{word}': {translation}")
    else:
        await bot.answer_callback_query(callback_query.id, text="Перевод не найден.")


@dp.message(F.text == "Посмотреть кнопки")
async def show_buttons(message: Message):
    if len(button_words) == 0: 
        await message.answer("У вас нет добавленных кнопок.")
    else:
        keyboard = InlineKeyboardMarkup(row_width=1) 
        for word in button_words.keys():
            keyboard.add(InlineKeyboardButton(text=word, callback_data=word))
        
        await message.answer("Нажмите на кнопку, чтобы увидеть перевод:", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data in button_words.keys())
async def handle_button_callback(callback_query: CallbackQuery):
    word = callback_query.data
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Перевод для {word}: {button_words[word]}")
