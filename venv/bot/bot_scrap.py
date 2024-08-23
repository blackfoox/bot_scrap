from bs4 import BeautifulSoup
import requests
import telebot
import time
import psycopg2
import sys

### Ответ бота на команду /start

bot = telebot.TeleBot('6926148773:AAHOHmkB1TfGR0Vu3QknwbDWLU9koFIzClw')

messages = ["Чтобы вытащить игры из категории низкой оценки, напишете 'мусор'",
           "Чтобы вытащить игры из категории средней оценки, напишете 'проходняк'",
           "Чтобы вытащить игры из категории больше среднего, напишете 'похвально'",
           "Чтобы вытащить игры из категории изумительной оценки, напишете 'изумительно'",
           "Если вы хотите узнать, есть ли та или иная игра на сайте пропишите её. Нужно точное название игры."
]

class BotMassege:
    def __init__(self, bot, messages):
        self.bot = bot
        self.messages = messages

    def bot_functionality(self, message):
        self.bot.send_message(message.chat.id, f"Привет {message.from_user.first_name}, я могу вытащить игры из сайта stopgame из категории 'мусор', 'проходняк', 'похвально' , 'изумительно'")
        for mess in self.messages:
            time.sleep(2)
            self.bot.send_message(message.chat.id, mess)



@bot.message_handler(commands=['start'])
def start_message(message):
    bot_message = BotMassege(bot, messages)
    bot_message.bot_functionality(message)


### 

urls = {'мусор': 'https://stopgame.ru/games/musor/new?p=',
        'проходняк': 'https://stopgame.ru/games/prohodnyak/new?p=',
        'похвально': 'https://stopgame.ru/games/pohvalno/new?p=',
        'изумительно': 'https://stopgame.ru/games/izumitelno/new?p='
}

@bot.message_handler()
def 

bot.polling(none_stop=True)