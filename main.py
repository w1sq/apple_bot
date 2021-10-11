# coding=utf8
import asyncio
import logging
from aiogram import Bot, Dispatcher, executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputTextMessageContent, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types.inline_query_result import InlineQueryResultArticle
from multiprocessing import Process
from aiogram.dispatcher.filters import BoundFilter
with open('key.txt','r') as file:
    API_KEY = file.readline()
logging.basicConfig(level=logging.INFO, filename='botlogs.log')
bot = Bot(token=API_KEY)
dp = Dispatcher(bot)
print('Bot started')
class MyFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()

dp.filters_factory.bind(MyFilter)
processes = {}

@dp.message_handler(is_admin=True, commands=['spam'], commands_prefix='!')
async def reply_and_pin(message: types.Message):
    id = message.chat.id
    if id in processes.keys():
        await message.reply("There is already a working loop")
    else:
        await message.delete()
        future = asyncio.ensure_future(resend(message), )
        processes[id] = future
        
async def resend(message):
    inside_post = False
    while True:
        if inside_post:
            await inside_post.delete()
        inside_post = await message.answer(' '.join(message.text.split()[1:]))
        await asyncio.sleep(60*45) 
        #await asyncio.sleep(5)

@dp.message_handler(is_admin=True, commands=['stop'], commands_prefix='!')
async def cancel(message: types.Message):
    id = message.chat.id
    if id in processes.keys():
        processes[id].cancel()
        del processes[id]
        await message.delete()
    else:
        await message.reply('There is nothing to stop')

async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())