import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import TOKEN, PRICE
from payment import create, check

bot = Bot(TOKEN)
db = Dispatcher()
router = Router()
db.include_router(router)


@router.message(Command(commands=['start']))
async def start_handler(message: Message):
    await message.answer('Привет!')


@router.message(Command(commands=['buy']))
async def buy_handler(message: Message):
    payment_url, payment_id = create(PRICE, message.chat.id)

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Оплатить',
        url=payment_url
    ))
    builder.add(types.InlineKeyboardButton(
        text='Проверить оплату',
        callback_data=f'check_{payment_id}'
    ))

    await message.answer(f"Счет сформирован!", reply_markup=builder.as_markup())


@router.callback_query(lambda c: 'check' in c.data)
async def check_handler(callback: types.CallbackQuery):
    result = check(callback.data.split('_')[-1])
    if result:
        await callback.message.answer('Оплата прошла успешно!')
    else:
        await callback.message.answer('Оплата еще не прошла или возникла ошибка')
    await callback.answer()


async def main():
    await db.start_polling(bot, skip_updates=False)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())