from bs4 import BeautifulSoup
import requests
import time
import psycopg2
from new_bot.import_data import messages, db_config, urls, bot

### Ответ бота на команду /start


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



class ProvidingGames:
    def __init__(self, bot, urls, message_in_user):
        self.bot = bot
        self.urls = urls
        self.message = message_in_user.text.lower()
    
    def scrap_games(self, message):
        try:
            page = 0
            games = []

            url = self.urls[self.message]

            while True:
                page += 1
                new_page_url = url + str(page)
                soup = BeautifulSoup(requests.get(new_page_url).text, 'html.parser')
                data = soup.select('._card_1u499_4')
                time.sleep(5)

                if data[0]['title'] not in games:
                    for item in data:
                        self.bot.send_message(message.chat.id, item['title'])
                        self.bot.send_message(message.chat.id, f"https://stopgame.ru{item['href']}")
                        self.bot.send_message(message.chat.id, '--------------------------------------------')
                        games.append(item['title'])
                        
                break

        except:
           game_info = OneGame(db_config, bot, message)
           game_info.game_in_db(message)
            


@bot.message_handler()
def games(message):
    providing_games = ProvidingGames(bot, urls, message)
    providing_games.scrap_games(message)


class OneGame:
    def __init__(self, db_config, bot, message):
        self.conn = psycopg2.connect(**db_config)
        self.cur = self.conn.cursor()
        self.bot = bot
        self.message = message

    
    def game_in_db(self, message):
        with self.conn.cursor() as self.cur:
            self.cur.execute("SELECT * FROM person WHERE game_name = %s", (message.text,))
            game = self.cur.fetchall()

        if game:
            
            soup = BeautifulSoup(requests.get(game[0][1]).text, 'html.parser')            
            release_data = soup.find('dd').text

            self.bot.send_message(message.chat.id, game[0][0])
            self.bot.send_message(message.chat.id, game[0][1])
            self.bot.send_message(message.chat.id, f"Дата выхода: {release_data}")
            self.bot.send_message(message.chat.id, '--------------------------------------------')
            self.conn.close()

        else:
            self.bot.send_message(message.chat.id, "Либо такой игры нет на сайте, либо вы допустили ошибку.")
            self.conn.close()


bot.polling(none_stop=True)