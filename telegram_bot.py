import logging

from aiogram import Bot, Dispatcher, executor, types
import google_sheets_handler

API_TOKEN = '5848049699:AAFOKETkVYECnImBkCqHlLbv5nhhy6CclRM'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
sheet_titles = ['Личное', 'Бизнес']


@dp.message_handler()
async def handler(message: types.Message):
    try:
        keywords = google_sheets_handler.get_titles(sheet_titles)[1::]
        if len(message.text.split()) != 2:
            await message.reply(
                f'Неправильный формат ввода!\nИспользуйте ключевое слово из списка\n{keywords}\n'
                f'и далее укажите сумму!\n\nПример: {keywords[0]} 500')
        elif message.text.split()[0].lower() not in keywords:
            await message.reply(f"Данного ключевого слова нет в списке {keywords}!")
        elif not message.text.split()[1].isdigit():
            await message.reply(f"Вторым аргументом указано не число!")
        else:
            data = message.text.split()
            google_sheets_handler.write_element(data[0], data[1])
            await message.reply(f'Информация успешно записана в таблицу!')
    except:
        await message.reply(f"Неожиданная ошибка!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
