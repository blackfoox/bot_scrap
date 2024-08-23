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


### Все игры из указанной категории и информация одной игры!

db_config = {
    'host': "localhost",
    'dbname': "postgres",
    'user': "postgres",
    'password': "yashka000",
    'port': "5432"
}
urls = {'мусор': 'https://stopgame.ru/games/musor/new?p=',
        'проходняк': 'https://stopgame.ru/games/prohodnyak/new?p=',
        'похвально': 'https://stopgame.ru/games/pohvalno/new?p=',
        'изумительно': 'https://stopgame.ru/games/izumitelno/new?p='
}


class ProvidingGames:
    def __init__(self, urls, messege_in_user):
        self.urls = urls
        self.messege = messege_in_user.text.lower()
    
    def scrap_gamse(self):
        try:
            page = 0
            games = []

            url = self.urls[self.messege]

            while True:
                page += 1
                new_page_url = url + str(page)
                soup = BeautifulSoup(requests.get(new_page_url).text, 'html.parser')
                data = soup.find_all('a', class_='._card_1u499_4')
                time.sleep(5)

                if data[0]['title'] not in games:
                    for item in data:
                        bot.send_message(self.message.chat.id, item['title'])
                        bot.send_message(self.message.chat.id, f"https://stopgame.ru{item['href']}")
                        bot.send_message(self.message.chat.id, '--------------------------------------------')
                        games.append(item['title'])
                break
        except:
            game_info = OneGame(db_config)
            game_info.game_in_db()
            


@bot.message_handler()
def start(message):
    providing_games = ProvidingGames(urls, message)
    providing_games.scrap_gamse(message)


class OneGame:
    def __init__(self, db_config, message):
        self.conn = psycopg2.connect(**db_config)
        self.cur = self.conn.cursor()
        self.message = message

    
    def game_in_db(self):
        with self.conn.cursor() as self.cur:
            self.cur.execute("SELECT * FORM person WHERE game_name = %s", (self.message))
            game = self.cur.fetchall()

        if game:
            soup = BeautifulSoup(requests.get(game[0][2]).text, 'html.parser')            
            release_data = soup.find('div', class_='info-grid_value_1hh2w_220').text.strip()
            bot.send_message(self.message.chat.id, game[0][1])
            bot.send_message(self.message.chat.id, game[0][2])
            bot.send_message(self.message.chat.id, f"Дата выхода: {release_data}")
            bot.send_message(self.message.chat.id, '--------------------------------------------')
            self.conn.close()
        else:
            bot.send_message(self.message.chat.id, "Либо такой игры нет на сайте, либо вы допустили ошибку.")


bot.polling(none_stop=True)