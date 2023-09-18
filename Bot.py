from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hlink
from modules.Scraping_sportmaster.Scraping_sportmaster import get_data
import asyncio
import os
import json


TOKEN = os.getenv("TOKEN")
dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handker(message: Message) -> None:
    start_buttons = [
        [types.KeyboardButton(text="Кроссовки со спорт мастера"),
         types.KeyboardButton(text="Погода")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=start_buttons, resize_keyboard=True)
    await message.answer(f"Что нужно?", reply_markup=keyboard)


@dp.message(F.text == "Кроссовки со спорт мастера")
async def get_discount_sneakers(message: Message):
    await message.answer('Подожди')

    get_data()

    with open("result_data_sneakers.json") as file:
        data = json.load(file)

        for item in data:
            card = f"{hlink(item.get('name'),item.get('link'))}\n"\
                f"{hbold('Новая цена: ')} {item.get('price_new')}\n"\
                f"{hbold('Старая цена: ')} {item.get('price_old')}"

            await message.answer(card)


async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
