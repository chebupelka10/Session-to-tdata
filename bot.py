from aiogram import Bot, Dispatcher, executor
from aiogram import types

from conversion import create_tdata
from config import token_bot

import os
import shutil

bot = Bot(token=token_bot, parse_mode='html')
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
	await bot.send_message(message.from_user.id, "<b>Отправь мне сессию <u>telethon'a</u>, а я тебе TData</b>")

# Обработчик сессии
@dp.message_handler(content_types=['document'])
async def download_session(message: types.Message):
	msg = await bot.send_message(message.from_user.id, '<b>Обработка...</b>')

	name = message.document.file_name

	# Делаем проверку на правильность сессии (*.session)
	if name.split('.')[-1] != 'session':
		await bot.edit_message_text(chat_id = message.from_user.id,
									message_id = msg.message_id,
									text = f'🚫 <b>Вы отправили "{name.split(".")[-1]}" файл!</b>')
		return

	# Качаем сессию
	file_info = await bot.get_file(message.document.file_id)
	await bot.download_file(file_info.file_path, f'Session/{name}')

	# Отравляем TData
	tdata = await create_tdata(session_name=name)
	if tdata:
		with open(f"TData/{name.split('.')[0]}/tdata.zip", "rb") as file:
			await bot.send_document(message.from_user.id, file)

		# 2 вида удаления. У меня были проблемы с удалением папки TData, мол в доступе отказано. Я решил не заморачиваться и ебнуть os and shutil :3 
		os.remove(f"Session/{name}")
		shutil.rmtree(f"TData/{name.split('.')[0]}")
	else:
		await bot.send_message(message.from_user.id, '<b>Что-то пошло не так!\nВозможно сессия не валидная.')

if __name__ == "__main__":
	executor.start_polling(dispatcher=dp,
						   skip_updates=True)