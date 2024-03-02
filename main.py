from aiogram import Bot, Dispatcher, executor, types
import logging
import config
import requests
from bs4 import BeautifulSoup

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def main(message: types.Message):
    if "/start" in message.text.lower():
        await bot.send_message(message.chat.id, "<b>Приветствую! Я бот-конвертер-валют.\n</b>"
                                                 "<b>Чтобы конвертировать валюту, вы должны написать:\n</b>"
                                                 "<i>/translate 'сумма' 'название валюты' 'в какую валюту перевести'</i>",
                               parse_mode=types.ParseMode.HTML)

    elif "/translate" in message.text.lower():
        # Получаем запрос пользователя
        query = message.text.lower()[11:]

        if not query.strip("/translate").strip():
            await bot.send_message(message.chat.id, "<b>Чтобы конвертировать валюту, вы должны написать:\n</b>"
                                                 "<i>/translate 'сумма' 'название валюты' 'в какую валюту перевести'</i>", 
                                parse_mode=types.ParseMode.HTML)
        
        # Формируем URL для поиска в Google
        url = f'https://www.google.com/search?q={query}'
        
        # Отправляем HTTP запрос к странице
        response = requests.get(url)
        
        # Проверяем успешность запроса
        if response.status_code == 200:
            # Получаем HTML содержимое страницы
            html_code = response.text
            
            # Создаем объект BeautifulSoup для парсинга HTML
            soup = BeautifulSoup(html_code, 'html.parser')
            
            # Находим результат поиска
            result = soup.find(class_="BNeawe iBp4i AP7Wnd")
            
            # Извлекаем текст из результата и отправляем его
            if result:
                result_text = result.text
                await bot.send_message(message.chat.id, result_text, reply_to_message_id=message.message_id)

            if not result:
                await bot.send_message(message.chat.id, "Результаты не найдены.")
        else:
            await bot.send_message(message.chat.id, f"Ошибка при загрузке страницы: {response.status_code}")
    
    
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
