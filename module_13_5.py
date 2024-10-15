from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация о боте')
kb_start.add(button_1)
kb_start.add(button_2)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет, я бот, помогающий здоровью!', reply_markup=kb_start)


@dp.message_handler(text=['Информация о боте'])
async def set_age(message):
    await message.answer('Я бот, помогающий здоровью!')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=['Рассчитать'])
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age_text=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    await state.update_data(growth_text=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_growth(message, state):
    await state.update_data(weight_text=message.text)
    data = await state.get_data()
    calories_norm = 10 * float(data['weight_text']) + 6.25 * float(data['growth_text']) - 5 * float(
        data['age_text']) + 5
    await message.answer(f'Ваша норма калорий в день: {calories_norm}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
